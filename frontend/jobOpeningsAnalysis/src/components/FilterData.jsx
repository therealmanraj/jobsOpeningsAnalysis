const FilterData = () => {
  return (
    <div className="filters">
      <div className="filterSection">
        <div>
          <ul className="filterList">
            <select name="cars" id="cars">
              <option value="2023">2023</option>
              <option value="2022">2022</option>
              <option value="2021">2021</option>
              <option value="2020">2020</option>
            </select>
            <button>Construstion</button>
            <button>Government</button>
            <button>Manufacturing</button>
          </ul>
        </div>
      </div>
    </div>
  );
};

export default FilterData;
