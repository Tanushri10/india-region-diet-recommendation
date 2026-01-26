import pandas as pd
from logic.region_mapper import normalize_region

def normalize_diet(diet):
    diet = str(diet).lower()

    if "vegetarian" in diet:
        return "veg"
    if "egg" in diet:
        return "eggetarian"
    if "non" in diet:
        return "non-veg"

    return "other"


def load_food_data():
    df = pd.read_excel("output.xlsx")

    # Normalize region
    df["region"] = df["region"].astype(str).apply(normalize_region)

    # Normalize diet type
    df["diet_type"] = df["diet_type"].apply(normalize_diet)

    return df
