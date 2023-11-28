import { Link } from "react-router-dom";

const Navbar = () => {
  return (
    <div style={{ display: "flex" }}>
      <div style={{ marginRight: "auto" }}>
        <p style={{ paddingLeft: "1vw" }}>Job Openings Data</p>
      </div>
      <div
        style={{
          display: "flex",
          width: "20vw",
          justifyContent: "space-evenly",
        }}
      >
        <p>
          <Link to="">Data</Link>
        </p>
        <p>
          <Link to="/visualizations">Visualizations</Link>
        </p>
      </div>
    </div>
  );
};

export default Navbar;
