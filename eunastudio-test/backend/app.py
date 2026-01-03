from flask import Flask, jsonify, request
from flask_cors import CORS

from brain.generator import generate_simulation
from brain.state import ExamState

app = Flask(__name__)
CORS(app)  # 🔥 CLAVE PARA FRONTEND

# 🧠 memoria temporal (luego Redis / DB)
EXAM_STATES: dict[str, ExamState] = {}

# -----------------------------
# HEALTH CHECK
# -----------------------------
@app.route("/", methods=["GET"])
def health():
    return {"status": "ok", "service": "simulacion-180"}

# -----------------------------
# GENERAR SIMULACIÓN
# -----------------------------
@app.route("/api/simulation/start", methods=["GET"])
def start_simulation():
    payload = generate_simulation()

    exam_id = payload["exam"]["id"]

    # 🧠 crear estado vivo
    state = ExamState(exam_id=exam_id)
    EXAM_STATES[exam_id] = state

    return jsonify({
        "exam": payload["exam"],
        "state": state.to_dict()
    })

# -----------------------------
# ENVIAR RESPUESTAS (PARCIAL)
# -----------------------------
@app.route("/api/simulation/submit", methods=["POST"])
def submit_partial():
    data = request.get_json(silent=True) or {}

    exam_id = data.get("exam_id")
    answers = data.get("answers", {})  # {question_id: option}

    if not exam_id or exam_id not in EXAM_STATES:
        return jsonify({"error": "Estado de examen no encontrado"}), 404

    state = EXAM_STATES[exam_id]

    # 📝 registrar respuestas
    for qid, value in answers.items():
        state.register_answer(qid, value)  # ✅ método correcto

    return jsonify({
        "message": "Respuestas registradas",
        "state": state.to_dict()
    })

# -----------------------------
# CONSULTAR ESTADO
# -----------------------------
@app.route("/api/simulation/state/<exam_id>", methods=["GET"])
def get_state(exam_id):
    state = EXAM_STATES.get(exam_id)

    if not state:
        return jsonify({"error": "Estado no encontrado"}), 404

    return jsonify(state.to_dict())

# -----------------------------
# RUN LOCAL
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True, port=5000)