import React, { useState } from "react";
import axios from "axios";

const Upload = () => {
  const [file, setFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);
  const [activeTab, setActiveTab] = useState<"base" | "purchase" | "sales" | "closing">("base");

  const endpointMap: Record<typeof activeTab, string> = {
    base: "/api/upload/product",
    purchase: "/api/upload/purchase",
    sales: "/api/upload/sales",
    closing: "/api/upload/closing-stock",
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selected = e.target.files?.[0];
    if (selected && selected.name.endsWith(".xlsx")) {
      setFile(selected);
    } else {
      alert("Only .xlsx files allowed");
      setFile(null);
    }
  };

  const handleUpload = async () => {
    if (!file) return alert("Please select a valid .xlsx file");

    const formData = new FormData();
    formData.append("file", file);

    try {
      setUploading(true);
      const response = await axios.post(endpointMap[activeTab], formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      alert("? Upload successful!");
      console.log("Response:", response.data);
    } catch (error) {
      alert("? Upload failed");
      console.error(error);
    } finally {
      setUploading(false);
    }
  };

  return (
    <div style={{ padding: "20px" }}>
      <h3>Upload Files</h3>

      {/* Tabs */}
      <div style={{ display: "flex", gap: "10px", marginBottom: "20px" }}>
        {["base", "purchase", "sales", "closing"].map((tab) => (
          <button
            key={tab}
            onClick={() => setActiveTab(tab as typeof activeTab)}
            style={{
              padding: "8px 16px",
              background: activeTab === tab ? "#222" : "#ccc",
              color: activeTab === tab ? "#fff" : "#000",
              border: "none",
              borderRadius: "4px",
              cursor: "pointer",
            }}
          >
            {tab.charAt(0).toUpperCase() + tab.slice(1)}
          </button>
        ))}
      </div>

      {/* Upload Form */}
      <input type="file" accept=".xlsx" onChange={handleFileChange} />
      <div style={{ marginTop: "10px", color: "#555" }}>
        {file && <span>?? Selected: {file.name}</span>}
      </div>

      <br />
      <button onClick={handleUpload} disabled={uploading || !file} style={{ marginTop: "10px" }}>
        {uploading ? "Uploading..." : "Upload"}
      </button>
    </div>
  );
};

export default Upload;
