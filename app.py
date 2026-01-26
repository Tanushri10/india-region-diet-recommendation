from logic.load_data import load_food_data
from logic.rule_engine import rule_based_filter

user = {
    "region": "south india",
    "goal": "fat_loss",
    "activity": "moderate",
    "diet_type": "veg"
}


df = load_food_data()
result = rule_based_filter(df, user)

print(result[["meal", "calories", "protein", "meal_type"]].head())
print(df["region"].unique())
print(df["diet_type"].unique())

