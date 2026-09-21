"""
judge.py

Takes both personas' arguments and synthesizes a final, balanced report.
The judge does NOT tell the user what to do -- it weighs both sides and
hands the decision back to the user, fully informed.
"""

from llm_client import get_response

JUDGE_INSTRUCTION = """You are a neutral, balanced financial advisor. You have been given two arguments about a purchase decision -- one in favor, one against -- along with the user's financial context.

Your job is NOT to make the final decision for the user. Your job is to:
- Briefly acknowledge the strongest point from each side (1-2 sentences each).
- Point out anything either side got right that the user should weigh carefully.
- End with a short, clear summary of the key trade-off the user is actually facing -- not a command to buy or not buy.
- For all the above (except the summary), use a Markdown bulleted list (using "-") with 2-3 distinct supporting points. Do not be repetitive. Leave a gap of one line before the summary.

Keep the whole response under 150 words. Be honest and grounded, not wishy-washy -- it's fine to say clearly which concerns matter most, just don't tell the user what to do."""


def get_verdict(context, impulse_argument, frugal_argument):
    """
    context: the combined profile + question text from build_context()
    impulse_argument: string returned by get_impulse_buyer_argument()
    frugal_argument: string returned by get_frugal_advisor_argument()

    Returns the judge's synthesized summary as a string.
    """
    judge_prompt = (
        f"{context}\n"
        f"Here is the argument IN FAVOR of the purchase:\n{impulse_argument}\n\n"
        f"Here is the argument AGAINST the purchase:\n{frugal_argument}\n"
    )

    return get_response(
        prompt=judge_prompt,
        system_instruction=JUDGE_INSTRUCTION,
    )
