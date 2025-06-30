import React, { useState } from "react";
import axios from "axios";

const Upload = () => {
  const [file, setFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);

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
      const response = await axios.post("/api/upload/closing-stock", formData, {
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
      <h3>Upload Closing Stock (.xlsx)</h3>
      <input type="file" accept=".xlsx" onChange={handleFileChange} />
      <br /><br />
      <button onClick={handleUpload} disabled={uploading || !file}>
        {uploading ? "Uploading..." : "Upload"}
      </button>
    </div>
  );
};

export default Upload;
