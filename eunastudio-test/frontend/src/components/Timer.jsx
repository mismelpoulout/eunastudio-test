// src/components/Timer.jsx
export default function Timer({ seconds }) {
  const min = Math.floor(seconds / 60);
  const sec = seconds % 60;

  return (
    <p>
      ⏱️ Tiempo restante:{" "}
      <strong>
        {min}:{sec.toString().padStart(2, "0")}
      </strong>
    </p>
  );
}