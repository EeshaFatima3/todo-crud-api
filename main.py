import sqlite3

from fastapi import FastAPI

app = FastAPI(title="Task API", version="1.0")

DB_NAME = "tasks.db"


def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db_connection()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            done BOOLEAN NOT NULL
        )
    """)

    count = conn.execute(
        "SELECT COUNT(*) FROM tasks"
    ).fetchone()[0]

    if count == 0:
        conn.executemany(
            """
            INSERT INTO tasks (id, title, done)
            VALUES (?, ?, ?)
            """,
            [
                (1, "Buy milk", 0),
                (2, "Do laundry", 1),
                (3, "Learn FastAPI", 0)
            ]
        )

    conn.commit()
    conn.close()


init_db()


@app.get("/")
def read_root():
    return {
        "name": "Task API",
        "version": "1.0",
        "endpoints": ["/tasks"]
    }


@app.get("/health")
def health_check():
    return {"status": "ok"}
