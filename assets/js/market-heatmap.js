(() => {
  const DEFAULT_DATE = null; // if null, auto-detect from page title or last_modified_at

  function findClosestMarketDate() {
    // Try: meta[article:modified_time] -> YYYY-MM-DD
    const meta = document.querySelector('meta[property="article:modified_time"]')?.getAttribute('content');
    if (meta) return meta.slice(0, 10);
    // Try: title begins with YYYY-MM-DD
    const h1 = document.querySelector('main h1');
    const t = (h1?.textContent || document.title || '').trim();
    const m = t.match(/(\d{4}-\d{2}-\d{2})/);
    return m ? m[1] : null;
  }

  async function fetchJson(url) {
    const res = await fetch(url, { cache: 'no-store' });
    if (!res.ok) throw new Error(`Failed to load ${url}: ${res.status}`);
    return res.json();
  }

  function colorForPct(pct) {
    // pct in percent, e.g. -2.31
    // Smooth red<->gray<->green
    const clamp = (x, a, b) => Math.max(a, Math.min(b, x));
    const x = clamp(pct, -5, 5) / 5; // -1..1
    if (x === 0) return '#9aa4b2';
    // negative: red, positive: green
    const lerp = (a, b, t) => Math.round(a + (b - a) * t);
    if (x < 0) {
      const t = Math.abs(x);
      return `rgb(${lerp(154, 220, t)},${lerp(44, 90, t)},${lerp(52, 110, t)})`;
    }
    {
      const t = x;
      return `rgb(${lerp(46, 80, t)},${lerp(160, 220, t)},${lerp(67, 120, t)})`;
    }
  }

  function formatPct(p) {
    const sign = p > 0 ? '+' : '';
    return `${sign}${p.toFixed(2)}%`;
  }

  function renderTreemap(el, payload) {
    // payload schema:
    // { label, items: [{ name, ticker, sector, pct, mcap_usd_b }], source, asOf }

    // Create a dedicated chart container so extra DOM (notes) won't change layout.
    el.innerHTML = '';
    const chartEl = document.createElement('div');
    chartEl.className = 'market-heatmap__chart';
    el.appendChild(chartEl);

    const chart = echarts.init(chartEl, null, { renderer: 'canvas' });

    const data = payload.items.map(it => ({
      name: it.name || it.ticker,
      value: it.mcap_usd_b || 1,
      ticker: it.ticker,
      sector: it.sector,
      pct: it.pct,
      itemStyle: { color: colorForPct(it.pct ?? 0) },
    }));

    chart.setOption({
      title: {
        text: payload.label || 'Market heatmap',
        subtext: payload.asOf ? `as of ${payload.asOf}` : undefined,
        left: 'center'
      },
      tooltip: {
        formatter: (info) => {
          const d = info.data;
          const pct = (d.pct == null) ? '—' : formatPct(d.pct);
          const mcap = (d.value == null) ? '—' : `${d.value.toLocaleString()}B`;
          const sec = d.sector ? `<br/>${d.sector}` : '';
          return `<b>${d.name}</b> (${d.ticker || ''})<br/>${pct}<br/>MCap: ${mcap}${sec}`;
        }
      },
      series: [
        {
          type: 'treemap',
          data,
          roam: false,
          nodeClick: false,
          breadcrumb: { show: false },
          label: {
            show: true,
            formatter: (p) => {
              const pct = p.data.pct;
              const tag = (pct == null) ? '' : `\n${formatPct(pct)}`;
              return `${p.data.ticker || p.name}${tag}`;
            },
            overflow: 'truncate'
          },
          upperLabel: { show: false },
          itemStyle: {
            borderColor: 'rgba(255,255,255,0.22)',
            borderWidth: 1,
            gapWidth: 1
          },
          emphasis: { itemStyle: { borderWidth: 2, borderColor: '#ffffff' } }
        }
      ]
    });

    const ro = new ResizeObserver(() => chart.resize());
    ro.observe(el);

    // One extra resize after paint to avoid rare "too-wide" initial layout.
    requestAnimationFrame(() => {
      try { chart.resize(); } catch (e) {}
    });
  }

  async function init() {
    const els = Array.from(document.querySelectorAll('.market-heatmap'));
    if (!els.length) return;

    // ECharts is loaded via defer; wait until it's available
    const waitEcharts = () => new Promise((resolve) => {
      const t = setInterval(() => {
        if (window.echarts) {
          clearInterval(t);
          resolve();
        }
      }, 50);
    });
    await waitEcharts();

    const date = DEFAULT_DATE || findClosestMarketDate();

    for (const el of els) {
      const country = el.dataset.country;
      const index = el.dataset.index;
      const mode = el.dataset.mode; // e.g., 'sectors'

      const key = mode ? `${country}-${mode}` : `${country}-${index}`;
      const asOf = el.dataset.asOf || date;

      if (!asOf || !key) {
        el.innerHTML = '<div class="heatmap-error">heatmap: missing data-date or data-index</div>';
        continue;
      }

      const url = `${document.querySelector('link[rel=canonical]')?.getAttribute('href')?.replace(/\/$/, '') || ''}`;
      // Use relative path (works on GitHub Pages)
      const jsonPath = `${document.documentElement.dataset.baseurl || ''}/assets/data/heatmaps/${asOf}/${key}.json`;

      try {
        const payload = await fetchJson(jsonPath);
        renderTreemap(el, payload);
        if (payload.source) {
          const note = document.createElement('div');
          note.className = 'heatmap-note';
          note.textContent = payload.source;
          el.appendChild(note);
        }
      } catch (e) {
        el.innerHTML = `<div class="heatmap-error">heatmap data not found: ${jsonPath}</div>`;
      }
    }
  }

  document.addEventListener('DOMContentLoaded', init);
})();
