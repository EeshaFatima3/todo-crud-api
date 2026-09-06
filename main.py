import sqlite3

from fastapi import FastAPI
from fastapi.responses import JSONResponse

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


@app.get("/tasks")
def get_tasks():
    conn = get_db_connection()

    tasks = conn.execute(
        "SELECT * FROM tasks"
    ).fetchall()

    conn.close()

    return [dict(task) for task in tasks]


@app.get("/tasks/{id}")
def get_task(id: int):
    conn = get_db_connection()

    task = conn.execute(
        "SELECT * FROM tasks WHERE id = ?",
        (id,)
    ).fetchone()

    conn.close()

    if task is None:
        return JSONResponse(
            status_code=404,
            content={"error": "Task not found"}
        )

    return dict(task)
