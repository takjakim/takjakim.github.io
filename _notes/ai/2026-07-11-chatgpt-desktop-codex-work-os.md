---
title: "ChatGPT desktop에 Codex가 들어간 이유: 챗봇이 아니라 작업 운영체제가 되려는 신호"
date: 2026-07-11 19:36:00 +0900
last_modified_at: 2026-07-11 19:36:00 +0900
categories: [ai]
type: note
tags: [ChatGPT, Codex, AI에이전트, 코딩에이전트, 업무자동화, 개발도구, 에이전틱AI]
description: "ChatGPT desktop 앱에 Codex가 들어간 변화는 단순한 앱 통합이 아니라, ChatGPT가 채팅 도구에서 로컬 프로젝트·파일·Git·스케줄 작업을 다루는 작업 운영체제로 이동하고 있다는 신호다."
excerpt: "Codex가 ChatGPT desktop 안으로 들어간 이유는 코딩 기능을 붙인 것이 아니라, AI가 작업을 맡고 사람은 지시·검토·승인하는 구조로 제품 중심이 이동하고 있기 때문이다."
image: /assets/images/ai/chatgpt-desktop-codex-work-os-2026-og.jpg
permalink: /ai/chatgpt-desktop-codex-work-os/
---

<figure class="note-cover">
  <img src="/assets/images/ai/chatgpt-desktop-codex-work-os-2026-og.jpg" alt="ChatGPT desktop과 Codex 통합 분석 SEO 이미지">
  <figcaption>ChatGPT desktop 안에서 Codex는 별도 코딩 앱이라기보다 로컬 프로젝트, Git, 파일, 브라우저, 스케줄 작업을 다루는 개발자용 작업 모드에 가까워지고 있다.</figcaption>
</figure>

ChatGPT desktop 앱에 Codex가 들어간 것을 처음 보면 약간 이상하게 느껴진다. ChatGPT는 대화형 AI 앱이고, Codex는 개발자를 위한 코딩 에이전트처럼 보였기 때문이다. 그런데 OpenAI의 최신 문서들을 보면 이 변화는 단순한 앱 통합이 아니다.

내가 보기에는 방향이 꽤 분명하다.

> ChatGPT는 더 이상 “질문하면 답하는 챗봇”만으로 남으려 하지 않는다.  
> 로컬 파일, 브라우저, 앱, Git, 스케줄 작업을 묶어 다루는 **작업 운영체제**가 되려는 쪽으로 움직이고 있다.

Codex는 그 안에서 개발자용 작업 모드가 된 것이다.

## Chat, Work, Codex라는 세 갈래

OpenAI의 ChatGPT desktop 문서는 작업을 시작할 때 사용자가 Chat, Work, Codex 중 하나를 선택하는 흐름을 보여준다.[^quickstart] 이 구분이 중요하다.

| 모드 | 주된 역할 |
|---|---|
| Chat | 빠른 질문, 대화, 아이디어 탐색 |
| Work | 문서, 분석, 파일, 업무 산출물 만들기 |
| Codex | 코드베이스, Git, 개발자 도구, 병렬 코딩 작업 |

즉 Codex는 ChatGPT와 별개의 세계가 아니라 ChatGPT 안의 한 작업 방식으로 들어왔다. 질문에 답하는 AI, 문서를 만드는 AI, 코드를 고치는 AI가 서로 다른 앱으로 흩어져 있는 것이 아니라 하나의 desktop 앱 안에서 작업 유형별로 나뉘는 구조다.

이건 꽤 큰 제품 방향 전환이다. 예전에는 “AI에게 물어보기”가 중심이었다면, 이제는 “AI에게 일을 맡기고 결과를 검토하기”가 중심이 된다.

## Codex는 코딩 답변기가 아니라 작업자에 가까워졌다

Codex가 단순히 코드 조각을 추천하는 도구라면 굳이 ChatGPT desktop 안에 깊게 들어올 필요가 없다. 웹에서 답변해도 되고, IDE 확장으로 남아도 된다.

하지만 지금 OpenAI 문서에서 Codex는 훨씬 더 작업자에 가깝다. Windows 문서는 ChatGPT desktop app이 병렬 작업, worktree, scheduled tasks, Git 기능, 내장 브라우저, 파일 미리보기, plugins, skills를 지원한다고 설명한다.[^windows]

이 말은 Codex가 “코드 알려줘” 수준을 넘어서 다음과 같은 일을 맡는다는 뜻이다.

- 로컬 프로젝트 폴더를 읽고 수정하기
- 여러 작업을 병렬로 진행하기
- Git worktree로 변경사항을 격리하기
- 브라우저나 파일 미리보기로 결과 확인하기
- 반복 작업을 scheduled task로 돌리기
- 필요하면 플러그인과 skill을 붙여 더 복잡한 절차 수행하기

이 정도가 되면 Codex는 더 이상 챗봇 기능 하나가 아니다. 개발자의 작업 환경 안에서 움직이는 [[에이전틱 AI|AI 에이전트]]다.

## 핵심은 worktree다

내가 가장 중요하게 본 기능은 Git worktree다.

OpenAI의 worktree 문서는 ChatGPT desktop app에서 Codex가 같은 프로젝트 안의 여러 독립 작업을 서로 방해하지 않고 병렬로 실행할 수 있다고 설명한다.[^worktrees] Git 저장소에서는 scheduled task도 별도의 background worktree에서 실행될 수 있다.

이 구조가 의미하는 바는 크다. 사용자는 한 프로젝트에서 이런 식으로 일을 나눠 맡길 수 있다.

- 이 버그 원인 찾아봐.
- 이 기능을 별도 브랜치처럼 구현해봐.
- 문서만 정리해봐.
- 테스트 깨지는 이유를 확인해봐.
- 매일 아침 의존성 업데이트 이슈를 점검해봐.

각 작업이 같은 파일을 동시에 건드리면 위험하다. 그래서 worktree가 필요하다. 작업 단위마다 독립된 체크아웃을 만들고, 나중에 사람이 비교·검토·병합할 수 있게 하는 것이다.

이건 “AI가 코드를 잘 짠다”보다 더 중요한 변화다. AI가 여러 개의 작업 흐름을 동시에 맡을 수 있게 되면 사람의 역할은 코드를 직접 치는 사람에서 **작업을 나누고, 결과를 비교하고, 병합 여부를 판단하는 사람**으로 이동한다.

## 데스크톱 앱이 필요한 이유

Codex가 웹 안에만 있으면 로컬 작업을 제대로 하기 어렵다. 개발 작업은 추상적인 대화가 아니라 구체적인 작업 환경 위에서 일어난다.

- 파일을 읽어야 한다.
- 테스트를 돌려야 한다.
- Git diff를 봐야 한다.
- 브라우저에서 결과를 확인해야 한다.
- 때로는 데스크톱 앱이나 GUI를 조작해야 한다.

OpenAI의 Computer Use 문서는 ChatGPT desktop app에서 ChatGPT가 macOS나 Windows의 그래픽 UI를 보고 조작할 수 있다고 설명한다.[^computer-use] 커맨드라인이나 구조화된 통합만으로 확인하기 어려운 데스크톱 앱 테스트, 브라우저 사용, 앱 설정 변경, GUI 버그 재현 같은 작업을 위한 기능이다.

이 지점에서 ChatGPT desktop의 의미가 선명해진다. 웹챗은 대화에는 좋지만, 로컬 작업에는 한계가 있다. desktop app은 AI가 실제 작업 환경에 접근하는 접점이다.

그래서 Codex가 desktop 안으로 들어간 것은 자연스럽다. 코딩 에이전트가 진짜 일을 하려면 로컬 파일, 실행 환경, 브라우저, 앱, 권한 관리가 필요하기 때문이다.

## scheduled task는 AI를 비서가 아니라 운영자로 만든다

또 하나 중요한 기능은 scheduled task다.

OpenAI 문서는 ChatGPT desktop app에서 scheduled tasks가 로컬 프로젝트와 함께 동작할 수 있고, 프로젝트 디렉터리나 격리된 worktree에서 실행될 수 있다고 설명한다.[^scheduled] 웹 작업은 업로드한 파일이나 연결 도구를 쓸 수 있지만, 컴퓨터의 로컬 폴더나 worktree를 직접 유지하지는 못한다.

이 차이가 크다. scheduled task가 로컬 프로젝트와 연결되면 AI는 단발성 답변자가 아니라 반복 운영자가 된다.

예를 들어 개발 환경에서는 이런 일이 가능해진다.

- 매일 아침 깨진 테스트 확인
- 오래된 dependency 점검
- GitHub issue 요약
- 문서와 코드 불일치 탐지
- 블로그 repo의 링크 깨짐 확인
- 주기적인 데이터 업데이트와 배포 확인

이건 내가 Hermes cron을 쓰면서 느끼는 지점과도 비슷하다. AI가 유용해지는 순간은 한 번 답을 잘하는 때만이 아니다. **반복되는 일을 맥락과 규칙 안에서 계속 점검할 때** AI는 업무 인프라가 된다.

## 결국 사람은 agent boss가 된다

이 흐름은 최근 AI 에이전트 논의와도 연결된다. Microsoft WorkLab은 모든 직원이 “agent boss”가 된다고 표현했다. 내가 이전 글에서 썼듯이, AI가 10명의 일을 해오면 사람은 10배 편해지는 것이 아니라 10명의 결과를 책임지는 사람이 된다.[^agent-boss]

Codex가 ChatGPT desktop에 들어간 것도 같은 방향이다. 사용자는 더 이상 단순히 “코드 알려줘”라고 묻는 사람이 아니다. 여러 에이전트 작업을 배정하고, 결과를 검토하고, 병합하고, 실패했을 때 되돌릴 책임을 가진 사람이 된다.

그래서 중요한 역량도 달라진다.

| 예전 개발 생산성 | 에이전트 시대 개발 생산성 |
|---|---|
| 내가 얼마나 빨리 구현하는가 | AI 작업을 얼마나 잘 나누는가 |
| 코드 작성량 | 검토 가능한 변경 단위 |
| IDE 숙련도 | 작업 지시, diff 검토, 테스트 설계 |
| 단일 작업 집중 | 병렬 작업 관리 |
| 직접 실행 | 승인·병합·롤백 구조 |

이 관점에서 보면 Codex 통합은 개발자를 대체한다는 이야기보다 개발자의 관리 범위를 넓히는 이야기다. 개발자는 직접 구현자이면서 동시에 작은 AI 개발팀의 리뷰어가 된다.

## ChatGPT는 어디로 가고 있나

OpenAI의 desktop 문서는 ChatGPT desktop app을 쓸 상황으로 “여러 프로젝트를 조율하기”, “파일을 만들고 검토하기”, “브라우저와 컴퓨터를 사용하기”, “반복 작업을 스케줄링하기”를 든다.[^desktop]

이 문장들을 이어보면 제품의 방향이 보인다.

ChatGPT는 더 이상 텍스트 상자 하나가 아니다. 사용자가 일을 설명하면 AI가 파일을 만들고, 브라우저를 열고, 앱을 조작하고, Git 작업을 나누고, 반복 작업을 예약하는 곳으로 확장되고 있다.

나는 이걸 **AI 업무 OS**에 가까운 방향이라고 본다. 운영체제라는 말이 과장처럼 들릴 수 있지만, 적어도 사용자 경험의 중심은 그렇게 이동하고 있다.

- 질문한다.
- 작업을 맡긴다.
- 프로젝트를 연다.
- 파일을 만든다.
- 브라우저를 쓴다.
- 로컬 앱을 조작한다.
- 스케줄을 건다.
- 결과를 검토한다.

이 모든 것이 하나의 앱 안으로 들어오면 ChatGPT는 단순한 AI 답변창이 아니라 작업을 배치하고 회수하는 인터페이스가 된다.

## 그래서 Codex는 왜 합쳐졌나

정리하면 이유는 다섯 가지다.

첫째, Codex가 단순 코딩 답변기가 아니라 로컬 프로젝트를 다루는 작업 에이전트가 되었기 때문이다.

둘째, 코딩 작업에는 파일, Git, 테스트, 브라우저, 앱 권한이 필요하고, 이건 desktop 앱이 가장 자연스럽게 제공할 수 있기 때문이다.

셋째, 일반 업무와 개발 업무의 경계가 흐려졌기 때문이다. PRD를 쓰고, 데이터를 정리하고, 자동화를 만들고, 웹페이지를 수정하는 일은 Work와 Codex 사이를 오간다.

넷째, 병렬 에이전트 작업을 관리하려면 채팅창보다 프로젝트·thread·worktree·Git 상태를 함께 보는 화면이 필요하기 때문이다.

다섯째, OpenAI가 ChatGPT를 “답변 앱”에서 “작업 허브”로 옮기려 하기 때문이다.

## 내 결론

ChatGPT desktop에 Codex가 들어간 것은 “코딩 기능 추가” 정도로 볼 일이 아니다. 더 큰 신호는 ChatGPT의 중심이 대화에서 작업으로 이동하고 있다는 점이다.

앞으로 AI 도구의 경쟁은 단순히 누가 더 똑똑한 답을 하는가에서 끝나지 않을 것이다. 누가 사용자의 실제 작업 환경에 더 안전하게 들어가고, 여러 작업을 더 잘 나누고, 결과를 더 검토 가능하게 만들며, 사람이 책임질 수 있는 구조로 돌려주는가가 중요해질 것이다.

Codex는 그 변화의 개발자 버전이다.

AI는 답변을 넘어 작업을 맡기 시작했고, 사람은 프롬프트 작성자를 넘어 작업 관리자와 [[검증|검증자]]가 되고 있다.

[^desktop]: OpenAI Developers, “ChatGPT desktop app.” <https://developers.openai.com/codex/app>
[^quickstart]: OpenAI Developers, “Quickstart.” <https://developers.openai.com/codex/quickstart>
[^windows]: OpenAI Developers, “Windows sandbox.” <https://developers.openai.com/codex/windows>
[^worktrees]: OpenAI Developers, “Worktrees.” <https://developers.openai.com/codex/app/worktrees>
[^computer-use]: OpenAI Developers, “Computer Use.” <https://developers.openai.com/codex/app/computer-use>
[^scheduled]: OpenAI Developers, “Scheduled tasks.” <https://developers.openai.com/codex/app/automations>
[^agent-boss]: 이전 글, 「[[AI 에이전트 시대의 진짜 병목은 작성이 아니라 책임이다]]」.
