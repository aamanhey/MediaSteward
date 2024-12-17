import sqlite3

def save_to_db(data, db_path):
    """
    Saves the extracted data to a SQLite database.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS video_data (
        video_name TEXT,
        transcript TEXT,
        summary TEXT
    )""")

    cursor.execute("INSERT INTO video_data VALUES (?, ?, ?)", data)
    conn.commit()
    conn.close()
    print("Data saved to database.")
