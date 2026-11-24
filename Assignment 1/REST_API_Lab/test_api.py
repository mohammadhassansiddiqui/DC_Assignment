"""
Automated test script for the Student Management API (Assignment 1).

Start the server first:   uvicorn main:app --reload
Then run in a 2nd terminal: python test_api.py

Every lab experiment and every exercise from the assignment handout is sent to
the running API, the HTTP status code is compared with the expected one, and the
results are saved to test_results.md.
"""

import json
import sys

import requests

BASE_URL = "http://127.0.0.1:8000"

# (test id, description, method, path, json body, expected status)
TESTS = [
    # ---- Lab experiments -------------------------------------------------
    ("E1", "GET - retrieve all students", "GET", "/students", None, 200),
    ("E2", "GET - retrieve student 101", "GET", "/students/101", None, 200),
    ("E3", "POST - add new student Zara", "POST", "/students",
     {"name": "Zara", "age": 20, "department": "Artificial Intelligence"}, 201),
    ("E4", "PUT - replace student 101", "PUT", "/students/101",
     {"name": "Ali Khan", "age": 21, "department": "Data Science"}, 200),
    ("E5", "PATCH - update only age of 101", "PATCH", "/students/101", {"age": 23}, 200),
    ("E6", "DELETE - remove student 104 (Zara)", "DELETE", "/students/104", None, 204),
    # ---- Exercises -------------------------------------------------------
    ("X1", "Add new student Hassan", "POST", "/students",
     {"name": "Hassan", "age": 23, "department": "Artificial Intelligence"}, 201),
    ("X1b", "Verify Hassan was added", "GET", "/students/104", None, 200),
    ("X2", "Search for student 102", "GET", "/students/102", None, 200),
    ("X3", "PATCH department of 101 to Cyber Security", "PATCH", "/students/101",
     {"department": "Cyber Security"}, 200),
    ("X4", "PUT - replace complete record of 102", "PUT", "/students/102",
     {"name": "Sara Ahmed", "age": 22, "department": "Data Science"}, 200),
    ("X5", "DELETE student 103", "DELETE", "/students/103", None, 204),
    ("X5b", "Verify 103 no longer exists", "GET", "/students/103", None, 404),
    # ---- Invalid requests / error handling -------------------------------
    ("ER1", "Search for student 999", "GET", "/students/999", None, 404),
    ("ER2", "Age sent as text", "POST", "/students",
     {"name": "Bilal", "age": "twenty", "department": "CS"}, 422),
    ("ER3", "POST without name field", "POST", "/students",
     {"age": 20, "department": "CS"}, 422),
    ("ER4", "PUT on non-existent student 999", "PUT", "/students/999",
     {"name": "Ghost", "age": 20, "department": "CS"}, 404),
    ("ER5", "PATCH on non-existent student 999", "PATCH", "/students/999", {"age": 25}, 404),
    ("ER6", "PATCH with empty body {}", "PATCH", "/students/101", {}, 400),
    ("ER7", "PATCH with unknown field", "PATCH", "/students/101", {"cgpa": 3.5}, 422),
    ("ER8", "DELETE non-existent student 999", "DELETE", "/students/999", None, 404),
    ("ER9", "Negative age", "POST", "/students",
     {"name": "Usman", "age": -5, "department": "CS"}, 422),
    ("ER10", "Non-integer student ID", "GET", "/students/abc", None, 422),
    # ---- Final state ---------------------------------------------------
    ("F1", "GET - final list of students", "GET", "/students", None, 200),
]


def short(text, limit=300):
    text = text.replace("\n", " ")
    return text if len(text) <= limit else text[:limit] + " ..."


def main():
    try:
        requests.get(BASE_URL + "/", timeout=3)
    except requests.ConnectionError:
        sys.exit("Server is not running. Start it with:  uvicorn main:app --reload")

    rows, passed = [], 0
    for tid, desc, method, path, body, expected in TESTS:
        r = requests.request(method, BASE_URL + path, json=body, timeout=5)
        ok = r.status_code == expected
        passed += ok
        resp = r.text if r.text else "(empty body)"
        try:
            resp = json.dumps(r.json(), separators=(", ", ": "))
        except ValueError:
            pass
        rows.append((tid, desc, method, path, body, expected, r.status_code, ok, resp))
        print(f"[{'PASS' if ok else 'FAIL'}] {tid:<5} {method:<6} {path:<16} "
              f"expected {expected} got {r.status_code}  - {desc}")

    print(f"\n{passed}/{len(TESTS)} tests passed")

    with open("test_results.md", "w", encoding="utf-8") as f:
        f.write("# Test Results - Student Management API (Assignment 1)\n\n")
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
