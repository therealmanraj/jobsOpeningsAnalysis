import "./App.css";
import FilterData from "./components/FilterData";
import TableData from "./components/tableData";

function App() {
  return (
    <div className="App">
      <h1>Job Openings Data</h1>
      <FilterData />
      <TableData />
    </div>
  );
}

export default App;
