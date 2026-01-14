TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "search_restaurants",
            "description": "Find GoodFoods restaurant locations by city and/or cuisine",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "City where the GoodFoods restaurant is located"
                    },
                    "cuisine": {
                        "type": "string",
                        "description": "Cuisine type (e.g., Italian, Indian, Chinese)"
                    }
                },
                "required": ["city"]
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "recommend_restaurants",
            "description": "Recommend GoodFoods locations based on preferences",
            "parameters": {
                "type": "object",
                "properties": {
                    "party_size": {
                        "type": "integer",
                        "description": "Number of people in the party"
                    },
                    "budget": {
                        "type": "string",
                        "description": "Budget preference (Low, Moderate, High)"
                    },
                    "ambience": {
                        "type": "string",
                        "description": "Ambience preference (Family, Romantic, Business, Casual)"
                    }
                },
                "required": []
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "make_reservation",
            "description": "Create a reservation at a GoodFoods restaurant location",
            "parameters": {
                "type": "object",
                "properties": {
                    "restaurant_id": {
                        "type": "integer",
                        "description": "ID of the selected GoodFoods restaurant location"
                    },
                    "party_size": {
                        "type": "integer",
                        "description": "Number of people"
                    },
                    "date": {
                        "type": "string",
                        "description": "Reservation date in MM/DD/YYYY format"
                    },
                    "time": {
                        "type": "string",
                        "description": "Reservation time (e.g., 7:00 PM)"
                    },
                    "user_name": {
                        "type": "string",
                        "description": "Name of the person making the reservation"
                    }
                },
                "required": [
                    "restaurant_id",
                    "party_size",
                    "date",
                    "time",
                    "user_name"
                ]
            }
        }
    }
]

