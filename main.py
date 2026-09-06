from fastapi import FastAPI
from fastapi.responses import JSONResponse, Response

app = FastAPI(title="Task API", version="1.0")


tasks_db = [
    {"id": 1, "title": "Buy milk", "done": False},
    {"id": 2, "title": "Do laundry", "done": True},
    {"id": 3, "title": "Learn FastAPI", "done": False}
]


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
    description="Returns all tasks."
)
def get_tasks():
    return tasks_db


@app.get(
    "/tasks/{id}",
    summary="Get a task",
    description="Returns a task by its ID. Returns 404 if the task does not exist."
)
def get_task(id: int):
    task = next((t for t in tasks_db if t["id"] == id), None)

    if not task:
        return JSONResponse(
            status_code=404,
            content={"error": f"Task {id} not found"}
        )

    return task


@app.post(
    "/tasks",
    status_code=201,
    summary="Create a task",
    description="Creates a new task. The title is required."
)
def create_task(task_data: dict):
    title = task_data.get("title")

    if not title or not str(title).strip():
        return JSONResponse(
            status_code=400,
            content={"error": "Title is required and cannot be empty"}
        )

    new_id = max([t["id"] for t in tasks_db], default=0) + 1

    new_task = {
        "id": new_id,
        "title": str(title).strip(),
        "done": False
    }

    tasks_db.append(new_task)

    return new_task


@app.put(
    "/tasks/{id}",
    summary="Update a task",
    description="Updates the title and/or completion status of an existing task."
)
def update_task(id: int, task_data: dict):
    task = next((t for t in tasks_db if t["id"] == id), None)

    if not task:
        return JSONResponse(
            status_code=404,
            content={"error": f"Task {id} not found"}
        )

    if "title" in task_data:
        title = task_data["title"]

        if not title or not str(title).strip():
            return JSONResponse(
                status_code=400,
                content={"error": "Title cannot be empty"}
            )

        task["title"] = str(title).strip()

    if "done" in task_data:
        task["done"] = bool(task_data["done"])

    return task


@app.delete(
    "/tasks/{id}",
    status_code=204,
    summary="Delete a task",
    description="Deletes an existing task."
)
def delete_task(id: int):
    task = next((t for t in tasks_db if t["id"] == id), None)

    if not task:
        return JSONResponse(
            status_code=404,
            content={"error": f"Task {id} not found"}
        )

    tasks_db.remove(task)

    return Response(status_code=204)
