import sqlite3

def init_db():
    conn = sqlite3.connect("ims.db")
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS admin (username TEXT, password TEXT)")
    cur.execute("""
        CREATE TABLE IF NOT EXISTS inventory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            quantity INTEGER,
            price REAL,
            reorder_quantity INTEGER,
            date_added TEXT
        )
    """)
    cur.execute("SELECT * FROM admin")
    if not cur.fetchone():
        cur.execute("INSERT INTO admin VALUES (?, ?)", ("admin", "admin"))
    conn.commit()
    conn.close()
