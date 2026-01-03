import { useState } from "react";
import {
  Button,
  Spinner,
  Alert,
  Container,
  Modal,
} from "react-bootstrap";
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

  const [showConfirm, setShowConfirm] = useState(false);

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

  // 📤 enviar respuestas (SIEMPRE permitido)
  const submitAnswers = async () => {
    if (!exam) return;

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

    return state.current_block === "A"
      ? exam.questions.slice(0, 90)
      : exam.questions.slice(90, 180);
  };

  // ⛔️ pantalla inicial
  if (!exam || !state) {
    return (
      <Container className="mt-4">
        <h3>🧠 Simulación 180</h3>

        <Button onClick={startSimulation} disabled={loading}>
          Iniciar simulación
        </Button>

        {loading && <Spinner className="ms-3" />}
        {error && <Alert variant="danger" className="mt-3">{error}</Alert>}
      </Container>
    );
  }

  const currentQuestions = questionsForBlock();
  const isBlockA = state.current_block === "A";

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

      {/* 🔴 BOTÓN TERMINAR BLOQUE */}
      <Button
        variant={isBlockA ? "warning" : "danger"}
        className="mt-4"
        onClick={() => setShowConfirm(true)}
      >
        {isBlockA ? "Terminar Bloque A" : "Finalizar Simulación"}
      </Button>

      {error && <Alert variant="danger" className="mt-3">{error}</Alert>}

      {/* ⚠️ MODAL CONFIRMACIÓN */}
      <Modal show={showConfirm} centered>
        <Modal.Header>
          <Modal.Title>
            {isBlockA
              ? "Confirmar cierre del Bloque A"
              : "Confirmar finalización del examen"}
          </Modal.Title>
        </Modal.Header>

        <Modal.Body>
          {isBlockA ? (
            <>
              <p>
                Estás a punto de cerrar el <b>Bloque A</b>.
              </p>
              <p>
                Tendrás un intermedio de <b>30 minutos</b> antes de comenzar
                el Bloque B.
              </p>
              <p className="text-danger">
                No podrás volver a este bloque.
              </p>
            </>
          ) : (
            <>
              <p>
                Estás a punto de <b>finalizar la simulación</b>.
              </p>
              <p className="text-danger">
                Se evaluarán tus respuestas sobre un total de <b>180 preguntas</b>,
                incluyendo las no respondidas.
              </p>
            </>
          )}
        </Modal.Body>

        <Modal.Footer>
          <Button
            variant="secondary"
            onClick={() => setShowConfirm(false)}
          >
            Cancelar
          </Button>

          <Button
            variant="danger"
            onClick={async () => {
              setShowConfirm(false);
              await submitAnswers();
            }}
          >
            Confirmar
          </Button>
        </Modal.Footer>
      </Modal>
    </Container>
  );
}