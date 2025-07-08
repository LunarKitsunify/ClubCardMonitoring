let cardData = [];
let currentSort = { column: null, ascending: false };

function updateTable() {
  fetch("/api/cardstats/")
    .then(response => response.json())
    .then(data => {
      cardData = data.map(card => ({
        ...card,
        winrate: card.games > 0 ? card.wins / card.games : 0,
        played_wr: card.played_games > 0 ? card.played_wins / card.played_games : 0,
        seen_wr: card.seen_games > 0 ? card.seen_wins / card.seen_games : 0,
      }));

      if (currentSort.column !== null) {
        applySort(currentSort.column, currentSort.ascending);
      } else {
        renderTable(cardData);
      }
    })
    .catch(err => {
      console.error("Loading error:", err);
      const tbody = document.querySelector("#stats-table tbody");
      tbody.innerHTML = `<tr><td colspan="10">Loading error</td></tr>`;
    });
}

function renderTable(data) {
  const tbody = document.querySelector("#stats-table tbody");
  tbody.innerHTML = "";

  data.forEach(card => {
    const winrate = (card.winrate * 100).toFixed(1);
    const playedRate = card.played_games > 0 ? (card.played_wr * 100).toFixed(1) : "-";
    const seenRate = card.seen_games > 0 ? (card.seen_wr * 100).toFixed(1) : "-";

    const row = `<tr>
      <td>${card.name}</td>
      <td>${card.games}</td>
      <td>${card.wins}</td>
      <td>${winrate}</td>
      <td>${card.played_games ?? 0}</td>
      <td>${playedRate ?? 0}</td>
      <td>${card.seen_games ?? 0}</td>
      <td>${seenRate ?? 0}</td>
      <td>${card.score.toFixed(1) ?? 0}</td>
      <td>${card.impact.toFixed(2) ?? 0}</td>
    </tr>`;
    tbody.innerHTML += row;
  });
}

function sortByColumn(index, numeric = false) {
  const ascending =
    currentSort.column === index
      ? !currentSort.ascending
      : numeric
        ? false
        : true;

  currentSort = { column: index, ascending };
  applySort(index, ascending);
}

function applySort(index, ascending) {
  const columnMap = [
    "name", "games", "wins", "winrate",
    "played_games", "played_wr",
    "seen_games", "seen_wr", "score", "impact"
  ];
  const key = columnMap[index];

  const sorted = [...cardData].sort((a, b) => {
    const aVal = a[key];
    const bVal = b[key];
    return typeof aVal === "number"
      ? (ascending ? aVal - bVal : bVal - aVal)
      : (ascending ? aVal.localeCompare(bVal) : bVal.localeCompare(aVal));
  });

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