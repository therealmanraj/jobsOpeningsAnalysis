import "./App.css";
import Navbar from "./components/Navbar";
import TableData from "./components/tableData";
import { BrowserRouter, Route, Routes } from "react-router-dom";

function App() {
  return (
    <div className="App">
      <BrowserRouter>
        <Navbar />
        <Routes>
          <Route path="/" element={<TableData />} />
          <Route path="/visualizations" element={<div>Viz</div>} />
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;
