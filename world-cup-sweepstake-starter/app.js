async function loadData() {
  const state = await fetch('data/state.json?cache=' + Date.now()).then(r => r.json());
  renderLeaderboard(state.leaderboard || []);
  renderMatches(state.matches || []);
  renderEvents(state.events || []);
  renderInsights(state.insights || {});
  document.getElementById('updated').innerText = state.last_updated
    ? `Last updated: ${new Date(state.last_updated).toLocaleString()}`
    : 'Waiting for first update';
}

function renderLeaderboard(rows) {
  const el = document.getElementById('leaderboard');
  el.innerHTML = rows.map(row => `
    <tr>
      <td class="rank">${row.rank}</td>
      <td>${row.name}</td>
      <td>${(row.teams || []).join(', ')}</td>
      <td class="points">${row.points}</td>
    </tr>
  `).join('');
}

function renderMatches(matches) {
  const el = document.getElementById('matches');
  el.innerHTML = matches.slice(-8).reverse().map(m => `
    <div class="match"><strong>${m.team1} ${m.score1}-${m.score2} ${m.team2}</strong><br><small>${m.status || ''}</small></div>
  `).join('') || '<p>No matches yet.</p>';
}

function renderEvents(events) {
  const el = document.getElementById('events');
  el.innerHTML = events.slice(-12).reverse().map(e => `
    <div class="event">${e.text}<br><small>${e.stage || ''}</small></div>
  `).join('') || '<p>No events yet.</p>';
}

function renderInsights(insights) {
  const el = document.getElementById('insights');
  el.innerHTML = `
    <div class="insight"><strong>Leader:</strong> ${insights.leader || '-'}</div>
    <div class="insight"><strong>Wooden spoon:</strong> ${insights.wooden_spoon || '-'}</div>
    <div class="insight"><strong>Top scoring nation:</strong> ${(insights.top_scoring_teams || []).join(', ') || '-'}</div>
  `;
}

loadData();
setInterval(loadData, 30000);
