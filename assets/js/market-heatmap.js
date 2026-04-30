/**
 * Market Heatmap Auto-Initializer
 * 페이지의 모든 .market-heatmap 요소를 자동으로 Plotly 히트맵으로 렌더링
 *
 * Usage in markdown:
 * <div class="market-heatmap" data-country="us" data-index="spx" data-as-of="2026-01-30"></div>
 */

function initHeatmaps() {
  // Plotly가 로드될 때까지 대기
  if (typeof Plotly === 'undefined') {
    setTimeout(initHeatmaps, 100);
    return;
  }

  var heatmaps = document.querySelectorAll('.market-heatmap');

  heatmaps.forEach(function(el, idx) {
    var country = el.dataset.country || 'us';
    var index = el.dataset.index || 'spx';
    var date = el.dataset.asOf || new Date().toISOString().split('T')[0];

    var containerId = 'heatmap-' + country + '-' + index + '-' + idx;
    el.id = containerId;
    el.style.minHeight = '400px';

    var dataFile = '/assets/data/heatmaps/' + date + '/' + country + '-' + index + '.json';

    fetch(dataFile)
      .then(function(res) {
        if (!res.ok) throw new Error('데이터 없음');
        return res.json();
      })
      .then(function(data) {
        // Support two schemas:
        // (1) legacy: {labels, parents, values, changes, title}
        // (2) current: {label, asOf, source, items:[{ticker,name,sector,pct,mcap_usd_b}]}

        function buildFromItems(items, rootLabel) {
          // Use explicit ids to avoid label/parent resolution issues on some browsers (notably iOS Safari).
          var ids = [];
          var labels = [];
          var parents = [];
          var values = [];
          var changes = [];

          // root
          ids.push('root');
          labels.push(rootLabel || 'Market');
          parents.push('');
          values.push(0);
          changes.push(0);

          var sectorIndex = {}; // sector -> idx
          var sectorAgg = {};   // sector -> {mcapSum, weightedPctSum}

          items.forEach(function(it) {
            var sector = (it.sector || 'Other').trim();
            if (!sector) sector = 'Other';
            var pct = Number(it.pct);
            if (!isFinite(pct)) pct = 0;
            var mcap = Number(it.mcap_usd_b);
            if (!isFinite(mcap) || mcap <= 0) mcap = 1;

            if (sectorIndex[sector] === undefined) {
              sectorIndex[sector] = labels.length;
              ids.push('sector:' + sector);
              labels.push(sector);
              parents.push('root');
              values.push(0);
              changes.push(0);
              sectorAgg[sector] = { mcapSum: 0, weightedPctSum: 0 };
            }

            // stock leaf
            var leafLabel = it.ticker || it.name || 'N/A';
            ids.push('leaf:' + sector + ':' + leafLabel);
            labels.push(leafLabel);
            parents.push('sector:' + sector);
            values.push(mcap);
            changes.push(pct);

            sectorAgg[sector].mcapSum += mcap;
            sectorAgg[sector].weightedPctSum += pct * mcap;
          });

          // fill sector values + sector colors
          Object.keys(sectorIndex).forEach(function(sector) {
            var idx = sectorIndex[sector];
            var agg = sectorAgg[sector];
            values[idx] = agg.mcapSum;
            changes[idx] = agg.mcapSum > 0 ? (agg.weightedPctSum / agg.mcapSum) : 0;
            values[0] += agg.mcapSum;
          });

          return { ids: ids, labels: labels, parents: parents, values: values, changes: changes };
        }

        var hm;
        if (data && Array.isArray(data.items)) {
          hm = buildFromItems(data.items, data.label || (country.toUpperCase() + ' ' + index.toUpperCase()));
        } else {
          hm = {
            labels: data.labels,
            parents: data.parents,
            values: data.values,
            changes: data.changes
          };
        }

        // Hard-normalize numeric arrays (some browsers are strict)
        hm.values = (hm.values || []).map(function(x) { x = Number(x); return isFinite(x) && x > 0 ? x : 0; });
        hm.changes = (hm.changes || []).map(function(x) { x = Number(x); return isFinite(x) ? x : 0; });

        var trace = {
          type: 'treemap',
          ids: hm.ids,
          labels: hm.labels,
          parents: hm.parents,
          values: hm.values,
          branchvalues: 'total',
          marker: {
            colors: hm.changes,
            colorscale: [
              [0, '#dc2626'],
              [0.35, '#f87171'],
              [0.5, '#f5f5f5'],
              [0.65, '#4ade80'],
              [1, '#16a34a']
            ],
            cmid: 0,
            cmin: -5,
            cmax: 5,
            showscale: true,
            colorbar: {
              title: { text: '등락률 (%)', font: { size: 12 } },
              ticksuffix: '%',
              thickness: 15
            }
          },
          customdata: hm.changes,
          texttemplate: '<b>%{label}</b><br>%{customdata:+.1f}%',
          hovertemplate: '<b>%{label}</b><br>등락률: %{customdata:+.2f}%<extra></extra>',
          textfont: { size: 10 }
        };

        var layout = {
          title: {
            text: (data && (data.title || data.label)) || (country.toUpperCase() + ' ' + index.toUpperCase() + ' (' + date + ')'),
            font: { size: 14 }
          },
          margin: { t: 40, l: 5, r: 5, b: 5 },
          paper_bgcolor: 'transparent'
        };

        var config = {
          responsive: true,
          displayModeBar: false
        };

        Plotly.newPlot(containerId, [trace], layout, config);
      })
      .catch(function(err) {
        el.innerHTML = '<div style="text-align:center; padding:2rem; color:#888; background:#f9f9f9; border-radius:8px;">' +
          '<p>📊 히트맵 데이터 준비 중</p>' +
          '<small>' + date + ' / ' + country + '-' + index + '</small>' +
          '</div>';
      });
  });
}

// DOM 로드 후 초기화
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initHeatmaps);
} else {
  initHeatmaps();
}
