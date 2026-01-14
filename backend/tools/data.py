# backend/tools/data.py

RESTAURANTS = []

cities = ["Hyderabad", "Bangalore", "Mumbai", "Delhi"]

cuisines = [
    ["Indian", "Chinese"],
    ["Italian", "Mexican"],
    ["Indian", "Italian"],
    ["Chinese", "Cafe"]
]

ambiences = [
    ["family", "business"],
    ["romantic"],
    ["rooftop", "business"],
    ["casual"]
]

# ✅ ADD THIS HERE
price_ranges = ["₹", "₹₹", "₹₹₹"]

restaurant_id = 1

for city in cities:
    for i in range(25):
        RESTAURANTS.append({
            "id": restaurant_id,
            "brand": "GoodFoods",
            "city": city,
            "area": f"{city} Area {i+1}",
            "cuisines": cuisines[i % len(cuisines)],
            "price_range": price_ranges[i % len(price_ranges)],  # ✅ ADD THIS
            "seating_capacity": 20 + (i * 5) % 120,
            "rating": round(3.5 + (i % 5) * 0.3, 1),
            "ambience_tags": ambiences[i % len(ambiences)]
        })
        restaurant_id += 1
