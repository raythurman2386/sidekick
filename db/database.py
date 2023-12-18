import sqlite3
from contextlib import contextmanager
from utils.logger import app_logger


@contextmanager
def db_session():
    conn = sqlite3.connect("chat_log.db")
    app_logger.info("Database connected successfully!")
    c = conn.cursor()
    try:
        yield c
    finally:
        conn.commit()
        conn.close()
        app_logger.info("Database closed successfully!")


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
                    "You are a helpful, Discord bot. Respond with markdown as accurately as possible to the commands, with just a sprinkle of humor.",
                ),
            )

        c.execute(
            """
            CREATE TABLE IF NOT EXISTS authorized_users (
                id INTEGER PRIMARY KEY,
                user_id TEXT
            )
        """
        )
        c.execute(
            """
            CREATE TABLE IF NOT EXISTS moderators (
                id INTEGER PRIMARY KEY,
                user_id TEXT
            )
        """
        )


def get_user_from_table(user_id, table_name):
    with db_session() as c:
        c.execute(f"SELECT * FROM {table_name} WHERE user_id = ?", (user_id,))
        user = c.fetchone()
    return user


def add_user_to_table(user_id, table_name):
    with db_session() as c:
        c.execute(f"INSERT INTO {table_name} (user_id) VALUES (?)", (user_id,))


def update_user_in_table(user_id, table_name, column_name, new_value):
    with db_session() as c:
        c.execute(
            f"UPDATE {table_name} SET {column_name} = ? WHERE user_id = ?",
            (new_value, user_id),
        )


def remove_user_from_table(user_id, table_name):
    with db_session() as c:
        c.execute(f"DELETE FROM {table_name} WHERE user_id=?", (user_id,))


def is_user_in_table(user_id, table_name):
    with db_session() as c:
        c.execute(f"SELECT * FROM {table_name} WHERE user_id=?", (user_id,))
        result = c.fetchone()
    return result is not None


def get_user_from_table(user_id, table_name):
    with db_session() as c:
        c.execute(f"SELECT * FROM {table_name} WHERE user_id = ?", (user_id,))
        user = c.fetchone()
    return user


def get_all_users_from_table(table_name):
    with db_session() as c:
        c.execute(f"SELECT * FROM {table_name}")
        users = c.fetchall()
    return users


def count_users_in_table(table_name):
    with db_session() as c:
        c.execute(f"SELECT COUNT(*) FROM {table_name}")
        count = c.fetchone()[0]
    return count


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
