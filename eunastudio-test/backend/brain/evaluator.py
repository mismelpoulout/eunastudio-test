def evaluate_simulation(exam: dict, answers: dict) -> dict:
    """
    Evalúa una simulación completa de 180 preguntas.
    El porcentaje SIEMPRE se calcula sobre 180,
    independientemente de cuántas se respondieron.
    """

    TOTAL_QUESTIONS = 180
    correct = 0
    detailed = []

    # 🔁 recorrer bloques A y B
    for block_key in ["A", "B"]:
        block = exam["blocks"].get(block_key, {})
        questions = block.get("questions", [])

        for q in questions:
            user_answer = answers.get(q["id"])
            is_correct = user_answer == q["answer"]

            if is_correct:
                correct += 1

            detailed.append({
                "id": q["id"],
                "block": block_key,
                "correct": is_correct,
                "user_answer": user_answer,
                "correct_answer": q["answer"],
                "feedback": q.get("feedback"),
            })

    incorrect = TOTAL_QUESTIONS - correct
    percentage = round((correct / TOTAL_QUESTIONS) * 100, 2)

    return {
        "total": TOTAL_QUESTIONS,
        "correct": correct,
        "incorrect": incorrect,
        "percentage": percentage,
        "status": "Aprobado" if percentage >= 51 else "Reprobado",
        "details": detailed,
    }