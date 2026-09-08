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
