const fetchCatData = () => {
  const url = "/cat/";
  return fetch(url)
    .then((response) => response.json())
    .then((data) => {
      console.log(data);
      return data;
    });
};

const addCatToTable = (cat) => {
  var table = document.getElementById("cat-data-table");
  var row = table.insertRow(-1);
  const props = ["id", "name", "kind", "age", "sex", "favorite_foods", "owner"];
  for (const prop of props) {
    var cell = row.insertCell(-1);
    cell.innerHTML = cat[prop];
  }
};

const clearTable = () => {
  var table = document.getElementById("cat-data-table");
  while (table.rows.length > 1) {
    table.deleteRow(-1);
  }
};

const updateTable = (cats) => {
  clearTable();
  for (const cat of cats) {
    addCatToTable(cat);
  }
};

fetchCatData().then((cats) => updateTable(cats));
