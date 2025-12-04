# medical_db.py
"""
Very simple offline medical knowledge base.
This is NOT a diagnosis tool. It only gives general info + first-aid style advice.
Always tell user to see a real doctor.
"""

CONDITIONS = [
    {
        "name": "Common Cold / Viral Infection",
        "keywords": ["cold", "runny nose", "sneezing", "sneeze", "blocked nose", "stuffy nose"],
        "symptoms": "Sneezing, runny or blocked nose, mild throat irritation, sometimes low-grade fever.",
        "first_aid": (
            "• Rest well and drink plenty of warm fluids.\n"
            "• You can use saline nasal drops or steam inhalation for blocked nose.\n"
            "• Simple paracetamol can help for fever or body pain (if not allergic and as per package/doctor)."
        ),
        "see_doctor": (
            "• If high fever lasts more than 3 days,\n"
            "• If you have breathing difficulty,\n"
            "• If chest pain or very bad throat pain develops."
        ),
    },
    {
        "name": "Fever (General)",
        "keywords": ["fever", "temperature", "high temperature"],
        "symptoms": "Rise in body temperature, may have chills, body pain, headache, tiredness.",
        "first_aid": (
            "• Check temperature with a thermometer every few hours.\n"
            "• Drink plenty of water and oral fluids.\n"
            "• Use light clothing and keep the room cool.\n"
            "• Paracetamol in correct dose may be used for relief (if not allergic and as per package/doctor)."
        ),
        "see_doctor": (
            "• If fever is more than 101°F (38.3°C) and persists more than 2–3 days,\n"
            "• If associated with rash, breathing difficulty, chest pain, confusion, or severe weakness."
        ),
    },
    {
        "name": "Migraine / Headache (Common)",
        "keywords": ["headache", "migraine", "head pain"],
        "symptoms": "Pain in head, sometimes with nausea, sensitivity to light or sound.",
        "first_aid": (
            "• Rest in a quiet, dark room.\n"
            "• Drink water; dehydration can worsen headache.\n"
            "• You may use simple pain relievers (like paracetamol) if not allergic and as per doctor/package.\n"
        ),
        "see_doctor": (
            "• If headache is sudden and very severe,\n"
            "• If associated with weakness, vision changes, confusion, or difficulty speaking,\n"
            "• If headache occurs after head injury or with high fever and neck stiffness."
        ),
    },
    {
        "name": "Gastric Acidity / Indigestion",
        "keywords": ["acidity", "gastric", "gas", "indigestion", "heartburn"],
        "symptoms": "Burning in chest or upper abdomen, sour taste, bloating, discomfort after meals.",
        "first_aid": (
            "• Avoid spicy, oily, and heavy meals for some time.\n"
            "• Eat smaller, more frequent meals.\n"
            "• Do not lie down immediately after eating.\n"
            "• Simple antacid syrups or tablets (as per doctor’s advice) can give relief."
        ),
        "see_doctor": (
            "• If pain is very severe or radiates to arm/jaw (could be heart-related),\n"
            "• If vomiting, weight loss, or black stools appear,\n"
            "• If chest pain occurs with sweating or breathlessness – this is an emergency."
        ),
    },
    {
        "name": "Possible Respiratory Infection",
        "keywords": ["cough", "breathless", "breathing", "shortness of breath", "sputum", "phlegm"],
        "symptoms": "Cough, sometimes with mucus, chest discomfort, sometimes fever or breathlessness.",
        "first_aid": (
            "• Sip warm water or herbal teas to soothe throat.\n"
            "• Avoid smoking and dusty areas.\n"
            "• Simple cough lozenges may give short relief (if not allergic)."
        ),
        "see_doctor": (
            "• If you have fast or difficult breathing,\n"
            "• If lips/face look bluish,\n"
            "• If high fever persists,\n"
            "• If chest pain or coughing blood is present.\n"
            "These signs need urgent medical attention."
        ),
    },
    {
        "name": "Possible Dehydration",
        "keywords": ["vomit", "vomiting", "loose motion", "diarrhea", "diarrhoea", "dehydrated", "dry mouth"],
        "symptoms": "Dry mouth, feeling very thirsty, passing very little urine, dizziness, weakness.",
        "first_aid": (
            "• Take frequent sips of ORS (oral rehydration solution) or salted-sugary fluids.\n"
            "• Avoid heavy, oily, and spicy food.\n"
            "• Rest in a cool place."
        ),
        "see_doctor": (
            "• If vomiting or loose motions are frequent and severe,\n"
            "• If there is blood in stool or vomit,\n"
            "• If very little or no urine is passed,\n"
            "• If the person is very drowsy or confused."
        ),
    },
]

def analyze_symptoms(user_text: str) -> str:
    """
    Very naive keyword-based matcher. Returns a formatted string if something matches,
    otherwise returns empty string.
    """
    text = user_text.lower()
    results = []

    for cond in CONDITIONS:
        for kw in cond["keywords"]:
            if kw in text:
                results.append(cond)
                break  # avoid duplicate adds for same condition

    if not results:
        return ""

    lines = []
    lines.append("🔎 *Offline Symptom Check (Not a diagnosis)*")
    for cond in results:
        lines.append("")
        lines.append("📌 Possible related condition: <b>%s</b>" % cond["name"])
        lines.append("• Typical symptoms: %s" % cond["symptoms"])
        lines.append("")
        lines.append("🩹 First-aid style guidance:")
        lines.append(cond["first_aid"])
        lines.append("")
        lines.append("⚠ When you should see a doctor:")
        lines.append(cond["see_doctor"])

    lines.append("")
    lines.append("❗ This is only general information. Please consult a qualified doctor for proper diagnosis and treatment.")

    # Join with <br> so that QTextEdit renders nicely as HTML
    return "<br>".join(lines)
