import sqlite3
from contextlib import contextmanager


@contextmanager
def db_session():
    conn = sqlite3.connect("chat_log.db")
    c = conn.cursor()
    try:
        yield c
    finally:
        conn.commit()
        conn.close()


def init_db():
    with db_session() as c:
        c.execute(
            """
            CREATE TABLE IF NOT EXISTS chat_log (
                id INTEGER PRIMARY KEY,
                role TEXT,
                content TEXT
            )
        """
        )
        # Check if the system entry already exists
        system_entry_exists = c.execute(
            "SELECT COUNT(*) FROM chat_log WHERE role = 'system'"
        ).fetchone()[0]

        # If it doesn't exist, insert the default system entry
        if not system_entry_exists:
            c.execute(
                "INSERT INTO chat_log (role, content) VALUES (?, ?)",
                (
                    "system",
                    "You are a helpful, Discord bot. Respond with plain text as accurately as possible to the commands, with just a sprinkle of humor.",
                ),
            )


def clear_table(table_name):
    with db_session() as c:
        c.execute(f"DELETE FROM {table_name}")


def add_message(role, content):
    with db_session() as c:
        c.execute("INSERT INTO chat_log (role, content) VALUES (?, ?)", (role, content))


def get_chat_log():
    with db_session() as c:
        c.execute("SELECT role, content FROM chat_log")
        chat_log = [
            {"role": role, "content": content} for role, content in c.fetchall()
        ]
    return chat_log
