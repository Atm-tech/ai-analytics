import React from "react";

const UnresolvedModal = ({
  open,
  data,
  onClose,
}: {
  open: boolean;
  data: any[];
  onClose: () => void;
}) => {
  if (!open) return null;

  return (
    <div
      style={{
        position: "fixed",
        top: 0,
        left: 0,
        right: 0,
        bottom: 0,
        background: "rgba(0,0,0,0.5)",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        zIndex: 9999,
      }}
    >
      <div
        style={{
          background: "#fff",
          padding: "20px",
          width: "80%",
          maxHeight: "80%",
          overflow: "auto",
          borderRadius: "8px",
        }}
      >
        <h4>🚫 Unresolved Rows</h4>
        <table border={1} cellPadding={5} style={{ width: "100%", fontSize: "14px" }}>
          <thead>
            <tr>
              {data.length > 0 &&
                Object.keys(data[0]).map((key) => <th key={key}>{key}</th>)}
            </tr>
          </thead>
          <tbody>
            {data.map((row, idx) => (
              <tr key={idx}>
                {Object.values(row).map((value, i) => (
                  <td key={i}>{String(value)}</td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
        <br />
        <button onClick={onClose} style={{ padding: "8px 16px", background: "#333", color: "#fff" }}>
          Close
        </button>
      </div>
    </div>
  );
};

export default UnresolvedModal;
