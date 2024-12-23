---
layout: page
permalink: /
---

<div class="youtube-layout">
  <div class="category-nav">
    <a href="#" class="category-item active">전체</a>
    <a href="#" class="category-item">게임</a>
    <a href="#" class="category-item">음악</a>
    <a href="#" class="category-item">엔터테인먼트</a>
    <a href="#" class="category-item">블로그</a>
    <a href="#" class="category-item">테크</a>
  </div>

  <div class="video-grid">
    {% assign recent_notes = site.notes | sort: "last_modified_at_timestamp" | reverse %}
    {% for note in recent_notes limit: 12 %}
      <div class="video-item">
        <div class="thumbnail">
          {% if note.thumbnail %}
            <img src="{{ note.thumbnail }}" alt="{{ note.title }}">
          {% else %}
            <div class="default-thumbnail">{{ note.title | first }}</div>
          {% endif %}
          <span class="duration">{{ note.duration | default: "00:00" }}</span>
        </div>
        <div class="video-info">
          <h3 class="video-title">
            <a class="internal-link" href="{{ site.baseurl }}{{ note.url }}">{{ note.title }}</a>
          </h3>
          <div class="meta-info">
            <span class="upload-date">{{ note.last_modified_at | date: "%Y-%m-%d" }}</span>
            {% if note.views %}
              <span class="views">조회수 {{ note.views }}회</span>
            {% endif %}
          </div>
        </div>
      </div>
    {% endfor %}
  </div>
</div>

<style>
.youtube-layout {
  max-width: 100%;
  padding: 20px;
}

.category-nav {
  display: flex;
  gap: 12px;
  margin-bottom: 24px;
  overflow-x: auto;
  padding-bottom: 12px;
}

.category-item {
  padding: 8px 12px;
  background: #f2f2f2;
  border-radius: 16px;
  white-space: nowrap;
  text-decoration: none;
  color: #030303;
}

.category-item.active {
  background: #030303;
  color: white;
}

.video-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 20px;
}

.video-item {
  cursor: pointer;
}

.thumbnail {
  position: relative;
  width: 100%;
  padding-top: 56.25%; /* 16:9 Aspect Ratio */
  background: #f2f2f2;
  border-radius: 12px;
  overflow: hidden;
}

.thumbnail img {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.default-thumbnail {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2em;
  color: #666;
}

.duration {
  position: absolute;
  bottom: 8px;
  right: 8px;
  background: rgba(0, 0, 0, 0.8);
  color: white;
  padding: 2px 4px;
  border-radius: 4px;
  font-size: 0.8em;
}

.video-info {
  padding: 12px 4px;
}

.video-title {
  margin: 0;
  font-size: 1em;
  line-height: 1.4;
  max-height: 2.8em;
  overflow: hidden;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

.video-title a {
  color: #030303;
  text-decoration: none;
}

.meta-info {
  margin-top: 8px;
  font-size: 0.9em;
  color: #606060;
}

.meta-info span:not(:last-child)::after {
  content: "•";
  margin: 0 4px;
}

.wrapper {
  max-width: none;
  padding: 0;
}
</style>