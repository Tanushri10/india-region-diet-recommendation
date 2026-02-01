import sqlite3

DB_NAME = "feedback.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            meal TEXT,
            calories REAL,
            protein REAL,
            carbs REAL,
            fat REAL,
            fiber REAL,
            goal TEXT,
            activity TEXT,
            region TEXT,
            liked INTEGER
        )
    """)

    conn.commit()
    conn.close()


def save_feedback(data):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO feedback (
            meal, calories, protein, carbs, fat, fiber,
            goal, activity, region, liked
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        data["meal"],
        data["calories"],
        data["protein"],
        data["carbs"],
        data["fat"],
        data["fiber"],
        data["goal"],
        data["activity"],
        data["region"],
        data["liked"]
    ))

    conn.commit()
    conn.close()
