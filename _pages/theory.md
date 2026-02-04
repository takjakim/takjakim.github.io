---
layout: page
title: Theory
permalink: /theory/
---

<div class="category-page">
  <h1>Theory</h1>
  <p>이론, 프레임워크, 개념에 대한 정리</p>

  <div class="notes-list">
    {% assign theory_notes = site.notes | where_exp: "note", "note.path contains '_notes/theory/'" | sort: "last_modified_at_timestamp" | reverse %}
    {% for note in theory_notes %}
      <article class="note-card">
        <a href="{{ site.baseurl }}{{ note.url }}">
          <h3>{{ note.title }}</h3>
          <p>{{ note.content | strip_html | truncate: 100 }}</p>
          <time>{{ note.last_modified_at | date: "%Y.%m.%d" }}</time>
        </a>
      </article>
    {% endfor %}
  </div>
</div>
