---
layout: page
title: Graph View
permalink: /graph
---

<h1>Graph View</h1>
<p>노트 간의 연결을 시각적으로 탐색하세요.</p>

<div id="graph-controls" class="graph-controls">
  <input id="graph-search" class="graph-search" type="search" placeholder="노트 제목 검색…" />
  <div class="graph-filters" role="group" aria-label="Category filters">
    <label><input type="checkbox" class="graph-filter" value="research" checked /> Research</label>
    <label><input type="checkbox" class="graph-filter" value="theory" checked /> Theory</label>
    <label><input type="checkbox" class="graph-filter" value="dev" checked /> 개발</label>
    <label><input type="checkbox" class="graph-filter" value="ai" checked /> AI</label>
  </div>
  <label class="graph-toggle"><input id="graph-neighbors" type="checkbox" /> 선택 노드 주변만 보기</label>
  <button id="graph-reset" class="graph-btn" type="button">Reset</button>
</div>

<div id="graph-container" style="width: 100%; height: 75vh; min-height: 520px; border: 1px solid #ddd; border-radius: 8px; margin: 1.2em 0 2em;">
  {% include notes_graph.html %}
</div>

<p style="margin-top: 2em;">
  <a class="internal-link" href="{{ site.baseurl }}/">← 홈으로 돌아가기</a>
</p>
