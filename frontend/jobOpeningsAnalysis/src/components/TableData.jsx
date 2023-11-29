import { useEffect, useState } from "react";
import { Grid } from "react-loader-spinner";

const TableData = () => {
  const [data, setData] = useState([]);
  //   const [message, setMessage] = useState("");

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const response = await fetch("http://127.0.0.1:4000/databaseGet");
      const result = await response.json();
      setData(result);
    } catch (error) {
      console.error("Error fetching data:", error);
    }
  };
  return (
    <div>
      {data.length > 0 ? (
        <div className="tableDiv">
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
            <tbody style={{ border: "10px solid white" }}>
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
        </div>
      ) : (
        <Grid
          height="80"
          width="80"
          color="white"
          ariaLabel="grid-loading"
          radius="12.5"
          wrapperStyle={{}}
          wrapperClass="gridLoader"
          visible={true}
        />
      )}
    </div>
  );
};

export default TableData;
