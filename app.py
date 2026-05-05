# app.py — Flask routes
import re
import json
from flask import Flask, render_template, request, jsonify
from database import init_db, find_student_by_lms_id, find_student_by_amo_id, \
    get_survey_progress, get_survey_responses, save_zone
from content import ZONE_ORDER, ZONE_META, CHECKBOXES, MOTIVATORS, PARENT_OPTIONS, compute_academics

app = Flask(__name__)

# ── AMO stub data (keyed by lms_id) ─────────────────────────────────────────

AMO_DATA = {
    "100415349": {
        "student_name": "Bintang Pratama",
        "age": 12,
        "current_course": "Roblox — Level 2",
        "class_level": "high",
        "tutor_name": "Anya Kuznetsova",
        "last_package_check": {"date": "2025-03-15", "paid_classes": 16, "amount": 320},
        "total_lessons": 48,
        "class_type": "individual",
        "prolongations": 3,
        "amo_link": "https://app.kommo.com/leads/detail/69c92748dcb57fafabddbfd0",
        "attendance_rate": 92,
        "solution_rate": 78,
        "class_details": {
            "device_type": "iPad + keyboard",
            "additional_lessons": "Extra session on Fridays",
            "parents_profession": "Engineer / Teacher",
            "school": "International school",
            "home_background": "Quiet workspace, supportive",
            "parents_communication": "Active via WhatsApp",
        },
    },
    "100222679": {
        "student_name": "Sari Dewi",
        "age": 10,
        "current_course": "Scratch — Level 1",
        "class_level": "middle",
        "tutor_name": "Pavel Orlov",
        "last_package_check": {"date": "2025-02-10", "paid_classes": 8, "amount": 160},
        "total_lessons": 24,
        "class_type": "group",
        "prolongations": 1,
        "amo_link": "https://app.kommo.com/leads/detail/68483311a3f14398e67151d2",
        "attendance_rate": 67,
        "solution_rate": 55,
        "class_details": {
            "device_type": "Laptop (Windows)",
            "additional_lessons": "None",
            "parents_profession": "Business owner",
            "school": "State school",
            "home_background": "Shared room, some distractions",
            "parents_communication": "Responds slowly",
        },
    },
    "100333626": {
        "student_name": "Rizky Aditya",
        "age": 14,
        "current_course": "Python — Level 3",
        "class_level": "low",
        "tutor_name": "Maria Sokolova",
        "last_package_check": {"date": "2025-04-01", "paid_classes": 12, "amount": 200},
        "total_lessons": 36,
        "class_type": "individual",
        "prolongations": 2,
        "amo_link": "https://app.kommo.com/leads/detail/69b23a333fc114b8a9d51cdf",
        "attendance_rate": 44,
        "solution_rate": 38,
        "class_details": {
            "device_type": "Desktop PC",
            "additional_lessons": "Occasional weekends",
            "parents_profession": "Doctor / Homemaker",
            "school": "Private school",
            "home_background": "Good setup, motivated parents",
            "parents_communication": "Very active, calls regularly",
        },
    },
}

# ── Helper ───────────────────────────────────────────────────────────────────

def extract_lms_id(url):
    m = re.search(r"/student/default/update/(\d+)", url)
    return m.group(1) if m else None

# ── Page routes ──────────────────────────────────────────────────────────────

@app.route("/")
def card_page():
    return render_template("card.html")

@app.route("/survey")
def survey_page():
    return render_template("survey.html")

# ── Survey API ───────────────────────────────────────────────────────────────

@app.route("/api/survey/lookup")
def survey_lookup():
    url = request.args.get("url", "").strip()
    lms_id = extract_lms_id(url)
    if not lms_id:
        return jsonify({"error": "Could not extract LMS ID from URL"}), 400
    student = find_student_by_lms_id(lms_id)
    if not student:
        return jsonify({"error": "Student not found"}), 404
    prog = get_survey_progress(student["id"])
    return jsonify({
        "student_id":   student["id"],
        "lms_id":       student["lms_id"],
        "name":         student["name"],
        "last_step":    prog["last_step"],
        "is_complete":  prog["is_complete"],
    })

@app.route("/api/survey/<int:sid>/responses")
def survey_responses(sid):
    data = get_survey_responses(sid)
    return jsonify(data)

@app.route("/api/survey/<int:sid>/save", methods=["POST"])
def survey_save(sid):
    body = request.get_json(force=True) or {}
    zone = body.get("zone")
    selections = body.get("selections", [])
    if zone not in ZONE_ORDER:
        return jsonify({"error": "Invalid zone"}), 400
    save_zone(sid, zone, selections)
    prog = get_survey_progress(sid)
    return jsonify({"ok": True, "is_complete": prog["is_complete"]})

# ── Card API ─────────────────────────────────────────────────────────────────

@app.route("/api/card/lookup")
def card_lookup():
    amo_id = request.args.get("amo_id", "").strip()
    if not amo_id:
        return jsonify({"error": "amo_id required"}), 400
    student = find_student_by_amo_id(amo_id)
    if not student:
        return jsonify({"error": "Student not found"}), 404
    return jsonify({"student_id": student["id"], "lms_id": student["lms_id"]})

@app.route("/api/card/<int:sid>")
def card_data(sid):
    # Find student row by id
    from database import get_conn
    conn = get_conn()
    row = conn.execute("SELECT * FROM students WHERE id = ?", (sid,)).fetchone()
    conn.close()
    if not row:
        return jsonify({"error": "Student not found"}), 404

    student = dict(row)
    lms_id  = student["lms_id"]
    amo     = AMO_DATA.get(lms_id, {})
    prog    = get_survey_progress(sid)

    service = {
        "student_name": amo.get("student_name", student["name"]),
        "age":          amo.get("age"),
        "current_course": amo.get("current_course"),
        "tutor_name":   amo.get("tutor_name"),
        "amo_link":     amo.get("amo_link", student.get("amo_url", "")),
    }

    pkg = amo.get("last_package_check", {})
    sales = {
        "class_level":        amo.get("class_level"),
        "last_package_check": pkg,
        "total_lessons":      amo.get("total_lessons"),
        "class_type":         amo.get("class_type"),
        "prolongations":      amo.get("prolongations"),
        "class_details":      amo.get("class_details", {}),
    }

    academic = None
    if prog["is_complete"]:
        responses = get_survey_responses(sid)
        academic = compute_academics(
            responses,
            amo.get("attendance_rate", 0),
            amo.get("solution_rate", 0),
            service["student_name"],
        )

    return jsonify({
        "service":        service,
        "sales":          sales,
        "academic":       academic,
        "survey_complete": prog["is_complete"],
        "survey_last_step": prog["last_step"],
    })

# ── Content API (for survey UI) ──────────────────────────────────────────────

@app.route("/api/content/zones")
def content_zones():
    """Return all zone definitions for the survey UI."""
    zones = []
    for key in ZONE_ORDER:
        meta = ZONE_META[key]
        entry = {"key": key, **meta}
        if meta["weighted"]:
            entry["checkboxes"] = [
                {"weight": w, "text": t, "index": i}
                for i, (w, t) in enumerate(CHECKBOXES[key])
            ]
        elif key == "motivators":
            entry["options"] = MOTIVATORS
        elif key == "parent":
            entry["options"] = PARENT_OPTIONS
        zones.append(entry)
    return jsonify(zones)

# ── Boot ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))