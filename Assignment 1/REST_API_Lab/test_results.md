# Test Results - Student Management API (Assignment 1)

**24/24 tests passed**

| ID | Test | Method | Endpoint | Request body | Expected | Actual | Result | Response |
|---|---|---|---|---|---|---|---|---|
| E1 | GET - retrieve all students | GET | `/students` | `-` | 200 | 200 | PASS | `{"101": {"name": "Ali", "age": 20, "department": "Computer Science"}, "102": {"name": "Sara", "age": 21, "department": "Information Technology"}, "103": {"name": "Ahmed", "age": 22, "department": "Software Engineering"}}` |
| E2 | GET - retrieve student 101 | GET | `/students/101` | `-` | 200 | 200 | PASS | `{"name": "Ali", "age": 20, "department": "Computer Science"}` |
| E3 | POST - add new student Zara | POST | `/students` | `{"name": "Zara", "age": 20, "department": "Artificial Intelligence"}` | 201 | 201 | PASS | `{"message": "Student added successfully", "student_id": 104, "student": {"name": "Zara", "age": 20, "department": "Artificial Intelligence"}}` |
| E4 | PUT - replace student 101 | PUT | `/students/101` | `{"name": "Ali Khan", "age": 21, "department": "Data Science"}` | 200 | 200 | PASS | `{"message": "Student updated successfully", "student": {"name": "Ali Khan", "age": 21, "department": "Data Science"}}` |
| E5 | PATCH - update only age of 101 | PATCH | `/students/101` | `{"age": 23}` | 200 | 200 | PASS | `{"message": "Student partially updated", "student": {"name": "Ali Khan", "age": 23, "department": "Data Science"}}` |
| E6 | DELETE - remove student 104 (Zara) | DELETE | `/students/104` | `-` | 204 | 204 | PASS | `(empty body)` |
| X1 | Add new student Hassan | POST | `/students` | `{"name": "Hassan", "age": 23, "department": "Artificial Intelligence"}` | 201 | 201 | PASS | `{"message": "Student added successfully", "student_id": 104, "student": {"name": "Hassan", "age": 23, "department": "Artificial Intelligence"}}` |
| X1b | Verify Hassan was added | GET | `/students/104` | `-` | 200 | 200 | PASS | `{"name": "Hassan", "age": 23, "department": "Artificial Intelligence"}` |
| X2 | Search for student 102 | GET | `/students/102` | `-` | 200 | 200 | PASS | `{"name": "Sara", "age": 21, "department": "Information Technology"}` |
| X3 | PATCH department of 101 to Cyber Security | PATCH | `/students/101` | `{"department": "Cyber Security"}` | 200 | 200 | PASS | `{"message": "Student partially updated", "student": {"name": "Ali Khan", "age": 23, "department": "Cyber Security"}}` |
| X4 | PUT - replace complete record of 102 | PUT | `/students/102` | `{"name": "Sara Ahmed", "age": 22, "department": "Data Science"}` | 200 | 200 | PASS | `{"message": "Student updated successfully", "student": {"name": "Sara Ahmed", "age": 22, "department": "Data Science"}}` |
| X5 | DELETE student 103 | DELETE | `/students/103` | `-` | 204 | 204 | PASS | `(empty body)` |
| X5b | Verify 103 no longer exists | GET | `/students/103` | `-` | 404 | 404 | PASS | `{"detail": "Student not found"}` |
| ER1 | Search for student 999 | GET | `/students/999` | `-` | 404 | 404 | PASS | `{"detail": "Student not found"}` |
| ER2 | Age sent as text | POST | `/students` | `{"name": "Bilal", "age": "twenty", "department": "CS"}` | 422 | 422 | PASS | `{"detail": [{"type": "int_parsing", "loc": ["body", "age"], "msg": "Input should be a valid integer, unable to parse string as an integer", "input": "twenty"}]}` |
| ER3 | POST without name field | POST | `/students` | `{"age": 20, "department": "CS"}` | 422 | 422 | PASS | `{"detail": [{"type": "missing", "loc": ["body", "name"], "msg": "Field required", "input": {"age": 20, "department": "CS"}}]}` |
| ER4 | PUT on non-existent student 999 | PUT | `/students/999` | `{"name": "Ghost", "age": 20, "department": "CS"}` | 404 | 404 | PASS | `{"detail": "Student not found"}` |
| ER5 | PATCH on non-existent student 999 | PATCH | `/students/999` | `{"age": 25}` | 404 | 404 | PASS | `{"detail": "Student not found"}` |
| ER6 | PATCH with empty body {} | PATCH | `/students/101` | `{}` | 400 | 400 | PASS | `{"detail": "Invalid or empty update fields"}` |
| ER7 | PATCH with unknown field | PATCH | `/students/101` | `{"cgpa": 3.5}` | 422 | 422 | PASS | `{"detail": [{"type": "extra_forbidden", "loc": ["body", "cgpa"], "msg": "Extra inputs are not permitted", "input": 3.5}]}` |
| ER8 | DELETE non-existent student 999 | DELETE | `/students/999` | `-` | 404 | 404 | PASS | `{"detail": "Student not found"}` |
| ER9 | Negative age | POST | `/students` | `{"name": "Usman", "age": -5, "department": "CS"}` | 422 | 422 | PASS | `{"detail": [{"type": "greater_than", "loc": ["body", "age"], "msg": "Input should be greater than 0", "input": -5, "ctx": {"gt": 0}}]}` |
| ER10 | Non-integer student ID | GET | `/students/abc` | `-` | 422 | 422 | PASS | `{"detail": [{"type": "int_parsing", "loc": ["path", "student_id"], "msg": "Input should be a valid integer, unable to parse string as an integer", "input": "abc"}]}` |
| F1 | GET - final list of students | GET | `/students` | `-` | 200 | 200 | PASS | `{"101": {"name": "Ali Khan", "age": 23, "department": "Cyber Security"}, "102": {"name": "Sara Ahmed", "age": 22, "department": "Data Science"}, "104": {"name": "Hassan", "age": 23, "department": "Artificial Intelligence"}}` |
