---
layout: page
title: Home
id: home
permalink: /
---

<div class="garden-container">
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
      <p class="hero-desc">대학컨설팅 · 대학리뷰 · 진로진학 전략과 Research · 개발 · AI · Running 기록을 연결하는 공간</p>
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
      <a class="topic-card topic-card--ai" href="{{ site.baseurl }}/worldcup-2026-scenarios/">
        <span class="topic-kicker">AI</span>
        <strong>월드컵 경우의 수</strong>
        <span>전적 현황판, 32강 대진표, 국가별 시나리오</span>
      </a>
      <a class="topic-card topic-card--running" href="{{ site.baseurl }}/tags/running/">
        <span class="topic-kicker">Running</span>
        <strong>러닝 · 트레일</strong>
        <span>트랜스제주, 훈련 로그, 장비 기록</span>
      </a>
      <a class="topic-card topic-card--education" href="{{ site.baseurl }}/college-consulting/">
        <span class="topic-kicker">Education</span>
        <strong>대학컨설팅</strong>
        <span>대학리뷰, 전공 선택, 진로진학 전략</span>
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
