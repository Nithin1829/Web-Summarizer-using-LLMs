import React, { useState } from "react";
import axios from "axios";
import "./index.css";

function App() {
  const [url, setUrl] = useState("");
  const [openaiSummary, setOpenaiSummary] = useState("");
  const [ollamaSummary, setOllamaSummary] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSummarize = async () => {
    if (!url.trim()) {
      setError("Please enter a valid URL.");
      return;
    }

    setLoading(true);
    setError("");
    setOpenaiSummary("");
    setOllamaSummary("");

    try {
      const response = await axios.post("http://127.0.0.1:5000/summarize", {
        url: url.trim(),
      });

      setOpenaiSummary(response.data.openai_summary);
      setOllamaSummary(response.data.ollama_summary);
    } catch (err) {
      setError("An error occurred. Please try again or check the backend.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 flex flex-col items-center justify-center p-6 space-y-6">
      <h1 className="text-3xl font-bold text-gray-800">Web Summarizer (LLM Comparison)</h1>
      <input
        type="text"
        value={url}
        onChange={(e) => setUrl(e.target.value)}
        placeholder="Enter website URL"
        className="w-full max-w-2xl px-4 py-2 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-400"
      />
      <button
        onClick={handleSummarize}
        className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition"
      >
        {loading ? "Summarizing..." : "Generate Summary"}
      </button>

      {error && <div className="text-red-600">{error}</div>}

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 w-full max-w-6xl mt-6">
        <div className="bg-white p-4 rounded-lg shadow">
          <h2 className="text-xl font-semibold text-blue-600 mb-2">🔵 OpenAI Summary</h2>
          <p className="whitespace-pre-line text-gray-700">{openaiSummary}</p>
        </div>
        <div className="bg-white p-4 rounded-lg shadow">
          <h2 className="text-xl font-semibold text-green-600 mb-2">🟢 Ollama Summary</h2>
          <p className="whitespace-pre-line text-gray-700">{ollamaSummary}</p>
        </div>
      </div>
    </div>
  );
}

export default App;
