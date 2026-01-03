// src/Home.jsx
import { Container, Row, Col, Card } from "react-bootstrap";
import { useNavigate } from "react-router-dom";

export default function Home() {
  const navigate = useNavigate();

  return (
    <Container className="mt-4">
      <h3 className="mb-4">📊 Dashboard</h3>

      <Row>
        <Col xs={12} md={6} lg={4}>
          <Card
            className="shadow-sm h-100"
            style={{ cursor: "pointer" }}
            onClick={() => navigate("/simulation")}
          >
            <Card.Body>
              <Card.Title>🧠 Simulación 180</Card.Title>

              <Card.Text className="text-muted">
                Evaluación completa estilo EUNACOM.
                <br />
                <strong>180 preguntas</strong> en dos bloques.
              </Card.Text>

              <div className="mt-3 text-primary">
                Entrar a simulación →
              </div>
            </Card.Body>
          </Card>
        </Col>
      </Row>
    </Container>
  );
}