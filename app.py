from flask import Flask, render_template, jsonify
import json

app = Flask(__name__)

# ─── DATA LAYER (stubs — replace with real connectors later) ──────────────────

def get_amo_data(student_id: str) -> dict:
    """Stub: replace with AMO CRM API call"""
    return {
        "student_name": "Bintang Pratama",
        "parent_name": "Dewi Pratama",
        "age": 12,
        "city": "Surabaya",
        "current_course": "Roblox",
        "class_level": "middle",
        "last_package_check": {
            "date": "2025-03-15",
            "paid_classes": 16
        },
        "total_lessons": 47,
        "class_type": "individual",
        "prolongations": 2,
        "amo_link": "https://amo.example.com/contacts/12345"
    }

def get_lms_data(student_id: str) -> dict:
    """Stub: replace with LMS API call"""
    return {
        "tutor_name": "Sarah Mitchell",
        "attendance_rate": 87,
        "solution_rate": 74
    }

def get_survey_data(student_id: str) -> dict:
    """
    Stub: replace with CSV / Google Sheets read.
    
    Checkbox groups (10 per zone, up to 3 selected):
      comprehension  → Cognitive barrier
      independence   → Executive barrier
      attention      → Behavioural barrier
      stability      → Systemic barrier
      motivation     → Motivational barrier

    Weights: green=+2, yellow=+1, red=-2
    Normalised score per group: sum / max_possible (6 if 3 greens)
    
    Computed metrics:
      Potential    = 0.5 * comprehension_score + 0.5 * independence_score
      Progress     = 0.4 * comprehension_score + 0.3 * stability_score + 0.3 * independence_score
      Engagement   = 0.6 * attention_score + 0.4 * motivation_score
    
    Growth zones: groups where normalised score < 0.6, pick 2 lowest.
    Parent: standalone rating.
    """

    # Raw checkbox selections per zone (indices within each group's 10 items)
    # Green items: 0-3, Yellow: 4-6, Red: 7-9
    selected_checkboxes = {
        "comprehension": [1, 4, 7],   # 1 green, 1 yellow, 1 red → score = (2+1-2)/6 = 0.17
        "independence":  [0, 4, 5],   # 1 green, 2 yellow       → score = (2+1+1)/6 = 0.67
        "attention":     [0, 1, 4],   # 2 green, 1 yellow        → score = (2+2+1)/6 = 0.83
        "stability":     [7, 8, 4],   # 0 green, 1 yellow, 2 red → score = (1-2-2)/6 = -0.50
        "motivation":    [2, 5, 6],   # 1 green, 2 yellow        → score = (2+1+1)/6 = 0.67
    }

    def score(selections):
        total = 0
        for i in selections:
            if i <= 3:   total += 2   # green
            elif i <= 6: total += 1   # yellow
            else:        total -= 2   # red
        return round(total / 6, 3)

    scores = {k: score(v) for k, v in selected_checkboxes.items()}

    # Composite metrics
    potential  = round(0.5 * scores["comprehension"] + 0.5 * scores["independence"], 3)
    progress   = round(0.4 * scores["comprehension"] + 0.3 * scores["stability"] + 0.3 * scores["independence"], 3)
    engagement = round(0.6 * scores["attention"]     + 0.4 * scores["motivation"], 3)

    def level_3(score, labels):
        """Map normalised score to 3-level label"""
        if score >= 0.6:   return labels[0]
        elif score >= 0.0: return labels[1]
        else:              return labels[2]

    potential_label  = level_3(potential,  ["high", "medium", "low"])
    progress_label   = level_3(progress,   ["strong", "stable", "weak"])
    engagement_label = level_3(engagement, ["high", "medium", "low"])

    # Growth zones: zones scoring < 0.6, pick 2 lowest
    barrier_scores = {
        "cognitive":     scores["comprehension"],
        "executive":     scores["independence"],
        "behavioural":   scores["attention"],
        "systemic":      scores["stability"],
        "motivational":  scores["motivation"],
    }
    below_threshold = {k: v for k, v in barrier_scores.items() if v < 0.6}
    growth_zones = sorted(below_threshold, key=lambda k: below_threshold[k])[:2]

    # Checkboxes grouped for raw data display
    checkbox_definitions = {
        "comprehension": {
            "label": "Comprehension",
            "items": [
                {"text": "Grasps new material quickly and applies it immediately", "color": "green"},
                {"text": "Understands after 1 explanation and retains the logic", "color": "green"},
                {"text": "Confidently transfers knowledge to new tasks", "color": "green"},
                {"text": "Asks deep 'why' questions", "color": "green"},
                {"text": "Understands after examples, with a slight delay", "color": "yellow"},
                {"text": "Understands the algorithm but not the reasoning", "color": "yellow"},
                {"text": "Can repeat but not always apply independently", "color": "yellow"},
                {"text": "Gets confused when task phrasing changes", "color": "red"},
                {"text": "Does not connect new topics to previous ones", "color": "red"},
                {"text": "Requires repeated explanations of basics", "color": "red"},
            ]
        },
        "independence": {
            "label": "Independence",
            "items": [
                {"text": "Finds solutions independently without hints", "color": "green"},
                {"text": "Corrects mistakes without external help", "color": "green"},
                {"text": "Builds solution steps on their own", "color": "green"},
                {"text": "Works confidently on novel tasks", "color": "green"},
                {"text": "Sometimes needs guidance at the start", "color": "yellow"},
                {"text": "Acts independently but slowly and cautiously", "color": "yellow"},
                {"text": "May get stuck without step clarification", "color": "yellow"},
                {"text": "Does not start a task without an explicit hint", "color": "red"},
                {"text": "Constantly needs steps checked", "color": "red"},
                {"text": "Avoids solving difficult tasks independently", "color": "red"},
            ]
        },
        "attention": {
            "label": "Attention",
            "items": [
                {"text": "Fully engaged throughout the lesson", "color": "green"},
                {"text": "Initiates discussion and questions themselves", "color": "green"},
                {"text": "Participates actively without prompting", "color": "green"},
                {"text": "Sustains lesson pace", "color": "green"},
                {"text": "Engages when asked by teacher", "color": "yellow"},
                {"text": "Occasionally distracted but returns", "color": "yellow"},
                {"text": "Participates selectively in activities", "color": "yellow"},
                {"text": "Frequently loses attention", "color": "red"},
                {"text": "Avoids active participation", "color": "red"},
                {"text": "Formally present but not engaged", "color": "red"},
            ]
        },
        "stability": {
            "label": "Stability",
            "items": [
                {"text": "Consistently consolidates material after lessons", "color": "green"},
                {"text": "Rarely makes recurring mistakes", "color": "green"},
                {"text": "Confidently retains previous topics", "color": "green"},
                {"text": "Maintains progress between sessions", "color": "green"},
                {"text": "Sometimes needs review for consolidation", "color": "yellow"},
                {"text": "Retention depends on topic complexity", "color": "yellow"},
                {"text": "Makes inconsistent errors", "color": "yellow"},
                {"text": "Quickly forgets covered material", "color": "red"},
                {"text": "Errors repeat from lesson to lesson", "color": "red"},
                {"text": "Progress is unstable without constant review", "color": "red"},
            ]
        },
        "motivation": {
            "label": "Motivation",
            "items": [
                {"text": "Stays interested even during difficult tasks", "color": "green"},
                {"text": "Works calmly through challenges", "color": "green"},
                {"text": "Demonstrates intrinsic motivation", "color": "green"},
                {"text": "Responsibly completes tasks to the end", "color": "green"},
                {"text": "Motivation depends on topic", "color": "yellow"},
                {"text": "Sometimes needs external stimulation", "color": "yellow"},
                {"text": "May lose energy on difficult tasks", "color": "yellow"},
                {"text": "Quickly loses interest when tasks get hard", "color": "red"},
                {"text": "Avoids difficult tasks", "color": "red"},
                {"text": "Gives up at the first failure", "color": "red"},
            ]
        },
    }

    # Build raw data for display
    raw_data = {}
    for zone_key, selections in selected_checkboxes.items():
        zone_def = checkbox_definitions[zone_key]
        checked_items = []
        for i in selections:
            item = zone_def["items"][i].copy()
            item["index"] = i
            checked_items.append(item)
        # Sort: green first, then yellow, then red
        order = {"green": 0, "yellow": 1, "red": 2}
        checked_items.sort(key=lambda x: order[x["color"]])
        raw_data[zone_key] = {
            "label": zone_def["label"],
            "score": scores[zone_key],
            "items": checked_items
        }

    return {
        "potential":       {"level": potential_label,  "score": potential},
        "progress":        {"level": progress_label,   "score": progress},
        "engagement":      {"level": engagement_label, "score": engagement},
        "growth_zones":    growth_zones,
        "parent":          "warm",
        "raw_data":        raw_data,
        "barrier_scores":  barrier_scores,
    }


# ─── INTERPRETATION LAYER ─────────────────────────────────────────────────────

TOOLTIP_COPY = {
    "potential": {
        "high":   "Student rapidly absorbs new material and confidently transfers knowledge to new tasks. Given the right pace, they can move ahead of the curriculum.",
        "medium": "Student steadily masters the curriculum at the current pace, handles tasks well with sufficient practice and explanation.",
        "low":    "Student absorbs material at a slower pace and needs regular support and repetition to consolidate basic concepts.",
    },
    "progress": {
        "strong": "Consistent improvement in understanding and task performance. Student consolidates new skills and reduces error rate.",
        "stable": "Student maintains current level and gradually acquires new material without marked acceleration or slowdown.",
        "weak":   "Learning dynamics are unstable: material is absorbed in fragments, some topics require revisiting.",
    },
    "engagement": {
        "high":   "Student actively participates in lessons, asks questions and joins discussions without external prompting.",
        "medium": "Student engages when prompted by the teacher, may lose focus occasionally but returns to tasks.",
        "low":    "Student is often passive during lessons, rarely initiates participation and needs constant external engagement.",
    },
    "growth_zones": {
        "cognitive":    "Student has difficulties understanding new material and applying knowledge in modified tasks.",
        "executive":    "Student struggles with independently starting and completing tasks without external support.",
        "behavioural":  "Student frequently loses focus during lessons and doesn't always maintain active participation.",
        "systemic":     "Student doesn't consolidate material stably enough, causing some knowledge to fade over time.",
        "motivational": "Student reduces activity when challenges arise and needs external stimulation to continue.",
    },
    "parent": {
        "warm":    "Communication with parents is constructive; there is trust and readiness for continued learning.",
        "neutral": "Communication is stable with no marked difficulties; discussions happen in a standard format.",
        "complex": "Communication requires additional argumentation and negotiation of learning decisions.",
    }
}

def build_card(student_id: str) -> dict:
    """Assemble final card data from all sources"""
    amo   = get_amo_data(student_id)
    lms   = get_lms_data(student_id)
    survey = get_survey_data(student_id)

    return {
        "service": {
            "student_name":   amo["student_name"],
            "parent_name":    amo["parent_name"],
            "age":            amo["age"],
            "city":           amo["city"],
            "current_course": amo["current_course"],
            "tutor_name":     lms["tutor_name"],
            "amo_link":       amo["amo_link"],
        },
        "sales": {
            "class_level":          amo["class_level"],
            "last_package_check":   amo["last_package_check"],
            "total_lessons":        amo["total_lessons"],
            "class_type":           amo["class_type"],
            "prolongations":        amo["prolongations"],
        },
        "academic": {
            "attendance_rate": lms["attendance_rate"],
            "solution_rate":   lms["solution_rate"],
            "potential":       {**survey["potential"],  "tooltip": TOOLTIP_COPY["potential"][survey["potential"]["level"]]},
            "progress":        {**survey["progress"],   "tooltip": TOOLTIP_COPY["progress"][survey["progress"]["level"]]},
            "engagement":      {**survey["engagement"], "tooltip": TOOLTIP_COPY["engagement"][survey["engagement"]["level"]]},
            "growth_zones":    [
                {"key": z, "tooltip": TOOLTIP_COPY["growth_zones"][z]}
                for z in survey["growth_zones"]
            ],
            "parent":          {"level": survey["parent"], "tooltip": TOOLTIP_COPY["parent"][survey["parent"]]},
            "raw_data":        survey["raw_data"],
        }
    }


# ─── ROUTES ───────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    return render_template("card.html")

@app.route("/api/student/<student_id>")
def student_api(student_id):
    return jsonify(build_card(student_id))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
