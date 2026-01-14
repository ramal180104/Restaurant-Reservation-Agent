from backend.tools.data import RESTAURANTS

def search_restaurants(city: str):
    results = []

    for r in RESTAURANTS:
        if not isinstance(r, dict):
            continue

        if r.get("city", "").lower() == city.lower():
            results.append(r)

    return results
