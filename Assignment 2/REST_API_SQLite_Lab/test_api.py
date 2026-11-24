"""
Automated test script for the Student Management API with SQLite (Assignment 2).

Start from an EMPTY database (delete students.db if it exists), then:
    Terminal 1:  uvicorn main:app --reload
    Terminal 2:  python test_api.py

Runs the lab experiments (A-D), exercise Tasks 1-4 and 7, and invalid-request
tests. Results are written to test_results.md and the final database state to
state_before_restart.json (used by persistence_check.py for Task 6).
"""

import json
import sys

import requests

BASE_URL = "http://127.0.0.1:8000"

NEW_STUDENTS = [  # Task 1 - five new students
    {"name": "Hassan", "age": 23, "department": "Artificial Intelligence"},
    {"name": "Fatima", "age": 20, "department": "Computer Science"},
    {"name": "Usman", "age": 22, "department": "Cyber Security"},
    {"name": "Ayesha", "age": 21, "department": "Data Science"},
    {"name": "Bilal", "age": 24, "department": "Computer Science"},
]

# (test id, description, method, path, json body, expected status)
TESTS = [
    # ---- Lab experiments A-D (fresh, empty database) ----------------------
    ("A", "POST - insert first student Ali", "POST", "/students",
     {"name": "Ali", "age": 20, "department": "Computer Science"}, 201),
    ("B1", "POST - insert Sara", "POST", "/students",
     {"name": "Sara", "age": 21, "department": "Information Technology"}, 201),
    ("B2", "POST - insert Ahmed", "POST", "/students",
     {"name": "Ahmed", "age": 22, "department": "Software Engineering"}, 201),
    ("C", "GET - retrieve all students", "GET", "/students", None, 200),
    ("D", "PATCH - change department of student 1", "PATCH", "/students/1",
     {"department": "Artificial Intelligence"}, 200),
    # ---- Task 1: insert five students ----------------------------------
    *[(f"T1.{i + 1}", f"POST - insert {s['name']}", "POST", "/students", s, 201)
      for i, s in enumerate(NEW_STUDENTS)],
    # ---- Task 2: retrieve ------------------------------------------------
    ("T2a", "GET - retrieve all students", "GET", "/students", None, 200),
    ("T2b", "GET - retrieve student by ID 5", "GET", "/students/5", None, 200),
    # ---- Task 3: update --------------------------------------------------
    ("T3", "PATCH - update department of student 2", "PATCH", "/students/2",
     {"department": "Cyber Security"}, 200),
    ("T3b", "PUT - replace complete record of student 4", "PUT", "/students/4",
     {"name": "Hassan Raza", "age": 24, "department": "Data Science"}, 200),
    # ---- Task 4: delete --------------------------------------------------
    ("T4", "DELETE - remove student 3", "DELETE", "/students/3", None, 204),
    ("T4b", "GET - verify student 3 no longer exists", "GET", "/students/3", None, 404),
    # ---- Task 7: department endpoint ------------------------------------
    ("T7a", "GET - students in Computer Science", "GET",
     "/students/department/Computer Science", None, 200),
    ("T7b", "GET - department search is case-insensitive", "GET",
     "/students/department/data science", None, 200),
    ("T7c", "GET - department with no students", "GET",
     "/students/department/Physics", None, 404),
    # ---- Invalid requests / error handling -------------------------------
    ("ER1", "GET non-existent student 999", "GET", "/students/999", None, 404),
    ("ER2", "POST age sent as text", "POST", "/students",
     {"name": "Zain", "age": "twenty", "department": "CS"}, 422),
    ("ER3", "POST without name field", "POST", "/students",
     {"age": 20, "department": "CS"}, 422),
    ("ER4", "PUT non-existent student 999", "PUT", "/students/999",
     {"name": "Ghost", "age": 20, "department": "CS"}, 404),
    ("ER5", "PATCH non-existent student 999", "PATCH", "/students/999", {"age": 25}, 404),
    ("ER6", "PATCH with empty body {}", "PATCH", "/students/1", {}, 400),
    ("ER7", "PATCH with unknown field", "PATCH", "/students/1", {"cgpa": 3.5}, 422),
    ("ER8", "DELETE non-existent student 999", "DELETE", "/students/999", None, 404),
    ("ER9", "POST negative age", "POST", "/students",
     {"name": "Omar", "age": -5, "department": "CS"}, 422),
    ("ER10", "GET non-integer student ID", "GET", "/students/abc", None, 422),
    # ---- Final state ---------------------------------------------------
    ("F1", "GET - final list of students", "GET", "/students", None, 200),
]


def short(text, limit=300):
    text = text.replace("\n", " ")
    return text if len(text) <= limit else text[:limit] + " ..."


def main():
    try:
        existing = requests.get(BASE_URL + "/students", timeout=3).json()
    except requests.ConnectionError:
        sys.exit("Server is not running. Start it with:  uvicorn main:app --reload")
    if existing:
        sys.exit("Database is not empty. Stop the server, delete students.db, restart and run again.")

    rows, passed = [], 0
    last_response = None
    for tid, desc, method, path, body, expected in TESTS:
        r = requests.request(method, BASE_URL + path, json=body, timeout=5)
        ok = r.status_code == expected
        passed += ok
        resp = r.text if r.text else "(empty body)"
        try:
            last_response = r.json()
            resp = json.dumps(last_response, separators=(", ", ": "))
        except ValueError:
            pass
        rows.append((tid, desc, method, path, body, expected, r.status_code, ok, resp))
        print(f"[{'PASS' if ok else 'FAIL'}] {tid:<5} {method:<6} {path:<38} "
              f"expected {expected} got {r.status_code}  - {desc}")

    print(f"\n{passed}/{len(TESTS)} tests passed")

    with open("state_before_restart.json", "w", encoding="utf-8") as f:
        json.dump(last_response, f, indent=2)

    with open("test_results.md", "w", encoding="utf-8") as f:
        f.write("# Test Results - Student Management API with SQLite (Assignment 2)\n\n")
        f.write(f"**{passed}/{len(TESTS)} tests passed**\n\n")
        f.write("| ID | Test | Method | Endpoint | Request body | Expected | Actual | Result | Response |\n")
        f.write("|---|---|---|---|---|---|---|---|---|\n")
        for tid, desc, method, path, body, exp, got, ok, resp in rows:
            b = json.dumps(body) if body is not None else "-"
            f.write(f"| {tid} | {desc} | {method} | `{path}` | `{b}` | {exp} | {got} | "
                    f"{'PASS' if ok else 'FAIL'} | `{short(resp)}` |\n")

    with open("test_results.json", "w", encoding="utf-8") as f:
        json.dump([dict(id=r[0], test=r[1], method=r[2], endpoint=r[3], body=r[4],
                        expected=r[5], actual=r[6], passed=r[7], response=r[8]) for r in rows],
                  f, indent=2)

    sys.exit(0 if passed == len(TESTS) else 1)


if __name__ == "__main__":
    main()
