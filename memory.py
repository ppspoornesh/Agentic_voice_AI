import sqlite3

DB_NAME = "conversation.db"

def get_conn():
    return sqlite3.connect(DB_NAME, check_same_thread=False)

with get_conn() as conn:
    conn.execute("""
        CREATE TABLE IF NOT EXISTS memory (
            session_id TEXT,
            key TEXT,
            value TEXT,
            PRIMARY KEY (session_id, key)
        )
    """)

def save_memory(session_id, key, value):
    with get_conn() as conn:
        conn.execute(
            "INSERT OR REPLACE INTO memory VALUES (?, ?, ?)",
            (session_id, key, str(value))
        )

def get_memory(session_id, key):
    with get_conn() as conn:
        row = conn.execute(
            "SELECT value FROM memory WHERE session_id=? AND key=?",
            (session_id, key)
        ).fetchone()
    return row[0] if row else None

def memory_snapshot(session_id):
    with get_conn() as conn:
        rows = conn.execute(
            "SELECT key, value FROM memory WHERE session_id=?",
            (session_id,)
        ).fetchall()

    snap = {}
    for k, v in rows:
        snap[k] = int(v) if v.isdigit() else v
    return snap

def check_contradiction(session_id, key, new_value):
    old = get_memory(session_id, key)
    if old and old != str(new_value):
        return f"మీరు ముందుగా {old} చెప్పారు. ఇప్పుడు {new_value}. నిర్ధారించాలా?"
    return None
