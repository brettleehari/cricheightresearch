/**
 * table.js - Player explorer table with search, filter, sort, and pagination.
 */
const PlayerTable = (() => {
  const PAGE_SIZE = 25;
  let allRows = [];
  let filteredRows = [];
  let sortCol = 'height_cm';
  let sortDir = 'desc';
  let currentPage = 0;

  function init() {
    // Header sort handlers
    document.querySelectorAll('#player-table th').forEach(th => {
      th.addEventListener('click', () => {
        const col = th.dataset.col;
        if (sortCol === col) {
          sortDir = sortDir === 'asc' ? 'desc' : 'asc';
        } else {
          sortCol = col;
          sortDir = th.dataset.type === 'num' ? 'desc' : 'asc';
        }
        updateSortIndicators();
        sortAndRender();
      });
    });

    // Filter handlers
    document.getElementById('table-search').addEventListener('input', applyFilters);
    document.getElementById('table-country').addEventListener('change', applyFilters);
    document.getElementById('table-category').addEventListener('change', applyFilters);
    document.getElementById('table-format').addEventListener('change', applyFilters);
  }

  function setData(rows) {
    allRows = rows;
    applyFilters();
  }

  function applyFilters() {
    const search = document.getElementById('table-search').value.toLowerCase();
    const country = document.getElementById('table-country').value;
    const category = document.getElementById('table-category').value;
    const format = document.getElementById('table-format').value;

    filteredRows = allRows.filter(r => {
      if (search && !r.full_name.toLowerCase().includes(search)) return false;
      if (country && r.country !== country) return false;
      if (category && r.category !== category) return false;
      if (format && r.format !== format) return false;
      return true;
    });

    currentPage = 0;
    sortAndRender();
  }

  function sortAndRender() {
    const isNum = ['height_cm', 'height_excess', 'tournament_year', 'batting_position'].includes(sortCol);
    filteredRows.sort((a, b) => {
      let va = a[sortCol], vb = b[sortCol];
      if (isNum) { va = Number(va); vb = Number(vb); }
      else { va = String(va).toLowerCase(); vb = String(vb).toLowerCase(); }
      if (va < vb) return sortDir === 'asc' ? -1 : 1;
      if (va > vb) return sortDir === 'asc' ? 1 : -1;
      return 0;
    });
    renderPage();
  }

  function updateSortIndicators() {
    document.querySelectorAll('#player-table th').forEach(th => {
      th.classList.remove('sort-asc', 'sort-desc');
      if (th.dataset.col === sortCol) {
        th.classList.add(sortDir === 'asc' ? 'sort-asc' : 'sort-desc');
      }
    });
  }

  function renderPage() {
    const tbody = document.getElementById('table-body');
    const start = currentPage * PAGE_SIZE;
    const end = Math.min(start + PAGE_SIZE, filteredRows.length);
    const pageRows = filteredRows.slice(start, end);

    tbody.innerHTML = pageRows.map(r => `
      <tr>
        <td>${escHtml(r.full_name)}</td>
        <td>${r.country}</td>
        <td><span class="cat-badge ${r.category}">${r.category}</span></td>
        <td>${r.height_cm.toFixed(1)}</td>
        <td style="color:${r.height_excess >= 0 ? 'var(--fast)' : 'var(--bat)'}">
          ${r.height_excess >= 0 ? '+' : ''}${r.height_excess.toFixed(1)}
        </td>
        <td>${r.tournament_id}</td>
        <td>${r.tournament_year}</td>
        <td>${r.format}</td>
      </tr>
    `).join('');

    document.getElementById('table-info').textContent =
      `Showing ${start + 1}\u2013${end} of ${filteredRows.length} records`;

    renderPagination();
    updateSortIndicators();
  }

  function renderPagination() {
    const totalPages = Math.ceil(filteredRows.length / PAGE_SIZE);
    const container = document.getElementById('table-pagination');
    if (totalPages <= 1) { container.innerHTML = ''; return; }

    let html = `<button ${currentPage === 0 ? 'disabled' : ''} data-page="${currentPage - 1}">&laquo; Prev</button>`;

    const maxVisible = 7;
    let startPage = Math.max(0, currentPage - 3);
    let endPage = Math.min(totalPages, startPage + maxVisible);
    if (endPage - startPage < maxVisible) startPage = Math.max(0, endPage - maxVisible);

    if (startPage > 0) html += `<button data-page="0">1</button><span>...</span>`;
    for (let i = startPage; i < endPage; i++) {
      html += `<button data-page="${i}" class="${i === currentPage ? 'active' : ''}">${i + 1}</button>`;
    }
    if (endPage < totalPages) html += `<span>...</span><button data-page="${totalPages - 1}">${totalPages}</button>`;

    html += `<button ${currentPage >= totalPages - 1 ? 'disabled' : ''} data-page="${currentPage + 1}">Next &raquo;</button>`;
    container.innerHTML = html;

    container.querySelectorAll('button[data-page]').forEach(btn => {
      btn.addEventListener('click', () => {
        currentPage = parseInt(btn.dataset.page);
        renderPage();
      });
    });
  }

  function escHtml(s) {
    const d = document.createElement('div');
    d.textContent = s;
    return d.innerHTML;
  }

  return { init, setData };
})();
