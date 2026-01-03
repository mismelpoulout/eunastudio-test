from datetime import datetime, timedelta


class ExamState:
    """
    Estado vivo de una simulación 180.
    NO corrige.
    NO califica.
    SOLO controla:
    - bloque actual
    - tiempos
    - progreso
    """

    def __init__(self, exam_id: str):
        self.exam_id = exam_id
        self.started_at = datetime.utcnow()

        # 🔹 bloques posibles: A → INTERMISSION → B → COMPLETED
        self.current_block = "A"
        self.block_start_time = datetime.utcnow()

        # ⏱️ duraciones oficiales
        self.block_durations = {
            "A": timedelta(minutes=80),
            "INTERMISSION": timedelta(minutes=30),
            "B": timedelta(minutes=80),
        }

        # 📊 límites por bloque
        self.block_limits = {
            "A": 90,     # preguntas bloque A
            "B": 180,    # total acumulado (A + B)
        }

        # 📝 respuestas
        self.answers: dict[str, str] = {}
        self.answered_count = 0

        # estado final
        self.completed = False

        # 🧠 métricas futuras
        self.by_topic = {}
        self.by_specialty = {}

    # ----------------------------------
    # ⏱️ Tiempo restante del bloque actual
    # ----------------------------------
    def remaining_time_seconds(self) -> int:
        elapsed = datetime.utcnow() - self.block_start_time
        duration = self.block_durations.get(self.current_block)
        if not duration:
            return 0

        remaining = duration - elapsed
        return max(0, int(remaining.total_seconds()))

    # ----------------------------------
    # 🔁 Avanzar de bloque
    # ----------------------------------
    def advance_block(self):
        if self.current_block == "A":
            self.current_block = "INTERMISSION"
        elif self.current_block == "INTERMISSION":
            self.current_block = "B"
        elif self.current_block == "B":
            self.completed = True
            self.current_block = "COMPLETED"
            return
        else:
            return

        self.block_start_time = datetime.utcnow()

    # ----------------------------------
    # 📝 Registrar respuesta
    # ----------------------------------
    def record_answer(self, question_id: str, answer: str):
        if self.completed or self.current_block == "INTERMISSION":
            return

        if question_id not in self.answers:
            self.answered_count += 1

        self.answers[question_id] = answer

        # 🔒 control por cantidad de preguntas
        if self.current_block in self.block_limits:
            limit = self.block_limits[self.current_block]
            if self.answered_count >= limit:
                self.advance_block()

    # ----------------------------------
    # ⏱️ Verificar tiempo y avanzar
    # ----------------------------------
    def check_time(self):
        if self.remaining_time_seconds() == 0:
            self.advance_block()

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
    # 🧭 Resumen para frontend
    # ----------------------------------
    def progress(self) -> dict:
        return {
            "answered": self.answered_count,
            "block": self.current_block,
            "remaining_seconds": self.remaining_time_seconds(),
            "completed": self.completed,
        }