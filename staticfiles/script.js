function updateTable() {
  fetch("/api/cardstats/")
    .then(response => response.json())
    .then(data => {
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
    })
    .catch(err => {
      console.error("Ошибка загрузки:", err);
      const tbody = document.querySelector("#stats-table tbody");
      tbody.innerHTML = `<tr><td colspan="5">Ошибка загрузки</td></tr>`;
    });
}

updateTable();                    // сразу при загрузке
setInterval(updateTable, 15000);  // и каждые 15 сек
