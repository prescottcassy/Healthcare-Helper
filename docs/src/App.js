import React from "react";
import QueryForm from "./components/QueryForm";


import { useState } from "react";

function App() {
  const [showChat, setShowChat] = useState(false);

  return (
    <div>
      {!showChat ? (
        <div className="home-page" style={{textAlign: 'center', marginTop: '5rem'}}>
          <h1 style={{color: '#1976d2', fontSize: '2.5rem', marginBottom: '1.5rem'}}>Healthcare Helper</h1>
          <p style={{fontSize: '1.2rem', color: '#555', marginBottom: '2rem'}}>Your AI-powered assistant for healthcare questions, insurance, and cost recommendations.</p>
          <button
            style={{background: '#38bdf8', color: '#fff', border: 'none', borderRadius: '8px', padding: '1rem 2rem', fontSize: '1.2rem', cursor: 'pointer'}}
            onClick={() => setShowChat(true)}
          >
            Start Chat
          </button>
        </div>
      ) : (
        <QueryForm />
      )}
    </div>
  );
}

export default App;