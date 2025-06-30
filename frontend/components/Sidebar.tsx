import React from "react";
import { Link } from "react-router-dom";

const Sidebar = () => {
  return (
    <div style={{ width: "200px", background: "#222", color: "#fff", height: "100vh", padding: "20px", boxSizing: "border-box" }}>
      <h3 style={{ marginBottom: "30px" }}>ISMS Panel</h3>
      <nav style={{ display: "flex", flexDirection: "column", gap: "10px" }}>
        <Link to="/" style={{ color: "#fff", textDecoration: "none" }}>Dashboard</Link>
        <Link to="/upload" style={{ color: "#fff", textDecoration: "none" }}>Upload Files</Link>
        <Link to="/analytics" style={{ color: "#fff", textDecoration: "none" }}>Analytics</Link>
      </nav>
    </div>
  );
};

export default Sidebar;
