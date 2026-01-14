from fastapi import FastAPI
from backend.tools.search import search_restaurants
from backend.tools.recommend import recommend_restaurants
from backend.tools.reserve import make_reservation

app = FastAPI()

ALLOWED_CITIES = {"hyderabad", "bangalore", "delhi"}
INTENTS = {"search", "recommend", "reserve"}
ALLOWED_AMBIENCE = {"family", "romantic", "business", "rooftop", "casual"}

BUDGET_MAP = {
    "low": "₹",
    "medium": "₹₹",
    "high": "₹₹₹"
}

# ---------------- HELPERS ----------------

def welcome():
    return (
        "Welcome to GoodFoods 🍽️\n\n"
        "What would you like to do?\n"
        "• Search restaurants\n"
        "• Get recommendations\n"
        "• Make a reservation\n\n"
        "Reply with: search, recommend, or reserve."
    )


def list_cities():
    return "GoodFoods is available in:\n• Hyderabad\n• Bangalore\n• Delhi"


def format_restaurants(restaurants):
    return "\n".join(
        f"{i}. GoodFoods – {r['area']} "
        f"({', '.join(r['cuisines'])}) – ⭐ {r['rating']}"
        for i, r in enumerate(restaurants, start=1)
    )


def explain_restaurants(restaurants):
    return "\n\n".join(
        f"{i}. GoodFoods – {r['area']} (⭐ {r['rating']})\n"
        f"   Ambience: {', '.join(r['ambience_tags'])}\n"
        f"   Price Range: {r['price_range']}\n"
        f"   Seating Capacity: {r['seating_capacity']}"
        for i, r in enumerate(restaurants, start=1)
    )


# ---------------- CHAT ENDPOINT ----------------

@app.post("/chat")
def chat(payload: dict):
    messages = payload.get("messages", [])
    context = payload.get("context", {})

    user_text = messages[-1]["content"].strip().lower()

    # ---------- RESET ----------
    if user_text in {"reset", "start over"}:
        context.clear()
        return {"role": "assistant", "content": welcome(), "context": context}

    # ---------- INTENT ----------
    if user_text in INTENTS:
        context["intent"] = user_text

    if "intent" not in context:
        return {"role": "assistant", "content": welcome(), "context": context}

    # ---------- CITY ----------
    if "city" not in context:
        if user_text in ALLOWED_CITIES:
            context["city"] = user_text.capitalize()
        else:
            return {
                "role": "assistant",
                "content": "Please select a city.\n\n" + list_cities(),
                "context": context
            }

    # ---------- SEARCH ----------
    if "restaurants" not in context:
        restaurants = search_restaurants(context["city"])[:15]
        context["restaurants"] = restaurants

        return {
            "role": "assistant",
            "content": (
                f"Here are the GoodFoods restaurants in {context['city']}:\n\n"
                + format_restaurants(restaurants)
                + "\n\nYou can say `recommend` for suggestions or `reserve` to book a table."
            ),
            "context": context
        }

    # =================================================
    # RECOMMENDATION FLOW
    # =================================================
    if context["intent"] == "recommend":

        # STEP 1: Ask ambience
        if "recommend_step" not in context:
            context["recommend_step"] = "ambience"
            return {
                "role": "assistant",
                "content": "What ambience are you looking for? (family, romantic, business, rooftop, casual)",
                "context": context
            }

        # STEP 2: Capture ambience
        if context["recommend_step"] == "ambience":
            if user_text not in ALLOWED_AMBIENCE:
                return {
                    "role": "assistant",
                    "content": "Please choose a valid ambience: family, romantic, business, rooftop, or casual.",
                    "context": context
                }

            context["ambience"] = user_text
            context["recommend_step"] = "budget"

            return {
                "role": "assistant",
                "content": "What’s your budget? (low / medium / high)",
                "context": context
            }

        # STEP 3: Capture budget + recommend
        if context["recommend_step"] == "budget":
            if user_text not in BUDGET_MAP:
                return {
                    "role": "assistant",
                    "content": "Please choose: low, medium, or high.",
                    "context": context
                }

            context["budget"] = BUDGET_MAP[user_text]

            # 1️⃣ Strict match
            filtered = recommend_restaurants(
                context["restaurants"],
                ambience=context["ambience"],
                budget=context["budget"]
            )

            # 2️⃣ Relax budget
            if len(filtered) < 3:
                filtered = recommend_restaurants(
                    context["restaurants"],
                    ambience=context["ambience"]
                )

            # 3️⃣ Relax ambience
            if len(filtered) < 3:
                filtered = recommend_restaurants(context["restaurants"])

            # 4️⃣ Final cap (min 3, max 6)
            filtered = filtered[:6]

            if not filtered:
                return {
                    "role": "assistant",
                    "content": "Sorry, I couldn’t find restaurants matching those preferences.",
                    "context": context
                }

            # Move to reservation
            context["restaurants"] = filtered
            context["intent"] = "reserve"
            context.pop("recommend_step", None)

            return {
                "role": "assistant",
                "content": (
                    "Based on your preferences, here are the best GoodFoods options:\n\n"
                    + explain_restaurants(filtered)
                    + "\n\nPlease select a restaurant number to continue booking."
                ),
                "context": context
            }

    # =================================================
    # RESERVATION FLOW
    # =================================================
    if context["intent"] == "reserve":

        if "restaurant_id" not in context:
            if not user_text.isdigit():
                return {
                    "role": "assistant",
                    "content": "Please enter a valid restaurant number from the list.",
                    "context": context
                }

            idx = int(user_text) - 1
            if idx < 0 or idx >= len(context["restaurants"]):
                return {
                    "role": "assistant",
                    "content": "Invalid selection. Please choose a number from the list.",
                    "context": context
                }

            context["restaurant"] = context["restaurants"][idx]
            context["restaurant_id"] = context["restaurant"]["id"]

            return {
                "role": "assistant",
                "content": "Please provide the reservation date (MM/DD/YYYY).",
                "context": context
            }

        if "date" not in context:
            context["date"] = user_text
            return {"role": "assistant", "content": "Please provide the time.", "context": context}

        if "time" not in context:
            context["time"] = user_text
            return {"role": "assistant", "content": "How many people will be dining?", "context": context}

        if "party_size" not in context:
            if not user_text.isdigit():
                return {"role": "assistant", "content": "Party size must be a number.", "context": context}

            context["party_size"] = int(user_text)
            return {
                "role": "assistant",
                "content": "Under whose name should I make the reservation?",
                "context": context
            }

        context["user_name"] = user_text.capitalize()

        result = make_reservation(
            restaurant_id=context["restaurant_id"],
            party_size=context["party_size"],
            date=context["date"],
            time=context["time"],
            user_name=context["user_name"]
        )

        context.clear()

        return {
            "role": "assistant",
            "content": (
                "✅ Your reservation is confirmed!\n\n"
                f"Date: {result['date']}\n"
                f"Time: {result['time']}\n"
                f"Party Size: {result['party_size']}\n"
                f"Reserved under the name: {result['user_name']}\n\n"
                "We look forward to serving you at GoodFoods 🍽️\n"
                "Type `reset` to start over."
            ),
            "context": context
        }
