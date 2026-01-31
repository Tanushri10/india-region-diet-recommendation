import sqlite3
import pandas as pd

def load_feedback():
    conn = sqlite3.connect("feedback.db")
    df = pd.read_sql("SELECT * FROM feedback", conn)
    conn.close()
    return df

if __name__ == "__main__":
    df = load_feedback()
    print(df.head())
