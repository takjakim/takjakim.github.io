/**
 * Market Heatmap Auto-Initializer
 * 페이지의 모든 .market-heatmap 요소를 자동으로 Plotly 히트맵으로 렌더링
 *
 * Usage in markdown:
 * <div class="market-heatmap" data-country="us" data-index="spx" data-as-of="2026-01-30"></div>
 */

document.addEventListener('DOMContentLoaded', function() {
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
        var trace = {
          type: 'treemap',
          labels: data.labels,
          parents: data.parents,
          values: data.values,
          marker: {
            colors: data.changes,
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
          texttemplate: '<b>%{label}</b><br>%{color:+.1f}%',
          hovertemplate: '<b>%{label}</b><br>등락률: %{color:+.2f}%<extra></extra>',
          textfont: { size: 10 }
        };

        var layout = {
          title: {
            text: data.title || (country.toUpperCase() + ' ' + index.toUpperCase() + ' (' + date + ')'),
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
});
