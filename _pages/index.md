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

  <!-- Recent Posts -->
  <section class="recent-section">
    <div class="section-header">
      <h2 class="section-title">최근 업데이트</h2>
      <div class="filter-pills">
        <button class="pill active" data-filter="all">전체</button>
        <button class="pill" data-filter="investing">투자</button>
        <button class="pill" data-filter="dev">개발</button>
        <button class="pill" data-filter="ai">AI</button>
        <button class="pill" data-filter="theory">Theory</button>
      </div>
    </div>

    <div class="glass-grid">
      {% assign recent_notes = site.notes | sort: "last_modified_at_timestamp" | reverse %}
      {% for note in recent_notes limit: 9 %}
        {% assign note_category = note.path | split: "/" | slice: 1 %}
        <article class="glass-card {% if note_category == 'investing' %}glass-investing{% elsif note_category == 'theory' %}glass-theory{% elsif note_category == 'dev' %}glass-dev{% elsif note_category == 'ai' %}glass-ai{% endif %}" data-category="{{ note_category }}">
          <a href="{{ site.baseurl }}{{ note.url }}" class="glass-link internal-link">
            <div class="glass-meta">
              <time>{{ note.last_modified_at | date: "%m.%d" }}</time>
              {% if note_category == "investing" %}
                <span class="glass-tag tag-investing">투자</span>
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
  </section>
</div>

<script>
document.addEventListener('DOMContentLoaded', function() {
  const pills = document.querySelectorAll('.pill');
  const cards = document.querySelectorAll('.glass-card');

  pills.forEach(pill => {
    pill.addEventListener('click', function() {
      const filter = this.dataset.filter;

      pills.forEach(p => p.classList.remove('active'));
      this.classList.add('active');

      cards.forEach(card => {
        if (filter === 'all' || card.dataset.category === filter) {
          card.style.opacity = '0';
          card.style.transform = 'translateY(20px)';
          setTimeout(() => {
            card.style.display = '';
            requestAnimationFrame(() => {
              card.style.opacity = '1';
              card.style.transform = 'translateY(0)';
            });
          }, 100);
        } else {
          card.style.opacity = '0';
          card.style.transform = 'translateY(20px)';
          setTimeout(() => {
            card.style.display = 'none';
          }, 300);
        }
      });
    });
  });
});
</script>
