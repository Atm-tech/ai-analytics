import React, { useState, useEffect } from "react";
import axios from "axios";
import { toast, ToastContainer } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";

// Define the tier structure
interface SpeedTier {
  name: string;
  percentage: number;
  days: number;
}

export default function SpeedTierConfig() {
  const [tiers, setTiers] = useState<SpeedTier[]>([]);
  const [loading, setLoading] = useState(true);

  // Fetch tiers from backend
  useEffect(() => {
    axios
      .get("/api/definitions/speed-tiers")
      .then((res) => {
        const data: SpeedTier[] = res.data;
        if (data.length === 0) {
          setTiers([{ name: "superfast", percentage: 80, days: 30 }]);
        } else {
          setTiers(data);
        }
      })
      .catch(() => toast.error("Failed to load speed tiers"))
      .finally(() => setLoading(false));
  }, []);

  // Handle field update
  const handleChange = (
    index: number,
    field: keyof SpeedTier,
    value: string
  ) => {
    const updated = [...tiers];
    const parsed = field === "percentage" || field === "days" ? parseFloat(value) : value;
    updated[index] = { ...updated[index], [field]: parsed } as SpeedTier;
    setTiers(updated);
  };

  // Add new row
  const addRow = () => {
    setTiers([...tiers, { name: "", percentage: 0, days: 0 }]);
  };

  // Delete row
  const deleteRow = (index: number) => {
    const updated = [...tiers];
    updated.splice(index, 1);
    setTiers(updated);
  };

  // Save to backend
  const saveTiers = () => {
    const invalid = tiers.some(
      (t) =>
        !t.name.trim() ||
        isNaN(t.percentage) || t.percentage < 0 ||
        isNaN(t.days) || t.days <= 0
    );

    if (invalid) {
      toast.error("All fields must be valid. % sold ≥ 0 and days > 0.");
      return;
    }

    axios
      .post("/api/definitions/speed-tiers", { tiers })
      .then(() => toast.success("Speed tiers saved"))
      .catch(() => toast.error("Failed to save tiers"));
  };

  return (
    <div style={{ padding: 24 }}>
      <h2>⚙️ Speed Tier Configuration</h2>

      {loading && <p>Loading...</p>}

      {!loading && (
        <>
          <table style={{ width: "100%", marginTop: 16, borderCollapse: "collapse" }}>
            <thead>
              <tr>
                <th style={thStyle}>Tier Name</th>
                <th style={thStyle}>% Sold</th>
                <th style={thStyle}>Days</th>
                <th style={thStyle}></th>
              </tr>
            </thead>
            <tbody>
              {tiers.map((tier, index) => (
                <tr key={index}>
                  <td style={tdStyle}>
                    <input
                      type="text"
                      value={tier.name}
                      onChange={(e) => handleChange(index, "name", e.target.value)}
                      required
                    />
                  </td>
                  <td style={tdStyle}>
                    <input
                      type="number"
                      min={0}
                      value={tier.percentage}
                      onChange={(e) => handleChange(index, "percentage", e.target.value)}
                      required
                    />
                  </td>
                  <td style={tdStyle}>
                    <input
                      type="number"
                      min={1}
                      value={tier.days}
                      onChange={(e) => handleChange(index, "days", e.target.value)}
                      required
                    />
                  </td>
                  <td style={tdStyle}>
                    <button onClick={() => deleteRow(index)}>❌</button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>

          <div style={{ marginTop: 16 }}>
            <button onClick={addRow}>➕ Add Tier</button>
            <button onClick={saveTiers} style={{ marginLeft: 10 }}>💾 Save</button>
          </div>
        </>
      )}

      <ToastContainer position="bottom-right" />
    </div>
  );
}

const thStyle: React.CSSProperties = {
  borderBottom: "1px solid #ccc",
  padding: "8px",
  textAlign: "left",
  backgroundColor: "#f9f9f9",
};

const tdStyle: React.CSSProperties = {
  padding: "8px",
  borderBottom: "1px solid #eee",
};
