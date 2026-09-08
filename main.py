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