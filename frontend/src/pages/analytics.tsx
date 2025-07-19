import React, { useState } from "react";
import UploadPanel from "../components/UploadPanel";
import DefinitionPanel from "../components/DefinitionPanel";
import QuestionPanel from "../components/QuestionPanel";
import OutputPanel from "../components/OutputPanel";

import SpeedTierAnalysis from "../components/analytics/SpeedTierAnalysis";
import SpeedTierConfig from "../components/analytics/SpeedTierConfig";

type Tab = "ai" | "speed";

export default function AnalyticsPage() {
  const [activeTab, setActiveTab] = useState<Tab>("ai");

  const [definitions, setDefinitions] = useState<string[]>([]);
  const [question, setQuestion] = useState<string>("");
  const [result, setResult] = useState<any>(null);

  return (
    <div style={{ display: "flex", height: "100vh" }}>
      {/* Sidebar */}
      <div style={{ width: 220, backgroundColor: "#f4f4f4", padding: 20 }}>
        <h2 style={{ fontSize: 18, marginBottom: 20 }}>📁 Features</h2>

        <button
          onClick={() => setActiveTab("ai")}
          style={{
            display: "block",
            width: "100%",
            marginBottom: 10,
            padding: "10px 12px",
            backgroundColor: activeTab === "ai" ? "#007bff" : "#ddd",
            color: activeTab === "ai" ? "white" : "black",
            border: "none",
            borderRadius: 6,
            cursor: "pointer",
            textAlign: "left",
          }}
        >
          💬 AI Panel
        </button>

        <button
          onClick={() => setActiveTab("speed")}
          style={{
            display: "block",
            width: "100%",
            padding: "10px 12px",
            backgroundColor: activeTab === "speed" ? "#007bff" : "#ddd",
            color: activeTab === "speed" ? "white" : "black",
            border: "none",
            borderRadius: 6,
            cursor: "pointer",
            textAlign: "left",
          }}
        >
          🚀 Speed Tiers
        </button>
      </div>

      {/* Main Panel */}
      <div style={{ flex: 1, padding: 24, overflowY: "auto" }}>
        <h1>📊 Analytics Dashboard</h1>

        {activeTab === "ai" && (
          <div style={{ border: "1px solid #ccc", padding: 20, borderRadius: 8 }}>
            <UploadPanel />
            <DefinitionPanel
              definitions={definitions}
              setDefinitions={setDefinitions}
            />
            <QuestionPanel
              question={question}
              setQuestion={setQuestion}
              definitions={definitions}
              setResult={setResult}
            />
            <OutputPanel result={result} />
          </div>
        )}

        {activeTab === "speed" && (
          <div style={{ border: "1px solid #ccc", padding: 20, borderRadius: 8 }}>
            {/* ⬆️ Config panel on top */}
            <SpeedTierConfig />
            <SpeedTierAnalysis />
          </div>
        )}
      </div>
    </div>
  );
}
