# database.py — SQLite init, CRUD
import sqlite3
import json
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "data.db")

SEED_STUDENTS = [
    {"name": "Bintang Pratama", "lms_id": "100415349", "amo_id": "69c92748dcb57fafabddbfd0"},
    {"name": "Sari Dewi",       "lms_id": "100222679", "amo_id": "68483311a3f14398e67151d2"},
    {"name": "Rizky Aditya",    "lms_id": "100333626", "amo_id": "69b23a333fc114b8a9d51cdf"},
]

def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_conn()
    c = conn.cursor()
    c.executescript("""
        CREATE TABLE IF NOT EXISTS students (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            lms_id     TEXT UNIQUE,
            amo_id     TEXT UNIQUE,
            lms_url    TEXT,
            amo_url    TEXT,
            name       TEXT,
            created_at TEXT DEFAULT (datetime('now'))
        );

        CREATE TABLE IF NOT EXISTS survey_responses (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id   INTEGER NOT NULL REFERENCES students(id),
            zone         TEXT NOT NULL,
            selections   TEXT NOT NULL DEFAULT '[]',
            completed_at TEXT DEFAULT (datetime('now')),
            UNIQUE(student_id, zone)
        );

        CREATE TABLE IF NOT EXISTS survey_progress (
            student_id   INTEGER PRIMARY KEY REFERENCES students(id),
            last_step    INTEGER DEFAULT -1,
            is_complete  INTEGER DEFAULT 0
        );
    """)
    # Seed students
    for s in SEED_STUDENTS:
        lms_url = f"https://lms.algonova.id/student/default/update/{s['lms_id']}"
        amo_url = f"https://app.kommo.com/leads/detail/{s['amo_id']}"
        c.execute("""
            INSERT OR IGNORE INTO students (lms_id, amo_id, lms_url, amo_url, name)
            VALUES (?, ?, ?, ?, ?)
        """, (s["lms_id"], s["amo_id"], lms_url, amo_url, s["name"]))
        # init progress row
        conn.execute("""
            INSERT OR IGNORE INTO survey_progress (student_id)
            SELECT id FROM students WHERE lms_id = ?
        """, (s["lms_id"],))
    conn.commit()
    conn.close()

def find_student_by_lms_id(lms_id):
    conn = get_conn()
    row = conn.execute("SELECT * FROM students WHERE lms_id = ?", (lms_id,)).fetchone()
    conn.close()
    return dict(row) if row else None

def find_student_by_amo_id(amo_id):
    conn = get_conn()
    row = conn.execute("SELECT * FROM students WHERE amo_id = ?", (amo_id,)).fetchone()
    conn.close()
    return dict(row) if row else None

def get_survey_progress(student_id):
    conn = get_conn()
    row = conn.execute(
        "SELECT last_step, is_complete FROM survey_progress WHERE student_id = ?",
        (student_id,)
    ).fetchone()
    conn.close()
    if row:
        return {"last_step": row["last_step"], "is_complete": bool(row["is_complete"])}
    return {"last_step": -1, "is_complete": False}

def get_survey_responses(student_id):
    conn = get_conn()
    rows = conn.execute(
        "SELECT zone, selections FROM survey_responses WHERE student_id = ?",
        (student_id,)
    ).fetchall()
    conn.close()
    return {r["zone"]: json.loads(r["selections"]) for r in rows}

def save_zone(student_id, zone, selections):
    """Upsert one zone's selections and update progress."""
    from content import ZONE_ORDER
    conn = get_conn()
    conn.execute("""
        INSERT INTO survey_responses (student_id, zone, selections)
        VALUES (?, ?, ?)
        ON CONFLICT(student_id, zone) DO UPDATE SET
            selections = excluded.selections,
            completed_at = datetime('now')
    """, (student_id, zone, json.dumps(selections)))

    # Update progress
    step_index = ZONE_ORDER.index(zone) if zone in ZONE_ORDER else -1
    conn.execute("""
        INSERT INTO survey_progress (student_id, last_step)
        VALUES (?, ?)
        ON CONFLICT(student_id) DO UPDATE SET
            last_step = MAX(last_step, excluded.last_step)
    """, (student_id, step_index))

    # Check completion: all 7 zones saved?
    count = conn.execute(
        "SELECT COUNT(*) as cnt FROM survey_responses WHERE student_id = ?",
        (student_id,)
    ).fetchone()["cnt"]
    if count >= 7:
        conn.execute("""
            UPDATE survey_progress SET is_complete = 1 WHERE student_id = ?
        """, (student_id,))

    conn.commit()
    conn.close()
