---
layout: single
classes: wide
author_profile: true
read_time: true
share: true
related: true
title: Safari 창을 그대로 Chrome에서 실행하기
excerpt:  Safari 창을 그대로 Chrome에서 실행하기
toc: true
toc_label: "Contents"

header:
  image: /assets/images/1910/automator/2.png
  caption: "**Automator** tip"
categories:
  - dev
  - macOS
tags:
  - takjakim
  - Automator
comments: true
breadcrumbs: true
---

## YouTube 실습

{% include youtube.html id="CznQ-b23mBc" %}

## 들어가며

* 종종 맥으로 웹서핑을 하다보면 `safari` 에서 보던 창을 `chrome` 에서 봐야할 필요가 있을때가 있습니다 *(유튜브4K는 safari에서는 지원하지 않아  chrome으로 켜야 합니다)*
* `macOS` 에 기본으로 탑재되어 있는 `Automator` 를 활용하여 무료로 구현해보겠습니다 *(참고로 유료구매시 340엔)*

## Automator 켜기

* Launchpad →  Utility →  Automator (혹은 `spotlight` 를 켜고 `Automator` 입력)

![Automator실행](/assets/images/1910/automator/1.png )

* 좌측 `라이브러리` → `인터넷` →  `safari` 에서 `현재의 웹페이지 가져오기` →  드래그해서 오른쪽 `workflow` 창으로 놓기

![Automator설정](/assets/images/1910/automator/4.png )

## AppleScript


~~~typescript
on run {input, parameters}
repeat with theURL in input
tell application "Google Chrome" to open location theURL
end repeat
return input 
end run
~~~

![AppleScript](/assets/images/1910/automator/2.png )

+ `라이브러리` →  `AppleScript 실행` →  위의 스크립트 복사(⌘+C) / 붙여넣기(⌘+V)
+ 상단의 작업흐름 수신 →  입력없음 선택
+ 편한 이름으로 저장 `ex. 사파리 크롬 전환`

![AppleScript](/assets/images/1910/automator/3.png )

+ 시스템 환경설정 →  키보드 →  단축키 →  서비스 →  본인이 저장한 이름을 찾아 적당한 단축키 설정 (⌘+ ctrl + S)
+ 이동시킬 `safari` 창을 띄운 후 아무곳에서 단축키 입력
+ 크롬에서 열리는 것을 확인하기



## Wrapup


위의 과정이 귀찮다~ 이말이야

[Workflow Download](https://drive.google.com/file/d/1EuFiK63aOotB3LlLSIpP9UW69HjuKn1G/view?usp=sharing){: target="_blank" } 

클릭하여 다운로드 후, 시스템 환경설정 →  키보드 →  단축키 →  서비스 →  본인이 저장한 이름을 찾아 적당한 단축키 설정 (⌘+ ctrl + S) 부터 실행

[맥러닝 간편하게 구독하기](https://www.youtube.com/channel/UCwq1IYf7GhmJgJtqjbBX1IA?sub_confirmation=1){: target="_blank" } 

 