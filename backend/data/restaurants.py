from backend.tools.data import RESTAURANTS

def search_restaurants(city=None, cuisine=None):
    results = RESTAURANTS

    if city:
        results = [
            r for r in results
            if r["city"].lower() == city.lower()
        ]

    if cuisine:
        results = [
            r for r in results
            if cuisine.lower() in [c.lower() for c in r["cuisines"]]
        ]

    return results

