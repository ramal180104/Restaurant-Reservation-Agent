import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

import random
import json
from faker import Faker

from backend.database import create_tables, get_connection

fake = Faker()

cities = {
    "Mumbai": ["Bandra", "Andheri", "Colaba"],
    "Bangalore": ["Indiranagar", "Whitefield", "Koramangala"],
    "Hyderabad": ["Hitech City", "Banjara Hills", "Gachibowli"],
}

cuisines = ["Indian", "Chinese", "Italian", "Mexican", "Cafe"]
ambiences = ["family", "romantic", "business", "rooftop"]

create_tables()
conn = get_connection()
cursor = conn.cursor()

cursor.execute("DELETE FROM restaurants")

for i in range(100):
    city = random.choice(list(cities.keys()))
    area = random.choice(cities[city])

    cursor.execute("""
        INSERT INTO restaurants (
            id, name, city, area, cuisines, price_range,
            seating_capacity, rating, ambience_tags
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        i + 1,
        fake.company(),
        city,
        area,
        json.dumps(random.sample(cuisines, k=2)),
        random.choice(["₹", "₹₹", "₹₹₹"]),
        random.randint(20, 200),
        round(random.uniform(3.5, 4.8), 1),
        json.dumps(random.sample(ambiences, k=2))
    ))

conn.commit()
conn.close()

print("✅ 100 restaurants inserted")
