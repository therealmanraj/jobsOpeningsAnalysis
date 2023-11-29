import "./App.css";
import DataView from "./components/DataView";
import Navbar from "./components/Navbar";
import { BrowserRouter, Route, Routes } from "react-router-dom";

function App() {
  return (
    <div className="App">
      <BrowserRouter>
        <Navbar />
        <Routes>
          <Route path="/" element={<DataView />} />
          <Route path="/visualizations" element={<div>Viz</div>} />
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;
