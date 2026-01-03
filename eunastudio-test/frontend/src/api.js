// src/api.js
import axios from "axios";

const api = axios.create({
  baseURL: "http://localhost:5000", // ajusta si usas otro puerto
  headers: {
    "Content-Type": "application/json",
  },
});

export default api;