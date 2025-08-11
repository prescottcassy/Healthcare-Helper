import React, { useState } from 'react';
import logo from './logo.svg';
import './App.css';

// Use environment variable for backend URL
const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;

function App() {
  const [response, setResponse] = useState(null);
const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:5000';

function App() {
  const [response, setResponse] = useState(null);

  // Warn if using fallback BACKEND_URL
  if (!process.env.REACT_APP_BACKEND_URL) {
    console.warn(
      'REACT_APP_BACKEND_URL is not set. Using default http://localhost:5000. ' +
      'Set REACT_APP_BACKEND_URL in your environment to avoid this warning.'
    );
  }
  // Handler for file upload
  const handleFileUpload = async (event) => {
    const file = event.target.files[0];
    if (!file) {
      setResponse('No file selected.');
      return;
    }
    const formData = new FormData();
    formData.append('file', file);

    try {
      const res = await fetch(`${BACKEND_URL}/api/insurance/upload`, {
        method: 'POST',
        body: formData,
        // Do NOT set Content-Type header; browser will set it automatically
      });
      if (!res.ok) {
        throw new Error(`Server error: ${res.status}`);
      }
      const data = await res.json();
      setResponse(JSON.stringify(data, null, 2));
    } catch (error) {
      setResponse('Error: ' + error.message);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <h2>Healthcare Helper</h2>
        <input type="file" accept=".pdf,.jpg,.jpeg,.png" onChange={handleFileUpload} />
        {response && (
          <pre style={{ textAlign: 'left', margin: '1em auto', maxWidth: 600 }}>{response}</pre>
        )}
      </header>
    </div>
  );
}

export default App;