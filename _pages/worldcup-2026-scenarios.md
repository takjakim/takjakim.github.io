---
layout: page
title: "2026 월드컵 경우의 수 계산기"
id: worldcup-2026-scenarios
permalink: /worldcup-2026-scenarios/
tags: [worldcup, football, calculator]
---

<style>
.wc-page{max-width:1180px;margin:0 auto;padding:1rem}.wc-hero{padding:2rem;border-radius:28px;background:linear-gradient(135deg,#0f172a,#1e3a8a);color:#fff;margin-bottom:1rem}.wc-hero h1{margin:.2rem 0 1rem;font-size:clamp(2rem,5vw,4rem)}.wc-toolbar{display:flex;gap:.7rem;flex-wrap:wrap;align-items:center;margin:1rem 0}.wc-toggle button,.wc-btn{border:1px solid #cbd5e1;background:#fff;border-radius:999px;padding:.55rem .9rem;cursor:pointer}.wc-toggle button.active{background:#0f172a;color:#fff}.wc-select{padding:.55rem .8rem;border:1px solid #cbd5e1;border-radius:12px}.wc-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(270px,1fr));gap:1rem}.wc-card,.wc-panel{background:rgba(255,255,255,.78);border:1px solid rgba(148,163,184,.35);border-radius:22px;padding:1rem;box-shadow:0 10px 30px rgba(15,23,42,.06);overflow:auto}.wc-card h3,.wc-panel h2{margin-top:0}table{width:100%;border-collapse:collapse;font-size:.88rem}th,td{padding:.45rem;border-bottom:1px solid #e2e8f0;text-align:left}tr.sel{background:#fef3c7}.wc-badge{display:inline-flex;border-radius:999px;padding:.18rem .45rem;font-size:.72rem;font-weight:700}.wc-badge.in{background:#dcfce7;color:#166534}.wc-badge.out{background:#fee2e2;color:#991b1b}.q{background:rgba(220,252,231,.45)}.nq{opacity:.7}.wc-match-inputs{display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:.7rem}.wc-group-editor{background:#fff;border:1px solid #e2e8f0;border-radius:16px;padding:.8rem}.wc-score-row{display:grid;grid-template-columns:1fr 50px 12px 50px 1fr;gap:.4rem;align-items:center;margin:.35rem 0}.wc-score-row input{width:45px;padding:.35rem;border:1px solid #cbd5e1;border-radius:8px}.wc-bracket{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:.75rem}.wc-bracket-match{display:grid;gap:.25rem;background:#fff;border:1px solid #e2e8f0;border-radius:16px;padding:.8rem;cursor:pointer}.wc-bracket-match.sel{outline:2px solid #f59e0b}.wc-bracket-match em{color:#64748b;font-size:.8rem}.wc-bracket-match small{color:#64748b}.wc-note{color:#64748b;font-size:.9rem}.wc-section{margin:1.4rem 0}.wc-sources{font-size:.85rem;color:#64748b}
</style>

<div class="wc-page">
  <header class="wc-hero">
    <p>48개국 · 12개 조 · 조 1/2위 + 3위 상위 8팀</p>
    <h1>2026 월드컵 경우의 수 계산기</h1>
    <p>경기 스코어를 입력하면 조별 순위, 3위 랭킹, 공식 32강 대진 슬롯, 선택 국가의 16강 경로를 자동으로 다시 계산한다.</p>
  </header>

  <section class="wc-toolbar wc-panel">
    <div class="wc-toggle" aria-label="국가 표시 언어">
      <button id="locale-ko" type="button">🇰🇷 국기+국문</button>
      <button id="locale-en" type="button">🇬🇧 Flag+English</button>
    </div>
    <label>선택 국가 <select id="team-select" class="wc-select"></select></label>
    <button id="reset-scores" class="wc-btn" type="button">초기 스코어로 리셋</button>
  </section>

  <section class="wc-section wc-panel">
    <h2>경기 결과 입력</h2>
    <p class="wc-note">초기값은 공개 기사에서 확인된 일부 조별리그 결과만 넣어뒀다. 빈 칸에 남은 경기 스코어를 넣으면 즉시 재계산된다.</p>
    <div id="wc-match-inputs" class="wc-match-inputs"></div>
  </section>

  <section class="wc-section">
    <h2>조별 순위</h2>
    <div id="wc-groups" class="wc-grid"></div>
  </section>

  <section class="wc-section wc-panel">
    <h2>3위 상위 8팀 랭킹</h2>
    <p class="wc-note">3위 12팀을 승점 → 득실차 → 다득점 순으로 정렬한다. 동률 세부 규정은 페어플레이/추첨까지 갈 수 있어 별도 표기한다.</p>
    <div id="wc-thirds"></div>
  </section>

  <section class="wc-section wc-panel">
    <h2>선택 국가 경로</h2>
    <div id="wc-team-path"></div>
  </section>

  <section class="wc-section wc-panel">
    <h2>공식 32강 대진표</h2>
    <p class="wc-note">32강 슬롯은 FIFA/Wikipedia에 공개된 구조를 따른다. 3위팀 배치는 495개 조합 lookup table로 계산한다.</p>
    <div id="wc-r32" class="wc-bracket"></div>
  </section>

  <section class="wc-section wc-panel">
    <h2>16강 브래킷 경로</h2>
    <div id="wc-r16" class="wc-bracket"></div>
  </section>

  <section class="wc-section wc-panel">
    <h2>상대전적 메모</h2>
    <div id="wc-h2h"></div>
  </section>

  <section class="wc-section wc-panel">
    <h2>규정 메모</h2>
    <ul>
      <li>조별 순위는 승점 → 골득실 → 다득점 → 동률 팀 간 상대전적 순으로 계산한다.</li>
      <li>페어플레이 점수와 추첨까지 필요한 경우는 “확정” 대신 주의가 필요하다.</li>
      <li>32강은 조 1위 12팀, 조 2위 12팀, 3위 상위 8팀으로 구성된다.</li>
    </ul>
    <ul id="wc-sources" class="wc-sources"></ul>
  </section>
</div>
<script src="{{ site.baseurl }}/assets/js/worldcup-2026-scenarios.js"></script>
