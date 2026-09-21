"""
classifier.py

A small gatekeeper: checks whether the user's input is actually a
purchase decision question before running the full three-persona debate.
"""

from llm_client import get_response

CLASSIFIER_INSTRUCTION = """You are a strict classifier. You will be given a single sentence or question. Decide whether it describes a purchase decision the user is considering making (e.g. buying an item, subscribing to a service, spending money on something).

Reply with exactly one word: YES or NO. Nothing else -- no punctuation, no explanation."""


def is_purchase_question(question):
    """
    question: a string, the user's raw input.
    Returns True if it's a purchase decision question, False otherwise.
    """
    answer = get_response(
        prompt=question,
        system_instruction=CLASSIFIER_INSTRUCTION,
    )
    return answer.strip().upper().startswith("YES")
