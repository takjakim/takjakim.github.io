---
layout: page
title: "2026 월드컵 경우의 수 계산기"
id: worldcup-2026-scenarios
permalink: /worldcup-2026-scenarios/
tags: [ai, worldcup, football, calculator]
---

<style>
:root{--wc-bg:#080b16;--wc-card:#101426;--wc-card2:#151b31;--wc-line:rgba(148,163,184,.18);--wc-text:#edf2ff;--wc-muted:#93a4bc;--wc-purple:#7132f5;--wc-blue:#38bdf8;--wc-green:#22c55e;--wc-red:#ef4444;--wc-amber:#f59e0b;--wc-radius:22px;--wc-shadow:0 22px 70px rgba(0,0,0,.35)}
body:has(.wc-page){background:#07130d}body:has(.wc-page) main,body:has(.wc-page) .page-content{background:transparent}
.wc-page{position:relative;isolation:isolate;max-width:1360px;margin:0 auto;padding:1rem;color:var(--wc-text);font-family:Inter,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}.wc-page::before{content:"";position:fixed;inset:0;z-index:-2;background:radial-gradient(circle at 18% 0%,rgba(34,197,94,.18),transparent 30%),radial-gradient(circle at 86% 8%,rgba(113,50,245,.26),transparent 32%),linear-gradient(180deg,rgba(4,23,16,.96),rgba(5,13,24,.98) 56%,#070911 100%)}.wc-page::after{content:"";position:fixed;left:50%;top:50%;width:min(1180px,92vw);height:min(760px,72vh);transform:translate(-50%,-48%);z-index:-1;opacity:.26;border:2px solid rgba(226,255,232,.6);border-radius:26px;background:linear-gradient(90deg,transparent calc(50% - 1px),rgba(226,255,232,.62) calc(50% - 1px),rgba(226,255,232,.62) calc(50% + 1px),transparent calc(50% + 1px)),radial-gradient(circle at 50% 50%,transparent 0 86px,rgba(226,255,232,.62) 87px 89px,transparent 90px),radial-gradient(circle at 50% 50%,rgba(226,255,232,.72) 0 5px,transparent 6px),linear-gradient(90deg,rgba(255,255,255,.07) 0 12.5%,rgba(255,255,255,.02) 12.5% 25%,rgba(255,255,255,.07) 25% 37.5%,rgba(255,255,255,.02) 37.5% 50%,rgba(255,255,255,.07) 50% 62.5%,rgba(255,255,255,.02) 62.5% 75%,rgba(255,255,255,.07) 75% 87.5%,rgba(255,255,255,.02) 87.5% 100%);box-shadow:0 0 0 9999px rgba(0,0,0,.08),inset 0 0 90px rgba(0,0,0,.46);pointer-events:none}.wc-pitch-mark{position:fixed;z-index:-1;pointer-events:none;opacity:.24;border:2px solid rgba(226,255,232,.58);border-left:0;border-radius:0 18px 18px 0}.wc-pitch-mark--left{left:4vw;top:36vh;width:min(190px,16vw);height:min(270px,28vh)}.wc-pitch-mark--right{right:4vw;top:36vh;width:min(190px,16vw);height:min(270px,28vh);transform:scaleX(-1)}
.wc-hero{position:relative;overflow:hidden;padding:2.2rem;border-radius:32px;background:linear-gradient(135deg,rgba(6,95,70,.9),rgba(15,23,42,.92) 48%,rgba(2,6,23,.98)),repeating-linear-gradient(90deg,rgba(255,255,255,.05) 0 42px,rgba(255,255,255,.015) 42px 84px);border:1px solid rgba(255,255,255,.12);box-shadow:var(--wc-shadow);margin-bottom:1rem}.wc-hero:before{content:"";position:absolute;inset:12px;border:1px solid rgba(220,252,231,.18);border-radius:24px;pointer-events:none}.wc-hero:after{content:"";position:absolute;right:-80px;top:-100px;width:360px;height:360px;border-radius:50%;background:radial-gradient(circle,rgba(34,197,94,.24),transparent 60%)}.wc-hero p{max-width:760px;color:#dbe7ff}.wc-hero h1{margin:.25rem 0 1rem;font-size:clamp(2.2rem,5.8vw,5rem);line-height:.96;letter-spacing:-.06em}.wc-live-pill{display:inline-flex;gap:.45rem;align-items:center;padding:.38rem .66rem;border-radius:999px;background:rgba(34,197,94,.15);border:1px solid rgba(34,197,94,.35);color:#bbf7d0;font-weight:800;font-size:.78rem;text-transform:uppercase;letter-spacing:.08em}.wc-live-dot{width:.55rem;height:.55rem;border-radius:50%;background:#22c55e;box-shadow:0 0 18px #22c55e}.wc-hero-kpis{display:grid;grid-template-columns:repeat(4,minmax(130px,1fr));gap:.75rem;margin-top:1.4rem;max-width:880px}.wc-kpi{background:rgba(255,255,255,.1);border:1px solid rgba(255,255,255,.14);border-radius:18px;padding:.9rem}.wc-kpi b{display:block;font-size:1.45rem}.wc-kpi span{font-size:.78rem;color:#cbd5e1}
.wc-toolbar{position:sticky;top:.5rem;z-index:10;display:flex;gap:.7rem;flex-wrap:wrap;align-items:center;justify-content:space-between;margin:1rem 0;backdrop-filter:blur(18px)}.wc-control-left,.wc-control-right{display:flex;gap:.7rem;flex-wrap:wrap;align-items:center}.wc-toggle{display:flex;background:rgba(15,23,42,.82);border:1px solid var(--wc-line);border-radius:14px;padding:.22rem}.wc-toggle button,.wc-btn{border:1px solid transparent;background:transparent;color:var(--wc-muted);border-radius:11px;padding:.58rem .85rem;cursor:pointer;font-weight:800}.wc-toggle button.active{background:var(--wc-purple);color:#fff;box-shadow:0 10px 28px rgba(113,50,245,.32)}.wc-btn{background:rgba(255,255,255,.07);border-color:var(--wc-line);color:#e2e8f0}.wc-select{padding:.62rem .8rem;border:1px solid var(--wc-line);border-radius:12px;background:#0f172a;color:#fff}.wc-section{margin:1.15rem 0}.wc-card,.wc-panel{background:linear-gradient(180deg,rgba(21,27,49,.94),rgba(11,16,30,.94));border:1px solid var(--wc-line);border-radius:var(--wc-radius);padding:1rem;box-shadow:0 16px 48px rgba(0,0,0,.23);overflow:auto}.wc-card h3,.wc-panel h2{margin-top:0}.wc-panel-head{display:flex;justify-content:space-between;gap:1rem;align-items:flex-end;margin-bottom:.8rem}.wc-note{color:var(--wc-muted);font-size:.9rem}.wc-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(390px,1fr));gap:1rem}.wc-dashboard{display:grid;grid-template-columns:1.1fr .9fr .9fr;gap:1rem}.wc-scoreboard{display:grid;gap:.55rem}.wc-score-line{display:grid;grid-template-columns:1fr auto 1fr;gap:.8rem;align-items:center;padding:.72rem;border-radius:16px;background:rgba(255,255,255,.045);border:1px solid rgba(255,255,255,.07)}.wc-score-team{display:flex;align-items:center;gap:.4rem;font-weight:900}.wc-score-team:last-child{justify-content:flex-end}.wc-score{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:1.15rem;font-weight:900;color:#fff}.wc-mini-list{display:grid;gap:.55rem}.wc-mini-row{display:flex;justify-content:space-between;gap:.8rem;align-items:center;padding:.65rem .75rem;border:1px solid rgba(255,255,255,.08);border-radius:14px;background:rgba(255,255,255,.04)}.wc-mini-row b{color:#fff}.wc-team-chip{display:inline-flex;align-items:center;gap:.35rem;font-weight:900}.wc-progress{height:8px;background:rgba(255,255,255,.08);border-radius:999px;overflow:hidden}.wc-progress span{display:block;height:100%;background:linear-gradient(90deg,var(--wc-purple),var(--wc-blue))}
table{width:100%;border-collapse:separate;border-spacing:0 6px;font-size:.88rem}th{padding:.35rem .55rem;color:var(--wc-muted);font-size:.72rem;text-transform:uppercase;letter-spacing:.06em;white-space:nowrap}td{padding:.62rem .55rem;background:rgba(255,255,255,.045);border-top:1px solid rgba(255,255,255,.06);border-bottom:1px solid rgba(255,255,255,.06);white-space:nowrap}.wc-card td:nth-child(2){min-width:110px;white-space:normal;word-break:keep-all;overflow-wrap:normal}td:first-child{border-left:1px solid rgba(255,255,255,.06);border-radius:12px 0 0 12px}td:last-child{border-right:1px solid rgba(255,255,255,.06);border-radius:0 12px 12px 0}tr.sel td{background:rgba(245,158,11,.18);border-color:rgba(245,158,11,.38)}.wc-badge{display:inline-flex;border-radius:999px;padding:.22rem .5rem;font-size:.72rem;font-weight:900}.wc-badge.in{background:rgba(34,197,94,.16);color:#86efac}.wc-badge.out{background:rgba(239,68,68,.16);color:#fca5a5}.q td{background:rgba(34,197,94,.08)}.nq{opacity:.72}.wc-match-inputs{display:grid;grid-template-columns:repeat(auto-fit,minmax(330px,1fr));gap:.75rem}.wc-group-editor{background:rgba(255,255,255,.04);border:1px solid var(--wc-line);border-radius:16px;padding:.8rem}.wc-group-editor summary{cursor:pointer;font-weight:900}.wc-score-row{display:grid;grid-template-columns:1fr 50px 12px 50px 1fr;gap:.4rem;align-items:center;margin:.45rem 0}.wc-score-row input{width:45px;padding:.42rem;border:1px solid rgba(255,255,255,.14);border-radius:10px;background:#070b16;color:#fff;text-align:center}.wc-knockout-panel{overflow:hidden}.wc-bracket-legend{display:flex;align-items:center;gap:.45rem;color:var(--wc-muted);font-size:.82rem;font-weight:800}.wc-bracket-legend span{width:22px;height:3px;border-radius:999px;background:var(--wc-amber);box-shadow:0 0 16px rgba(245,158,11,.55)}.wc-knockout-board{display:grid;grid-template-columns:minmax(760px,1.45fr) minmax(360px,.75fr);gap:1.1rem;overflow:auto;padding:.4rem .2rem .8rem}.wc-stage{position:relative;min-width:0}.wc-stage-head{display:flex;justify-content:space-between;align-items:end;margin:0 0 .75rem;color:#fff}.wc-stage-head b{font-size:.88rem;text-transform:uppercase;letter-spacing:.12em;color:#bbf7d0}.wc-stage-head span{color:var(--wc-muted);font-size:.84rem}.wc-bracket{display:grid;gap:.72rem}.wc-bracket-r32{grid-template-columns:repeat(2,minmax(350px,1fr))}.wc-bracket-r16{grid-template-columns:1fr;padding-top:2.1rem;gap:1.44rem}.wc-bracket-match{position:relative;display:grid;gap:.42rem;padding:.72rem .78rem .68rem 1rem;border-radius:16px;background:linear-gradient(180deg,rgba(15,23,42,.92),rgba(8,13,25,.96));border:1px solid rgba(148,163,184,.2);box-shadow:0 12px 30px rgba(0,0,0,.22);cursor:pointer}.wc-bracket-match:before{content:"";position:absolute;left:0;top:12px;bottom:12px;width:4px;border-radius:999px;background:linear-gradient(var(--wc-green),var(--wc-blue))}.wc-bracket-match:after{content:"";position:absolute;right:-18px;top:50%;width:18px;border-top:1px solid rgba(226,255,232,.24)}.wc-bracket-r16 .wc-bracket-match:after{display:none}.wc-bracket-match.sel{border-color:rgba(245,158,11,.65);box-shadow:0 0 0 1px rgba(245,158,11,.25),0 0 30px rgba(245,158,11,.18)}.wc-bracket-match.sel:before{background:var(--wc-amber);box-shadow:0 0 16px rgba(245,158,11,.55)}.wc-match-meta{display:flex;justify-content:space-between;gap:.5rem;align-items:center;color:var(--wc-muted);font-size:.72rem;text-transform:uppercase;letter-spacing:.08em}.wc-match-meta b{color:#dbeafe;font-size:.76rem}.wc-bracket-team{display:flex;justify-content:space-between;align-items:center;gap:.75rem;min-height:32px;padding:.45rem .55rem;border-radius:11px;background:rgba(255,255,255,.045);border:1px solid rgba(255,255,255,.06);font-weight:900}.wc-bracket-team small{color:var(--wc-muted);font-weight:800;font-size:.72rem}.wc-bracket-team.placeholder{color:var(--wc-muted);font-weight:800}.wc-vs-line{display:flex;align-items:center;gap:.5rem;color:var(--wc-muted);font-size:.72rem;font-weight:900;text-transform:uppercase}.wc-vs-line:before,.wc-vs-line:after{content:"";height:1px;flex:1;background:rgba(226,255,232,.14)}.wc-path-label{color:var(--wc-muted);font-size:.75rem}.wc-sources{font-size:.85rem;color:var(--wc-muted)}@media(max-width:900px){.wc-dashboard{grid-template-columns:1fr}.wc-hero-kpis{grid-template-columns:repeat(2,1fr)}.wc-toolbar{position:static}.wc-panel-head{display:block}}@media(max-width:900px){.wc-knockout-board{grid-template-columns:1fr}.wc-bracket-r32{grid-template-columns:1fr}.wc-bracket-r16{padding-top:0}.wc-bracket-match:after{display:none}}@media(max-width:560px){.wc-page{padding:.5rem}.wc-hero{padding:1.35rem}.wc-hero-kpis{grid-template-columns:1fr}.wc-score-row{grid-template-columns:1fr 42px 10px 42px 1fr;font-size:.8rem}.wc-knockout-board{margin:0 -.6rem;padding:.2rem .6rem .8rem}.wc-bracket-match{padding:.65rem}}
.wc-h2h-record{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:.6rem;margin:.8rem 0}.wc-h2h-record div{padding:.75rem;border:1px solid rgba(255,255,255,.1);border-radius:16px;background:rgba(255,255,255,.055)}.wc-h2h-record b{display:block;font-size:1.35rem;color:#fff}.wc-h2h-record span{display:block;margin-top:.2rem;color:var(--wc-muted);font-size:.78rem;line-height:1.25}@media(max-width:720px){.wc-h2h-record{grid-template-columns:repeat(2,minmax(0,1fr))}}
</style>

<div class="wc-page">
  <div class="wc-pitch-mark wc-pitch-mark--left" aria-hidden="true"></div>
  <div class="wc-pitch-mark wc-pitch-mark--right" aria-hidden="true"></div>
  <header class="wc-hero">
    <span class="wc-live-pill"><i class="wc-live-dot"></i> Live scenario board</span>
    <h1>2026 월드컵 전적 현황판</h1>
    <p>48개국 · 12개 조 · 조 1/2위 + 3위 상위 8팀. 스코어를 입력하면 조별 순위, 3위 커트라인, 공식 32강 대진표와 선택 국가 경로가 실시간으로 바뀐다.</p>
    <div class="wc-hero-kpis" id="wc-hero-kpis"></div>
  </header>

  <section class="wc-toolbar wc-panel">
    <div class="wc-control-left">
      <div class="wc-toggle" aria-label="국가 표시 언어">
        <button id="locale-ko" type="button">🇰🇷 국기+국문</button>
        <button id="locale-en" type="button">🇬🇧 Flag+English</button>
      </div>
      <label>선택 국가 <select id="team-select" class="wc-select"></select></label>
    </div>
    <div class="wc-control-right">
      <button id="reset-scores" class="wc-btn" type="button">초기 스코어로 리셋</button>
    </div>
  </section>

  <section class="wc-section wc-dashboard">
    <div class="wc-panel">
      <div class="wc-panel-head"><div><h2>최근 입력 전적</h2><p class="wc-note">입력된 경기만 스코어보드처럼 표시한다.</p></div></div>
      <div id="wc-scoreboard" class="wc-scoreboard"></div>
    </div>
    <div class="wc-panel">
      <div class="wc-panel-head"><div><h2>3위 커트라인</h2><p class="wc-note">현재 8위와 9위 경계.</p></div></div>
      <div id="wc-cutline" class="wc-mini-list"></div>
    </div>
    <div class="wc-panel">
      <div class="wc-panel-head"><div><h2>선택 국가</h2><p class="wc-note">현재 입력값 기준 예상 경로.</p></div></div>
      <div id="wc-team-path"></div>
    </div>
  </section>

  <section class="wc-section wc-panel">
    <div class="wc-panel-head">
      <div><h2>경기 결과 입력</h2><p class="wc-note">빈 칸에 남은 경기 스코어를 넣으면 현황판 전체가 즉시 재계산된다.</p></div>
    </div>
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

  <section class="wc-section wc-panel wc-knockout-panel">
    <div class="wc-panel-head">
      <div>
        <h2>토너먼트 대진표</h2>
        <p class="wc-note">공식 32강 슬롯과 16강 연결 경로. 3위팀 배치는 495개 조합 lookup table로 계산한다.</p>
      </div>
      <div class="wc-bracket-legend"><span></span> 선택 국가 하이라이트</div>
    </div>
    <div class="wc-knockout-board">
      <section class="wc-stage wc-stage-r32">
        <div class="wc-stage-head"><b>Round of 32</b><span>32강</span></div>
        <div id="wc-r32" class="wc-bracket wc-bracket-r32"></div>
      </section>
      <section class="wc-stage wc-stage-r16">
        <div class="wc-stage-head"><b>Round of 16</b><span>16강 경로</span></div>
        <div id="wc-r16" class="wc-bracket wc-bracket-r16"></div>
      </section>
    </div>
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
