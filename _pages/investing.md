---
layout: page
title: 지수 투자
permalink: /investing
---

<div class="category-header category-header-investing">
  <h1>지수 투자</h1>
  <p>매일 지수 투자 로깅</p>
</div>

<ul class="posts-list">
  {% assign category_notes = site.notes | where_exp: "note", "note.path contains '_notes/investing/'" | sort: "last_modified_at_timestamp" | reverse %}
  {% for note in category_notes %}
    <li class="post-item">
      <span class="post-date">{{ note.last_modified_at | date: "%Y-%m-%d" }}</span>
      <a class="internal-link" href="{{ site.baseurl }}{{ note.url }}">{{ note.title }}</a>
    </li>
  {% else %}
    <li class="post-item">아직 포스트가 없습니다.</li>
  {% endfor %}
</ul>

<p style="margin-top: 2em;">
  <a class="internal-link" href="{{ site.baseurl }}/">← 홈으로 돌아가기</a>
</p>
