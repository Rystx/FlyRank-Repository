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
