"""
Assignment 1 - Developing and Testing a REST API Using Python FastAPI
Student Management API (in-memory Python dictionary storage)

Student : Muhammad Hassan Siddiqui
Roll No : CT-23094
Dept.   : Computer Science

Run:
    uvicorn main:app --reload
Swagger UI:
    http://127.0.0.1:8000/docs
"""

from fastapi import FastAPI, HTTPException, status, Response
from pydantic import BaseModel, Field, ConfigDict

app = FastAPI(
    title="Student Management API",
    description="A REST API for managing student records (Assignment 1 - Muhammad Hassan Siddiqui, CT-23094)",
    version="1.0",
)


# ---------------------------------------------------------------------------
# Data models (Pydantic validates every incoming JSON body against these)
# ---------------------------------------------------------------------------
class Student(BaseModel):
    """Full student record - used by POST (create) and PUT (replace)."""

    model_config = ConfigDict(extra="forbid")  # reject unknown fields

    name: str = Field(..., min_length=1, max_length=100, examples=["Ali"])
    age: int = Field(..., gt=0, lt=120, examples=[20])
    department: str = Field(..., min_length=1, max_length=100, examples=["Computer Science"])


class StudentUpdate(BaseModel):
    """Partial student record - used by PATCH. Every field is optional."""

    model_config = ConfigDict(extra="forbid")

    name: str | None = Field(None, min_length=1, max_length=100)
    age: int | None = Field(None, gt=0, lt=120)
    department: str | None = Field(None, min_length=1, max_length=100)


# ---------------------------------------------------------------------------
# Temporary data storage (in memory - reset when the server restarts)
# ---------------------------------------------------------------------------
students = {
    101: {"name": "Ali", "age": 20, "department": "Computer Science"},
    102: {"name": "Sara", "age": 21, "department": "Information Technology"},
    103: {"name": "Ahmed", "age": 22, "department": "Software Engineering"},
}


def find_student_or_404(student_id: int) -> dict:
    """Return the student record or raise HTTP 404 if the ID does not exist."""
    if student_id not in students:
        raise HTTPException(status_code=404, detail="Student not found")
    return students[student_id]


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------
@app.get("/", tags=["Info"])
def home():
    """Simple health check / welcome message."""
    return {"message": "Student Management API is running", "docs": "/docs"}


# GET: Retrieve all students
@app.get("/students", tags=["Students"])
def get_students():
    return students


# GET: Retrieve a specific student
@app.get("/students/{student_id}", tags=["Students"])
def get_student(student_id: int):
    return find_student_or_404(student_id)


# POST: Add a new student
@app.post("/students", status_code=status.HTTP_201_CREATED, tags=["Students"])
def add_student(student: Student):
    new_id = max(students.keys(), default=100) + 1
    students[new_id] = student.model_dump()
    return {
        "message": "Student added successfully",
        "student_id": new_id,
        "student": students[new_id],
    }


# PUT: Replace the complete student record
@app.put("/students/{student_id}", tags=["Students"])
def update_student(student_id: int, student: Student):
    find_student_or_404(student_id)
    students[student_id] = student.model_dump()
    return {
        "message": "Student updated successfully",
        "student": students[student_id],
    }


# PATCH: Update only the selected fields
@app.patch("/students/{student_id}", tags=["Students"])
def patch_student(student_id: int, data: StudentUpdate):
    record = find_student_or_404(student_id)

    # only the fields the client actually sent (null values are ignored)
    update_data = data.model_dump(exclude_unset=True, exclude_none=True)
    if not update_data:
        raise HTTPException(status_code=400, detail="Invalid or empty update fields")

    record.update(update_data)
    return {
        "message": "Student partially updated",
        "student": record,
    }


# DELETE: Remove a student
@app.delete("/students/{student_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Students"])
def delete_student(student_id: int):
    find_student_or_404(student_id)
    del students[student_id]
    return Response(status_code=status.HTTP_204_NO_CONTENT)
