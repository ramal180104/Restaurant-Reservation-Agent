def recommend_restaurants(restaurants: list, ambience=None, budget=None):
    if not restaurants:
        return []

    results = []

    for r in restaurants:
        # 🚨 SAFETY CHECK
        if not isinstance(r, dict):
            continue

        if ambience:
            tags = r.get("ambience_tags", [])
            if ambience.lower() not in [a.lower() for a in tags]:
                continue

        if budget:
            if r.get("price_range") != budget:
                continue

        results.append(r)

    return sorted(results, key=lambda r: r.get("rating", 0), reverse=True)
