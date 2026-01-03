def evaluate_simulation(exam, answers):
    correct = 0
    total = 0
    detailed = []

    for block in exam["blocks"].values():
        for q in block["questions"]:
            total += 1
            user_answer = answers.get(q["id"])
            is_correct = user_answer == q["answer"]

            if is_correct:
                correct += 1

            detailed.append({
                "id": q["id"],
                "correct": is_correct,
                "correct_answer": q["answer"],
                "user_answer": user_answer,
                "feedback": q.get("feedback"),
            })

    percentage = round((correct / total) * 100, 2)

    return {
        "total": total,
        "correct": correct,
        "incorrect": total - correct,
        "percentage": percentage,
        "status": "Aprobado" if percentage >= 60 else "Reprobado",
        "details": detailed,
    }