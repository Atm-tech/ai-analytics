import React, { useState } from "react";

type DefinitionSet = {
  id: number;
  label: string;
  definitions: string[];
};

const Analytics = () => {
  const [definitionInput, setDefinitionInput] = useState("");
  const [questionInput, setQuestionInput] = useState("");
  const [definitionSets, setDefinitionSets] = useState<DefinitionSet[]>([]);
  const [activeDefinitions, setActiveDefinitions] = useState<string[]>([]);
  const [savedCount, setSavedCount] = useState(0);

  const handleAddDefinition = () => {
    if (definitionInput.trim()) {
      setActiveDefinitions([...activeDefinitions, definitionInput.trim()]);
      setDefinitionInput("");
    }
  };

  const handleSaveDefinitionSet = () => {
    if (activeDefinitions.length === 0) return;
    const newSet: DefinitionSet = {
      id: savedCount + 1,
      label: `Definition Set ${savedCount + 1}`,
      definitions: [...activeDefinitions],
    };
    setDefinitionSets([...definitionSets, newSet]);
    setSavedCount(savedCount + 1);
    setActiveDefinitions([]);
  };

  const handleUseDefinitionSet = (set: DefinitionSet) => {
    setActiveDefinitions(set.definitions);
  };

  const handleClearSession = () => {
    setActiveDefinitions([]);
    setDefinitionSets([]);
    setSavedCount(0);
  };

  return (
    <div
      style={{
        display: "flex",
        height: "100vh",
        fontFamily: "sans-serif",
        background: "#1e1e1e",
        color: "#f5f5f5",
      }}
    >
      {/* LEFT PANEL - DEFINITIONS */}
      <div
        style={{
          width: "50%",
          padding: "30px",
          background: "#2c2c2c",
          borderRight: "1px solid #444",
          overflowY: "auto",
        }}
      >
        <h2 style={{ marginBottom: "20px" }}>🧾 Define Analytics</h2>

        <textarea
          value={definitionInput}
          onChange={(e) => setDefinitionInput(e.target.value)}
          rows={3}
          placeholder="e.g. superfast = 80% sold in 30 days"
          style={{
            width: "100%",
            padding: "10px",
            background: "#1e1e1e",
            color: "#f5f5f5",
            border: "1px solid #555",
            borderRadius: "4px",
            marginBottom: "10px",
          }}
        />
        <div style={{ marginBottom: "20px" }}>
          <button
            onClick={handleAddDefinition}
            style={{
              padding: "8px 16px",
              background: "#444",
              color: "#fff",
              border: "none",
              marginRight: "10px",
              borderRadius: "4px",
              cursor: "pointer",
            }}
          >
            ➕ Add Definition
          </button>
          <button
            onClick={handleSaveDefinitionSet}
            style={{
              padding: "8px 16px",
              background: "#007bff",
              color: "#fff",
              border: "none",
              marginRight: "10px",
              borderRadius: "4px",
              cursor: "pointer",
            }}
          >
            💾 Save Set
          </button>
          <button
            onClick={handleClearSession}
            style={{
              padding: "8px 16px",
              background: "#b00020",
              color: "#fff",
              border: "none",
              borderRadius: "4px",
              cursor: "pointer",
            }}
          >
            🔄 Clear Session
          </button>
        </div>

        <div>
          <h4>📌 Active Definitions</h4>
          <ul>
            {activeDefinitions.map((def, idx) => (
              <li key={idx}>{def}</li>
            ))}
          </ul>
        </div>

        <div style={{ marginTop: "30px" }}>
          <h4>🗂 Saved Templates</h4>
          {definitionSets.map((set) => (
            <div
              key={set.id}
              style={{
                background: "#333",
                padding: "10px",
                marginBottom: "10px",
                borderRadius: "4px",
              }}
            >
              <strong style={{ color: "#ddd" }}>{set.label}</strong>
              <ul>
                {set.definitions.map((def, idx) => (
                  <li key={idx} style={{ fontSize: "14px", color: "#bbb" }}>
                    {def}
                  </li>
                ))}
              </ul>
              <button
                onClick={() => handleUseDefinitionSet(set)}
                style={{
                  marginTop: "5px",
                  padding: "6px 12px",
                  background: "#555",
                  color: "#fff",
                  border: "none",
                  borderRadius: "4px",
                  cursor: "pointer",
                }}
              >
                Use This Set
              </button>
            </div>
          ))}
        </div>
      </div>

      {/* RIGHT PANEL - QUESTIONS */}
      <div style={{ width: "50%", padding: "30px", background: "#121212", overflowY: "auto" }}>
        <h2>🧠 Ask a Question</h2>
        <textarea
          value={questionInput}
          onChange={(e) => setQuestionInput(e.target.value)}
          rows={6}
          placeholder="e.g. What are the superfast items with good margin?"
          style={{
            width: "100%",
            padding: "10px",
            background: "#1e1e1e",
            color: "#f5f5f5",
            border: "1px solid #555",
            borderRadius: "4px",
          }}
        />
        <button
          style={{
            marginTop: "10px",
            padding: "10px 16px",
            background: "#009688",
            color: "#fff",
            border: "none",
            borderRadius: "4px",
            cursor: "pointer",
          }}
        >
          ▶️ Ask
        </button>

        <div style={{ marginTop: "30px" }}>
          <h4>🔍 Definitions in Use</h4>
          <ul>
            {activeDefinitions.map((def, idx) => (
              <li key={idx} style={{ color: "#ccc" }}>
                {def}
              </li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
};

export default Analytics;
