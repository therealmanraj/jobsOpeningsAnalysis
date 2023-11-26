import { useState, useEffect } from "react";
import "./App.css";

function App() {
  const [data, setData] = useState([]);
  const [message, setMessage] = useState("");

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const response = await fetch("http://127.0.0.1:4000/databaseGet");
      const result = await response.json();
      setData(result);
      console.log(result);
      setMessage("Data Received");
    } catch (error) {
      console.error("Error fetching data:", error);
      setMessage("Error fetching data");
    }
  };

  return (
    <div className="App">
      <h1>Job Openings Data</h1>
      <p>{message}</p>
      <div className="tableDiv">
        {data.length > 0 ? (
          <table>
            <thead>
              <tr>
                <th>Date</th>
                {Object.keys(data[0])
                  .filter((key) => key !== "Date") // Exclude 'Date' from keys
                  .map((key) => (
                    <th key={key}>{key}</th>
                  ))}
              </tr>
            </thead>
            <tbody>
              {data.map((row) => (
                <tr key={row.Date}>
                  <td>{row.Date}</td>
                  {Object.keys(row)
                    .filter((key) => key !== "Date")
                    .map((key) => (
                      <td key={key}>{row[key]}</td>
                    ))}
                </tr>
              ))}
            </tbody>
          </table>
        ) : (
          <p>No data available</p>
        )}
      </div>
    </div>
  );
}

export default App;
