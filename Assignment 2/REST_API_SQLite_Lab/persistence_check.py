"""
Task 6 - Persistence test.

1. Run test_api.py (it saves the final records to state_before_restart.json).
2. Stop the server with CTRL + C.
3. Start it again:  uvicorn main:app --reload
4. Run:            python persistence_check.py

The script fetches GET /students after the restart and compares it with the
records saved before the restart.
"""

import json
import sys

import requests

with open("state_before_restart.json", encoding="utf-8") as f:
    before = json.load(f)

try:
    after = requests.get("http://127.0.0.1:8000/students", timeout=3).json()
except requests.ConnectionError:
    sys.exit("Server is not running. Start it with:  uvicorn main:app --reload")

print(f"Records before restart : {len(before)}")
print(f"Records after restart  : {len(after)}")
for s in after:
    print(f"  id={s['id']:<3} {s['name']:<12} age={s['age']:<3} {s['department']}")

if before == after:
    print("\nPASS - all records survived the server restart (data is stored permanently in students.db)")
    sys.exit(0)
print("\nFAIL - records differ after restart")
sys.exit(1)
