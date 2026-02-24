def calculate_emi(P, annual_rate, months):
    r = annual_rate / (12 * 100)

    emi = (P * r * (1+r)**months) / ((1+r)**months - 1)
    total_payment = emi * months
    total_interest = total_payment - P

    return {
        "EMI": round(emi, 2),
        "Total Payment": round(total_payment, 2),
        "Total Interest": round(total_interest, 2)
    }