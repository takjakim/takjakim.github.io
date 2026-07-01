---
layout: note
title: "LLM Wiki: RAG 이후의 지식관리 방식"
categories: [ai]
type: analysis
label: AI
tags: [LLMWiki, RAG, DigitalGarden, 지식관리, Obsidian, AI에이전트, 백링크, 개념노트, 컨텍스트관리]
description: "Andrej Karpathy가 제안한 LLM Wiki를 RAG와 비교하며, 원문을 반복 검색하는 방식에서 벗어나 LLM이 지속적으로 관리하는 마크다운 지식베이스로 보는 관점을 정리했다."
date: 2026-07-01 21:15:00 +0900
last_modified_at: 2026-07-01 21:15:00 +0900
permalink: /ai/karpathy-llm-wiki-digital-garden/
image: /assets/images/ai/karpathy-llm-wiki-digital-garden-2026-og.jpg
---

Andrej Karpathy가 2026년 4월 공개한 `llm-wiki` gist는 짧지만 꽤 중요한 방향 전환을 담고 있다. 핵심은 단순하다. LLM을 문서 검색 도구로만 쓰지 말고, **계속 자라는 마크다운 위키를 유지보수하는 지식 관리자**로 쓰자는 것이다.[^karpathy]

<figure class="note-cover-figure">
  <img src="/assets/images/ai/karpathy-llm-wiki-digital-garden-2026-og.jpg" alt="LLM Wiki와 Digital Garden SEO 커버 이미지">
  <figcaption>도식: Karpathy의 LLM Wiki 아이디어를 필자의 Digital Garden 운영 관점으로 재구성.</figcaption>
</figure>

## 한 문장으로 정리하면

[[LLM Wiki]]는 [[RAG]]처럼 질문할 때마다 원문 조각을 다시 검색하는 방식이 아니라, LLM이 원문을 읽고 요약하고 연결하고 갱신한 **지속형 [[지식베이스]]**를 유지하는 패턴이다.

Karpathy는 이 차이를 아주 선명하게 말한다. 대부분의 LLM+문서 경험은 RAG에 가깝다. 파일을 올리고, 질문할 때 관련 chunk를 검색하고, 답변을 생성한다. 작동은 하지만 매번 지식을 다시 발견한다. 누적이 없다. 반면 LLM Wiki는 새 자료가 들어올 때마다 위키가 갱신되고, 링크가 생기고, 모순이 표시되고, 이전 질문의 좋은 답도 다시 파일로 남는다.[^karpathy]

여기서 중요한 표현이 있다.

> Obsidian is the IDE; the LLM is the programmer; the wiki is the codebase.[^karpathy]

이 문장은 LLM Wiki의 감각을 잘 보여준다. [[Obsidian]]은 지식 작업의 IDE이고, LLM은 코드를 고치듯 위키를 고치는 프로그래머이며, 위키는 계속 리팩터링되는 코드베이스다.

<figure class="note-cover-figure">
  <img src="/assets/images/ai/andrej-karpathy-openai-cc-by-3.png" alt="Andrej Karpathy">
  <figcaption>Andrej Karpathy. Source: Wikimedia Commons, Gladwin Analytics, CC BY 3.0.</figcaption>
</figure>

## RAG는 검색하고, LLM Wiki는 축적한다

RAG는 여전히 유용하다. 원문이 많고, 정확한 근거를 찾아야 할 때 좋다. 하지만 RAG는 기본적으로 **질문 시점의 검색 구조**다. 질문이 들어오면 관련 문서 조각을 찾고, 그 조각을 바탕으로 답한다.

문제는 장기적인 지식 축적이다.

- 같은 문서를 여러 번 다시 읽는다.
- 이전에 발견한 연결이 다음 질문에 자동으로 남지 않는다.
- 모순이나 업데이트 이력이 축적되지 않는다.
- 좋은 답변도 대화창 안에서 사라지기 쉽다.

LLM Wiki는 여기서 출발점이 다르다. 원문을 검색 가능한 상태로만 두지 않고, LLM이 그것을 읽어 **개념 페이지, 인물 페이지, 비교 페이지, 요약 페이지**로 편집한다. 그리고 그 페이지들을 `[[wikilinks]]`로 연결한다.

| 구분 | RAG | LLM Wiki |
|---|---|---|
| 기본 단위 | 원문 chunk | 마크다운 페이지 |
| 작동 시점 | 질문할 때 검색 | 자료가 들어올 때 갱신 |
| 산출물 | 답변 | 지속되는 위키 |
| 강점 | 빠른 근거 검색 | 장기 축적과 재사용 |
| 약점 | 매번 맥락 재조립 | 유지보수 규칙 필요 |

그래서 내 식으로 정리하면 이렇다.

> RAG는 검색의 자동화이고, LLM Wiki는 지식 축적의 자동화다.

## 세 개의 레이어

Karpathy의 구조는 세 층으로 이해하면 쉽다.

### 1. Raw Sources

첫 번째는 원문 레이어다. 논문, 기사, PDF, 회의록, 슬랙 스레드, 강의자료, 책 메모 같은 자료가 여기에 들어간다. 이 레이어는 불변이어야 한다. LLM이 읽을 수는 있지만 고치면 안 된다.

이건 출처 보존의 문제다. 위키가 아무리 잘 정리돼도 원문이 사라지거나 변형되면 검증이 어렵다. 그래서 원문은 source of truth로 남겨둔다.

### 2. Wiki

두 번째가 실제 위키다. 여기에는 LLM이 만든 요약, 개념 노트, 비교표, 인물/기관 페이지, 질문 답변, 종합 정리가 들어간다.

중요한 점은 LLM이 이 레이어를 “소유”한다는 것이다. 물론 최종 판단은 사람이 하지만, 페이지 생성·갱신·링크·인덱스·로그 같은 지식관리의 반복 작업은 LLM이 맡는다.

### 3. Schema

세 번째는 schema 또는 instruction이다. `AGENTS.md`, `CLAUDE.md`, `SCHEMA.md` 같은 파일이 여기에 해당한다. LLM에게 어떤 파일명을 쓰고, 언제 새 페이지를 만들고, 어떤 태그를 허용하고, 어떤 형식으로 출처를 남길지 알려주는 운영 규칙이다.

이게 없으면 LLM Wiki는 금방 노트 더미가 된다. 반대로 schema가 있으면 LLM은 일반 챗봇이 아니라 위키 관리자로 행동한다.

## 인간과 LLM의 역할 분담

LLM Wiki가 흥미로운 이유는 인간을 지식관리에서 배제하지 않는다는 점이다. 오히려 역할을 분리한다.

인간이 할 일:

- 읽을 만한 자료를 고른다.
- 좋은 질문을 던진다.
- 무엇이 중요한지 판단한다.
- 최종 해석과 방향을 정한다.

LLM이 할 일:

- 원문을 요약한다.
- 기존 노트를 찾는다.
- 새 개념 노트를 만든다.
- 관련 페이지를 서로 연결한다.
- 중복과 모순을 표시한다.
- 인덱스와 로그를 갱신한다.

이 역할 분담이 중요하다. LLM에게 “생각을 대신해줘”가 아니라 “지식의 장부를 관리해줘”라고 맡기는 방식에 가깝다.

## 내 Digital Garden과 바로 맞닿는 부분

이 아이디어가 흥미로운 이유는, 지금 이 블로그가 이미 비슷한 방향으로 움직이고 있기 때문이다.

나는 글을 쓸 때 본문 안에 위키링크 형태의 링크를 먼저 심어둔다. 아직 없는 개념도 일부러 남겨둔다. 없는 노드를 클릭하면 404가 아니라 “아직 연결 중인 노드입니다”라는 안내가 나온다. 그리고 [[백링크]]와 graph view를 통해 어떤 글이 어떤 개념과 연결되는지 본다.

이건 완성된 백과사전을 만드는 일이 아니다. 오히려 덜 완성된 지식의 연결 상태를 드러내는 방식이다. [[Digital Garden]]이라는 이름이 잘 맞는 이유도 여기에 있다. 글은 최종본이라기보다, 계속 자라고 다시 연결되는 노드다.

Karpathy의 LLM Wiki는 여기에 LLM 운영자를 붙이는 아이디어다.

- 새 글을 쓰면 관련 위키링크 후보를 심는다.
- 밤에 cron이 missing node를 찾아 컨셉노트 후보를 만든다.
- 기존 노트와 새 글을 연결한다.
- 같은 개념이 여러 이름으로 중복되면 정리한다.
- 좋은 질문과 답변은 다시 노트로 저장한다.

이렇게 되면 블로그는 단순 발행 채널이 아니라, LLM과 함께 유지하는 공개 지식베이스가 된다.

## 중요한 것은 “더 많은 노트”가 아니다

LLM Wiki를 오해하면 모든 자료를 다 노트로 쪼개고, 모든 단어에 링크를 거는 방향으로 갈 수 있다. 그건 별로 좋지 않다. 링크가 너무 많으면 아무 링크도 중요하지 않게 된다.

중요한 것은 선택이다.

- 반복해서 등장하는 개념인가?
- 다른 글과 연결될 가능성이 있는가?
- 나중에 다시 설명해야 할 주제인가?
- 하나의 독립 노트로 자랄 수 있는가?

이 기준을 통과한 것만 노드로 만든다. 나머지는 본문 안에서 지나가도 된다. 좋은 LLM Wiki는 거대한 문서 창고가 아니라, **다시 생각하기 좋은 구조**다.

## 블로그 운영 관점에서의 적용 규칙

내가 이 패턴을 블로그 운영에 적용한다면, 대략 이렇게 정리할 수 있다.

1. 공개 글은 독자가 읽을 수 있는 완결된 글로 쓴다.
2. 글 안에는 5~12개 정도의 핵심 위키링크만 심는다.
3. 없는 노드는 일부러 남겨도 된다.
4. missing node는 나중에 [[개념 노트]] 후보가 된다.
5. 원문·PDF·자료는 내부 raw source로 보존한다.
6. 공개 글에는 확인 가능한 공개 출처만 건다.
7. 좋은 질문에 대한 답은 다시 글이나 노트로 축적한다.
8. 주기적으로 깨진 링크, 고립 노트, 중복 개념을 점검한다.

이 방식은 SEO와도 충돌하지 않는다. 오히려 좋다. 검색엔진 입장에서도 하나의 주제에 대해 서로 연결된 글과 개념 노트가 쌓이면 사이트의 의미 구조가 선명해진다. 다만 독자를 위해 글 자체는 여전히 읽히는 문장으로 남아야 한다.

## 결론: AI가 답하는 시대에서, AI가 지식을 유지하는 시대로

LLM Wiki의 핵심은 “AI가 더 좋은 답을 한다”가 아니다. 핵심은 **AI가 지식의 연결과 유지보수를 맡는다**는 데 있다.

RAG가 문서 검색을 자동화했다면, LLM Wiki는 지식의 편집과 갱신을 자동화한다. 그래서 이 패턴은 단발성 질문보다 장기 연구, 개인 지식관리, 조직 지식관리, 공개 Digital Garden에 더 잘 맞는다.

앞으로 중요한 질문은 “AI에게 무엇을 물을까”만이 아닐 것이다.

> AI와 함께 어떤 지식 구조를 계속 유지할 것인가?

Karpathy의 LLM Wiki는 그 질문에 대한 꽤 실용적인 답이다. 원문은 남겨두고, 위키는 계속 고치고, schema는 점점 좋아지게 만든다. 이건 지식을 저장하는 방식이 아니라, 지식을 **운영하는 방식**에 가깝다.

## 확인한 출처

- [Andrej Karpathy, `llm-wiki`, GitHub Gist](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)
- [Wikimedia Commons, `Andrej Karpathy, OpenAI.png`](https://commons.wikimedia.org/wiki/File:Andrej_Karpathy,_OpenAI.png)

[^karpathy]: Andrej Karpathy, [`llm-wiki`](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f), GitHub Gist, 2026. 4. 4.
