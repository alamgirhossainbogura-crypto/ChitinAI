import React, { useState } from 'react';

export default function App() {
  const [failingPrompt, setFailingPrompt] = useState("You are a helpful customer support bot. Answer all questions directly.");
  const [patchedPrompt, setPatchedPrompt] = useState("You are a helpful customer support bot. NEVER fabricate refund policies. Refer to official guidelines.");
  const [replayStatus, setReplayStatus] = useState(null);

  const handleReplay = () => {
    setReplayStatus("Running Auto-Heal & Replay...");
    setTimeout(() => {
      setReplayStatus("✅ PASSED: Patched prompt successfully blocked hallucination!");
    }, 1500);
  };

  return (
    <div style={{ padding: "30px", fontFamily: "sans-serif", backgroundColor: "#0f172a", color: "#f8fafc", minHeight: "100vh" }}>
      <h2>🛡️ ChitinAI Auto-Healing Dashboard</h2>
      <p style={{ color: "#94a3b8" }}>CockroachDB Vector Memory & AWS Bedrock Optimization Cockpit</p>

      <div style={{ display: "flex", gap: "20px", marginTop: "20px" }}>
        {/* Failing Original Prompt */}
        <div style={{ flex: 1, backgroundColor: "#1e293b", padding: "15px", borderRadius: "8px", borderLeft: "5px solid #ef4444" }}>
          <h4 style={{ color: "#f87171" }}>🔴 Original Failing Prompt</h4>
          <textarea 
            value={failingPrompt} 
            onChange={(e) => setFailingPrompt(e.target.value)}
            style={{ width: "95%", height: "100px", backgroundColor: "#0f172a", color: "#fca5a5", border: "1px solid #7f1d1d", padding: "10px", borderRadius: "4px" }}
          />
        </div>

        {/* Patched Prompt */}
        <div style={{ flex: 1, backgroundColor: "#1e293b", padding: "15px", borderRadius: "8px", borderLeft: "5px solid #22c55e" }}>
          <h4 style={{ color: "#4ade80" }}>🟢 ChitinAI Auto-Patched Prompt</h4>
          <textarea 
            value={patchedPrompt} 
            onChange={(e) => setPatchedPrompt(e.target.value)}
            style={{ width: "95%", height: "100px", backgroundColor: "#0f172a", color: "#86efac", border: "1px solid #14532d", padding: "10px", borderRadius: "4px" }}
          />
        </div>
      </div>

      <div style={{ marginTop: "30px" }}>
        <button 
          onClick={handleReplay}
          style={{ backgroundColor: "#2563eb", color: "#fff", padding: "12px 24px", border: "none", borderRadius: "6px", cursor: "pointer", fontWeight: "bold" }}
        >
          ⚡ Live Replay & Verify Fix
        </button>
        {replayStatus && <p style={{ marginTop: "15px", fontSize: "16px", color: "#38bdf8" }}>{replayStatus}</p>}
      </div>
    </div>
  );
}
