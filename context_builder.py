def build_context(profile, question, price=None):
    
    disposable_income = profile["monthly_income"] - profile["monthly_expenses"]

    context = (
        f"Here is the user's financial situation:\n"
        f"- Monthly income: ${profile['monthly_income']}\n"
        f"- Monthly expenses: ${profile['monthly_expenses']}\n"
        f"- Disposable income after expenses: ${disposable_income}\n"
        f"- Current savings: ${profile['current_savings']}\n"
        f"- Savings goal: {profile['savings_goal']}\n"
        f"- Recent spending pattern: {profile['recent_spending_note']}\n"
        f"\n"
        f"The user is considering the following purchase decision:\n"
        f"\"{question}\"\n"
    )

    if price is not None:
        context += f"The price of this purchase is: ${price}\n"

    return context
