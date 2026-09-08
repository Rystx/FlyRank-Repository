#Stage 0
from fastapi import FastAPI, HTTPException, Query
from typing import Optional
from pydantic import BaseModel

app = FastAPI(
    title="Task API",
    version="1.0",
    description="In-memory CRUD API for tasks.",
)


class Task(BaseModel):
    id: int
    title: str
    done: bool

class CreateTaskRequest(BaseModel):
    title: str

class UpdateTaskRequest(BaseModel):
    title: Optional[str] = None
    done: Optional[bool] = None


SEED_TASKS = [
    {"id": 1, "title": "Buy groceries", "done": False},
    {"id": 2, "title": "Walk the dog", "done": True},
    {"id": 3, "title": "Read a book", "done": False},
]

tasks = [dict(task) for task in SEED_TASKS]

def reset_tasks():
    tasks.clear()
    tasks.extend(dict(task) for task in SEED_TASKS)


#Stage 1

@app.get("/", summary="API info", description="Returns basic metadata about the API.")
def root():
    return {
        "name": "Task API",
        "version": "1.0",
        "endpoints": ["/tasks", "/stats", "/reset"],
    }

@app.get("/health", summary="Health check", description="Returns a simple status to confirm the server is alive.")
def health():
    return {"status": "ok"}

#Stage 2
@app.get("/tasks", summary="List tasks", description="Returns all tasks, optionally filtered by done status and/or a search word in the title.")
def list_tasks(done: Optional[bool] = None, search: Optional[str] = Query(None)):
    result = tasks

    if done is not None:
        result = [t for t in result if t["done"] == done]

    if search is not None:
        word = search.strip()
        if word == "":
            raise HTTPException(status_code=400, detail="search must not be empty")
        lower = word.lower()
        result = [t for t in result if lower in t["title"].lower()]

    return result


@app.get("/stats", summary="Task counts", description="Returns aggregate counts: total, done, and open tasks.")
def get_stats():
    done_count = sum(1 for t in tasks if t["done"])
    return {
        "total": len(tasks),
        "done": done_count,
        "open": len(tasks) - done_count,
    }


@app.post("/reset", summary="Reset to seed data", description="Restores the three seed example tasks. Useful for demos and testing.")
def reset():
    reset_tasks()
    return tasks


#Stage 3

@app.post("/tasks", status_code=201, summary="Create a task", description="Creates a new task from a title. The new task starts with done set to false.")
def create_task(body: CreateTaskRequest):
    title = body.title.strip() if body.title else ""

    if title == "":
        raise HTTPException(status_code=400, detail="title is required and cannot be empty")

    new_id = 1 if len(tasks) == 0 else max(t["id"] for t in tasks) + 1
    task = {"id": new_id, "title": title, "done": False}

    tasks.append(task)
    return task

@app.get("/tasks/{id}", summary="Get one task", description="Returns a single task by id, or a 404 error if it doesn't exist.")
def get_task(id: int):
    task = next((t for t in tasks if t["id"] == id), None)

    if task is None:
        raise HTTPException(status_code=404, detail=f"Task {id} not found")

    return task

#Stage 4

@app.put("/tasks/{id}", summary="Update a task", description="Updates a task's title and/or done status. At least one field must be provided.")
def update_task(id: int, body: UpdateTaskRequest):
    task = next((t for t in tasks if t["id"] == id), None)

    if task is None:
        raise HTTPException(status_code=404, detail=f"Task {id} not found")

    has_title = body.title is not None
    has_done = body.done is not None

    if not has_title and not has_done:
        raise HTTPException(status_code=400, detail="request body must include title and/or done")

    if has_title:
        trimmed = body.title.strip()
        if trimmed == "":
            raise HTTPException(status_code=400, detail="title cannot be empty")
        task["title"] = trimmed

    if has_done:
        task["done"] = body.done

    return task

@app.delete("/tasks/{id}", status_code=204, summary="Delete a task", description="Deletes a task by id, or returns a 404 error if it doesn't exist.")
def delete_task(id: int):
    index = next((i for i, t in enumerate(tasks) if t["id"] == id), -1)

    if index == -1:
        raise HTTPException(status_code=404, detail=f"Task {id} not found")

    tasks.pop(index)
    return None
