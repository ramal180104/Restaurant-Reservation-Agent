def make_reservation(restaurant_id, party_size, date, time, user_name):
    return {
        "restaurant_id": restaurant_id,
        "party_size": party_size,
        "date": date,
        "time": time,
        "user_name": user_name,
        "status": "confirmed"
    }
