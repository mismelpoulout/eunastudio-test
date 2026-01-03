// src/components/QuestionCard.jsx
import { Card } from "react-bootstrap";

export default function QuestionCard({ question, onAnswer }) {
  return (
    <Card className="mt-3">
      <Card.Body>
        <strong>{question.question}</strong>

        {question.options.map((opt, i) => (
          <div key={i}>
            <input
              type="radio"
              name={question.id}
              onChange={() => onAnswer(opt)}
            />{" "}
            {opt}
          </div>
        ))}
      </Card.Body>
    </Card>
  );
}