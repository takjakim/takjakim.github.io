---
title: "팀으로 Claude Code 돌릴 때: tmux 에이전트 대시보드(실시간 모니터링)"
last_modified_at: 2026-02-11
categories: [dev, project]
tags: [claude-code, dashboard, tmux, monitoring, automation, agent]
description: "tmux pane에 여러 에이전트를 띄워놓고 일할 때, DOING/TODO/DONE·컨텍스트 사용량·압축 타이밍을 한 화면에서 보는 Team Dashboard. 설치/운영 방법까지 정리."
image: /assets/og-default.png
permalink: /dev/claude-code-team-dashboard/
---

# Claude Code Team Dashboard: tmux 에이전트 팀을 한 화면에 모니터링

> 소스: <https://github.com/takjakim/claude-code-team-dashboard>

여러 개의 Claude Code(또는 다른 에이전트)를 tmux pane에 띄워놓고 일하는 순간부터, 상태 확인이 은근히 번거로워진다.

- 지금 누가 **DOING/TODO/DONE** 인지
- 컨텍스트가 **80%/90%**에 가까워졌는지
- 압축(COMPRESS) 타이밍이 왔는지
- 최근에 뭐가 완료됐는지

이 repo는 그걸 **NASA 관제실 느낌의 웹 대시보드**로 한 방에 보여주는 도구다.

## 1) 이 프로젝트가 해결하는 문제

에이전트를 늘리면 생산성이 올라가는 구간이 있다. 대신 아래 비용이 생긴다.

- 상태를 머리로 기억해야 함
- pane 사이를 오가며 확인해야 함
- 컨텍스트 관리(압축/토큰 감각)가 어려워짐

Team Dashboard는 tmux 상태/로그/파일 기반 상태를 수집해서, “지금 팀이 어떻게 돌고 있는지”를 한 화면에 모아준다.

## 2) 기능 요약

- **실시간 상태 모니터링**: 에이전트 상태(DOING/TODO/DONE) 추적
- **컨텍스트 사용량 추적**: 80%/90% 경고
- **활동 피드**: 최근 완료/현재 작업
- **압축 감지**: COMPRESS 필요시 경고
- **데이터 소스 어댑터**: tmux / 로그 파일 / 파일 기반 / 데모

## 3) 빠른 시작(내가 추천하는 방식)

대시보드는 정적 페이지라서, 핵심은 “상태 JSON을 갱신하는 스크립트”를 주기적으로 돌리는 것.

### 3.1 팀 설정(team-config.json)

`team-config.json`에 tmux 세션/윈도우/pane 매핑과 팀원 정보를 적는다.

```json
{
  "tmux": { "session": "my-team", "window": 0 },
  "team": [
    { "pane": 0, "name": "Agent 0", "model": "Claude", "role": "Planner" }
  ]
}
```

### 3.2 상태 업데이터 실행

```bash
watch -n2 ./update-status.sh
```

- tmux pane의 텍스트 패턴을 감지해서 DOING/TODO/DONE으로 분류
- 컨텍스트 사용량/압축 신호도 함께 표시

### 3.3 대시보드 서버

```bash
python3 -m http.server 8080
open http://localhost:8080
```

## 4) tmux 없이도 쓸 수 있음(어댑터)

tmux가 아닌 환경이면 `adapters/`를 사용하면 된다.

- 데모 모드
  ```bash
  watch -n2 ./adapters/demo.sh
  ```
- 파일 기반 상태
  ```bash
  watch -n2 ./adapters/file-based.sh
  ```
- 로그 파서
  ```bash
  LOG_DIR=.claude-logs watch -n2 ./adapters/log-watcher.sh
  ```

## 5) 내가 생각하는 ‘운영 팁’

- **Pane 이름/역할을 고정**하면 대시보드 가치가 커짐 (Planner/Builder/Reviewer 등)
- 임계값(80/90)은 “경고”이지 “실패”가 아니라서, 경고 뜨면 바로 압축하기보다
  - *큰 파일 수정/긴 테스트* 같은 작업 전에 먼저 정리하는 식이 좋음
- 데모/파일 기반 어댑터를 써서 **tmux 없는 팀도** 상태 공유 가능(협업용)

## 6) 연결

- GitHub: <https://github.com/takjakim/claude-code-team-dashboard>
- Dev: [[개발 노트 시작하기]]
