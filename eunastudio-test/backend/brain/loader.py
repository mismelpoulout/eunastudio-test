import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data", "questions.json")

def load_questions():
    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError("questions.json no encontrado")

    with open(DATA_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    questions = []

    for idx, q in enumerate(data):
        questions.append({
            "id": q.get("id", f"q_{idx}"),
            "question": q["question"],
            "options": q["options"],
            "answer": q["answer"],
            "feedback": q.get("feedback"),
        })

    return questions