import sqlite3
import pandas as pd

conn = sqlite3.connect("feedback.db")

df = pd.read_sql("SELECT * FROM feedback", conn)

conn.close()

print(df)
