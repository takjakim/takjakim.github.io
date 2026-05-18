/**
 * Market Heatmap Static Renderer
 *
 * Legacy posts used:
 *   <div class="market-heatmap" data-country="us" data-index="spx" data-as-of="2026-01-30"></div>
 *
 * We no longer render interactive Plotly treemaps (iOS Safari issues).
 * Instead, we replace the div with a static PNG if it exists.
 */

function heatmapKey(country, index) {
  country = (country || 'us').toLowerCase();
  index = (index || 'spx').toLowerCase();

  // Map legacy (country,index) -> filename key used by our PNG renderer.
  if (country === 'us' && index === 'spx') return 'us-spx';
  if (country === 'us' && index === 'ndx') return 'us-ndx';
  if (country === 'hk' && index === 'hsi') return 'hk-hsi';
  if (country === 'hk' && index === 'hstech') return 'hk-hstech';
  if (country === 'cn' && index === 'csi300') return 'cn-csi300';
  if (country === 'all' && index === 'sectors') return 'all-sectors';

  // Fallback: assume already in the right form.
  return country + '-' + index;
}

function initHeatmaps() {
  var heatmaps = document.querySelectorAll('.market-heatmap');

  heatmaps.forEach(function(el) {
    var country = el.dataset.country || 'us';
    var index = el.dataset.index || 'spx';
    var date = el.dataset.asOf || new Date().toISOString().split('T')[0];

    var key = heatmapKey(country, index);
    var imgUrl = '/assets/img/heatmaps/' + date + '/' + key + '.png';

    var img = document.createElement('img');
    img.loading = 'lazy';
    img.decoding = 'async';
    img.alt = (country.toUpperCase() + ' ' + index.toUpperCase() + ' heatmap (' + date + ')');
    img.style.maxWidth = '100%';
    img.style.height = 'auto';

    img.onerror = function() {
      el.innerHTML = '<div style="text-align:center; padding:1.25rem; color:#888; background:#f9f9f9; border-radius:8px;">' +
        '<div style="font-weight:600; margin-bottom:0.25rem;">히트맵 이미지 없음</div>' +
        '<small>' + date + ' / ' + key + '</small>' +
        '</div>';
    };

    img.src = imgUrl;

    // Replace content
    el.innerHTML = '';
    el.appendChild(img);
  });
}

// DOM 로드 후 초기화
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initHeatmaps);
} else {
  initHeatmaps();
}
