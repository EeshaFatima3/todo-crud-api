import sqlite3

from fastapi import FastAPI
from fastapi.responses import JSONResponse, Response

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


@app.get(
    "/",
    summary="API information",
    description="Returns the Task API name, version, and available endpoints."
)
def read_root():
    return {
        "name": "Task API",
        "version": "1.0",
        "endpoints": ["/tasks"]
    }


@app.get(
    "/health",
    summary="Health check",
    description="Checks whether the API is running."
)
def health_check():
    return {"status": "ok"}


@app.get(
    "/tasks",
    summary="Get all tasks",
    description="Returns all tasks from the SQLite database."
)
def get_tasks():
    conn = get_db_connection()

    tasks = conn.execute(
        "SELECT * FROM tasks"
    ).fetchall()

    conn.close()

    return [dict(task) for task in tasks]


@app.get(
    "/tasks/{id}",
    summary="Get a task",
    description="Returns a task by its ID."
)
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


@app.post(
    "/tasks",
    status_code=201,
    summary="Create a task",
    description="Creates a new task in the SQLite database."
)
def create_task(task_data: dict):
    title = task_data.get("title")

    if not title or not str(title).strip():
        return JSONResponse(
            status_code=400,
            content={"error": "Title is required and cannot be empty"}
        )

    conn = get_db_connection()

    cursor = conn.execute(
        """
        INSERT INTO tasks (title, done)
        VALUES (?, ?)
        """,
        (str(title).strip(), 0)
    )

    new_id = cursor.lastrowid

    conn.commit()

    task = conn.execute(
        "SELECT * FROM tasks WHERE id = ?",
        (new_id,)
    ).fetchone()

    conn.close()

    return dict(task)


@app.put(
    "/tasks/{id}",
    summary="Update a task",
    description="Updates the title and/or completion status of a task."
)
def update_task(id: int, task_data: dict):
    conn = get_db_connection()

    task = conn.execute(
        "SELECT * FROM tasks WHERE id = ?",
        (id,)
    ).fetchone()

    if task is None:
        conn.close()
        return JSONResponse(
            status_code=404,
            content={"error": "Task not found"}
        )

    if "title" in task_data:
        title = task_data["title"]

        if not title or not str(title).strip():
            conn.close()
            return JSONResponse(
                status_code=400,
                content={"error": "Title cannot be empty"}
            )

        conn.execute(
            "UPDATE tasks SET title = ? WHERE id = ?",
            (str(title).strip(), id)
        )

    if "done" in task_data:
        conn.execute(
            "UPDATE tasks SET done = ? WHERE id = ?",
            (bool(task_data["done"]), id)
        )

    conn.commit()

    updated_task = conn.execute(
        "SELECT * FROM tasks WHERE id = ?",
        (id,)
    ).fetchone()

    conn.close()

    return dict(updated_task)


@app.delete(
    "/tasks/{id}",
    status_code=204,
    summary="Delete a task",
    description="Deletes a task from the SQLite database."
)
def delete_task(id: int):
    conn = get_db_connection()

    task = conn.execute(
        "SELECT * FROM tasks WHERE id = ?",
        (id,)
    ).fetchone()

    if task is None:
        conn.close()
        return JSONResponse(
            status_code=404,
            content={"error": "Task not found"}
        )

    conn.execute(
        "DELETE FROM tasks WHERE id = ?",
        (id,)
    )

    conn.commit()
    conn.close()

    return Response(status_code=204)
