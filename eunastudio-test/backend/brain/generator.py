# backend/brain/generator.py
import json
import random
import uuid
from datetime import datetime
from pathlib import Path

from brain.state import ExamState

# -----------------------------
# CONFIGURACIÓN
# -----------------------------
TOTAL_QUESTIONS = 180
BLOCK_SIZE = 90

BLOCK_A_DURATION = 80      # minutos
INTERMISSION_DURATION = 30 # minutos
BLOCK_B_DURATION = 80      # minutos

BASE_DIR = Path(__file__).resolve().parent.parent
QUESTIONS_PATH = BASE_DIR / "data" / "questions.json"


# -----------------------------
# GENERADOR PRINCIPAL
# -----------------------------
def generate_simulation():
    # 📥 cargar preguntas
    with open(QUESTIONS_PATH, "r", encoding="utf-8") as f:
        raw_questions = json.load(f)

    if len(raw_questions) < TOTAL_QUESTIONS:
        raise ValueError(
            f"No hay suficientes preguntas: {len(raw_questions)} / {TOTAL_QUESTIONS}"
        )

    # 🧼 normalizar + asegurar ID
    questions = []
    for idx, q in enumerate(raw_questions):
        questions.append({
            "id": q.get("id") or f"q_{idx}",
            "question": q["question"],
            "options": q["options"],
            "answer": q["answer"],
            "feedback": q.get("feedback"),
        })

    # 🔀 aleatorizar
    random.shuffle(questions)

    # ✂️ seleccionar 180
    selected = questions[:TOTAL_QUESTIONS]

    # 🆔 examen
    exam_id = f"sim-{uuid.uuid4()}"

    exam = {
        "id": exam_id,
        "created_at": datetime.utcnow().isoformat(),
        "config": {
            "block_a_minutes": BLOCK_A_DURATION,
            "intermission_minutes": INTERMISSION_DURATION,
            "block_b_minutes": BLOCK_B_DURATION,
        },
        # 🔑 IMPORTANTE PARA FRONTEND
        "questions": selected,
    }

    # 🧠 estado inicial vivo
    state = ExamState(exam_id=exam_id)

    return {
        "exam": exam,
        "state": state.to_dict(),
    }