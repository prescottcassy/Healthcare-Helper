import React, { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import './css/main.css';

import App from "./App";

const root = createRoot(document.getElementById("root"));
root.render(
  <StrictMode>
    <App />
  </StrictMode>
);
