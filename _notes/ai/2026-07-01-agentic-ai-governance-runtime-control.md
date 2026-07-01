---
layout: note
title: "에이전틱 AI 시대의 거버넌스: 윤리 체크리스트에서 런타임 통제로"
categories: [ai]
type: analysis
label: AI
tags: [AI거버넌스, 에이전틱AI, AgenticAI, AI에이전트, 런타임통제, 섀도우AI, ResponsibleAI, 기업AI, AI보안, 프롬프트인젝션, AI위험관리]
description: "에이전틱 AI 시대의 AI 거버넌스를 윤리 체크리스트가 아니라 런타임 통제, 데이터 추적성, 권한 관리, 리더십 책임 구조가 결합된 전사 아키텍처 문제로 정리했다."
date: 2026-07-01 19:55:00 +0900
last_modified_at: 2026-07-01 19:55:00 +0900
permalink: /ai/agentic-ai-governance-runtime-control/
image: /assets/images/ai/agentic-ai-governance-runtime-control-2026-og.jpg
---

기업의 [[AI 거버넌스]]는 더 이상 윤리 원칙을 적어둔 문서나 내부 포털에 올라간 체크리스트만으로는 충분하지 않다. [[에이전틱 AI]]가 기업 데이터에 접근하고, 도구를 호출하고, 시스템 안에서 실제 행동을 수행하기 시작하면 거버넌스는 문서가 아니라 **런타임 통제 아키텍처**가 된다.

<figure class="note-cover-figure">
  <img src="/assets/images/ai/agentic-ai-governance-runtime-control-2026-og.jpg" alt="에이전틱 AI 거버넌스와 런타임 통제 SEO 커버 이미지">
  <figcaption>도식: Lily Kollé, Gartner, EY, IBM, EW Solutions의 공개 자료를 바탕으로 필자의 관점에서 재구성.</figcaption>
</figure>

## 오늘의 핵심

AI 거버넌스 논의는 빠르게 바뀌고 있다. 기존에는 “AI를 윤리적으로 쓰자”, “개인정보를 조심하자”, “승인된 도구만 쓰자” 정도의 원칙이 중심이었다. 물론 여전히 중요하다. 하지만 에이전트가 기업 시스템 안에서 행동하기 시작하면 질문이 달라진다.

> 이 에이전트는 무엇을 볼 수 있고, 무엇을 제안할 수 있으며, 무엇을 실행할 수 있는가?

Gartner는 기업들이 AI 에이전트 거버넌스를 이분법적으로 다루는 것이 실패의 원인이라고 지적한다. 모든 에이전트를 똑같이 잠그거나, 반대로 모두 신뢰하는 방식이 문제라는 것이다. Gartner는 에이전트의 자율성과 접근 범위에 따라 `Observe`, `Advise`, `Act with Approval`, `Act Autonomously`처럼 다른 통제 수준을 적용해야 한다고 설명한다.[^gartner]

IBM도 비슷한 방향을 말한다. AI 에이전트는 기존 생성형 AI 도구와 달리 단순히 답을 생성하는 수준을 넘어 실제 행동을 수행할 수 있다. 그래서 자율성, 설명가능성, 사이버보안, 모니터링, 인간 감독, 비상 중단 장치가 거버넌스의 핵심 요소가 된다.[^ibm]

## 왜 기존 AI 거버넌스로는 부족한가

기존 AI 거버넌스는 대체로 세 가지 방식으로 작동했다.

1. 사용 가능한 AI 도구 목록을 정한다.
2. 입력하면 안 되는 데이터 유형을 정한다.
3. 위험한 사용 사례는 승인 절차를 거치게 한다.

이 방식은 챗봇형 AI나 문서 생성 도구에는 어느 정도 통한다. 하지만 에이전틱 AI에서는 부족하다. 에이전트는 답변만 하는 것이 아니라 도구를 호출하고, API를 사용하고, 업무 시스템에 접근하고, 때로는 사용자의 개별 승인 없이 다음 단계를 이어갈 수 있다.

Lily Kollé의 Medium 글은 대기업이 이미 큰 [[섀도우 AI]] 문제를 갖고 있다고 지적한다. 정책이 SharePoint 같은 내부 저장소에 올라가 있어도, 실제 현업 워크플로우 안에서 작동하지 않으면 규제가 도움이 되지 않는다는 문제의식이다.[^kolle]

이 말은 꽤 현실적이다. 회사에 AI 사용규정이 있어도 직원이 개인 계정으로 외부 AI 도구를 쓰거나, 팀 단위로 승인되지 않은 자동화 워크플로우를 만들면 거버넌스는 문서 밖으로 밀려난다.

## 에이전틱 AI 거버넌스의 네 층

여러 공개 자료를 종합하면, 에이전틱 AI 시대의 거버넌스는 네 층으로 봐야 한다.

| 층 | 질문 | 필요한 통제 |
|---|---|---|
| 리더십 책임 | 누가 최종 책임을 지는가 | 이사회, C-Suite, 책임위원회 |
| 가치·리스크 정렬 | 왜 이 AI를 쓰는가 | 사업가치, 위험등급, 사용 목적 |
| 데이터·자산 추적 | 무엇에 접근하는가 | 데이터 계보, 권한, 자산 목록 |
| 런타임 통제 | 실제로 무엇을 하는가 | 로그, 모니터링, 승인 게이트, 중단 장치 |

EY는 Responsible AI가 단순 컴플라이언스가 아니라 성과 레버라고 말한다. EY의 Responsible AI Pulse Survey 기반 글에 따르면 책임 있는 AI 실행은 원칙 수립에서 끝나지 않고, KPI, 교육, 전담 예산, 실시간 모니터링, 감독위원회, 독립 평가로 이어져야 한다.[^ey]

EW Solutions는 AI를 확장하기 전에 데이터 거버넌스와 자산 관리 체계가 먼저 있어야 한다고 강조한다. 어떤 데이터가 어디서 왔고, 어떤 모델이나 AI 시스템에 들어갔는지 추적할 수 없으면 AI 판단의 책임도 흐려진다.[^ew]

즉 좋은 AI 거버넌스는 하나의 위원회나 하나의 정책 파일이 아니다. 리더십, 데이터, 보안, 현업, 법무, IT 운영이 함께 작동하는 **Full-Stack Governance**에 가깝다.

## 핵심 전환: 사전 승인에서 런타임 통제로

에이전틱 AI의 핵심 문제는 속도다. 사람이 모든 행동을 사전에 검토하면 업무 자동화의 장점이 사라진다. 반대로 아무 통제 없이 실행하게 두면 데이터 유출, 오작동, 잘못된 고객 응대, 규정 위반이 순식간에 커질 수 있다.

그래서 필요한 것이 [[런타임 텔레메트리]]다. 쉽게 말하면 에이전트가 실제 실행 중에 무엇을 보고, 무엇을 호출하고, 어떤 결정을 내리고, 어떤 시스템을 변경했는지 실시간으로 관찰하는 구조다.

Gartner는 자율 에이전트가 인간 감독보다 빠른 속도와 규모로 행동할 수 있다고 지적한다. 그래서 에이전트의 자율성 수준에 따라 접근권한, 승인 흐름, 로그, 보안 테스트, 사고 대응 절차를 다르게 설계해야 한다.[^gartner]

여기서 중요한 것은 모든 에이전트를 똑같이 통제하지 않는 것이다.

| 에이전트 유형 | 예시 | 통제 방향 |
|---|---|---|
| 관찰형 | 문서 검색, 요약, 질의응답 | 접근 범위, 로그, 인증 |
| 조언형 | 보고서 초안, 의사결정 지원 | 정확도, 환각 테스트, 사용자 교육 |
| 승인 후 실행형 | 메일 발송, 설정 변경, 데이터 입력 | 승인 워크플로우, 감사추적, 사고 대응 |
| 자율 실행형 | 반복 업무 자동 실행, 다중 시스템 조정 | 강한 권한관리, 실시간 모니터링, 킬스위치 |

이 구조가 없으면 두 가지 문제가 생긴다. 단순 요약 에이전트는 과도하게 막혀서 현업이 우회하고, 자율 실행 에이전트는 너무 느슨하게 풀려서 사고를 만든다.

## 인간은 어디에 개입해야 하나

에이전틱 AI 거버넌스에서 흔한 오해는 “중요한 것은 모두 사람이 승인하면 된다”는 생각이다. 하지만 현실적으로 모든 행동을 사람이 승인할 수는 없다. 승인 요청이 많아지면 사람은 지치고, 승인 버튼은 형식이 된다.

그래서 인간 개입은 더 정교하게 설계되어야 한다.

- 저위험 반복 작업은 기계적 정책과 로그로 통제한다.
- 중간 위험 작업은 명확한 승인 워크플로우를 둔다.
- 고위험 판단은 인간의 의미 있는 검토를 요구한다.
- 윤리·법무·고객 신뢰와 연결된 판단은 에스컬레이션한다.

이것이 [[Human-in-the-loop]]의 현실적인 형태다. 모든 루프에 인간을 넣는 것이 아니라, 인간이 꼭 판단해야 하는 지점을 설계하는 것이다.

## 좋은 AI 거버넌스의 KPI

AI 거버넌스의 성과를 “규정이 있는가”로만 보면 실패한다. 진짜 봐야 할 것은 운영 지표다.

| 지표 | 의미 |
|---|---|
| 승인되지 않은 AI 사용 탐지율 | 섀도우 AI를 얼마나 발견하는가 |
| 에이전트 오작동 감지 시차 | 사고를 얼마나 빨리 알아차리는가 |
| 권한 초과 시도 차단률 | 에이전트가 허용 범위를 넘을 때 막는가 |
| 데이터 출처 추적 가능성 | 어떤 데이터가 AI 판단에 쓰였는지 설명되는가 |
| 고위험 사용사례 승인 리드타임 | 통제가 현업 속도를 과도하게 늦추지 않는가 |
| 사고 후 복구 시간 | 문제가 생겼을 때 얼마나 빨리 멈추고 되돌리는가 |

EY의 글도 책임 있는 AI가 비용만 늘리는 장치가 아니라, AI 투자를 실제 성과로 연결하는 성과 레버가 될 수 있다고 본다.[^ey] 이 관점이 중요하다. 거버넌스는 브레이크만이 아니다. 제대로 설계된 거버넌스는 조직이 AI를 더 과감하게 배포할 수 있게 해주는 안전한 가속 페달이다.

## 조직이 지금 점검해야 할 것

기업이 에이전틱 AI를 도입하려면 최소한 다음 질문에 답해야 한다.

1. 우리 조직에서 승인 없이 쓰이는 AI 도구와 워크플로우는 무엇인가?
2. AI 에이전트가 접근할 수 있는 데이터와 시스템은 어디까지인가?
3. 읽기, 추천, 실행, 자율 실행을 구분한 권한 체계가 있는가?
4. 에이전트 행동 로그를 실시간으로 볼 수 있는가?
5. 고위험 행동에는 의미 있는 인간 승인 절차가 있는가?
6. 문제가 생겼을 때 중단·롤백·보고 라인이 있는가?
7. AI 거버넌스가 법무팀 문서가 아니라 현업 워크플로우 안에서 작동하는가?

이 질문에 답하지 못한다면, 조직은 AI를 쓰는 것이 아니라 AI 사용이 조직 안에서 퍼지는 것을 뒤늦게 따라가고 있을 가능성이 크다.

## 한 문장으로 정리하면

에이전틱 AI 시대의 거버넌스는 윤리 체크리스트가 아니라 **전사 운영 아키텍처**다. 정책은 필요하지만 충분하지 않다. AI 에이전트가 실제로 무엇을 볼 수 있고, 무엇을 할 수 있으며, 문제가 생겼을 때 누가 멈출 수 있는지를 설계해야 한다.

앞으로 좋은 AI 조직은 “AI를 금지하지 않는 조직”도, “AI를 마음대로 쓰게 하는 조직”도 아닐 것이다. 좋은 조직은 AI의 자율성을 단계별로 나누고, 데이터와 권한을 추적하며, 런타임에서 행동을 관찰하고, 인간이 개입해야 할 지점을 정확히 설계하는 조직이다.

## 확인한 출처

- [Lily Kollé, 「How to Design AI Governance for Enterprise」, Medium / Bootcamp](https://medium.com/design-bootcamp/how-to-design-ai-governance-for-enterprise-f83c06e2be91)
- [Gartner, 「Gartner Says Applying Uniform Governance Across AI Agents Will Lead to Enterprise AI Agent Failure」](https://www.gartner.com/en/newsroom/press-releases/2026-05-26-gartner-says-applying-uniform-governance-across-ai-agents-will-lead-to-enterprise-ai-agent-failure)
- [EY, 「How responsible AI translates investment into impact」](https://www.ey.com/en_gl/insights/ai/how-can-responsible-ai-bridge-the-gap-between-investment-and-impact)
- [IBM Think, 「AI Agent Governance: Big Challenges, Big Opportunities」](https://www.ibm.com/think/insights/ai-agent-governance)
- [EW Solutions, 「The Enterprise AI Governance Framework: What You Need Before You Scale AI」](https://www.ewsolutions.com/the-enterprise-ai-governance-framework/)

[^kolle]: Lily Kollé, 「How to Design AI Governance for Enterprise」, Medium / Bootcamp, 2026. 6. 24. Medium 회원 전용 글이라 공개 추출 가능한 범위의 요지와 제목·서지 정보를 확인했다.
[^gartner]: Gartner, 「Gartner Says Applying Uniform Governance Across AI Agents Will Lead to Enterprise AI Agent Failure」, 2026. 5. 26.
[^ey]: EY, 「How responsible AI translates investment into impact」, 2025. 10. 8.
[^ibm]: IBM Think, 「AI Agent Governance: Big Challenges, Big Opportunities」.
[^ew]: EW Solutions, 「The Enterprise AI Governance Framework: What You Need Before You Scale AI」.
