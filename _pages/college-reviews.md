---
layout: page
title: "대학리뷰"
permalink: /college-reviews/
description: "대학 홍보자료를 그대로 요약하지 않고, 학생·학부모가 실제 지원 전에 확인해야 할 대학별 이슈, 교육과정, 정책사업, 전공·취업 연결을 정리한 대학리뷰 모음."
---

# 대학리뷰

대학리뷰는 학교 홍보자료를 다시 쓰는 글이 아니다.  
**학생·학부모가 지원 전에 확인해야 할 대학의 방향, 교육과정, 정책사업, 전공 구조, 실습·취업 연결**을 상담 관점에서 정리하는 글이다.

## 대학리뷰에서 보는 기준

| 기준 | 질문 |
|---|---|
| 대학의 방향 | 이 대학은 어떤 산업·지역·전공으로 자신을 설명하는가? |
| 교육과정 | 학과 이름이 아니라 실제 커리큘럼과 모듈이 무엇인가? |
| 입시 구조 | 수시·정시, 통합모집, 수능 최저, 지역인재 조건은 어떤가? |
| 정책사업 | [[RISE]], [[글로컬대학30]], 국책사업이 학과에 실제로 내려오는가? |
| 진로 연결 | 실습처, 산학협력, 취업처, 지역정주 가능성이 있는가? |
| 학생 적합성 | 어떤 학생에게 맞고, 어떤 학생은 신중히 봐야 하는가? |

## 최근 대학리뷰

{% assign university_reviews = site.notes | where: "type", "university_review" | sort: "date" | reverse %}
{% if university_reviews.size > 0 %}
<div class="review-list">
{% for note in university_reviews %}
  <article class="review-list-card">
    <a href="{{ site.baseurl }}{{ note.url }}" class="internal-link">
      <span class="glass-tag tag-education">{{ note.label | default: "UNIV" }}</span>
      <h2>{{ note.title }}</h2>
      <p>{{ note.description | default: note.excerpt | default: note.content | strip_html | truncate: 150 }}</p>
    </a>
  </article>
{% endfor %}
</div>
{% else %}
아직 대학리뷰 글이 없습니다.
{% endif %}

## 같이 보면 좋은 개념 키워드

### 대학 정책

- [[RISE]]
- [[글로컬대학30]]
- [[지역정주]]
- [[지역인재]]
- [[산학협력]]

### 입시 구조

- [[통합모집]]
- [[전공자율선택제]]
- [[수능 최저]]
- [[장학금]]

### 교육과정·전공

- [[모듈형 교육과정]]
- [[보건계열]]
- [[K-MEDI]]
- [[K-뷰티]]
- [[푸드테크]]

### 취업·평생교육

- [[K-Move]]
- [[해외취업]]
- [[성인학습자]]
- [[평생교육]]

## 대학리뷰를 읽는 법

대학을 볼 때는 “좋은 학교냐 나쁜 학교냐”보다 먼저 봐야 할 것이 있다.

1. 이 대학이 어떤 산업·지역·전공과 연결되는가?
2. 내가 지원하려는 학과가 그 방향의 중심에 있는가, 주변에 있는가?
3. 입학 후 실제로 경험할 수 있는 교육과정·실습·프로젝트가 있는가?
4. 졸업 후 진로가 지역·산업·자격·취업처와 연결되는가?
5. 장학금과 전형 조건이 나에게 실제로 적용되는가?

대학 이름보다 중요한 것은 **학생의 진로와 대학의 교육과정이 만나는 지점**이다.
