import sqlite3
from datetime import datetime, timedelta, timezone


DB_NAME = "news_ai.db"

# Initialize database and table
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS news (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            link TEXT UNIQUE,
            date TEXT,
            source TEXT,
            category TEXT,
            fetched_at       
        )
    ''')
    conn.commit()
    conn.close()

# Insert news into database (skip duplicates)
def insert_news(news_list):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    now = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
    print("insert start")
    for news in news_list:
        try:
            cursor.execute('''
                INSERT OR IGNORE INTO news (title, link, date, source, fetched_at)
                VALUES (?, ?, ?, ?, ?)
            ''', (news["title"], news["link"], news["date"], news["source"], now))
        except Exception:
            continue
    print("insert done")
    conn.commit()
    conn.close()

# Delete news older than X hours (default: 48 hours)
def delete_old_news(hours=48):
    threshold_time = (datetime.now(timezone.utc) - timedelta(hours=hours)).strftime('%Y-%m-%d %H:%M:%S')
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM news WHERE fetched_at < ?", (threshold_time,))
    conn.commit()
    conn.close()

# Get news by optional filters (e.g., keyword only)
def get_news(keyword=None, limit=100):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    query = "SELECT title, link, date, source FROM news WHERE 1=1"
    params = []

    if keyword:
        query += " AND LOWER(title) LIKE ?"
        params.append(f"%{keyword.lower()}%")

    query += " ORDER BY date DESC LIMIT ?"
    params.append(limit)

    cursor.execute(query, params)
    results = cursor.fetchall()
    conn.close()

    return [
        {"title": r[0], "link": r[1], "date": r[2], "source": r[3]}
        for r in results
    ]

