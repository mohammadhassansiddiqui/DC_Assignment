# Assignment 1 – Live Demo Guide and Viva Preparation
Muhammad Hassan Siddiqui – CT-23094

## A. Live demonstration (about 5 minutes)

**Before class:** open the `REST_API_Lab` folder in VS Code and run `python -m venv venv`, then `venv\Scripts\activate`, then `pip install -r requirements.txt`.

1. **Start the server**: `uvicorn main:app --reload`. Show the line "Uvicorn running on http://127.0.0.1:8000".
2. **Open Swagger UI** at http://127.0.0.1:8000/docs and point out the 6 student endpoints.
3. **GET /students**: Try it out, then Execute. Three students (101–103) come back, with **200 OK**.
4. **GET /students/{student_id}** with 101 returns Ali, with **200**.
5. **POST /students** with body `{"name": "Hassan", "age": 23, "department": "Artificial Intelligence"}` returns **201 Created** and `student_id: 104`.
6. **PUT /students/101** with `{"name": "Ali Khan", "age": 21, "department": "Data Science"}`. The whole record is replaced.
7. **PATCH /students/101** with `{"department": "Cyber Security"}`. Only the department changes.
8. **DELETE /students/103** returns **204 No Content**. Then GET 103 returns **404**, which proves it was deleted.
9. **Error handling:**
   - GET 999 returns **404** "Student not found".
   - POST with `"age": "twenty"` returns **422**.
   - POST without `name` returns **422**.
   - PATCH with `{}` returns **400**.
10. **Automated test:** in a second terminal run `python test_api.py`. It reports **24/24 tests passed**.
11. **Limitation:** stop the server with CTRL + C and start it again. GET /students shows the original 3 students, because the data was only in memory. This leads into Assignment 2 (the database).

## B. Likely viva questions

| Question | Answer |
|---|---|
| What is a REST API? | An interface where clients use standard HTTP methods on resources identified by URLs (for example `/students/101`). It is stateless, and data is exchanged as JSON. |
| What is the difference between PUT and PATCH? | PUT replaces the **whole** record, so all fields are required. PATCH changes **only the fields sent**. |
| Why does POST return 201 and not 200? | 201 Created means a new resource was created. |
| Why does DELETE return 204? | The deletion succeeded and there is no content to send back. |
| What is the difference between 400 and 422? | 422 is automatic: Pydantic rejects data with a wrong type or a missing or invalid field. 400 is raised by my own code, for example when PATCH has no fields to update. |
| What is 404? | The requested student ID does not exist. |
| What is Pydantic / BaseModel? | A library that defines the expected structure of JSON data and validates it automatically. |
| What does `Field(gt=0, lt=120)` do? | It adds a validation rule: age must be between 1 and 119, otherwise the API returns 422. |
| What does `extra="forbid"` do? | It rejects unknown fields such as `cgpa`, returning 422. |
| What is Uvicorn? | The ASGI server that runs the FastAPI app and listens on port 8000. |
| What is a path parameter? | A value inside the URL, such as `{student_id}` in `/students/101`. |
| What is the main limitation? | Data lives in a Python dictionary in RAM, so it is lost when the server restarts. The fix is a database (Assignment 2). |
| What is Swagger UI? | Interactive documentation that FastAPI generates automatically from the OpenAPI schema at `/docs`, used to test endpoints. |
| How is the new ID generated? | `max(students.keys(), default=100) + 1`. |
| Why `exclude_unset=True` in PATCH? | So that only the fields the client actually sent are updated. |
| Is REST stateless? | Yes. Each request contains everything the server needs, and the server keeps no client session. |
