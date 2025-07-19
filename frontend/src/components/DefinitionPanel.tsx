import React, { useState } from "react";

interface Props {
  definitions: string[];
  setDefinitions: React.Dispatch<React.SetStateAction<string[]>>;
}

export default function DefinitionPanel({ definitions, setDefinitions }: Props) {
  const [newDef, setNewDef] = useState("");

  const handleAdd = () => {
    if (!newDef.trim()) return;
    setDefinitions((prev) => [...prev, newDef.trim()]);
    setNewDef("");
  };

  const handleDelete = (index: number) => {
    setDefinitions((prev) => prev.filter((_, i) => i !== index));
  };

  return (
    <div>
      <input
        value={newDef}
        onChange={(e) => setNewDef(e.target.value)}
        placeholder="e.g. superfast = 80% sold in 30 days"
        style={{ width: "100%", padding: "6px", marginBottom: "6px" }}
      />
      <button onClick={handleAdd} style={{ padding: "6px 12px" }}>
        Add
      </button>

      <ul style={{ marginTop: 10 }}>
        {definitions.map((def, index) => (
          <li key={index} style={{ marginBottom: 6 }}>
            {def}
            <button
              onClick={() => handleDelete(index)}
              style={{
                marginLeft: 10,
                background: "red",
                color: "#fff",
                border: "none",
                padding: "2px 6px",
                borderRadius: 4,
              }}
            >
              ✕
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
}
