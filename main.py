from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from rag import retrieve
from emi import calculate_emi
from intent import detect_intent
import google.generativeai as genai
from twilio.twiml.messaging_response import MessagingResponse

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

genai.configure(api_key="AIzaSyDnBDj5E8BmQibpVMIl0plUIwmY0JaxZts")
model = genai.GenerativeModel("gemini-1.5-flash")

@app.get("/ask")
def ask_agent(query: str):

    intent = detect_intent(query)

    # EMI Calculator Mode
    if intent == "loan" and "," in query:
        try:
            P, rate, months = map(float, query.split(","))
            result = calculate_emi(P, rate, int(months))
            return result
        except:
            return {"message": "Enter format: 200000,12,24"}

    # Fraud Warning
    warning = ""
    if intent == "fraud":
        warning = "⚠️ ALERT: Never share OTP. QR code is for sending money.\n\n"

    context = retrieve(query)

    prompt = f"""
    Use this verified context:
    {context}

    Explain in simple Hindi or English.
    Avoid technical terms.

    Question: {query}
    """

    response = model.generate_content(prompt)

    return {"answer": warning + response.text}


# WhatsApp Webhook
@app.post("/whatsapp")
async def whatsapp_reply(request: Request):
    form = await request.form()
    msg = form.get("Body")

    context = retrieve(msg)

    prompt = f"Explain simply:\n{context}\nQuestion:{msg}"

    response = model.generate_content(prompt)

    resp = MessagingResponse()
    resp.message(response.text)

    return str(resp)

import os

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)