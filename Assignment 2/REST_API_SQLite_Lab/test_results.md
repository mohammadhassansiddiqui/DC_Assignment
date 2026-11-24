# Test Results - Student Management API with SQLite (Assignment 2)

**30/30 tests passed**

| ID | Test | Method | Endpoint | Request body | Expected | Actual | Result | Response |
|---|---|---|---|---|---|---|---|---|
| A | POST - insert first student Ali | POST | `/students` | `{"name": "Ali", "age": 20, "department": "Computer Science"}` | 201 | 201 | PASS | `{"id": 1, "name": "Ali", "age": 20, "department": "Computer Science"}` |
| B1 | POST - insert Sara | POST | `/students` | `{"name": "Sara", "age": 21, "department": "Information Technology"}` | 201 | 201 | PASS | `{"id": 2, "name": "Sara", "age": 21, "department": "Information Technology"}` |
| B2 | POST - insert Ahmed | POST | `/students` | `{"name": "Ahmed", "age": 22, "department": "Software Engineering"}` | 201 | 201 | PASS | `{"id": 3, "name": "Ahmed", "age": 22, "department": "Software Engineering"}` |
| C | GET - retrieve all students | GET | `/students` | `-` | 200 | 200 | PASS | `[{"id": 1, "name": "Ali", "age": 20, "department": "Computer Science"}, {"id": 2, "name": "Sara", "age": 21, "department": "Information Technology"}, {"id": 3, "name": "Ahmed", "age": 22, "department": "Software Engineering"}]` |
| D | PATCH - change department of student 1 | PATCH | `/students/1` | `{"department": "Artificial Intelligence"}` | 200 | 200 | PASS | `{"id": 1, "name": "Ali", "age": 20, "department": "Artificial Intelligence"}` |
| T1.1 | POST - insert Hassan | POST | `/students` | `{"name": "Hassan", "age": 23, "department": "Artificial Intelligence"}` | 201 | 201 | PASS | `{"id": 4, "name": "Hassan", "age": 23, "department": "Artificial Intelligence"}` |
| T1.2 | POST - insert Fatima | POST | `/students` | `{"name": "Fatima", "age": 20, "department": "Computer Science"}` | 201 | 201 | PASS | `{"id": 5, "name": "Fatima", "age": 20, "department": "Computer Science"}` |
| T1.3 | POST - insert Usman | POST | `/students` | `{"name": "Usman", "age": 22, "department": "Cyber Security"}` | 201 | 201 | PASS | `{"id": 6, "name": "Usman", "age": 22, "department": "Cyber Security"}` |
| T1.4 | POST - insert Ayesha | POST | `/students` | `{"name": "Ayesha", "age": 21, "department": "Data Science"}` | 201 | 201 | PASS | `{"id": 7, "name": "Ayesha", "age": 21, "department": "Data Science"}` |
| T1.5 | POST - insert Bilal | POST | `/students` | `{"name": "Bilal", "age": 24, "department": "Computer Science"}` | 201 | 201 | PASS | `{"id": 8, "name": "Bilal", "age": 24, "department": "Computer Science"}` |
| T2a | GET - retrieve all students | GET | `/students` | `-` | 200 | 200 | PASS | `[{"id": 1, "name": "Ali", "age": 20, "department": "Artificial Intelligence"}, {"id": 2, "name": "Sara", "age": 21, "department": "Information Technology"}, {"id": 3, "name": "Ahmed", "age": 22, "department": "Software Engineering"}, {"id": 4, "name": "Hassan", "age": 23, "department": "Artificial I ...` |
| T2b | GET - retrieve student by ID 5 | GET | `/students/5` | `-` | 200 | 200 | PASS | `{"id": 5, "name": "Fatima", "age": 20, "department": "Computer Science"}` |
| T3 | PATCH - update department of student 2 | PATCH | `/students/2` | `{"department": "Cyber Security"}` | 200 | 200 | PASS | `{"id": 2, "name": "Sara", "age": 21, "department": "Cyber Security"}` |
| T3b | PUT - replace complete record of student 4 | PUT | `/students/4` | `{"name": "Hassan Raza", "age": 24, "department": "Data Science"}` | 200 | 200 | PASS | `{"id": 4, "name": "Hassan Raza", "age": 24, "department": "Data Science"}` |
| T4 | DELETE - remove student 3 | DELETE | `/students/3` | `-` | 204 | 204 | PASS | `(empty body)` |
| T4b | GET - verify student 3 no longer exists | GET | `/students/3` | `-` | 404 | 404 | PASS | `{"detail": "Student not found"}` |
| T7a | GET - students in Computer Science | GET | `/students/department/Computer Science` | `-` | 200 | 200 | PASS | `[{"id": 5, "name": "Fatima", "age": 20, "department": "Computer Science"}, {"id": 8, "name": "Bilal", "age": 24, "department": "Computer Science"}]` |
| T7b | GET - department search is case-insensitive | GET | `/students/department/data science` | `-` | 200 | 200 | PASS | `[{"id": 4, "name": "Hassan Raza", "age": 24, "department": "Data Science"}, {"id": 7, "name": "Ayesha", "age": 21, "department": "Data Science"}]` |
| T7c | GET - department with no students | GET | `/students/department/Physics` | `-` | 404 | 404 | PASS | `{"detail": "No students found in department 'Physics'"}` |
| ER1 | GET non-existent student 999 | GET | `/students/999` | `-` | 404 | 404 | PASS | `{"detail": "Student not found"}` |
| ER2 | POST age sent as text | POST | `/students` | `{"name": "Zain", "age": "twenty", "department": "CS"}` | 422 | 422 | PASS | `{"detail": [{"type": "int_parsing", "loc": ["body", "age"], "msg": "Input should be a valid integer, unable to parse string as an integer", "input": "twenty"}]}` |
| ER3 | POST without name field | POST | `/students` | `{"age": 20, "department": "CS"}` | 422 | 422 | PASS | `{"detail": [{"type": "missing", "loc": ["body", "name"], "msg": "Field required", "input": {"age": 20, "department": "CS"}}]}` |
| ER4 | PUT non-existent student 999 | PUT | `/students/999` | `{"name": "Ghost", "age": 20, "department": "CS"}` | 404 | 404 | PASS | `{"detail": "Student not found"}` |
| ER5 | PATCH non-existent student 999 | PATCH | `/students/999` | `{"age": 25}` | 404 | 404 | PASS | `{"detail": "Student not found"}` |
| ER6 | PATCH with empty body {} | PATCH | `/students/1` | `{}` | 400 | 400 | PASS | `{"detail": "No update fields provided"}` |
| ER7 | PATCH with unknown field | PATCH | `/students/1` | `{"cgpa": 3.5}` | 422 | 422 | PASS | `{"detail": [{"type": "extra_forbidden", "loc": ["body", "cgpa"], "msg": "Extra inputs are not permitted", "input": 3.5}]}` |
| ER8 | DELETE non-existent student 999 | DELETE | `/students/999` | `-` | 404 | 404 | PASS | `{"detail": "Student not found"}` |
| ER9 | POST negative age | POST | `/students` | `{"name": "Omar", "age": -5, "department": "CS"}` | 422 | 422 | PASS | `{"detail": [{"type": "greater_than", "loc": ["body", "age"], "msg": "Input should be greater than 0", "input": -5, "ctx": {"gt": 0}}]}` |
| ER10 | GET non-integer student ID | GET | `/students/abc` | `-` | 422 | 422 | PASS | `{"detail": [{"type": "int_parsing", "loc": ["path", "student_id"], "msg": "Input should be a valid integer, unable to parse string as an integer", "input": "abc"}]}` |
| F1 | GET - final list of students | GET | `/students` | `-` | 200 | 200 | PASS | `[{"id": 1, "name": "Ali", "age": 20, "department": "Artificial Intelligence"}, {"id": 2, "name": "Sara", "age": 21, "department": "Cyber Security"}, {"id": 4, "name": "Hassan Raza", "age": 24, "department": "Data Science"}, {"id": 5, "name": "Fatima", "age": 20, "department": "Computer Science"}, {" ...` |
