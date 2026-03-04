import sqlite3

DB_PATH = "releases.db"

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS releases (
            url TEXT PRIMARY KEY
        )
    """)
    return conn

def is_new(url):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT url FROM releases WHERE url = ?", (url,))
    result = cur.fetchone()
    conn.close()
    return result is None

def save_release(release):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT OR IGNORE INTO releases (url) VALUES (?)", (release["url"],))
    conn.commit()
    conn.close()
