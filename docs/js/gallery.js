/**
 * gallery.js - Figure gallery with lightbox and topic filtering.
 */
const Gallery = (() => {
  const FIGURES = [
    { file: 'fig1_category_distributions.png', caption: 'Fig 1: Height distributions by player category', topic: 'distribution' },
    { file: 'fig2_temporal_trends.png', caption: 'Fig 2: Temporal trends in player height', topic: 'temporal' },
    { file: 'fig3_country_comparison.png', caption: 'Fig 3: Country-wise height comparison', topic: 'country' },
    { file: 'fig4_era_boxplot.png', caption: 'Fig 4: Height distribution by era', topic: 'distribution' },
    { file: 'fig5_population_adjusted.png', caption: 'Fig 5: Population-adjusted height trends', topic: 'temporal' },
    { file: 'fig6_breakpoint.png', caption: 'Fig 6: Structural breakpoint analysis', topic: 'temporal' },
    { file: 'fig7_format_comparison.png', caption: 'Fig 7: ODI vs T20 format comparison', topic: 'comparison' },
    { file: 'fig8_main_figure.png', caption: 'Fig 8: Main composite figure', topic: 'other' },
    { file: 'fig9_country_bat_vs_population.png', caption: 'Fig 9: Country batsman height vs population', topic: 'country' },
    { file: 'fig10_country_bat_segmented.png', caption: 'Fig 10: Country batsman segmented trends', topic: 'country' },
    { file: 'fig11_country_fast_segmented.png', caption: 'Fig 11: Country fast bowler segmented trends', topic: 'country' },
    { file: 'fig12_height_arms_race.png', caption: 'Fig 12: Height arms race', topic: 'temporal' },
    { file: 'fig13_tallest_vs_shortest_xi.png', caption: 'Fig 13: Tallest vs shortest XIs', topic: 'comparison' },
    { file: 'fig14_batting_position_profile.png', caption: 'Fig 14: Batting position height profile', topic: 'distribution' },
    { file: 'fig15_fast_bat_gap.png', caption: 'Fig 15: Fast bowler - batsman height gap', topic: 'comparison' },
    { file: 'fig16_age_height_demographics.png', caption: 'Fig 16: Age and height demographics', topic: 'other' },
    { file: 'fig17_wicketkeeper_paradox.png', caption: 'Fig 17: Wicketkeeper height paradox', topic: 'comparison' },
    { file: 'fig18_team_height_diversity.png', caption: 'Fig 18: Team height diversity', topic: 'country' },
    { file: 'fig19_spin_vs_fast.png', caption: 'Fig 19: Spin vs fast bowler heights', topic: 'comparison' },
    { file: 'fig20_career_span_giants.png', caption: 'Fig 20: Career span of tallest players', topic: 'other' },
    { file: 'fig21_south_asian_catchup.png', caption: 'Fig 21: South Asian height catch-up', topic: 'country' },
    { file: 'fig22_ridgeline_decades.png', caption: 'Fig 22: Ridgeline plot by decade', topic: 'distribution' },
    { file: 'fig23_allrounder_effect.png', caption: 'Fig 23: All-rounder height effect', topic: 'comparison' },
    { file: 'fig24_team_silhouettes.png', caption: 'Fig 24: Team height silhouettes', topic: 'country' },
    { file: 'fig25_height_thresholds.png', caption: 'Fig 25: Height thresholds over time', topic: 'temporal' },
    { file: 'fig26_nation_clustering.png', caption: 'Fig 26: Nation height clustering', topic: 'country' },
    { file: 'fig27_data_quality_mosaic.png', caption: 'Fig 27: Data quality mosaic', topic: 'other' },
    { file: 'fig28_effect_size_dashboard.png', caption: 'Fig 28: Effect size dashboard', topic: 'other' },
    { file: 'fig29_height_inequality.png', caption: 'Fig 29: Height inequality measures', topic: 'distribution' },
    { file: 'fig30_generation_game.png', caption: 'Fig 30: Generation game', topic: 'temporal' },
    { file: 'fig31_team_composition.png', caption: 'Fig 31: Team composition by height', topic: 'country' },
    { file: 'fig32_outlier_gallery.png', caption: 'Fig 32: Outlier gallery', topic: 'other' },
  ];

  let visibleFigures = [...FIGURES];
  let lightboxIndex = -1;

  function init() {
    renderGrid();
    setupFilters();
    setupLightbox();
  }

  function renderGrid() {
    const grid = document.getElementById('gallery-grid');
    grid.innerHTML = visibleFigures.map((fig, i) => `
      <div class="gallery-item" data-index="${i}">
        <img src="figures/${fig.file}" alt="${fig.caption}" loading="lazy">
        <div class="gallery-caption">${fig.caption}</div>
      </div>
    `).join('');

    grid.querySelectorAll('.gallery-item').forEach(item => {
      item.addEventListener('click', () => {
        openLightbox(parseInt(item.dataset.index));
      });
    });
  }

  function setupFilters() {
    document.querySelectorAll('#gallery-filter button').forEach(btn => {
      btn.addEventListener('click', () => {
        document.querySelectorAll('#gallery-filter button').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        const topic = btn.dataset.topic;
        visibleFigures = topic === 'all' ? [...FIGURES] : FIGURES.filter(f => f.topic === topic);
        renderGrid();
      });
    });
  }

  function setupLightbox() {
    const lb = document.getElementById('lightbox');
    lb.querySelector('.lightbox-close').addEventListener('click', closeLightbox);
    lb.querySelector('.lightbox-prev').addEventListener('click', () => navigate(-1));
    lb.querySelector('.lightbox-next').addEventListener('click', () => navigate(1));

    lb.addEventListener('click', (e) => {
      if (e.target === lb) closeLightbox();
    });

    document.addEventListener('keydown', (e) => {
      if (!lb.classList.contains('open')) return;
      if (e.key === 'Escape') closeLightbox();
      if (e.key === 'ArrowLeft') navigate(-1);
      if (e.key === 'ArrowRight') navigate(1);
    });
  }

  function openLightbox(index) {
    lightboxIndex = index;
    const fig = visibleFigures[index];
    document.getElementById('lightbox-img').src = `figures/${fig.file}`;
    document.getElementById('lightbox-caption').textContent = fig.caption;
    document.getElementById('lightbox').classList.add('open');
    document.body.style.overflow = 'hidden';
  }

  function closeLightbox() {
    document.getElementById('lightbox').classList.remove('open');
    document.body.style.overflow = '';
  }

  function navigate(dir) {
    lightboxIndex = (lightboxIndex + dir + visibleFigures.length) % visibleFigures.length;
    const fig = visibleFigures[lightboxIndex];
    document.getElementById('lightbox-img').src = `figures/${fig.file}`;
    document.getElementById('lightbox-caption').textContent = fig.caption;
  }

  return { init };
})();
