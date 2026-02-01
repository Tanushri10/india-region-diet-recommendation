# ===============================
# Diet filtering
# ===============================
def apply_diet_filter(df, user_diet):
    if user_diet == "veg":
        return df[df["diet_type"] == "veg"]

    if user_diet == "eggetarian":
        return df[df["diet_type"].isin(["veg", "eggetarian"])]

    if user_diet == "non-veg":
        return df[df["diet_type"].isin(["veg", "eggetarian", "non-veg"])]

    return df


# ===============================
# Rule-based filtering
# ===============================
def rule_based_filter(df, user):
    filtered = df.copy()

    filtered = filtered[filtered["region"] == user["region"]]
    filtered = apply_diet_filter(filtered, user["diet_type"])

    calorie_target = estimate_calorie_target(user)

    if user["goal"] == "fat_loss":
     if calorie_target:
        filtered = filtered[filtered["calories"] <= calorie_target * 0.4]
     else:
        filtered = filtered[filtered["calories"] <= 800]

    elif user["goal"] == "muscle_gain":
     filtered = filtered[filtered["protein"] >= 8]


    if user.get("activity") == "sedentary":
        filtered = filtered[filtered["carbs"] <= 50]

    if user.get("allergy"):
        filtered = filtered[
            ~filtered["allergens"].str.contains(
                user["allergy"], case=False, na=False
            )
        ]

    return filtered


# ===============================
# Heavy meal tagging
# ===============================
def mark_heavy_meals(df):
    df = df.copy()
    df["is_heavy"] = df["meal"].str.contains(
        "biryani|pulao|rice", case=False, na=False
    )
    return df


# ===============================
# Ranking
# ===============================

def rank_meals(df, user):
    
    df = df.copy()

    # 1️⃣ Initialize score FIRST
    df["score"] = 0.0

    # 2️⃣ Base health score
    df["score"] += df["protein"] * 0.6
    df["score"] += (df["calories"] / 100)

    # 3️⃣ Weight-aware personalization
    weight = user.get("weight_kg")
    if weight:
        df["score"] += (df["calories"] / weight) * 0.3

    # 4️⃣ Preference bias
    if user.get("diet_type") == "non_veg" and user.get("prefer_non_veg"):
        df.loc[df["diet_type"] == "non-veg", "score"] += 2

    # 5️⃣ Meal timing bias
    df.loc[df["meal_type"].str.contains("Breakfast", case=False), "score"] += 1
    df.loc[df["meal_type"].str.contains("Lunch", case=False), "score"] += 2
    df.loc[df["meal_type"].str.contains("Dinner", case=False), "score"] += 1.5
    df.loc[
    df["ingredients"].str.contains(
        "chicken|mutton|fish|egg|meat|prawns",
        case=False,
        na=False
    ),
    "score"
] -= 100
# Goal-specific ranking bias
    if user["goal"] == "muscle_gain":
     df["score"] += df["protein"] * 1.5
     df["score"] += df["calories"] * 0.01

     print(
    "DEBUG ranking:",
           df[["meal", "calories", "protein", "score"]].head()
)


    return df.sort_values("score", ascending=False)


# ===============================
# Meal plan generation (FIXED)
# ===============================
def generate_meal_plan(df):
    df = df.fillna("None")
    df = mark_heavy_meals(df)

    used_meals = set()
    heavy_used = False  # ✅ ONE heavy meal per DAY

    def pick(meal_df):
        nonlocal heavy_used
        for _, row in meal_df.iterrows():
            if row["meal"] in used_meals:
                continue

            if row["is_heavy"] and heavy_used:
                continue

            used_meals.add(row["meal"])
            if row["is_heavy"]:
                heavy_used = True

            return row.to_dict()

        return None

    breakfast = pick(df[df["meal_type"].str.contains("Breakfast", case=False)])
    lunch = pick(df[df["meal_type"].str.contains("Lunch", case=False)])
    dinner = pick(df[df["meal_type"].str.contains("Dinner", case=False)])

    return [
        {"meal_type": "Breakfast", "meal": breakfast},
        {"meal_type": "Lunch", "meal": lunch},
        {"meal_type": "Dinner", "meal": dinner},
    ]


# ===============================
# Daily totals
# ===============================
def calculate_daily_totals(meal_plan):
    total_calories = 0
    total_protein = 0

    for slot in meal_plan:
        meal = slot["meal"]
        if meal:
            total_calories += meal.get("calories", 0)
            total_protein += meal.get("protein", 0)

    return {
        "total_calories": round(total_calories, 1),
        "total_protein": round(total_protein, 1)
    }

def estimate_calorie_target(user):
    weight = user.get("weight_kg")
    height = user.get("height_cm")
    activity = user.get("activity", "moderate")
    goal = user.get("goal")

    if not weight or not height:
        return None  # fallback to default rules

    # Base calories (very simple heuristic)
    base_calories = weight * 30

    if activity == "sedentary":
        base_calories -= 200
    elif activity == "active":
        base_calories += 200

    if goal == "fat_loss":
        return base_calories - 300
    elif goal == "muscle_gain":
        return base_calories + 300

    return base_calories

