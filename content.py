# content.py — Checkbox definitions, scoring formulas, ISM copy

# Zone metadata
ZONE_ORDER = ["comprehension", "independence", "attention", "stability", "motivation", "motivators", "parent"]

ZONE_META = {
    "comprehension": {
        "label": "Comprehension",
        "icon": "🧠",
        "subtitle": "Understanding of material",
        "max_selections": 3,
        "weighted": True,
    },
    "independence": {
        "label": "Independence",
        "icon": "🚀",
        "subtitle": "Independent work skills",
        "max_selections": 3,
        "weighted": True,
    },
    "attention": {
        "label": "Attention",
        "icon": "👁️",
        "subtitle": "Focus and engagement in lesson",
        "max_selections": 3,
        "weighted": True,
    },
    "stability": {
        "label": "Stability",
        "icon": "📈",
        "subtitle": "Knowledge retention between lessons",
        "max_selections": 3,
        "weighted": True,
    },
    "motivation": {
        "label": "Motivation",
        "icon": "⚡",
        "subtitle": "Drive and attitude to learning",
        "max_selections": 3,
        "weighted": True,
    },
    "motivators": {
        "label": "Motivators",
        "icon": "🎯",
        "subtitle": "What drives the student",
        "max_selections": 2,
        "weighted": False,
    },
    "parent": {
        "label": "Parent Communication",
        "icon": "👨‍👩‍👦",
        "subtitle": "Parent engagement level",
        "max_selections": 1,
        "weighted": False,
    },
}

# Weighted zone checkboxes: (weight, text)
# green=+2, yellow=+1, red=-2
CHECKBOXES = {
    "comprehension": [
        (2,  "Grasps new material quickly and applies it right away"),
        (2,  "Confidently transfers knowledge to unfamiliar tasks"),
        (2,  "Understands the logic of a topic — the 'why', not just the 'how'"),
        (1,  "Understands after examples, but with a slight delay"),
        (1,  "Follows the algorithm but struggles with reasoning"),
        (1,  "Can repeat but doesn't always apply independently"),
        (-2, "Gets confused when task phrasing changes"),
        (-2, "Doesn't connect new topics to previous ones"),
        (-2, "Needs repeated explanations of basic material"),
    ],
    "independence": [
        (2,  "Builds and executes a solution independently without hints"),
        (2,  "Self-corrects mistakes and adjusts approach without help"),
        (2,  "Takes on unfamiliar tasks and searches for a solution unprompted"),
        (1,  "Sometimes needs direction at the start of a task"),
        (1,  "Works independently but slowly and cautiously"),
        (1,  "Can get stuck without clarification of the next step"),
        (-2, "Won't start a task without an explicit hint"),
        (-2, "Constantly needs each step checked"),
        (-2, "Avoids independent decisions, waits for a ready answer"),
    ],
    "attention": [
        (2,  "Fully engaged throughout the entire lesson without losing focus"),
        (2,  "Actively responds to tasks and questions even without prompting"),
        (2,  "Switches between activities easily without losing the thread"),
        (1,  "Engages when directly addressed by the teacher"),
        (1,  "Gets distracted occasionally but returns quickly"),
        (1,  "Participates selectively — engaged in some activities, not others"),
        (-2, "Often loses the thread of the lesson, needs reminders"),
        (-2, "Responds when addressed but quickly drifts off again"),
        (-2, "Formally present but not engaged in the process"),
    ],
    "stability": [
        (2,  "Reproduces covered material confidently without prior review"),
        (2,  "Rarely makes the same mistake twice"),
        (2,  "Progress is stable between lessons — no rollbacks"),
        (1,  "Sometimes needs a short review to restore material"),
        (1,  "Handles basic topics well, complex ones are unstable"),
        (1,  "Knowledge is inconsistent — sometimes recalls, sometimes not"),
        (-2, "Quickly forgets covered material without review"),
        (-2, "The same mistakes repeat from lesson to lesson"),
        (-2, "Progress rolls back without constant reinforcement"),
    ],
    "motivation": [
        (2,  "Maintains interest and energy even on difficult tasks"),
        (2,  "Completes assignments responsibly without reminders"),
        (2,  "Shows curiosity — asks 'why' and explores the topic"),
        (1,  "Motivation depends on topic or task type"),
        (1,  "Sometimes needs encouragement or praise to maintain pace"),
        (1,  "Energy noticeably drops on lengthy or difficult tasks"),
        (-2, "Loses interest and abandons a task at the first difficulty"),
        (-2, "Avoids difficult tasks, looks for shortcuts or waits"),
        (-2, "Won't engage without constant external stimulation"),
    ],
}

MOTIVATORS = [
    {"title": "Creation",     "text": "Loves creating something visible and tangible (game, animation, picture, program)"},
    {"title": "Logic",        "text": "Enjoys solving problems and puzzles, understanding how things work"},
    {"title": "Exploration",  "text": "Loves experimenting, breaking things apart and reassembling, trying options"},
    {"title": "Achievement",  "text": "Motivated by completion, results, the feeling of 'I did it'"},
    {"title": "Recognition",  "text": "Needs to show their work and get a reaction — from teacher, parents, peers"},
    {"title": "Autonomy",     "text": "Gets excited when there's freedom to choose what and how to do things"},
]

PARENT_OPTIONS = [
    {"text": "Hard to reach — doesn't respond to messages",                           "color": "red"},
    {"text": "Responds but never initiates and shows no interest in progress",         "color": "yellow"},
    {"text": "Occasionally asks about progress, generally reachable",                  "color": "yellow"},
    {"text": "Active — writes first, follows progress, has booked extra lessons",      "color": "green"},
]

# ISM talking points
# Translated from the CSV (Russian → English), [name] is a placeholder
ISM_COPY = {
    "potential": {
        "low": {
            "warmup":    "The tutor can clearly see growth areas — that's not an argument against continuing, it's an argument for it: the earlier you start working on them, the smaller the gap.",
            "urgency":   "Without structured work the gap with the curriculum will only grow — right now is the cheapest moment to close it.",
            "objection": "Your concerns are understandable, but having identified growth areas actually makes continuing more important, not less.",
        },
        "medium": {
            "warmup":    "The tutor sees a solid foundation — [name] understands the material but still needs some direction. This is a great moment to show the parent that progress is already happening.",
            "urgency":   "[name] is at the stage where consistency is everything — the potential is there, but without continuing it won't be realised.",
            "objection": "This is exactly the critical growth moment — a pause at this stage is the hardest to recover from.",
        },
        "high": {
            "warmup":    "The tutor sees strong potential in [name] — a great entry point to help the parent feel proud and open to the conversation.",
            "urgency":   "[name]'s potential is real, but it only unfolds with regularity — a pause now means losing momentum that's very hard to rebuild.",
            "objection": "The tutor's observation isn't a compliment — it's a specific signal. Students like this grow fast, but only if they keep going.",
        },
    },
    "progress": {
        "low": {
            "warmup":    "The tutor notes that material isn't consolidating stably yet — that's a sign [name] needs more practice, not less.",
            "urgency":   "Without continuing, the gap between what [name] knows and what the curriculum requires will only widen — closing it now is the easiest it will ever be.",
            "objection": "Precisely because progress is unstable — continuing now matters more than when everything is going well. This is the moment when support decides things.",
        },
        "medium": {
            "warmup":    "The tutor sees forward movement, but uneven — material is being absorbed, though consolidation takes time. The parent should know progress is happening, it just needs support.",
            "urgency":   "[name] is progressing but inconsistently — without regularity what's already been learned will be lost faster than it accumulates.",
            "objection": "Progress is there, but it's fragile at this stage — a pause now will very likely roll back what has already been achieved.",
        },
        "high": {
            "warmup":    "The tutor sees stable progress in [name] — material is consolidating and isn't lost between lessons. It's important for the parent to hear that their investment is working.",
            "urgency":   "[name] has built up good momentum — progress is visible and measurable. Stopping now means losing what's been built, and recovering it will take time.",
            "objection": "[name]'s progress is not a feeling — it's the tutor's observation. Right now, while there's momentum, continuing delivers maximum return.",
        },
    },
    "engagement": {
        "low": {
            "warmup":    "The tutor sees that engagement is currently low — but this often changes with the right approach and consistency.",
            "urgency":   "Without continuing, low engagement becomes a pattern — and changing that later is significantly harder.",
            "objection": "A lack of visible interest now is not a reason to stop — it's a signal that [name] needs more time to open up.",
        },
        "medium": {
            "warmup":    "The tutor notes selective engagement — [name] switches on when the topic interests them. That's normal, and the right curriculum will strengthen it.",
            "urgency":   "[name]'s motivation depends on regular contact with the material — without continuing, interest will fade before it has a chance to become stable.",
            "objection": "Right now is when the habit of learning is being formed — a pause at this stage breaks it more easily than at any other.",
        },
        "high": {
            "warmup":    "The tutor sees that [name] is genuinely engaged and motivated — the child actually wants to learn. Parents love hearing this and it makes the decision easier.",
            "urgency":   "[name] is engaged and curious right now — this kind of internal drive in a child is rare, and it should be supported while it's there.",
            "objection": "[name]'s interest isn't a coincidence — the tutor sees it consistently. Children lose motivation during breaks far faster than adults do.",
        },
    },
}

# Which raw zones contribute to each composite metric
METRIC_SOURCES = {
    "potential":  ["comprehension", "independence", "motivation"],
    "progress":   ["stability", "comprehension", "independence"],
    "engagement": ["attention", "motivation"],
}

# Scoring formulas
def compute_zone_score(zone_key, selections):
    """
    selections: list of 0-based indices into CHECKBOXES[zone_key]
    returns float in roughly [-1, 1]
    """
    items = CHECKBOXES[zone_key]
    total = sum(items[i][0] for i in selections if 0 <= i < len(items))
    return round(total / 6, 4)

def score_to_level(score):
    if score >= 0.5:
        return "high"
    elif score >= 0.0:
        return "medium"
    else:
        return "low"

def compute_academics(responses, attendance_rate, solution_rate, student_name):
    """
    responses: dict {zone_key: [list of selected indices]}
    Returns the full academic dict.
    """
    # Raw zone scores
    zone_scores = {}
    for z in ["comprehension", "independence", "attention", "stability", "motivation"]:
        sels = responses.get(z, [])
        zone_scores[z] = compute_zone_score(z, sels)

    C = zone_scores["comprehension"]
    I = zone_scores["independence"]
    A = zone_scores["attention"]
    S = zone_scores["stability"]
    M = zone_scores["motivation"]

    potential_score  = round(0.40 * C + 0.40 * I + 0.20 * M, 4)
    progress_score   = round(0.40 * S + 0.35 * C + 0.25 * I, 4)
    engagement_score = round(0.60 * A + 0.40 * M, 4)

    def build_metric(score, metric_key):
        level = score_to_level(score)
        ism_raw = ISM_COPY[metric_key][level]
        name = student_name or "the student"
        ism = {k: v.replace("[name]", name) for k, v in ism_raw.items()}

        # Build sources: checked items from contributing zones
        source_zones = METRIC_SOURCES[metric_key]
        seen = set()
        sources = {}
        for z in source_zones:
            items = CHECKBOXES[z]
            sels = responses.get(z, [])
            checked = []
            for idx in sels:
                if 0 <= idx < len(items):
                    w, text = items[idx]
                    if text not in seen:
                        seen.add(text)
                        checked.append({"text": text, "weight": w, "index": idx, "zone": z})
            # sort green → yellow → red
            checked.sort(key=lambda x: -x["weight"])
            if checked:
                sources[ZONE_META[z]["label"]] = checked

        return {
            "score": score,
            "level": level,
            "ism": ism,
            "sources": sources,
        }

    # Growth zones
    negative_zones = {z: v for z, v in zone_scores.items() if v < 0}
    growth_zone_keys = sorted(negative_zones, key=lambda z: negative_zones[z])[:2]

    red_by_zone = {}
    for z in growth_zone_keys:
        label = ZONE_META[z]["label"]
        items = CHECKBOXES[z]
        sels = responses.get(z, [])
        reds = [items[i][1] for i in sels if 0 <= i < len(items) and items[i][0] < 0]
        if reds:
            red_by_zone[label] = reds

    # Motivators
    motivator_sels = responses.get("motivators", [])
    motivators = [MOTIVATORS[i] for i in motivator_sels if 0 <= i < len(MOTIVATORS)]

    # Parent
    parent_sels = responses.get("parent", [])
    parent_text = None
    parent_color = None
    if parent_sels:
        idx = parent_sels[0]
        if 0 <= idx < len(PARENT_OPTIONS):
            parent_text = PARENT_OPTIONS[idx]["text"]
            parent_color = PARENT_OPTIONS[idx]["color"]

    return {
        "attendance_rate": attendance_rate,
        "solution_rate": solution_rate,
        "zone_scores": zone_scores,
        "potential":  build_metric(potential_score, "potential"),
        "progress":   build_metric(progress_score, "progress"),
        "engagement": build_metric(engagement_score, "engagement"),
        "growth_zones": {
            "zones": growth_zone_keys,
            "red_by_zone": red_by_zone,
        },
        "motivators": motivators,
        "parent": parent_text,
        "parent_color": parent_color,
    }
