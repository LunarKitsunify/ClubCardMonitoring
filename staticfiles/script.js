let cardData = [];
let currentSort = { column: null, ascending: false };

function updateTable() {
  fetch("/api/cardstats/")
    .then(response => response.json())
    .then(data => {
      cardData = data.map(card => ({
        ...card,
        winrate: card.games > 0 ? card.wins / card.games : 0,
        played_wr: card.played_count > 0 ? card.played_win / card.played_count : 0,
        seen_wr: card.seen_count > 0 ? card.seen_win / card.seen_count : 0,
      }));
      renderTable(cardData);
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
    const playedRate = card.played_count > 0 ? (card.played_wr * 100).toFixed(1) : "-";
    const seenRate = card.seen_count > 0 ? (card.seen_wr * 100).toFixed(1) : "-";

    const row = `<tr>
      <td>${card.name}</td>
      <td>${card.games}</td>
      <td>${card.wins}</td>
      <td>${winrate}</td>
      <td>${card.played_count ?? 0}</td>
      <td>${playedRate ?? 0}</td>
      <td>${card.seen_count ?? 0}</td>
      <td>${seenRate ?? 0}</td>
      <td>${card.score.toFixed(1) ?? 0}</td>
      <td>${card.impact.toFixed(2) ?? 0}</td>
    </tr>`;
    tbody.innerHTML += row;
  });
}

function sortByColumn(index, numeric = false) {
  const columnMap = [
    "name",         // 0
    "games",        // 1
    "wins",         // 2
    "winrate",      // 3
    "played_count", // 4
    "played_wr",    // 5
    "seen_count",   // 6
    "seen_wr",      // 7
    "score",        // 8
    "impact"        // 9
  ];

  let key = columnMap[index];
  let ascending = currentSort.column === index ? !currentSort.ascending : false;

  let sorted = [...cardData].sort((a, b) => {
    let aVal = a[key];
    let bVal = b[key];
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