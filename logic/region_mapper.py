def normalize_region(region_value):
    region_value = region_value.lower()

    south_keywords = [
        "south", "andhra", "telangana", "rayalaseema",
        "tamil", "tn", "karnataka", "kerala",
        "hyderabad", "deccan", "telugu"
    ]

    north_keywords = [
        "north", "punjab", "delhi", "haryana", "up",
        "uttar", "bihar", "rajasthan"
    ]

    if any(word in region_value for word in south_keywords):
        return "south india"

    if any(word in region_value for word in north_keywords):
        return "north india"

    return "other"
