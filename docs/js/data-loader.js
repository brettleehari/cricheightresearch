/**
 * data-loader.js - Fetch and reconstruct dashboard data from column-oriented JSON.
 */
const DataLoader = (() => {
  let playerData = null;
  let temporalStats = null;
  let countryStats = null;
  let analysisStats = null;

  async function loadAll() {
    const [pRes, tRes, cRes, aRes] = await Promise.all([
      fetch('data/dashboard-data.json').then(r => r.json()),
      fetch('data/temporal-stats.json').then(r => r.json()),
      fetch('data/country-stats.json').then(r => r.json()),
      fetch('data/analysis-stats.json').then(r => r.json()),
    ]);
    playerData = pRes;
    temporalStats = tRes;
    countryStats = cRes;
    analysisStats = aRes;
    return { playerData, temporalStats, countryStats, analysisStats };
  }

  /** Reconstruct row i from column-oriented data. */
  function getRow(i) {
    return {
      player_id: playerData.player_id[i],
      full_name: playerData.full_name[i],
      country: playerData.country[i],
      category: playerData.category[i],
      batting_position: playerData.batting_position[i],
      birth_year: playerData.birth_year[i],
      height_cm: playerData.height_cm[i],
      height_verified: playerData.height_verified[i],
      pop_height: playerData.pop_height[i],
      height_excess: playerData.height_excess[i],
      tournament_id: playerData.tournament_id[i],
      format: playerData.format[i],
      tournament_year: playerData.tournament_year[i],
      era: playerData.era[i],
      region: playerData.region[i],
    };
  }

  function rowCount() {
    return playerData ? playerData.player_id.length : 0;
  }

  /** Get all rows matching filters. */
  function getFilteredRows(filters = {}) {
    const n = rowCount();
    const rows = [];
    for (let i = 0; i < n; i++) {
      if (filters.country && playerData.country[i] !== filters.country) continue;
      if (filters.category && playerData.category[i] !== filters.category) continue;
      if (filters.format && playerData.format[i] !== filters.format) continue;
      if (filters.search) {
        const s = filters.search.toLowerCase();
        if (!playerData.full_name[i].toLowerCase().includes(s)) continue;
      }
      rows.push(getRow(i));
    }
    return rows;
  }

  /** Get temporal stats filtered by format. */
  function getTemporalStats(format = 'ALL') {
    return temporalStats.filter(d => d.format === format);
  }

  /** Get country stats filtered by category. */
  function getCountryStats(category = 'ALL') {
    return countryStats.filter(d => d.category === category);
  }

  function getAnalysisStats() {
    return analysisStats;
  }

  return { loadAll, getRow, rowCount, getFilteredRows, getTemporalStats, getCountryStats, getAnalysisStats };
})();
