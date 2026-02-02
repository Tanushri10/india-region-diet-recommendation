def normalize_region(region_value):
    region_value = str(region_value).lower()
    region_value = region_value.replace("/", " ").replace("-", " ")

    south_keywords = [
        "south", "andhra", "telangana", "rayalaseema",
        "tamil", "tn", "karnataka", "kerala",
        "hyderabad", "deccan", "telugu"
    ]

    if any(word in region_value for word in south_keywords):
        return "south india"

    return "other"

