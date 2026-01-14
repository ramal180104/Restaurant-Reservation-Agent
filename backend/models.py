from pydantic import BaseModel
from typing import List

class Restaurant(BaseModel):
    id: int
    name: str
    city: str
    area: str
    cuisines: List[str]
    price_range: str
    seating_capacity: int
    rating: float
    ambience_tags: List[str]


class Reservation(BaseModel):
    reservation_id: int
    restaurant_id: int
    user_name: str
    date: str
    time: str
    party_size: int
    status: str

