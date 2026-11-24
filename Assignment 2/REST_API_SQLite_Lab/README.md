# Assignment 2 – Student Management REST API with SQLite

**Muhammad Hassan Siddiqui – CT-23094 – Department of Computer Science**

The Assignment 1 API, upgraded to store students permanently in a SQLite database
(`students.db`) through the SQLAlchemy ORM.

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

`students.db` is created automatically the first time the server runs.
Swagger UI is at http://127.0.0.1:8000/docs.

## Endpoints

| Method | Endpoint | Operation | SQL equivalent | Success | Errors |
|---|---|---|---|---|---|
| GET | `/students` | All students | `SELECT * FROM students` | 200 | – |
| GET | `/students/{id}` | One student | `SELECT … WHERE id = ?` | 200 | 404, 422 |
| GET | `/students/department/{department}` | Students in a department (Task 7) | `SELECT … WHERE lower(department) = ?` | 200 | 404 |
| POST | `/students` | Add student | `INSERT INTO students …` | 201 | 422 |
| PUT | `/students/{id}` | Replace record | `UPDATE … SET all fields` | 200 | 404, 422 |
| PATCH | `/students/{id}` | Update selected fields | `UPDATE … SET some fields` | 200 | 400, 404, 422 |
| DELETE | `/students/{id}` | Delete student | `DELETE FROM students WHERE id = ?` | 204 | 404 |

## Testing

1. **Swagger UI**: `/docs`, then **Try it out** and **Execute**.
2. **Postman**: import `Student_API_A2.postman_collection.json`.
3. **Automated** (start from an empty database: delete `students.db`, then start the server):
   - `python test_api.py` runs all the tests and writes `test_results.md`.
   - `python verify_db.py` reads `students.db` directly (Task 5).
   - Stop the server (CTRL + C), start it again, then run `python persistence_check.py` (Task 6).

You can also open `students.db` in **DB Browser for SQLite** (Browse Data, then the `students` table).

## Switching to MySQL

```
pip install pymysql
```

Then change only the database configuration in `main.py`:

```python
DATABASE_URL = "mysql+pymysql://root:YOUR_PASSWORD@localhost:3306/student_db"
engine = create_engine(DATABASE_URL)
```
