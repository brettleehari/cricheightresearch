/**
 * charts.js - All Chart.js chart definitions.
 */
const Charts = (() => {
  const CAT_COLORS = {
    ALL: '#333',
    BAT: '#0072B2',
    FAST: '#D55E00',
    SPIN: '#009E73',
    WK: '#E69F00',
  };

  const COUNTRY_COLORS = {
    AUS: '#FFD700',
    ENG: '#003399',
    IND: '#FF9933',
    NZL: '#000000',
    PAK: '#006400',
    RSA: '#007749',
    SL: '#0000CD',
    WI: '#800020',
  };

  const chartInstances = {};

  function destroyChart(id) {
    if (chartInstances[id]) {
      chartInstances[id].destroy();
      delete chartInstances[id];
    }
  }

  /** Section 2: Temporal trend lines by category */
  function renderTemporalChart(canvasId, data, activeCategories) {
    destroyChart(canvasId);
    const cats = ['BAT', 'FAST', 'SPIN', 'WK'];
    const datasets = cats
      .filter(c => activeCategories.includes(c) || activeCategories.includes('ALL'))
      .map(cat => {
        const catData = data.filter(d => d.category === cat);
        return {
          label: cat,
          data: catData.map(d => ({ x: d.year, y: d.mean_height })),
          borderColor: CAT_COLORS[cat],
          backgroundColor: CAT_COLORS[cat] + '20',
          borderWidth: 2.5,
          pointRadius: 4,
          pointHoverRadius: 6,
          tension: 0.3,
        };
      });

    chartInstances[canvasId] = new Chart(document.getElementById(canvasId), {
      type: 'line',
      data: { datasets },
      options: {
        responsive: true,
        maintainAspectRatio: true,
        plugins: {
          title: { display: true, text: 'Mean Height by Category Over Time', font: { size: 14 } },
          legend: { position: 'bottom' },
          tooltip: {
            callbacks: {
              label: ctx => `${ctx.dataset.label}: ${ctx.parsed.y.toFixed(1)} cm (n=${data.find(d => d.category === ctx.dataset.label && d.year === ctx.parsed.x)?.count || '?'})`,
            },
          },
        },
        scales: {
          x: { type: 'linear', title: { display: true, text: 'Tournament Year' }, min: 1975, max: 2026, ticks: { stepSize: 5 } },
          y: { title: { display: true, text: 'Mean Height (cm)' }, min: 170, max: 192 },
        },
      },
    });
  }

  /** Section 2: Population excess chart */
  function renderPopExcessChart(canvasId, data) {
    destroyChart(canvasId);
    const batData = data.filter(d => d.category === 'BAT');
    const years = batData.map(d => d.year);

    chartInstances[canvasId] = new Chart(document.getElementById(canvasId), {
      type: 'line',
      data: {
        labels: years,
        datasets: [
          {
            label: 'BAT Mean Height',
            data: batData.map(d => d.mean_height),
            borderColor: CAT_COLORS.BAT,
            backgroundColor: CAT_COLORS.BAT + '15',
            borderWidth: 2.5,
            fill: false,
            pointRadius: 4,
            tension: 0.3,
          },
          {
            label: 'Population Baseline',
            data: batData.map(d => d.mean_pop),
            borderColor: '#999',
            borderDash: [5, 5],
            borderWidth: 2,
            fill: false,
            pointRadius: 3,
            tension: 0.3,
          },
          {
            label: 'Population Excess',
            data: batData.map(d => d.mean_height - d.mean_pop),
            borderColor: CAT_COLORS.BAT,
            backgroundColor: CAT_COLORS.BAT + '30',
            borderWidth: 1.5,
            fill: true,
            pointRadius: 3,
            tension: 0.3,
            yAxisID: 'y1',
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: true,
        plugins: {
          title: { display: true, text: 'Batsman Height vs Population Baseline', font: { size: 14 } },
          legend: { position: 'bottom' },
        },
        scales: {
          x: { title: { display: true, text: 'Tournament Year' } },
          y: { position: 'left', title: { display: true, text: 'Height (cm)' }, min: 168, max: 186 },
          y1: { position: 'right', title: { display: true, text: 'Excess (cm)' }, min: 0, max: 15, grid: { drawOnChartArea: false } },
        },
      },
    });
  }

  /** Section 3: Category bar charts */
  function renderCategoryBar(canvasId, stats) {
    destroyChart(canvasId);
    const cats = ['BAT', 'FAST', 'SPIN', 'WK'];
    chartInstances[canvasId] = new Chart(document.getElementById(canvasId), {
      type: 'bar',
      data: {
        labels: cats,
        datasets: [{
          label: 'Mean Height (cm)',
          data: cats.map(c => stats.category_means[c]),
          backgroundColor: cats.map(c => CAT_COLORS[c]),
          borderRadius: 4,
        }],
      },
      options: {
        responsive: true,
        maintainAspectRatio: true,
        plugins: {
          title: { display: true, text: 'Mean Height by Category', font: { size: 14 } },
          legend: { display: false },
          tooltip: {
            callbacks: {
              label: ctx => `${ctx.parsed.y.toFixed(1)} cm (n=${stats.category_counts[cats[ctx.dataIndex]]})`,
            },
          },
        },
        scales: {
          y: { min: 170, title: { display: true, text: 'Height (cm)' } },
        },
      },
    });
  }

  /** Section 3: Category excess bar */
  function renderCategoryExcess(canvasId, stats) {
    destroyChart(canvasId);
    const cats = ['BAT', 'FAST', 'SPIN', 'WK'];
    chartInstances[canvasId] = new Chart(document.getElementById(canvasId), {
      type: 'bar',
      data: {
        labels: cats,
        datasets: [{
          label: 'Mean Population Excess (cm)',
          data: cats.map(c => stats.category_excess[c]),
          backgroundColor: cats.map(c => CAT_COLORS[c] + 'CC'),
          borderColor: cats.map(c => CAT_COLORS[c]),
          borderWidth: 1,
          borderRadius: 4,
        }],
      },
      options: {
        responsive: true,
        maintainAspectRatio: true,
        plugins: {
          title: { display: true, text: 'Population Excess by Category', font: { size: 14 } },
          legend: { display: false },
          tooltip: {
            callbacks: {
              label: ctx => `+${ctx.parsed.y.toFixed(1)} cm above population`,
            },
          },
        },
        scales: {
          y: { min: 0, title: { display: true, text: 'Excess (cm)' } },
        },
      },
    });
  }

  /** Section 3: Era small multiples */
  function renderEraChart(canvasId, data, era) {
    destroyChart(canvasId);
    const eraData = data.filter(d => d.era === era);
    const cats = ['BAT', 'FAST', 'SPIN', 'WK'];
    const means = {};
    const counts = {};
    cats.forEach(c => { means[c] = []; counts[c] = 0; });
    eraData.forEach(r => {
      if (cats.includes(r.category)) {
        means[r.category].push(r.height_cm);
        counts[r.category]++;
      }
    });
    const avgData = cats.map(c => means[c].length ? (means[c].reduce((a, b) => a + b, 0) / means[c].length) : 0);

    chartInstances[canvasId] = new Chart(document.getElementById(canvasId), {
      type: 'bar',
      data: {
        labels: cats,
        datasets: [{
          data: avgData,
          backgroundColor: cats.map(c => CAT_COLORS[c]),
          borderRadius: 3,
        }],
      },
      options: {
        responsive: true,
        maintainAspectRatio: true,
        plugins: { legend: { display: false }, tooltip: { callbacks: { label: ctx => `${ctx.parsed.y.toFixed(1)} cm` } } },
        scales: {
          y: { min: 170, max: 190, ticks: { font: { size: 10 } } },
          x: { ticks: { font: { size: 10 } } },
        },
      },
    });
  }

  /** Section 4: Country horizontal bar */
  function renderCountryBar(canvasId, data) {
    destroyChart(canvasId);
    const sorted = [...data].sort((a, b) => b.mean_height - a.mean_height);
    const labels = sorted.map(d => d.country);
    chartInstances[canvasId] = new Chart(document.getElementById(canvasId), {
      type: 'bar',
      data: {
        labels,
        datasets: [{
          label: 'Mean Height (cm)',
          data: sorted.map(d => d.mean_height),
          backgroundColor: labels.map(c => COUNTRY_COLORS[c] || '#666'),
          borderRadius: 4,
        }],
      },
      options: {
        indexAxis: 'y',
        responsive: true,
        maintainAspectRatio: true,
        plugins: {
          title: { display: true, text: 'Mean Height by Country', font: { size: 14 } },
          legend: { display: false },
          tooltip: {
            callbacks: {
              label: ctx => `${ctx.parsed.x.toFixed(1)} cm (n=${sorted[ctx.dataIndex].count})`,
            },
          },
        },
        scales: {
          x: { min: 172, title: { display: true, text: 'Height (cm)' } },
        },
      },
    });
  }

  /** Section 4: Country slope chart */
  function renderCountrySlope(canvasId, stats) {
    destroyChart(canvasId);
    const countries = Object.keys(stats.country_slopes).sort(
      (a, b) => stats.country_slopes[b].slope - stats.country_slopes[a].slope
    );
    const slopes = countries.map(c => stats.country_slopes[c].slope);
    const colors = countries.map(c => {
      const p = stats.country_slopes[c].p_value;
      return p < 0.05 ? (COUNTRY_COLORS[c] || '#666') : '#ccc';
    });

    chartInstances[canvasId] = new Chart(document.getElementById(canvasId), {
      type: 'bar',
      data: {
        labels: countries,
        datasets: [{
          label: 'Height Trend (cm/year)',
          data: slopes,
          backgroundColor: colors,
          borderRadius: 4,
        }],
      },
      options: {
        indexAxis: 'y',
        responsive: true,
        maintainAspectRatio: true,
        plugins: {
          title: { display: true, text: 'Height Trend Slope by Country (cm/year)', font: { size: 14 } },
          legend: { display: false },
          tooltip: {
            callbacks: {
              label: ctx => {
                const c = countries[ctx.dataIndex];
                const s = stats.country_slopes[c];
                return `${s.slope > 0 ? '+' : ''}${s.slope.toFixed(4)} cm/yr (p=${s.p_value < 0.001 ? '<.001' : s.p_value.toFixed(3)})`;
              },
            },
          },
        },
        scales: {
          x: { title: { display: true, text: 'Slope (cm/year)' } },
        },
      },
    });
  }

  /** Section 5: Format comparison */
  function renderFormatComparison(canvasId, stats) {
    destroyChart(canvasId);
    const cats = ['BAT', 'FAST', 'SPIN', 'WK'];
    // We'll show ODI vs T20 for the overlapping period
    chartInstances[canvasId] = new Chart(document.getElementById(canvasId), {
      type: 'bar',
      data: {
        labels: ['ODI', 'T20'],
        datasets: [{
          label: 'Mean Height (cm)',
          data: [stats.format_comparison.odi_mean, stats.format_comparison.t20_mean],
          backgroundColor: ['#0072B2', '#D55E00'],
          borderRadius: 4,
        }],
      },
      options: {
        responsive: true,
        maintainAspectRatio: true,
        plugins: {
          title: { display: true, text: 'Mean Height: ODI vs T20 (Overlapping Years)', font: { size: 14 } },
          legend: { display: false },
          tooltip: {
            callbacks: {
              label: ctx => {
                const n = ctx.dataIndex === 0 ? stats.format_comparison.odi_n : stats.format_comparison.t20_n;
                return `${ctx.parsed.y.toFixed(1)} cm (n=${n})`;
              },
            },
          },
        },
        scales: {
          y: { min: 178, max: 184, title: { display: true, text: 'Height (cm)' } },
        },
      },
    });
  }

  return {
    renderTemporalChart,
    renderPopExcessChart,
    renderCategoryBar,
    renderCategoryExcess,
    renderEraChart,
    renderCountryBar,
    renderCountrySlope,
    renderFormatComparison,
    CAT_COLORS,
    COUNTRY_COLORS,
  };
})();
