from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI(title="Task API", version="1.0")


tasks_db = [
    {"id": 1, "title": "Buy milk", "done": False},
    {"id": 2, "title": "Do laundry", "done": True},
    {"id": 3, "title": "Learn FastAPI", "done": False}
]


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
    return tasks_db


@app.get("/tasks/{id}")
def get_task(id: int):
    task = next((t for t in tasks_db if t["id"] == id), None)

    if not task:
        return JSONResponse(
            status_code=404,
            content={"error": f"Task {id} not found"}
        )

    return task


@app.post("/tasks", status_code=201)
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
