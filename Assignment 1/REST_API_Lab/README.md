# Assignment 1 – Student Management REST API (FastAPI)

**Muhammad Hassan Siddiqui – CT-23094 – Department of Computer Science**

A REST API that manages student records stored in a Python dictionary (in memory).
It supports GET, POST, PUT, PATCH and DELETE.

## Setup (Windows, VS Code terminal)

```
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## Run

```
uvicorn main:app --reload
```

- API: http://127.0.0.1:8000
- Swagger UI: http://127.0.0.1:8000/docs

## Endpoints

| Method | Endpoint | Operation | Success | Errors |
|---|---|---|---|---|
| GET | `/students` | Retrieve all students | 200 | – |
| GET | `/students/{student_id}` | Retrieve one student | 200 | 404, 422 |
| POST | `/students` | Add a new student | 201 | 422 |
| PUT | `/students/{student_id}` | Replace a complete record | 200 | 404, 422 |
| PATCH | `/students/{student_id}` | Update selected fields | 200 | 400, 404, 422 |
| DELETE | `/students/{student_id}` | Delete a student | 204 | 404 |

## Testing

1. **Swagger UI**: open `/docs`, choose an endpoint, click **Try it out**, then **Execute**.
2. **Postman**: import `Student_API_A1.postman_collection.json` and run the requests in order.
3. **Automated**: keep the server running and, in a second terminal, run `python test_api.py`.
   The script runs all 24 tests and writes `test_results.md`.

The records are stored in memory, so restarting the server resets them to students 101–103.
