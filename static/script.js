let cardData = [];
let currentSort = { column: null, ascending: false };

function updateTable() {
  fetch("/api/cardstats/")
    .then(response => response.json())
    .then(data => {
      cardData = data;
      renderTable(cardData);
    })
    .catch(err => {
      console.error("Loading error:", err);
      const tbody = document.querySelector("#stats-table tbody");
      tbody.innerHTML = `<tr><td colspan="6">Loading error</td></tr>`;
    });
}

function renderTable(data) {
  const tbody = document.querySelector("#stats-table tbody");
  tbody.innerHTML = "";

  data.forEach(card => {
    const winrate = card.games > 0 ? ((card.wins / card.games) * 100).toFixed(1) : "0.0";
    const row = `<tr>
      <td>${card.name}</td>
      <td>${card.games}</td>
      <td>${card.wins}</td>
      <td>${winrate}</td>
      <td>${card.score.toFixed(1)}</td>
      <td>${card.impact.toFixed(2)}</td>
    </tr>`;
    tbody.innerHTML += row;
  });
}

function sortByColumn(index, numeric = false) {
  const columnMap = ["name", "games", "wins", "winrate", "score", "impact"];

  let key = columnMap[index];
  let ascending = currentSort.column === index ? !currentSort.ascending : false;

  let sorted = [...cardData].sort((a, b) => {
    let aVal, bVal;
    if (key === "winrate") {
      aVal = a.games > 0 ? a.wins / a.games : 0;
      bVal = b.games > 0 ? b.wins / b.games : 0;
    } else {
      aVal = a[key];
      bVal = b[key];
    }

    if (numeric) {
      return ascending ? aVal - bVal : bVal - aVal;
    } else {
      return ascending ? aVal.localeCompare(bVal) : bVal.localeCompare(aVal);
    }
  });

  currentSort = { column: index, ascending };
  renderTable(sorted);

  // Обновляем стрелки и стили
  document.querySelectorAll(".sort-arrow").forEach(el => el.textContent = "⇅");
  document.querySelectorAll("th").forEach(el => el.classList.remove("active"));

  const arrows = document.querySelectorAll(".sort-arrow");
  const ths = document.querySelectorAll("th");

  arrows[index].textContent = ascending ? "↑" : "↓";
  ths[index].classList.add("active");
}

updateTable();
setInterval(updateTable, 60000);