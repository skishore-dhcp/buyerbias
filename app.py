import os
import markdown
from flask import Flask, render_template, request, redirect, url_for, session

from context_builder import build_context
from personas import get_impulse_buyer_argument, get_frugal_advisor_argument
from judge import get_verdict
from classifier import is_purchase_question
from report_stats import compute_stats, build_donut_chart

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "dev-only-change-me")


def render_markdown(text):
    return markdown.markdown(text)


@app.route("/", methods=["GET", "POST"])
def profile_form():
    if request.method == "POST":
        profile = {
            "monthly_income": float(request.form["monthly_income"]),
            "monthly_expenses": float(request.form["monthly_expenses"]),
            "current_savings": float(request.form["current_savings"]),
            "savings_goal": request.form["savings_goal"],
            "recent_spending_note": request.form["recent_spending_note"],
        }
        session["profile"] = profile
        return redirect(url_for("question"))

    profile = session.get("profile")
    return render_template("profile_form.html", profile=profile)


@app.route("/question", methods=["GET", "POST"])
def question():
    profile = session.get("profile")
    if not profile:
        return redirect(url_for("profile_form"))

    if request.method == "POST":
        user_question = request.form["question"].strip()
        price = float(request.form["price"])

        if not is_purchase_question(user_question):
            return render_template(
                "question.html",
                error="That doesn't look like a purchase decision. Try describing something you're thinking of buying.",
                question=user_question,
                price=price,
            )

        context = build_context(profile, user_question, price)
        impulse_argument = get_impulse_buyer_argument(context)
        frugal_argument = get_frugal_advisor_argument(context)
        verdict = get_verdict(context, impulse_argument, frugal_argument)

        stats = compute_stats(profile, price)
        chart_svg = build_donut_chart(price, profile["current_savings"])

        return render_template(
            "report.html",
            question=user_question,
            price=price,
            profile=profile,
            stats=stats,
            chart_svg=chart_svg,
            impulse_argument=render_markdown(impulse_argument),
            frugal_argument=render_markdown(frugal_argument),
            verdict=render_markdown(verdict),
        )

    return render_template("question.html")


if __name__ == "__main__":
    app.run(debug=True)
