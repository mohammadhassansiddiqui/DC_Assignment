"""
Task 5 - Database verification without the API.

Opens students.db directly with Python's built-in sqlite3 module (the same
check that DB Browser for SQLite does graphically) and prints the table
structure and all stored rows.

Run:  python verify_db.py
"""

import sqlite3

conn = sqlite3.connect("students.db")
cur = conn.cursor()

print("Table definition (sqlite_master):")
for (sql,) in cur.execute("SELECT sql FROM sqlite_master WHERE type IN ('table','index') AND sql IS NOT NULL"):
    print("  " + sql.replace("\n", "\n  "))

print("\nSELECT * FROM students;")
rows = cur.execute("SELECT id, name, age, department FROM students ORDER BY id").fetchall()
print(f"  {'id':<4}| {'name':<12}| {'age':<4}| department")
print("  " + "-" * 45)
for r in rows:
    print(f"  {r[0]:<4}| {r[1]:<12}| {r[2]:<4}| {r[3]}")
print(f"\n{len(rows)} row(s) stored in students.db")

conn.close()
