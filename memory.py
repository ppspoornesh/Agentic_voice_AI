import sqlite3

# Database file used to store conversation memory
DB_NAME = "conversation.db"


def get_conn():
    """
    Creates and returns a SQLite database connection.
    check_same_thread=False allows access from different parts of the app.
    """
    return sqlite3.connect(DB_NAME, check_same_thread=False)


# Create memory table if it does not already exist
# Stores one value per key per session
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
    """
    Saves or updates a key-value pair for a given session.
    Used to remember user details across conversation turns.
    """
    with get_conn() as conn:
        conn.execute(
            "INSERT OR REPLACE INTO memory VALUES (?, ?, ?)",
            (session_id, key, str(value))
        )


def get_memory(session_id, key):
    """
    Fetches a specific stored value for a session and key.
    Returns None if the value does not exist.
    """
    with get_conn() as conn:
        row = conn.execute(
            "SELECT value FROM memory WHERE session_id=? AND key=?",
            (session_id, key)
        ).fetchone()

    return row[0] if row else None


def memory_snapshot(session_id):
    """
    Returns all stored memory for a session as a dictionary.
    This snapshot is used by the planner to decide next actions.
    """
    with get_conn() as conn:
        rows = conn.execute(
            "SELECT key, value FROM memory WHERE session_id=?",
            (session_id,)
        ).fetchall()

    snap = {}
    for k, v in rows:
        # Convert numeric values back to integers where possible
        snap[k] = int(v) if v.isdigit() else v

    return snap


def check_contradiction(session_id, key, new_value):
    """
    Checks whether the user is changing a previously given value.
    If a contradiction is found, a confirmation message is returned.
    """
    old = get_memory(session_id, key)

    if old and old != str(new_value):
        return f"మీరు ముందుగా {old} చెప్పారు. ఇప్పుడు {new_value}. నిర్ధారించాలా?"

    return None
