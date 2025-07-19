import React, { useEffect, useState } from "react";
import axios from "axios";
import { toast, ToastContainer } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";

interface SpeedTierResult {
  barcode: string;
  name: string;
  sold_pct: number;
  days_since_arrival: number;
  classification: string;
  potential: string | null;
  transfer_suggestion: string | null;
}

export default function SpeedTierAnalysis() {
  const [data, setData] = useState<SpeedTierResult[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    axios
      .get("/analyze/speed-tiers")
      .then((res) => {
        setData(res.data);
        if (res.data.length === 0) {
          toast.info("No product classification found yet.");
        }
      })
      .catch(() => toast.error("Failed to fetch speed tier analysis"))
      .finally(() => setLoading(false));
  }, []);

  return (
    <div style={{ padding: 24 }}>
      <h2>🧠 Speed Tier Analysis</h2>

      {loading && <p>Loading...</p>}

      {!loading && data.length === 0 && (
        <p style={{ color: "gray" }}>
          No classification data yet. Upload some purchase + sales files first.
        </p>
      )}

      {!loading && data.length > 0 && (
        <table style={{ width: "100%", marginTop: 16, borderCollapse: "collapse" }}>
          <thead>
            <tr>
              <th style={thStyle}>Barcode</th>
              <th style={thStyle}>Name</th>
              <th style={thStyle}>Sold %</th>
              <th style={thStyle}>Days Since Arrival</th>
              <th style={thStyle}>Classification</th>
              <th style={thStyle}>Potential</th>
              <th style={thStyle}>Transfer Suggestion</th>
            </tr>
          </thead>
          <tbody>
            {data.map((item, idx) => (
              <tr key={idx}>
                <td style={tdStyle}>{item.barcode}</td>
                <td style={tdStyle}>{item.name}</td>
                <td style={tdStyle}>{item.sold_pct}%</td>
                <td style={tdStyle}>{item.days_since_arrival}</td>
                <td style={tdStyle}>{item.classification}</td>
                <td style={tdStyle}>{item.potential || "-"}</td>
                <td style={{ ...tdStyle, color: item.transfer_suggestion ? "red" : "gray" }}>
                  {item.transfer_suggestion || "-"}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
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
