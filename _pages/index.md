---
layout: page
title: Home
id: home
permalink: /
---

<div class="garden-container">
  <!-- Hero Section with Graph Background -->
  <header class="hero-2026">
    <div class="hero-graph-bg">
      {% include notes_graph.html %}
    </div>
    <div class="hero-content">
      <div class="hero-badge">Personal Knowledge Base</div>
      <h1 class="hero-title">
        <span class="gradient-text">Digital</span>
        <span class="gradient-text-alt">Garden</span>
      </h1>
      <p class="hero-desc">투자 · 개발 · AI · Theory에 대한 생각과 기록을 연결하는 공간</p>
      <div class="hero-stats">
        <div class="stat-item">
          <span class="stat-number">{% assign note_count = site.notes | size %}{{ note_count }}</span>
          <span class="stat-label">Notes</span>
        </div>
        <div class="stat-divider"></div>
        <div class="stat-item">
          <span class="stat-number">4</span>
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

  <!-- Tags / Knowledge Base -->
  <section class="recent-section">
    <div class="section-header">
      <h2 class="section-title">태그로 탐색</h2>
      <div class="filter-pills">
        <a class="pill" href="{{ site.baseurl }}/tags/">전체 태그 보기</a>
      </div>
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

    {% if uniq_tags.size > 0 %}
      <div class="note-tags" style="margin-top: 0;">
        {% for t in uniq_tags limit: 30 %}
          <a class="tag-pill" href="{{ site.baseurl }}/tags/{{ t | slugify }}/">#{{ t }}</a>
        {% endfor %}
      </div>
      {% if uniq_tags.size > 30 %}
        <p style="margin-top: 0.75rem; color: #6b7280;">+ {{ uniq_tags.size | minus: 30 }} more…</p>
      {% endif %}
    {% else %}
      <p>(태그 없음)</p>
    {% endif %}
  </section>

  <!-- Recent Posts -->
  <section class="recent-section">
    <div class="section-header">
      <h2 class="section-title">최근 업데이트</h2>
      <div class="filter-pills">
        <button class="pill active" data-filter="all">전체</button>
        <button class="pill" data-filter="research">Research</button>
        <button class="pill" data-filter="theory">Theory</button>
        <button class="pill" data-filter="dev">개발</button>
        <button class="pill" data-filter="ai">AI</button>
      </div>
    </div>

    <div class="glass-grid" id="notes-grid">
      {% assign recent_notes = site.notes | sort: "last_modified_at_timestamp" | reverse %}
      {% for note in recent_notes %}
        {% assign note_category = note.path | split: "/" | slice: 1 | first %}
        <article class="glass-card {% if note_category == 'investing' %}glass-investing{% elsif note_category == 'theory' %}glass-theory{% elsif note_category == 'dev' %}glass-dev{% elsif note_category == 'ai' %}glass-ai{% endif %}" data-category="{{ note_category }}" data-index="{{ forloop.index }}"{% if forloop.index > 9 %} style="display: none;"{% endif %}>
          <a href="{{ site.baseurl }}{{ note.url }}" class="glass-link internal-link">
            <div class="glass-meta">
              <time>{{ note.last_modified_at | date: "%m.%d" }}</time>
              {% if note_category == "investing" %}
                <span class="glass-tag tag-investing">Research</span>
              {% elsif note_category == "theory" %}
                <span class="glass-tag tag-theory">Theory</span>
              {% elsif note_category == "dev" %}
                <span class="glass-tag tag-dev">개발</span>
              {% elsif note_category == "ai" %}
                <span class="glass-tag tag-ai">AI</span>
              {% endif %}
            </div>
            <h3 class="glass-title">{{ note.title }}</h3>
            <p class="glass-excerpt">{{ note.content | strip_html | truncate: 60 }}</p>
            <div class="glass-footer">
              <span class="read-more">읽기 →</span>
            </div>
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
  const pills = document.querySelectorAll('.pill');
  const cards = document.querySelectorAll('.glass-card');
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
      const totalFiltered = Array.from(cards).filter(c =>
        currentFilter === 'all' || c.dataset.category === currentFilter
      ).length;
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
