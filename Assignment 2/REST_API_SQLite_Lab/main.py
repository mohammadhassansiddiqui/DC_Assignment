"""
Assignment 2 - Connecting a REST API to a Real Database Using SQLite
Student Management API (FastAPI + SQLAlchemy ORM + SQLite)

Student : Muhammad Hassan Siddiqui
Roll No : CT-23094
Dept.   : Computer Science

Run:
    uvicorn main:app --reload
Swagger UI:
    http://127.0.0.1:8000/docs
Database file (created automatically on first run):
    students.db
"""

from fastapi import FastAPI, HTTPException, Depends, Response, status
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import create_engine, Column, Integer, String, func
from sqlalchemy.orm import sessionmaker, declarative_base, Session


# ---------------------------------------------------------------------------
# 1. Database configuration
# ---------------------------------------------------------------------------
DATABASE_URL = "sqlite:///./students.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},  # needed for SQLite + FastAPI threads
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# ---------------------------------------------------------------------------
# 2. Database table (SQLAlchemy model)
# ---------------------------------------------------------------------------
class StudentDB(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    department = Column(String, nullable=False, index=True)


# ---------------------------------------------------------------------------
# 3. Request and response models (Pydantic)
# ---------------------------------------------------------------------------
class StudentCreate(BaseModel):
    """Required data when adding (POST) or replacing (PUT) a student."""

    model_config = ConfigDict(extra="forbid")

    name: str = Field(..., min_length=1, max_length=100, examples=["Ali"])
    age: int = Field(..., gt=0, lt=120, examples=[20])
    department: str = Field(..., min_length=1, max_length=100, examples=["Computer Science"])


class StudentUpdate(BaseModel):
    """Optional fields for a partial update (PATCH)."""

    model_config = ConfigDict(extra="forbid")

    name: str | None = Field(None, min_length=1, max_length=100)
    age: int | None = Field(None, gt=0, lt=120)
    department: str | None = Field(None, min_length=1, max_length=100)


class StudentResponse(BaseModel):
    """Structure of the data returned to the client."""

    id: int
    name: str
    age: int
    department: str

    model_config = ConfigDict(from_attributes=True)


# ---------------------------------------------------------------------------
# 4. Database session dependency
# ---------------------------------------------------------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_student_or_404(student_id: int, db: Session) -> StudentDB:
    student = db.query(StudentDB).filter(StudentDB.id == student_id).first()
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return student


# ---------------------------------------------------------------------------
# 5. FastAPI application
# ---------------------------------------------------------------------------
app = FastAPI(
    title="Student Management API",
    description="REST API with SQLite Database (Assignment 2 - Muhammad Hassan Siddiqui, CT-23094)",
    version="2.0",
)

# Create the database table automatically (only if it does not exist yet)
Base.metadata.create_all(bind=engine)


@app.get("/", tags=["Info"])
def home():
    return {"message": "Student Management API (SQLite) is running", "docs": "/docs"}


# 6. GET: Retrieve all students            ->  SELECT * FROM students;
@app.get("/students", response_model=list[StudentResponse], tags=["Students"])
def get_students(db: Session = Depends(get_db)):
    return db.query(StudentDB).all()


# Task 7. GET: Retrieve students of one department
#   ->  SELECT * FROM students WHERE lower(department) = lower(:department);
@app.get(
    "/students/department/{department}",
    response_model=list[StudentResponse],
    tags=["Students"],
)
def get_students_by_department(department: str, db: Session = Depends(get_db)):
    students = (
        db.query(StudentDB)
        .filter(func.lower(StudentDB.department) == department.strip().lower())
        .all()
    )
    if not students:
        raise HTTPException(
            status_code=404,
            detail=f"No students found in department '{department}'",
        )
    return students


# 7. GET: Retrieve one student             ->  SELECT * FROM students WHERE id = :id;
@app.get("/students/{student_id}", response_model=StudentResponse, tags=["Students"])
def get_student(student_id: int, db: Session = Depends(get_db)):
    return get_student_or_404(student_id, db)


# 8. POST: Add new student                 ->  INSERT INTO students (...) VALUES (...);
@app.post(
    "/students",
    response_model=StudentResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Students"],
)
def add_student(student: StudentCreate, db: Session = Depends(get_db)):
    new_student = StudentDB(
        name=student.name,
        age=student.age,
        department=student.department,
    )
    db.add(new_student)
    db.commit()
    db.refresh(new_student)  # load the auto-generated id
    return new_student


# 9. PUT: Replace student information      ->  UPDATE students SET name=.., age=.., department=.. WHERE id = :id;
@app.put("/students/{student_id}", response_model=StudentResponse, tags=["Students"])
def update_student(student_id: int, student: StudentCreate, db: Session = Depends(get_db)):
    existing_student = get_student_or_404(student_id, db)

    existing_student.name = student.name
    existing_student.age = student.age
    existing_student.department = student.department

    db.commit()
    db.refresh(existing_student)
    return existing_student


# 10. PATCH: Partially update student      ->  UPDATE students SET <only sent fields> WHERE id = :id;
@app.patch("/students/{student_id}", response_model=StudentResponse, tags=["Students"])
def patch_student(student_id: int, data: StudentUpdate, db: Session = Depends(get_db)):
    student = get_student_or_404(student_id, db)

    update_data = data.model_dump(exclude_unset=True, exclude_none=True)
    if not update_data:
        raise HTTPException(status_code=400, detail="No update fields provided")

    for key, value in update_data.items():
        setattr(student, key, value)

    db.commit()
    db.refresh(student)
    return student


# 11. DELETE: Remove student               ->  DELETE FROM students WHERE id = :id;
@app.delete(
    "/students/{student_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Students"],
)
def delete_student(student_id: int, db: Session = Depends(get_db)):
    student = get_student_or_404(student_id, db)
    db.delete(student)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
