# Task API

A simple FastAPI CRUD API for managing tasks.

## Getting started

### Windows (PowerShell)

```powershell
python -m venv venv
venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

If activation fails with an error mentioning "running scripts is disabled on this system," run this once in the same window, then try activating again:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
```

This only affects the current terminal window — it resets the next time you open a new one, so it's safe to run each time you start working.

### macOS / Linux

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

### After the server starts

You should see `Application startup complete.` in the terminal. Leave this window open and running — the API is now live at `http://localhost:8000`.

OpenAPI docs (Swagger UI) are at [http://localhost:8000/docs](http://localhost:8000/docs). The spec is generated automatically from the code — no separate spec file needed. This is also the easiest way to test the API: click "Try it out" on any endpoint, no terminal commands required.

### Testing with curl

The server occupies its terminal window while running, so open a **second terminal** to send test requests (a new tab in VS Code, a split pane, or any other terminal window — it doesn't need to be activated or in the project folder).

**Windows (PowerShell) users:** PowerShell has a built-in `curl` that behaves differently from real curl and will not work with the examples below. Use `curl.exe` instead of `curl` for every command in this README:

```powershell
curl.exe -i http://localhost:8000/tasks
```

**macOS / Linux users:** plain `curl` works as written in every example below.

## Endpoints

### `GET /`

Returns metadata about the API.

**Response**

```json
{
  "name": "Task API",
  "version": "1.0",
  "endpoints": ["/tasks", "/stats", "/reset"]
}
```

**Example**

```bash
curl http://localhost:8000/
```

### `GET /health`

Health check endpoint.

**Response**

```json
{
  "status": "ok"
}
```

**Example**

```bash
curl http://localhost:8000/health
```

### `GET /tasks`

Returns all tasks. Optional query parameters filter the list (the part after `?` — filters, not addresses).

| Query | Example | Effect |
|-------|---------|--------|
| `done` | `?done=true` | Only finished tasks |
| `done` | `?done=false` | Only open tasks |
| `search` | `?search=milk` | Title contains the word (case-insensitive) |

Filters can be combined: `?done=false&search=book`

**Response**

```json
[
  { "id": 1, "title": "Buy groceries", "done": false },
  { "id": 2, "title": "Walk the dog", "done": true },
  { "id": 3, "title": "Read a book", "done": false }
]
```

**Example**

```bash
curl http://localhost:8000/tasks
curl "http://localhost:8000/tasks?done=true"
curl "http://localhost:8000/tasks?search=milk"
```

### `GET /stats`

Returns computed counts for the current task list.

**Response**

```json
{ "total": 7, "done": 3, "open": 4 }
```

**Example**

```bash
curl http://localhost:8000/stats
```

### `POST /reset`

Restores the three seed example tasks. Useful for demos and testing.

**Response (200)**

```json
[
  { "id": 1, "title": "Buy groceries", "done": false },
  { "id": 2, "title": "Walk the dog", "done": true },
  { "id": 3, "title": "Read a book", "done": false }
]
```

**Example**

```bash
curl -X POST http://localhost:8000/reset
```

### `GET /tasks/{id}`

Returns a single task by id.

**Response (200)**

```json
{ "id": 1, "title": "Buy groceries", "done": false }
```

**Response (404)**

```json
{ "detail": "Task 99 not found" }
```

**Example**

```bash
curl http://localhost:8000/tasks/1
curl http://localhost:8000/tasks/99
```

### `POST /tasks`

Creates a new task.

**Request body**

```json
{ "title": "Buy milk" }
```

**Response (201)**

```json
{ "id": 4, "title": "Buy milk", "done": false }
```

**Response (400)**

```json
{ "detail": "title is required and cannot be empty" }
```

**Example**

```bash
curl -X POST http://localhost:8000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Buy milk"}'
```

### `PUT /tasks/{id}`

Updates a task's `title` and/or `done`. Send one or both fields; omitted fields stay unchanged.

**Request body**

```json
{ "title": "Buy oat milk", "done": true }
```

**Response (200)**

```json
{ "id": 1, "title": "Buy oat milk", "done": true }
```

**Response (400)**

```json
{ "detail": "request body must include title and/or done" }
```

**Response (404)**

```json
{ "detail": "Task 99 not found" }
```

**Example**

```bash
curl -X PUT http://localhost:8000/tasks/1 \
  -H "Content-Type: application/json" \
  -d '{"done": true}'
```

### `DELETE /tasks/{id}`

Deletes a task.

**Response (204)**

Empty body — success, nothing to return.

**Response (404)**

```json
{ "detail": "Task 99 not found" }
```

**Example**

```bash
curl -X DELETE http://localhost:8000/tasks/1
```
