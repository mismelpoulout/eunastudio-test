// src/App.jsx
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { Container } from "react-bootstrap";

import Home from "./Home";
import Simulation from "./Simulation";

export default function App() {
  return (
    <BrowserRouter>
      <Container fluid>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/simulation" element={<Simulation />} />
        </Routes>
      </Container>
    </BrowserRouter>
  );
}