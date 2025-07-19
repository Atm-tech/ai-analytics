import React, { useState } from "react";
import axios from "axios";

interface SkippedRow {
  barcode: string;
  grc_number: string;
  reason: string;
}

export default function UploadPanel() {
  const [file, setFile] = useState<File | null>(null);
  const [fileType, setFileType] = useState("purchase");
  const [uploading, setUploading] = useState(false);
  const [message, setMessage] = useState("");
  const [inserted, setInserted] = useState<number | null>(null);
  const [skipped, setSkipped] = useState<number | null>(null);
  const [updated, setUpdated] = useState<number | null>(null);
  const [skippedRows, setSkippedRows] = useState<SkippedRow[]>([]);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      setFile(e.target.files[0]);
    }
  };

  const handleUpload = async () => {
    if (!file) {
      setMessage("Please select a file.");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);
    formData.append("type", fileType);

    setUploading(true);
    setMessage("");
    setInserted(null);
    setSkipped(null);
    setUpdated(null);
    setSkippedRows([]);

    try {
      const res = await axios.post("http://localhost:8000/api/upload", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });

      const result = res.data.result || {};

      setInserted(result.inserted || 0);
      setSkipped(result.skipped || 0);
      setUpdated(result.updated_products || result.updated || 0); // compatible with both naming
      setSkippedRows(result.skipped_rows || []);

      setMessage(
        `${res.data.message || "Upload successful!"} — Inserted: ${result.inserted || 0}, Updated: ${
          result.updated_products || result.updated || 0
        }, Skipped: ${result.skipped || 0}`
      );
    } catch (err: any) {
      setMessage(err.response?.data?.detail || "Upload failed.");
    } finally {
      setUploading(false);
    }
  };

  return (
    <div style={containerStyle}>
      <h3>📤 Upload Data File</h3>

      <label style={{ fontWeight: "bold" }}>Select File Type: </label>
      <select value={fileType} onChange={(e) => setFileType(e.target.value)} style={{ marginLeft: 8 }}>
        <option value="base">Base File</option>
        <option value="purchase">Purchase File</option>
        <option value="sale">Sale File</option>
        <option value="stock">Closing Stock</option>
      </select>

      <div style={{ marginTop: 12 }}>
        <input type="file" accept=".xlsx" onChange={handleFileChange} />
      </div>

      <button
        onClick={handleUpload}
        disabled={uploading}
        style={buttonStyle(uploading)}
      >
        {uploading ? "Uploading..." : "Upload"}
      </button>

      {message && <p style={{ marginTop: 16, color: "#333" }}>{message}</p>}

      {(inserted !== null || skipped !== null || updated !== null) && (
        <div style={{ marginTop: 12 }}>
          <p><strong>Inserted:</strong> {inserted}</p>
          <p><strong>Updated:</strong> {updated}</p>
          <p><strong>Skipped:</strong> {skipped}</p>
        </div>
      )}

      {skippedRows.length > 0 && (
        <div style={{ marginTop: 20 }}>
          <h4>⛔ Skipped Rows</h4>
          <table style={tableStyle}>
            <thead>
              <tr>
                <th style={cellStyle}>Barcode</th>
                <th style={cellStyle}>GRC Number</th>
                <th style={cellStyle}>Reason</th>
              </tr>
            </thead>
            <tbody>
              {skippedRows.map((row, i) => (
                <tr key={i}>
                  <td style={cellStyle}>{row.barcode}</td>
                  <td style={cellStyle}>{row.grc_number}</td>
                  <td style={cellStyle}>{row.reason}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}

const containerStyle = {
  maxWidth: 800,
  margin: "20px auto",
  padding: 20,
  border: "1px solid #ccc",
  borderRadius: 8,
};

const buttonStyle = (disabled: boolean) => ({
  marginTop: 16,
  padding: "10px 18px",
  backgroundColor: "#007bff",
  color: "#fff",
  border: "none",
  borderRadius: 6,
  cursor: disabled ? "not-allowed" : "pointer",
});

const tableStyle = {
  width: "100%",
  borderCollapse: "collapse" as const,
  marginTop: 10,
};

const cellStyle = {
  border: "1px solid #ddd",
  padding: "8px",
  textAlign: "left" as const,
};
