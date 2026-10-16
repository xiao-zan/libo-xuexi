import sqlite3

DB_FILE = "history.db"

def init_db():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        session_id TEXT,
        text TEXT,
        score REAL,
        label TEXT,
        pinyin TEXT,
        created_at TEXT
    )
    """)
    cur.execute(
        "CREATE INDEX IF NOT EXISTS idx_history_session_created "
        "ON history(session_id, created_at)"
    )
    conn.commit()
    conn.close()

def get_conn():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row      # 让查询结果带上列名（默认是元组）
    return conn


def save_record(session_id, record):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO history (session_id, text, score, label, pinyin, created_at)"
        " VALUES (?, ?, ?, ?, ?, ?)",
        [session_id, record["text"], record["score"],
         record["label"], record["pinyin"], record["created_at"]],
    )
    conn.commit()
    conn.close()

def get_history(session_id, limit):
    if not session_id:
        return []
    try:
        conn = get_conn()
        cur = conn.cursor()
        rows = cur.execute(
            "SELECT * FROM history WHERE session_id = ? ORDER BY created_at DESC LIMIT ?",
            [session_id, limit],
        ).fetchall()
        conn.close()
        records = [dict(row) for row in rows]
        return records
    except Exception as e:
        print("数据库查询历史失败：", e)
        return []
