import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "restaurants.db"

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS restaurants (
        id INTEGER PRIMARY KEY,
        name TEXT,
        city TEXT,
        area TEXT,
        cuisines TEXT,
        price_range TEXT,
        seating_capacity INTEGER,
        rating REAL,
        ambience_tags TEXT
    )
    """)

    conn.commit()
    conn.close()
def create_reservations_table():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS reservations (
        reservation_id INTEGER PRIMARY KEY AUTOINCREMENT,
        restaurant_id INTEGER,
        user_name TEXT,
        date TEXT,
        time TEXT,
        party_size INTEGER,
        status TEXT
    )
    """)

    conn.commit()
    conn.close()
if __name__ == "__main__":
    create_tables()
    create_reservations_table()
    print("Tables ready")
