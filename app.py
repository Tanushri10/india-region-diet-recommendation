from logic.load_data import load_food_data
from logic.rule_engine import rule_based_filter, generate_meal_plan

user = {
    "region": "south india",
    "goal": "fat_loss",
    "activity": "moderate",
    "diet_type": "veg"
}


df = load_food_data()
filtered = rule_based_filter(df, user)
meal_plan = generate_meal_plan(filtered)

for meal_time, items in meal_plan.items():
    print(f"\n{meal_time}:")
    for item in items:
        print(f"- {item['meal']} ({item['calories']} kcal, {item['protein']}g protein)")

print(filtered[["meal", "calories", "protein", "meal_type"]].head())
print(df["region"].unique())
print(df["diet_type"].unique())

