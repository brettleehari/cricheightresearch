/**
 * app.js - Main initialization, navigation, and filter state management.
 */
(async function () {
  // Load all data
  const { playerData, temporalStats, countryStats, analysisStats } = await DataLoader.loadAll();
  const stats = DataLoader.getAnalysisStats();

  // === Stat Card Counter Animation ===
  document.querySelectorAll('.stat-card .stat-value').forEach(el => {
    const target = parseFloat(el.dataset.target);
    const decimals = parseInt(el.dataset.decimals || '0');
    const prefix = el.dataset.prefix || '';
    const suffix = el.dataset.suffix || '';
    animateCounter(el, target, decimals, prefix, suffix);
  });

  function animateCounter(el, target, decimals, prefix, suffix) {
    const duration = 1200;
    const start = performance.now();
    function tick(now) {
      const elapsed = now - start;
      const progress = Math.min(elapsed / duration, 1);
      const eased = 1 - Math.pow(1 - progress, 3);
      const value = target * eased;
      el.textContent = prefix + value.toFixed(decimals).replace(/\B(?=(\d{3})+(?!\d))/g, ',') + suffix;
      if (progress < 1) requestAnimationFrame(tick);
    }
    requestAnimationFrame(tick);
  }

  // === Abstract Tab Switching ===
  document.querySelectorAll('.abstract-tab').forEach(tab => {
    tab.addEventListener('click', () => {
      document.querySelectorAll('.abstract-tab').forEach(t => t.classList.remove('active'));
      tab.classList.add('active');
      const target = tab.dataset.tab;
      document.getElementById('abstract-fan').classList.toggle('hidden', target !== 'fan');
      document.getElementById('abstract-researcher').classList.toggle('hidden', target !== 'researcher');
    });
  });

  // === Section 2: Temporal Trends ===
  let activeCategories = ['ALL', 'BAT', 'FAST', 'SPIN', 'WK'];
  let activeFormat = 'ALL';

  function updateTemporalCharts() {
    const data = DataLoader.getTemporalStats(activeFormat);
    Charts.renderTemporalChart('chart-temporal', data, activeCategories);
    Charts.renderPopExcessChart('chart-pop-excess', data);
  }

  // Category chip toggles
  document.querySelectorAll('#temporal-filters .chip').forEach(chip => {
    chip.addEventListener('click', () => {
      const cat = chip.dataset.cat;
      if (cat === 'ALL') {
        // Toggle all
        const allActive = chip.classList.contains('active');
        document.querySelectorAll('#temporal-filters .chip').forEach(c => {
          c.classList.toggle('active', !allActive);
        });
        activeCategories = allActive ? [] : ['ALL', 'BAT', 'FAST', 'SPIN', 'WK'];
      } else {
        chip.classList.toggle('active');
        if (chip.classList.contains('active')) {
          activeCategories.push(cat);
        } else {
          activeCategories = activeCategories.filter(c => c !== cat && c !== 'ALL');
          document.querySelector('#temporal-filters .chip[data-cat="ALL"]').classList.remove('active');
        }
      }
      updateTemporalCharts();
    });
  });

  // Format filter
  document.getElementById('format-filter').addEventListener('change', (e) => {
    activeFormat = e.target.value;
    updateTemporalCharts();
  });

  updateTemporalCharts();

  // === Section 3: Category Comparison ===
  Charts.renderCategoryBar('chart-category-bar', stats);
  Charts.renderCategoryExcess('chart-category-excess', stats);

  // Era small multiples
  const allRows = [];
  const n = DataLoader.rowCount();
  for (let i = 0; i < n; i++) allRows.push(DataLoader.getRow(i));

  Charts.renderEraChart('chart-era1', allRows, 1);
  Charts.renderEraChart('chart-era2', allRows, 2);
  Charts.renderEraChart('chart-era3', allRows, 3);
  Charts.renderEraChart('chart-era4', allRows, 4);

  // === Section 4: Country Analysis ===
  function updateCountryCharts() {
    const cat = document.getElementById('country-cat-filter').value;
    const data = DataLoader.getCountryStats(cat);
    Charts.renderCountryBar('chart-country-bar', data);
  }

  document.getElementById('country-cat-filter').addEventListener('change', updateCountryCharts);
  updateCountryCharts();
  Charts.renderCountrySlope('chart-country-slope', stats);

  // === Section 5: Format Comparison ===
  Charts.renderFormatComparison('chart-format-comparison', stats);
  document.getElementById('odi-mean').textContent = stats.format_comparison.odi_mean.toFixed(1);
  document.getElementById('t20-mean').textContent = stats.format_comparison.t20_mean.toFixed(1);
  document.getElementById('format-d').textContent = Math.abs(stats.format_comparison.cohens_d).toFixed(4);

  // === Section 6: Player Table ===
  PlayerTable.init();
  PlayerTable.setData(allRows);

  // === Section 7: Gallery ===
  Gallery.init();

  // === Navigation active state ===
  const sections = document.querySelectorAll('section[id]');
  const navLinks = document.querySelectorAll('.nav-links a');

  function onScroll() {
    let current = '';
    sections.forEach(section => {
      const top = section.offsetTop - 80;
      if (window.scrollY >= top) current = section.id;
    });
    navLinks.forEach(link => {
      link.classList.toggle('active', link.getAttribute('href') === '#' + current);
    });
  }

  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  // Update breakpoint callout from stats
  const bp = stats.breakpoint_bat;
  if (bp) {
    const callout = document.getElementById('breakpoint-callout');
    callout.innerHTML = `<strong>Breakpoint detected at ${bp.best_breakpoint}:</strong> Batsman heights rose at +${bp.pre_slope.toFixed(2)} cm/year before ${bp.best_breakpoint}, slowing to +${bp.post_slope.toFixed(2)} cm/year after (Chow test <em>p</em> = ${bp.p_value < 0.001 ? '<.001' : bp.p_value.toFixed(3)}).`;
  }
})();
