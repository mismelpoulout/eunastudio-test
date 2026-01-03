from datetime import datetime, timedelta


class ExamState:
    """
    Estado vivo de una simulación.
    NO corrige.
    NO califica.
    Solo sabe:
    - dónde va el usuario
    - cuánto tiempo queda
    - qué bloque está activo
    """

    def __init__(self, exam_id: str):
        self.exam_id = exam_id
        self.started_at = datetime.utcnow()

        # 🔹 bloques
        self.current_block = "A"
        self.block_start_time = datetime.utcnow()

        self.block_durations = {
            "A": timedelta(minutes=30),
            "B": timedelta(minutes=60),
        }

        self.block_limits = {
            "A": 90,
            "B": 180,  # total acumulado
        }

        # 📝 respuestas
        self.answers: dict[str, str] = {}

        # 📊 progreso
        self.answered_count = 0
        self.completed = False

        # 🧠 métricas futuras (adaptatividad)
        self.by_topic = {}
        self.by_specialty = {}

    # ----------------------------------
    # ⏱️ Tiempo restante del bloque actual
    # ----------------------------------
    def remaining_time_seconds(self) -> int:
        elapsed = datetime.utcnow() - self.block_start_time
        remaining = self.block_durations[self.current_block] - elapsed
        return max(0, int(remaining.total_seconds()))

    # ----------------------------------
    # 🔁 Cambiar de bloque
    # ----------------------------------
    def switch_block(self):
        if self.current_block == "A":
            self.current_block = "B"
            self.block_start_time = datetime.utcnow()
        else:
            self.completed = True

    # ----------------------------------
    # 📝 Registrar respuesta (API estándar)
    # ----------------------------------
    def record_answer(self, question_id: str, answer: str):
        if self.completed:
            return

        if question_id not in self.answers:
            self.answered_count += 1

        self.answers[question_id] = answer

        # ⏩ control de bloque
        limit = self.block_limits[self.current_block]
        if self.answered_count >= limit:
            self.switch_block()

    # ----------------------------------
    # 📊 Registrar desempeño (futuro)
    # ----------------------------------
    def register_result(self, question, is_correct: bool):
        topic = getattr(question, "topic", None)
        if topic:
            self.by_topic.setdefault(topic, {"total": 0, "correct": 0})
            self.by_topic[topic]["total"] += 1
            if is_correct:
                self.by_topic[topic]["correct"] += 1

        specialty = getattr(question, "specialty", None)
        if specialty:
            self.by_specialty.setdefault(
                specialty, {"total": 0, "correct": 0}
            )
            self.by_specialty[specialty]["total"] += 1
            if is_correct:
                self.by_specialty[specialty]["correct"] += 1

    # ----------------------------------
    # 📦 Serializar estado (API safe)
    # ----------------------------------
    def to_dict(self):
        return {
            "exam_id": self.exam_id,
            "current_block": self.current_block,
            "answered": self.answered_count,
            "remaining_time_seconds": self.remaining_time_seconds(),
            "completed": self.completed,
            "started_at": self.started_at.isoformat(),
        }

    # ----------------------------------
    # 🧭 Resumen rápido para frontend
    # ----------------------------------
    def progress(self) -> dict:
        return {
            "answered": self.answered_count,
            "remaining_seconds": self.remaining_time_seconds(),
            "block": self.current_block,
            "completed": self.completed,
        }