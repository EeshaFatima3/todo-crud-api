# To-Do List CRUD API (FastAPI)

A lightweight RESTful CRUD API built with Python and FastAPI for managing a to-do list in memory. Built for the FlyRank Week 2 Assignment.

## How to Install & Run

You can get this API running on your local machine in under a minute. Run these commands in your terminal:

```bash
# 1. Clone this repository
git clone https://github.com/EeshaFatima3/todo-crud-api.git
cd todo-crud-api

# 2. Install the required dependencies
pip install fastapi uvicorn

# 3. Start the server
python -m uvicorn main:app --reload --port 8000
```

Once the server is running, open your web browser and navigate to `http://localhost:8000/docs` to interact with the API using the Swagger UI.

---

## API Endpoints Table

| Method | Endpoint | Description | Expected Status |
| --- | --- | --- | --- |
| GET | `/` | API Metadata | `200 OK` |
| GET | `/health` | Health Check | `200 OK` |
| GET | `/tasks` | List all tasks | `200 OK` |
| GET | `/tasks/{id}` | Get single task | `200 OK` / `404 Not Found` |
| POST | `/tasks` | Create task | `201 Created` / `400 Bad Request` |
| PUT | `/tasks/{id}` | Update task | `200 OK` / `400` / `404` |
| DELETE | `/tasks/{id}` | Delete task | `204 No Content` / `404` |

---

## Sample Request & Output (`curl -i`)

**Request:**
```bash
curl.exe -i -X DELETE http://localhost:8000/tasks/1
```

**Output:**
```http
HTTP/1.1 204 No Content
date: Sat, 08 Aug 2026 15:21:05 GMT
server: uvicorn
```

---

## Swagger UI Screenshot

![Swagger UI](swagger.png)