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
    let aVal = key === "winrate" ? (a.games > 0 ? a.wins / a.games : 0) : a[key];
    let bVal = key === "winrate" ? (b.games > 0 ? b.wins / b.games : 0) : b[key];
    return numeric
      ? (ascending ? aVal - bVal : bVal - aVal)
      : (ascending ? aVal.localeCompare(bVal) : bVal.localeCompare(aVal));
  });

  currentSort = { column: index, ascending };
  renderTable(sorted);

  document.querySelectorAll(".sort-arrow").forEach(el => el.textContent = "⇅");
  document.querySelectorAll("th").forEach(el => el.classList.remove("active"));

  const arrows = document.querySelectorAll(".sort-arrow");
  const ths = document.querySelectorAll("th");
  arrows[index].textContent = ascending ? "↑" : "↓";
  ths[index].classList.add("active");
}

function applyTheme(theme) {
  document.documentElement.classList.remove("light-theme", "dark-theme");
  document.documentElement.classList.add(`${theme}-theme`);
  localStorage.setItem("theme", theme);
  document.getElementById("theme-toggle").textContent = theme === "dark" ? "☀️" : "🌙";
}

function initTheme() {
  const saved = localStorage.getItem("theme");
  const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
  applyTheme(saved || (prefersDark ? "dark" : "light"));
}

document.addEventListener("DOMContentLoaded", () => {
  initTheme();
  document.getElementById("theme-toggle").addEventListener("click", () => {
    const isDark = document.documentElement.classList.contains("dark-theme");
    applyTheme(isDark ? "light" : "dark");
  });
});

updateTable();
setInterval(updateTable, 60000);