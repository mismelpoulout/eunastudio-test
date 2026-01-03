// src/Simulation.jsx
import { useState } from "react";
import { Button, Spinner, Alert, Container } from "react-bootstrap";
import api from "./api";

import QuestionCard from "./components/QuestionCard";
import Timer from "./components/Timer";
import ProgressBar from "./components/ProgressBar";

export default function Simulation() {
  const [exam, setExam] = useState(null);
  const [state, setState] = useState(null);
  const [answers, setAnswers] = useState({});
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // 🚀 iniciar simulación
  const startSimulation = async () => {
    setLoading(true);
    setError(null);

    try {
      const res = await api.get("/api/simulation/start");
      setExam(res.data.exam);
      setState(res.data.state);
    } catch (e) {
      console.error(e);
      setError("No se pudo iniciar la simulación");
    } finally {
      setLoading(false);
    }
  };

  // 📤 enviar respuestas parciales
  const submitAnswers = async () => {
    if (!exam || Object.keys(answers).length === 0) return;

    try {
      const res = await api.post("/api/simulation/submit", {
        exam_id: exam.id,
        answers,
      });

      setState(res.data.state);
      setAnswers({});
    } catch (e) {
      console.error(e);
      setError("Error enviando respuestas");
    }
  };

  // 🧩 preguntas del bloque actual
  const questionsForBlock = () => {
    if (!exam || !state) return [];

    if (state.current_block === "A") {
      return exam.questions.slice(0, 90);
    }

    if (state.current_block === "B") {
      return exam.questions.slice(90, 180);
    }

    return [];
  };

  // ⛔️ GUARD GLOBAL
  if (!exam || !state) {
    return (
      <Container className="mt-4">
        <h3>🧠 Simulación 180</h3>

        <Button onClick={startSimulation} disabled={loading}>
          Iniciar simulación
        </Button>

        {loading && <Spinner className="ms-3" />}
        {error && (
          <Alert variant="danger" className="mt-3">
            {error}
          </Alert>
        )}
      </Container>
    );
  }

  const currentQuestions = questionsForBlock();

  return (
    <Container className="mt-4">
      <h4>Bloque {state.current_block}</h4>

      <Timer seconds={state.remaining_time_seconds} />

      <ProgressBar
        answered={state.answered}
        total={currentQuestions.length}
      />

      {currentQuestions.map((q) => (
        <QuestionCard
          key={q.id}
          question={q}
          onAnswer={(value) =>
            setAnswers((prev) => ({ ...prev, [q.id]: value }))
          }
        />
      ))}

      <Button className="mt-4" onClick={submitAnswers}>
        Guardar respuestas
      </Button>

      {error && (
        <Alert variant="danger" className="mt-3">
          {error}
        </Alert>
      )}
    </Container>
  );
}