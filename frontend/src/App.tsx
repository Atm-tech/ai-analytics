import { BrowserRouter, Routes, Route } from "react-router-dom";
import Sidebar from "../components/Sidebar";
import Topbar from "../components/Topbar";
import Dashboard from "../pages/Dashboard";
import Upload from "../pages/Upload";
import Analytics from "../pages/analytics";  
const App = () => {
  return (
    <BrowserRouter>
      <div style={{ display: "flex" }}>
        <Sidebar />
        <div style={{ flex: 1 }}>
          <Topbar />
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/upload" element={<Upload />} />
            <Route path="/analytics" element={<Analytics />} />   
          </Routes>
        </div>
      </div>
    </BrowserRouter>
  );
};

export default App;
