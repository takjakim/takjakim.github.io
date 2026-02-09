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

  // ===== GitHub stars chart =====
  const repoButtons = document.querySelectorAll('.pub-controls .pub-sort-btn[data-repo]');
  const starsCurrent = document.getElementById('stars-current');
  const starsLast30 = document.getElementById('stars-last30');
  const starsLast365 = document.getElementById('stars-last365');
  const chartEl = document.getElementById('stars-chart');
  const chartEmpty = document.getElementById('stars-chart-empty');

  const DAY = 24 * 60 * 60 * 1000;

  function parseDate(s) {
    // expects YYYY-MM-DD
    const [y, m, d] = s.split('-').map(Number);
    return new Date(Date.UTC(y, m - 1, d));
  }

  function diffFrom(series, days) {
    if (!series.length) return null;
    const last = series[series.length - 1];
    const lastDate = parseDate(last.date);
    const target = new Date(lastDate.getTime() - days * DAY);

    // find nearest point <= target
    let prev = series[0];
    for (const p of series) {
      const dt = parseDate(p.date);
      if (dt <= target) prev = p;
      else break;
    }
    return last.stars - prev.stars;
  }

  function svgLineChart(points) {
    // points: [{date, stars}]
    const w = 860;
    const h = 180;
    const padX = 18;
    const padY = 18;

    const values = points.map((p) => p.stars);
    const min = Math.min(...values);
    const max = Math.max(...values);
    const span = Math.max(1, max - min);

    const x = (i) => padX + (i * (w - padX * 2)) / Math.max(1, points.length - 1);
    const y = (v) => padY + (h - padY * 2) * (1 - (v - min) / span);

    const d = points
      .map((p, i) => `${i === 0 ? 'M' : 'L'} ${x(i).toFixed(2)} ${y(p.stars).toFixed(2)}`)
      .join(' ');

    const last = points[points.length - 1];
    const lastX = x(points.length - 1);
    const lastY = y(last.stars);

    return `
<svg viewBox="0 0 ${w} ${h}" width="100%" height="${h}" role="img" aria-label="GitHub stars history">
  <defs>
    <linearGradient id="starsGrad" x1="0" x2="1" y1="0" y2="0">
      <stop offset="0%" stop-color="#ff6b6b"/>
      <stop offset="100%" stop-color="#4ecdc4"/>
    </linearGradient>
  </defs>
  <rect x="0" y="0" width="${w}" height="${h}" fill="rgba(0,0,0,0.02)" rx="14" />
  <path d="${d}" fill="none" stroke="url(#starsGrad)" stroke-width="3" />
  <circle cx="${lastX}" cy="${lastY}" r="4.5" fill="#111" />
  <text x="${w - 10}" y="${lastY - 10}" text-anchor="end" font-size="12" fill="#6b7280">${last.date} · ${last.stars}★</text>
</svg>
`.trim();
  }

  async function loadStarsData() {
    const res = await fetch(`${document.documentElement.getAttribute('data-baseurl') || ''}/assets/data/github-stars.json`, { cache: 'no-store' });
    if (!res.ok) throw new Error('failed to load stars data');
    return res.json();
  }

  function renderRepo(data, repo) {
    const series = (data.repos?.find((r) => r.repo === repo)?.series) || [];

    if (chartEmpty) chartEmpty.textContent = series.length ? '' : '아직 히스토리 데이터가 없어. (cron으로 자동 수집 가능)';

    if (starsCurrent) starsCurrent.textContent = series.length ? String(series[series.length - 1].stars) : '–';

    const d30 = series.length ? diffFrom(series, 30) : null;
    const d365 = series.length ? diffFrom(series, 365) : null;

    if (starsLast30) starsLast30.textContent = d30 === null ? '–' : `${d30 >= 0 ? '+' : ''}${d30}`;
    if (starsLast365) starsLast365.textContent = d365 === null ? '–' : `${d365 >= 0 ? '+' : ''}${d365}`;

    if (chartEl) {
      chartEl.innerHTML = series.length >= 2 ? svgLineChart(series) : `<div class="stars-chart-empty">아직 데이터가 부족해. (2포인트 이상 필요)</div>`;
    }
  }

  let starsData = null;
  async function initStars(repo) {
    try {
      if (!starsData) starsData = await loadStarsData();
      renderRepo(starsData, repo);
    } catch (e) {
      if (chartEl) chartEl.innerHTML = `<div class="stars-chart-empty">stars 데이터 로딩 실패</div>`;
      if (starsCurrent) starsCurrent.textContent = '–';
      if (starsLast30) starsLast30.textContent = '–';
      if (starsLast365) starsLast365.textContent = '–';
    }
  }

  repoButtons.forEach((btn) => {
    btn.addEventListener('click', () => {
      setActive(repoButtons, btn);
      initStars(btn.dataset.repo);
    });
  });

  // default
  if (repoButtons.length) {
    initStars(repoButtons[0].dataset.repo);
  }
})();
