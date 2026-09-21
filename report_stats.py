import math

def compute_stats(profile, price):

    income = profile["monthly_income"]
    expenses = profile["monthly_expenses"]
    savings = profile["current_savings"]

    disposable_income = income - expenses

    pct_of_savings = (price / savings * 100) if savings > 0 else None
    pct_of_disposable = (price / disposable_income * 100) if disposable_income > 0 else None
    months_needed = (price / disposable_income) if disposable_income > 0 else None

    return {
        "disposable_income": round(disposable_income, 2),
        "pct_of_savings": round(pct_of_savings, 1) if pct_of_savings is not None else None,
        "pct_of_disposable": round(pct_of_disposable, 1) if pct_of_disposable is not None else None,
        "months_needed": round(months_needed, 1) if months_needed is not None else None,
    }


def build_donut_chart(price, current_savings, size=150, stroke_width=20):

    remaining = max(current_savings - price, 0)
    total = price + remaining if (price + remaining) > 0 else 1

    r = (size - stroke_width) / 2
    cx = cy = size / 2
    circumference = 2 * math.pi * r

    segments = [
        ("This purchase", price, "#e8a24c"),
        ("Remaining savings", remaining, "#7fc7b3"),
    ]

    circles = []
    offset = 0
    for label, value, color in segments:
        pct = value / total
        length = circumference * pct
        dasharray = f"{length:.2f} {circumference - length:.2f}"
        circles.append(
            f'<circle cx="{cx}" cy="{cy}" r="{r:.2f}" fill="none" '
            f'stroke="{color}" stroke-width="{stroke_width}" '
            f'stroke-dasharray="{dasharray}" stroke-dashoffset="{-offset:.2f}" '
            f'transform="rotate(-90 {cx} {cy})" />'
        )
        offset += length

    alt_text = ", ".join(f"{label} {value / total * 100:.0f}%" for label, value, _ in segments)

    return (
        f'<svg viewBox="0 0 {size} {size}" width="{size}" height="{size}" '
        f'role="img" aria-label="Chart showing {alt_text}">'
        + "".join(circles) +
        "</svg>"
    )
