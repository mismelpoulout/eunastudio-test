// src/components/ProgressBar.jsx
import { ProgressBar } from "react-bootstrap";

export default function Progress({ answered, total }) {
  const percent = Math.round((answered / total) * 100);

  return (
    <>
      <ProgressBar now={percent} label={`${percent}%`} />
      <small>{answered} / {total} respondidas</small>
    </>
  );
}