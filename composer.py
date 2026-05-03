def compose(category, merchant, trigger, customer=None):

    trigger_type = trigger.get("type", "")
    rating = merchant.get("rating", 4.0)
    discount = merchant.get("discount", 20)

    last_seen = 999
    if customer:
        last_seen = customer.get("last_seen_days", 999)

    # -----------------------------
    # SCORING
    # -----------------------------
    score = 0

    if trigger_type == "drop_in_sales":
        score += 5
        goal = "reactivate"
    elif trigger_type == "high_demand":
        score += 3
        goal = "upsell"
    elif trigger_type == "festival":
        score += 2
        goal = "promotion"
    elif trigger_type == "low_rating":
        score += 4
        goal = "trust_recovery"
    else:
        goal = "engage"

    if rating < 3.5:
        score += 4
    elif rating < 4.2:
        score += 2

    if last_seen > 30:
        score += 5
    elif last_seen > 7:
        score += 2

    # -----------------------------
    # DECISION
    # -----------------------------
    if score < 5:
        return {"actions": []}

    # -----------------------------
    # CTA
    # -----------------------------
    if category == "restaurant":
        cta = "Order now"
    elif category == "gym":
        cta = "Join today"
    elif category == "salon":
        cta = "Book now"
    else:
        cta = "Explore now"

    # -----------------------------
    # MESSAGE
    # -----------------------------
    if goal == "reactivate":
        prefix = "We miss you!"
    elif goal == "upsell":
        prefix = "You're on a roll!"
    elif goal == "trust_recovery":
        prefix = "We’re improving for you!"
    else:
        prefix = "Don’t miss out!"

    message = f"{prefix} Enjoy {discount}% off today."

    reason = f"trigger={trigger_type}, inactivity={last_seen}d, rating={rating} → {goal} (score={score})"

    return {
        "actions": [
            {
                "type": "message",
                "text": message,
                "cta": cta,
                "reason": reason
            }
        ]
    }