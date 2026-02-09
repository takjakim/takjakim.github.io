(() => {
  // ===== Publications sort =====
  const pubList = document.getElementById('pub-list');
  const sortButtons = document.querySelectorAll('.pub-controls .pub-sort-btn[data-sort]');

  function setActive(btns, activeBtn) {
    btns.forEach((b) => b.classList.toggle('is-active', b === activeBtn));
  }

  function sortPublications(mode) {
    if (!pubList) return;
    const items = Array.from(pubList.querySelectorAll('li'));

    const score = (li) => {
      const cites = Number(li.dataset.cites || '0');
      const year = Number(li.dataset.year || '0');
      if (mode === 'recent') return year * 1_000_000 + cites; // recent, then cites
      return cites * 1_000_000 + year; // cites, then recent-ish
    };

    items
      .sort((a, b) => score(b) - score(a))
      .forEach((li) => pubList.appendChild(li));
  }

  sortButtons.forEach((btn) => {
    btn.addEventListener('click', () => {
      setActive(sortButtons, btn);
      sortPublications(btn.dataset.sort);
    });
  });

  // ===== Scholar citations chart =====
  const scopeButtons = document.querySelectorAll('.pub-controls .pub-sort-btn[data-scope]');
  const citesTotal = document.getElementById('cites-total');
  const citesH = document.getElementById('cites-hindex');
  const citesI10 = document.getElementById('cites-i10');
  const chartEl = document.getElementById('cites-chart');
  const chartEmpty = document.getElementById('cites-chart-empty');

  function svgBarChart(points) {
    // points: [{year, count}]
    const w = 860;
    const h = 180;
    const padX = 18;
    const padY = 22;

    const max = Math.max(1, ...points.map((p) => p.count));
    const barW = (w - padX * 2) / points.length;

    const y = (v) => padY + (h - padY * 2) * (1 - v / max);
    const barH = (v) => (h - padY * 2) * (v / max);

    const bars = points
      .map((p, i) => {
        const x = padX + i * barW + barW * 0.15;
        const bw = barW * 0.7;
        const yy = y(p.count);
        const hh = barH(p.count);
        return `
  <g>
    <rect x="${x.toFixed(2)}" y="${yy.toFixed(2)}" width="${bw.toFixed(2)}" height="${hh.toFixed(2)}" rx="8" fill="url(#citesGrad)" opacity="0.9" />
    <text x="${(x + bw / 2).toFixed(2)}" y="${(h - 6).toFixed(2)}" text-anchor="middle" font-size="11" fill="#6b7280">${p.year}</text>
  </g>`;
      })
      .join('');

    return `
<svg viewBox="0 0 ${w} ${h}" width="100%" height="${h}" role="img" aria-label="Citations per year">
  <defs>
    <linearGradient id="citesGrad" x1="0" x2="1" y1="0" y2="0">
      <stop offset="0%" stop-color="#ff6b6b"/>
      <stop offset="100%" stop-color="#4ecdc4"/>
    </linearGradient>
  </defs>
  <rect x="0" y="0" width="${w}" height="${h}" fill="rgba(0,0,0,0.02)" rx="14" />
  ${bars}
</svg>
`.trim();
  }

  async function loadScholarData() {
    const base = document.documentElement.getAttribute('data-baseurl') || '';
    const res = await fetch(`${base}/assets/data/scholar-metrics.json`, { cache: 'no-store' });
    if (!res.ok) throw new Error('failed to load scholar data');
    return res.json();
  }

  function renderScholar(data, scope) {
    const s = data.scopes?.[scope];
    if (!s) return;

    if (citesTotal) citesTotal.textContent = String(s.citations ?? '–');
    if (citesH) citesH.textContent = String(s.hIndex ?? '–');
    if (citesI10) citesI10.textContent = String(s.i10Index ?? '–');

    const pts = data.citationsByYear || [];
    if (chartEmpty) chartEmpty.textContent = pts.length ? '' : '연도별 데이터가 없어';
    if (chartEl) chartEl.innerHTML = pts.length ? svgBarChart(pts) : `<div class="stars-chart-empty">데이터 없음</div>`;
  }

  let scholarData = null;
  async function initScholar(scope) {
    try {
      if (!scholarData) scholarData = await loadScholarData();
      renderScholar(scholarData, scope);
    } catch (e) {
      if (chartEl) chartEl.innerHTML = `<div class="stars-chart-empty">데이터 로딩 실패</div>`;
      if (citesTotal) citesTotal.textContent = '–';
      if (citesH) citesH.textContent = '–';
      if (citesI10) citesI10.textContent = '–';
    }
  }

  scopeButtons.forEach((btn) => {
    btn.addEventListener('click', () => {
      setActive(scopeButtons, btn);
      initScholar(btn.dataset.scope);
    });
  });

  if (scopeButtons.length) {
    initScholar(scopeButtons[0].dataset.scope);
  }
})();
