import React, { useState } from "react";

function QueryForm() {
  const [query, setQuery] = useState("");
  const [chatHistory, setChatHistory] = useState([]);
  const [loading, setLoading] = useState(false);
  const [selectedFile, setSelectedFile] = useState(null);

  async function getChatResponse() {
    setLoading(true);
    const response = await fetch("https://healthcare-helper-pt6e.onrender.com/api/chat/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query })
    });
    const data = await response.json();
    setChatHistory(prev => [...prev, { query, response: data }]);
    setLoading(false);
    setQuery("");
  }

  async function handleFileUpload(e) {
    const file = e.target.files[0];
    setSelectedFile(file);
    if (!file) return;
    setLoading(true);
    const formData = new FormData();
    formData.append("file", file);
    const response = await fetch("https://healthcare-helper-pt6e.onrender.com/api/insurance/analyze", {
      method: "POST",
      body: formData
    });
    const data = await response.json();
    // Store extracted fields as plain data, not JSX
    let extractedFields = data.extracted_data;
    setChatHistory(prev => [...prev, {
      query: `Uploaded file: ${file.name}`,
      response: {
        answer: "Extracted Data:",
        extracted_text: JSON.stringify(extractedFields, null, 2),
        extractedFields
      }
    }]);
    setLoading(false);
  }

  return (
    <div>
      <h1 style={{textAlign: 'center', margin: '2rem 0 1rem 0', color: '#1976d2'}}>Healthcare Helper</h1>
      <div className="chat-ui">
        <aside className="chat-sidebar">
          <h3>Chat History</h3>
          <ul>
            {chatHistory.map((chat, idx) => (
              <li key={idx} className="chat-history-item">
                <span className="chat-q">Q:</span> {chat.query}
              </li>
            ))}
          </ul>
        </aside>
        <div className="chat-main">
          <form className="upload-form" style={{marginBottom: '1rem'}}>
            <label htmlFor="insurance-upload" className="upload-label">
              Please upload your health insurance document (PDF, JPG, or PNG).
            </label>
            <input
              type="file"
              id="insurance-upload"
              name="insurance"
              accept=".pdf,.jpg,.jpeg,.png"
              disabled={loading}
              style={{marginTop: '0.5rem'}}
              onChange={handleFileUpload}
            />
          </form>
          <div className="chat-bubbles">
            {chatHistory.map((chat, idx) => (
              <React.Fragment key={idx}>
                <div className="chat-bubble user-bubble">
                  <span className="bubble-label">You:</span> {chat.query}
                </div>
                <div className="chat-bubble ai-bubble">
                  <span className="bubble-label">AI:</span> {chat.response.answer}
                  {chat.response.confidence !== undefined && (
                    <span className="confidence-badge">Confidence: {chat.response.confidence}</span>
                  )}
                  {chat.response.entities && Object.keys(chat.response.entities).length > 0 && (
                    <details className="bubble-details">
                      <summary>Entities</summary>
                      <pre>{JSON.stringify(chat.response.entities, null, 2)}</pre>
                    </details>
                  )}
                  {chat.response.recommendations && chat.response.recommendations.length > 0 && (
                    <details className="bubble-details">
                      <summary>Recommendations</summary>
                      <ul>
                        {chat.response.recommendations.map((rec, idx2) => (
                          <li key={idx2}>{rec}</li>
                        ))}
                      </ul>
                    </details>
                  )}
                  {chat.response.coverage && chat.response.coverage.length > 0 && (
                    <details className="bubble-details">
                      <summary>Coverage</summary>
                      <pre>{JSON.stringify(chat.response.coverage, null, 2)}</pre>
                    </details>
                  )}
                  {/* Show extracted fields directly if present */}
                  {chat.response.extractedFields && typeof chat.response.extractedFields === 'object' && Object.keys(chat.response.extractedFields).length > 0 && (
                    <ul style={{ margin: 0, paddingLeft: 20 }}>
                      {Object.entries(chat.response.extractedFields).map(([key, value]) => (
                        <li key={key}><strong>{key}:</strong> {String(value)}</li>
                      ))}
                    </ul>
                  )}
                  {/* Show raw extracted text as expandable details */}
                  {chat.response.extracted_text && (
                    <details className="bubble-details">
                      <summary>Extracted Text (Raw JSON)</summary>
                      <pre>{chat.response.extracted_text}</pre>
                    </details>
                  )}
                </div>
              </React.Fragment>
            ))}
            {loading && (
              <div className="chat-bubble loading-bubble">
                <span className="bubble-label">AI:</span>
                <span className="loading-dots">
                  <span></span><span></span><span></span>
                </span>
                <span className="loading-message">Thinking...</span>
              </div>
            )}
          </div>
          <form className="chat-form" onSubmit={e => {e.preventDefault(); getChatResponse();}}>
            <input
              type="text"
              value={query}
              onChange={e => setQuery(e.target.value)}
              placeholder="Type your question..."
              disabled={loading}
            />
            <button type="submit" disabled={loading || !query.trim()}>Send</button>
          </form>
        </div>
      </div>
    </div>
  );
}

export default QueryForm;