---
layout: page
title: Home
id: home
permalink: /
---

<div class="garden-container">
  <button class="garden-sidebar-toggle" id="garden-sidebar-toggle" type="button" aria-controls="garden-sidebar" aria-expanded="false">
    <span class="garden-sidebar-toggle-icon" aria-hidden="true">☰</span>
    <span>Garden Map</span>
  </button>

  <div class="garden-sidebar-backdrop" id="garden-sidebar-backdrop" hidden></div>

  <aside class="garden-sidebar" id="garden-sidebar" aria-label="Garden Map" aria-hidden="true">
    <div class="garden-sidebar-panel">
      <div class="garden-sidebar-head">
        <div>
          <span class="garden-sidebar-kicker">Navigation</span>
          <strong>Garden Map</strong>
        </div>
        <button class="garden-sidebar-close" id="garden-sidebar-close" type="button" aria-label="Garden Map 닫기">×</button>
      </div>

      <nav class="garden-sidebar-nav" aria-label="주요 탐색">
        <div class="garden-sidebar-group">
          <span class="garden-sidebar-label">주제</span>
          <a href="{{ site.baseurl }}/tags/ai/"><span>AI</span><small>생성형 AI · 거버넌스</small></a>
          <a href="{{ site.baseurl }}/college-consulting/"><span>대학컨설팅</span><small>대학전략 · 교육과정</small></a>
          <a href="{{ site.baseurl }}/tags/market/"><span>Market</span><small>증시 · 매크로 관찰</small></a>
          <a href="{{ site.baseurl }}/tags/running/"><span>Running</span><small>트레일 · 훈련 로그</small></a>
          <a href="{{ site.baseurl }}/tags/dev/"><span>Dev</span><small>개발 · 자동화</small></a>
        </div>

        <div class="garden-sidebar-group">
          <span class="garden-sidebar-label">탐색</span>
          <a href="{{ site.baseurl }}/graph/"><span>Graph View</span><small>노트 연결 보기</small></a>
          <a href="{{ site.baseurl }}/tags/"><span>Tags</span><small>태그 지도</small></a>
          <a href="#recent-notes"><span>최근 업데이트</span><small>새로 쓴 노트</small></a>
          <a href="#topic-explore"><span>주제별 탐색</span><small>카테고리 입구</small></a>
        </div>

        <div class="garden-sidebar-group garden-sidebar-group--contact">
          <span class="garden-sidebar-label">Contacts</span>
          <a class="garden-sidebar-kakao" href="https://open.kakao.com/o/s1FJhUAi" target="_blank" rel="noopener noreferrer">
            <span>KakaoTalk</span><small>Open Chat</small>
          </a>
        </div>
      </nav>
    </div>
  </aside>

  <!-- Hero Section with Graph Background -->
  <header class="hero-2026">
    <div class="hero-graph-bg" aria-hidden="true">
      {% include notes_graph.html %}
    </div>
    <div class="hero-content">
      <div class="hero-badge">Personal Knowledge Base</div>
      <h1 class="hero-title">
        <span class="gradient-text">Digital</span>
        <span class="gradient-text-alt">Garden</span>
      </h1>
      <p class="hero-desc">대학컨설팅과 고등교육 전략, AI·개발·러닝을 함께 기록하고 기획으로 연결하는 공간</p>
      <div class="hero-stats">
        <div class="stat-item">
          <span class="stat-number">{% assign note_count = site.notes | size %}{{ note_count }}</span>
          <span class="stat-label">Notes</span>
        </div>
        <div class="stat-divider"></div>
        <div class="stat-item">
          <span class="stat-number">5</span>
          <span class="stat-label">Categories</span>
        </div>
        <div class="stat-divider"></div>
        <div class="stat-item">
          <span class="stat-number">&infin;</span>
          <span class="stat-label">Connections</span>
        </div>
      </div>
    </div>
  </header>

  <!-- Topic entry points / Knowledge Base -->
  <section class="recent-section" id="topic-explore">
    <div class="section-header">
      <h2 class="section-title">주제별 탐색</h2>
      <div class="filter-pills">
        <a class="pill" href="{{ site.baseurl }}/tags/">전체 태그 보기</a>
      </div>
    </div>

    <div class="topic-grid" aria-label="주요 주제">
      <a class="topic-card topic-card--research" href="{{ site.baseurl }}/tags/market/">
        <span class="topic-kicker">Research</span>
        <strong>시장 · 투자</strong>
        <span>증시 요약, 히트맵, 매크로 관찰</span>
      </a>
      <a class="topic-card topic-card--dev" href="{{ site.baseurl }}/tags/dev/">
        <span class="topic-kicker">Dev</span>
        <strong>개발 · 자동화</strong>
        <span>서비스 개발기, 배포, 자동화 실험</span>
      </a>
      <a class="topic-card topic-card--ai" href="{{ site.baseurl }}/tags/ai/">
        <span class="topic-kicker">AI</span>
        <strong>AI · 생산성</strong>
        <span>생성형 AI, 리터러시, 업무 자동화와 거버넌스</span>
      </a>
      <a class="topic-card topic-card--running" href="{{ site.baseurl }}/tags/running/">
        <span class="topic-kicker">Running</span>
        <strong>러닝 · 트레일</strong>
        <span>트랜스제주, 훈련 로그, 장비 기록</span>
      </a>
      <a class="topic-card topic-card--education" href="{{ site.baseurl }}/college-consulting/">
        <span class="topic-kicker">Education</span>
        <strong>대학컨설팅</strong>
        <span>대학 전략, 정책사업, 교육과정 개발</span>
      </a>
    </div>

    {% comment %}GitHub Pages 환경에서 collections.notes.docs가 비어 보일 때가 있어 site.notes 사용{% endcomment %}
    {% assign docs = site.notes %}
    {% assign all_tags = "" | split: "" %}
    {% for d in docs %}
      {% if d.tags %}
        {% for t in d.tags %}
          {% assign all_tags = all_tags | push: t %}
        {% endfor %}
      {% endif %}
    {% endfor %}
    {% assign uniq_tags = all_tags | uniq | sort %}
    {% assign priority_tags = "ai,automation,dev,github,market,heatmap,running,trail-running,transjeju,training,english,theory" | split: "," %}

    {% if uniq_tags.size > 0 %}
      <div class="note-tags note-tags--featured">
        {% for t in priority_tags %}
          {% if uniq_tags contains t %}
            <a class="tag-pill" href="{{ site.baseurl }}/tags/{{ t | slugify }}/">#{{ t }}</a>
          {% endif %}
        {% endfor %}
      </div>
    {% else %}
      <p>(태그 없음)</p>
    {% endif %}
  </section>

  <!-- Featured Posts -->
  {% assign featured_notes = site.data.home_recommendations %}
  {% if featured_notes and featured_notes.size > 0 %}
  <section class="recent-section">
    <div class="section-header">
      <h2 class="section-title">추천</h2>
      <div class="filter-pills">
        <span class="pill pill-ghost">큐레이션 + 자동</span>
      </div>
    </div>

    {% assign recommendation_graph = site.data.home_recommendations_graph %}
    <div class="featured-grid">
      {% for note in featured_notes limit: 3 %}
        {% assign note_category = note.category %}
        <article class="glass-card glass-card--featured {% if forloop.first %}glass-card--xl{% else %}glass-card--md{% endif %} {% if note_category == 'investing' %}glass-investing{% elsif note_category == 'theory' %}glass-theory{% elsif note_category == 'dev' %}glass-dev{% elsif note_category == 'ai' %}glass-ai{% elsif note_category == 'education' %}glass-education{% elsif note_category == 'running' %}glass-running{% endif %}">
          <a href="{{ site.baseurl }}{{ note.url }}" class="glass-link internal-link">
            <div class="glass-meta">
              <time>{{ note.date_label }}</time>
              {% if note.views and note.views > 0 %}
                <span class="glass-views">👀 {{ note.views }}</span>
              {% else %}
                <span class="glass-views glass-views--new">NEW</span>
              {% endif %}
              {% if note.reason %}
                <span class="glass-views glass-views--new">{{ note.reason }}</span>
              {% endif %}
              {% if note_category == "investing" %}
                <span class="glass-tag tag-investing">Research</span>
              {% elsif note_category == "theory" %}
                <span class="glass-tag tag-theory">Theory</span>
              {% elsif note_category == "dev" %}
                <span class="glass-tag tag-dev">개발</span>
              {% elsif note_category == "ai" %}
                <span class="glass-tag tag-ai">AI</span>
              {% elsif note_category == "education" %}
                <span class="glass-tag tag-education">{{ note.label | default: "EDU" }}</span>
              {% elsif note_category == "running" %}
                <span class="glass-tag tag-running">Running</span>
              {% endif %}
            </div>
            <h3 class="glass-title">{{ note.title }}</h3>
            {% if forloop.first %}
              <p class="glass-excerpt">{{ note.excerpt | strip_html | truncate: 160 }}</p>
            {% else %}
              <p class="glass-excerpt">{{ note.excerpt | strip_html | truncate: 110 }}</p>
            {% endif %}
            {% if forloop.first and recommendation_graph and recommendation_graph.nodes and recommendation_graph.nodes.size > 1 %}
              <div class="home-feature-graph home-feature-graph--embedded" aria-label="이 추천 노트의 주변 연결">
                <div class="home-feature-graph-head">
                  <span>Graph View</span>
                  <strong>이 글 주변의 연결된 노트</strong>
                </div>
                <svg viewBox="0 0 520 156" role="img" aria-label="가장 큰 추천 노트와 주변 노트의 미니 그래프">
                  <defs>
                    <linearGradient id="home-mini-graph-line" x1="0" x2="1" y1="0" y2="1">
                      <stop offset="0%" stop-color="#ec4899" stop-opacity="0.42" />
                      <stop offset="100%" stop-color="#3b82f6" stop-opacity="0.32" />
                    </linearGradient>
                    <filter id="home-mini-graph-glow" x="-30%" y="-30%" width="160%" height="160%">
                      <feGaussianBlur stdDeviation="3" result="coloredBlur" />
                      <feMerge>
                        <feMergeNode in="coloredBlur" />
                        <feMergeNode in="SourceGraphic" />
                      </feMerge>
                    </filter>
                  </defs>
                  {% for edge in recommendation_graph.edges %}
                    {% assign sx = nil %}{% assign sy = nil %}{% assign tx = nil %}{% assign ty = nil %}
                    {% for graph_node in recommendation_graph.nodes %}
                      {% if graph_node.id == edge.source %}{% assign sx = graph_node.x %}{% assign sy = graph_node.y %}{% endif %}
                      {% if graph_node.id == edge.target %}{% assign tx = graph_node.x %}{% assign ty = graph_node.y %}{% endif %}
                    {% endfor %}
                    {% if sx and sy and tx and ty %}
                      <line class="home-mini-graph-edge" x1="{{ sx }}" y1="{{ sy }}" x2="{{ tx }}" y2="{{ ty }}" />
                    {% endif %}
                  {% endfor %}
                  {% for graph_node in recommendation_graph.nodes %}
                    {% assign node_radius = 9 %}
                    {% if graph_node.kind == 'featured' %}{% assign node_radius = 14 %}{% endif %}
                    <g class="home-mini-graph-node-group" aria-label="{{ graph_node.title | escape }}">
                      <circle class="home-mini-graph-node home-mini-graph-node--{{ graph_node.kind }} home-mini-graph-node--{{ graph_node.category }}" cx="{{ graph_node.x }}" cy="{{ graph_node.y }}" r="{{ node_radius }}" />
                      <text class="home-mini-graph-label {% if graph_node.kind == 'featured' %}home-mini-graph-label--featured{% endif %}" x="{{ graph_node.x }}" y="{{ graph_node.y | plus: node_radius | plus: 13 }}">
                        {{ graph_node.title | truncate: 15 | escape }}
                      </text>
                    </g>
                  {% endfor %}
                </svg>
              </div>
            {% endif %}
            <div class="glass-footer"><span class="read-more">읽기 →</span></div>
          </a>
        </article>
      {% endfor %}
    </div>
  </section>
  {% endif %}

  <!-- Recent Posts (Magazine) -->
  <section class="recent-section" id="recent-notes">
    <div class="section-header">
      <h2 class="section-title">최근 업데이트</h2>
      <div class="filter-pills">
        <button class="pill active" data-filter="all">전체</button>
        <button class="pill" data-filter="research">Research</button>
        <button class="pill" data-filter="theory">Theory</button>
        <button class="pill" data-filter="dev">개발</button>
        <button class="pill" data-filter="ai">AI</button>
        <button class="pill" data-filter="education">Education</button>
        <button class="pill" data-filter="running">Running</button>
      </div>
    </div>

    <div class="glass-grid glass-grid--magazine" id="notes-grid">
      {% assign recent_notes = site.notes | where_exp: "note", "note.type != 'concept'" | sort: "last_modified_at_timestamp" | reverse %}
      {% for note in recent_notes %}
        {% assign note_category = note.path | split: "/" | slice: 1 | first %}
        {% assign importance = note.importance | default: 1 %}
        {% assign size_class = "" %}
        {% if note.featured == true or importance >= 3 %}
          {% assign size_class = "glass-card--lg" %}
        {% elsif importance == 2 %}
          {% assign size_class = "glass-card--md" %}
        {% endif %}

        <article class="glass-card {{ size_class }} {% if note_category == 'investing' %}glass-investing{% elsif note_category == 'theory' %}glass-theory{% elsif note_category == 'dev' %}glass-dev{% elsif note_category == 'ai' %}glass-ai{% elsif note_category == 'education' %}glass-education{% elsif note_category == 'running' %}glass-running{% endif %}" data-category="{{ note_category }}" data-index="{{ forloop.index }}"{% if forloop.index > 9 %} style="display: none;"{% endif %}>
          <a href="{{ site.baseurl }}{{ note.url }}" class="glass-link internal-link">
            <div class="glass-meta">
              <time>{{ note.last_modified_at | date: "%m.%d" }}</time>
              {% assign pv = site.data.pageviews.paths[note.url].views %}
              {% if pv != nil %}
                <span class="glass-views">👀 {{ pv }}</span>
              {% else %}
                <span class="glass-views glass-views--new">NEW</span>
              {% endif %}
              {% if note_category == "investing" %}
                <span class="glass-tag tag-investing">Research</span>
              {% elsif note_category == "theory" %}
                <span class="glass-tag tag-theory">Theory</span>
              {% elsif note_category == "dev" %}
                <span class="glass-tag tag-dev">개발</span>
              {% elsif note_category == "ai" %}
                <span class="glass-tag tag-ai">AI</span>
              {% elsif note_category == "education" %}
                <span class="glass-tag tag-education">{{ note.label | default: "EDU" }}</span>
              {% elsif note_category == "running" %}
                <span class="glass-tag tag-running">Running</span>
              {% endif %}
            </div>
            <h3 class="glass-title">{{ note.title }}</h3>
            {% if size_class == "glass-card--lg" %}
              <p class="glass-excerpt">{{ note.content | strip_html | truncate: 160 }}</p>
            {% elsif size_class == "glass-card--md" %}
              <p class="glass-excerpt">{{ note.content | strip_html | truncate: 110 }}</p>
            {% else %}
              <p class="glass-excerpt">{{ note.content | strip_html | truncate: 80 }}</p>
            {% endif %}
            <div class="glass-footer"><span class="read-more">읽기 →</span></div>
          </a>
        </article>
      {% endfor %}
    </div>

    {% if recent_notes.size > 9 %}
    <div class="load-more-container">
      <button class="load-more-btn" id="load-more">
        더보기 <span class="load-more-count">(+{{ recent_notes.size | minus: 9 }})</span>
      </button>
    </div>
    {% endif %}
  </section>
</div>

<script>
document.addEventListener('DOMContentLoaded', function() {
  const sidebar = document.getElementById('garden-sidebar');
  const sidebarToggle = document.getElementById('garden-sidebar-toggle');
  const sidebarClose = document.getElementById('garden-sidebar-close');
  const sidebarBackdrop = document.getElementById('garden-sidebar-backdrop');
  const sidebarStorageKey = 'takjakim:garden-sidebar-open';

  function setSidebarState(isOpen, options = {}) {
    if (!sidebar || !sidebarToggle || !sidebarBackdrop) return;
    sidebar.classList.toggle('is-open', isOpen);
    sidebar.setAttribute('aria-hidden', String(!isOpen));
    sidebarToggle.setAttribute('aria-expanded', String(isOpen));
    sidebarBackdrop.hidden = !isOpen;
    document.body.classList.toggle('garden-sidebar-open', isOpen);

    if (options.persist !== false) {
      try {
        window.localStorage.setItem(sidebarStorageKey, isOpen ? '1' : '0');
      } catch (error) {}
    }

    if (isOpen && options.focus !== false && sidebarClose) {
      sidebarClose.focus({ preventScroll: true });
    }
  }

  if (sidebar && sidebarToggle && sidebarBackdrop) {
    let shouldRestoreSidebar = false;
    try {
      shouldRestoreSidebar = window.localStorage.getItem(sidebarStorageKey) === '1' && window.matchMedia('(min-width: 900px)').matches;
    } catch (error) {}

    setSidebarState(shouldRestoreSidebar, { persist: false, focus: false });

    sidebarToggle.addEventListener('click', function() {
      setSidebarState(!sidebar.classList.contains('is-open'));
    });

    if (sidebarClose) {
      sidebarClose.addEventListener('click', function() {
        setSidebarState(false);
        sidebarToggle.focus({ preventScroll: true });
      });
    }

    sidebarBackdrop.addEventListener('click', function() {
      setSidebarState(false);
    });

    sidebar.querySelectorAll('a').forEach(link => {
      link.addEventListener('click', function() {
        if (this.getAttribute('href') && this.getAttribute('href').startsWith('#')) {
          setSidebarState(false);
        }
      });
    });

    document.addEventListener('keydown', function(event) {
      if (event.key === 'Escape' && sidebar.classList.contains('is-open')) {
        setSidebarState(false);
        sidebarToggle.focus({ preventScroll: true });
      }
    });
  }

  const pills = document.querySelectorAll('#recent-notes button.pill[data-filter]');
  const cards = document.querySelectorAll('#notes-grid .glass-card');
  const loadMoreBtn = document.getElementById('load-more');
  const ITEMS_PER_PAGE = 9;
  let visibleCount = ITEMS_PER_PAGE;
  let currentFilter = 'all';

  function updateVisibility() {
    let count = 0;
    cards.forEach(card => {
      const matchesFilter =
        currentFilter === 'all' ||
        (currentFilter === 'research' && (card.dataset.category === 'investing' || card.dataset.category === 'market-analysis')) ||
        card.dataset.category === currentFilter;
      if (matchesFilter) {
        count++;
        if (count <= visibleCount) {
          card.style.display = '';
          card.style.opacity = '1';
          card.style.transform = 'translateY(0)';
        } else {
          card.style.display = 'none';
        }
      } else {
        card.style.display = 'none';
      }
    });

    // Update load more button
    if (loadMoreBtn) {
      const totalFiltered = Array.from(cards).filter(c => {
        if (currentFilter === 'all') return true;
        if (currentFilter === 'research') return (c.dataset.category === 'investing' || c.dataset.category === 'market-analysis');
        return c.dataset.category === currentFilter;
      }).length;
      const remaining = totalFiltered - visibleCount;
      if (remaining > 0) {
        loadMoreBtn.parentElement.style.display = '';
        loadMoreBtn.querySelector('.load-more-count').textContent = `(+${remaining})`;
      } else {
        loadMoreBtn.parentElement.style.display = 'none';
      }
    }
  }

  pills.forEach(pill => {
    pill.addEventListener('click', function() {
      currentFilter = this.dataset.filter;
      visibleCount = ITEMS_PER_PAGE;
      pills.forEach(p => p.classList.remove('active'));
      this.classList.add('active');
      updateVisibility();
    });
  });

  if (loadMoreBtn) {
    loadMoreBtn.addEventListener('click', function() {
      visibleCount += ITEMS_PER_PAGE;
      updateVisibility();
    });
  }

  updateVisibility();
});
</script>
