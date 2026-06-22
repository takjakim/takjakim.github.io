---
layout: page
title: Graph View
permalink: /graph
---

<section id="graph-page" class="graph-page-shell">
  <header class="graph-hero">
    <div>
      <p class="graph-kicker">Knowledge Map</p>
      <h1>Graph View</h1>
      <p class="graph-lead">노트 사이의 연결을 검색하고, 주제별로 좁히고, 허브 노트에서 다음 읽을거리를 찾는 지도.</p>
    </div>
    <div class="graph-stats" aria-label="Graph statistics">
      <div class="graph-stat-card">
        <span id="graph-node-count">—</span>
        <small>Notes</small>
      </div>
      <div class="graph-stat-card">
        <span id="graph-edge-count">—</span>
        <small>Links</small>
      </div>
      <div class="graph-stat-card">
        <span id="graph-visible-count">—</span>
        <small>Visible</small>
      </div>
    </div>
  </header>

  <div class="graph-workspace">
    <aside class="graph-sidebar" aria-label="Graph controls">
      <div class="graph-panel">
        <h2>탐색</h2>
        <p>검색 후 Enter. 노드는 클릭하면 선택, 더블클릭하면 글로 이동.</p>
        <div id="graph-controls" class="graph-controls">
          <label class="graph-search-label" for="graph-search">검색</label>
          <input id="graph-search" class="graph-search" type="search" placeholder="노트 제목 검색…" autocomplete="off" />

          <div class="graph-filters" role="group" aria-label="Category filters">
            <label class="graph-chip graph-chip--research"><input type="checkbox" class="graph-filter" value="research" checked /> Research</label>
            <label class="graph-chip graph-chip--theory"><input type="checkbox" class="graph-filter" value="theory" checked /> Theory</label>
            <label class="graph-chip graph-chip--dev"><input type="checkbox" class="graph-filter" value="dev" checked /> 개발</label>
            <label class="graph-chip graph-chip--ai"><input type="checkbox" class="graph-filter" value="ai" checked /> AI</label>
            <label class="graph-chip graph-chip--running"><input type="checkbox" class="graph-filter" value="running" checked /> Running</label>
            <label class="graph-chip graph-chip--education"><input type="checkbox" class="graph-filter" value="education" checked /> 교육·진로</label>
            <label class="graph-chip graph-chip--default"><input type="checkbox" class="graph-filter" value="default" checked /> 기타</label>
          </div>

          <label class="graph-toggle"><input id="graph-neighbors" type="checkbox" /> 선택 노드 주변만 보기</label>
          <button id="graph-reset" class="graph-btn" type="button">초기화</button>
        </div>
      </div>

      <div class="graph-panel graph-selected-panel">
        <h2>선택한 노트</h2>
        <p id="graph-selected-empty" class="graph-muted">노드를 클릭하면 제목, 연결 수, 바로가기 링크가 여기에 표시돼.</p>
        <div id="graph-selected-card" class="graph-selected-card" hidden>
          <span id="graph-selected-category" class="graph-selected-category">—</span>
          <h3 id="graph-selected-title">—</h3>
          <p><span id="graph-selected-degree">0</span>개의 연결</p>
          <a id="graph-selected-link" class="graph-open-link" href="#">글 열기 →</a>
        </div>
      </div>
    </aside>

    <main class="graph-canvas-card">
      <div class="graph-canvas-topbar">
        <div>
          <strong>Digital Garden Map</strong>
          <span>드래그로 고정 · 스크롤로 확대 · Shift+클릭으로 핀 토글</span>
        </div>
        <a class="graph-home-link" href="{{ site.baseurl }}/">홈으로</a>
      </div>
      <div id="graph-container" class="graph-container">
        {% include notes_graph.html %}
      </div>
    </main>
  </div>
</section>
