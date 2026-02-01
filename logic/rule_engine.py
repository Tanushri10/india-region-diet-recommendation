def rule_based_filter(df, user):
    filtered = df.copy()

    # Region filter
    filtered = filtered[filtered["region"] == user["region"]]

    # Diet type filter
    if "diet_type" in user:
        filtered = filtered[filtered["diet_type"] == user["diet_type"]]

    # Goal-based rules
    if user["goal"] == "fat_loss":
        filtered = filtered[
            (filtered["calories"] <= 500) &
            (filtered["fat"] <= 20)
        ]

    elif user["goal"] == "muscle_gain":
        filtered = filtered[
            (filtered["protein"] >= 20) &
            (filtered["calories"] >= 400)
        ]

    # Activity-based
    if user["activity"] == "sedentary":
        filtered = filtered[filtered["carbs"] <= 50]

    # Allergy exclusion
    if "allergy" in user:
        filtered = filtered[
            ~filtered["allergens"].str.contains(
                user["allergy"], case=False, na=False
            )
        ]

    return filtered
def generate_meal_plan(df):
    df = df.fillna("None")
    plan = {}

    plan["Breakfast"] = (
        df[df["meal_type"].str.contains("Breakfast", case=False)]
        .head(2)
        .to_dict(orient="records")
    )

    plan["Lunch"] = (
        df[df["meal_type"].str.contains("Lunch", case=False)]
        .head(2)
        .to_dict(orient="records")
    )

    plan["Dinner"] = (
        df[df["meal_type"].str.contains("Dinner", case=False)]
        .head(2)
        .to_dict(orient="records")
    )

    return plan
