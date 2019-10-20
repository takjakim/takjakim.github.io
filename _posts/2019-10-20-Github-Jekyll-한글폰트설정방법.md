---
layout: single
classes: wide
author_profile: true
read_time: true
share: true
related: true
title: Jekyll 한글폰트 설정방법
excerpt:  Jekyll 에서 한글 나눔고딕폰트 설정방법
toc: true
toc_label: "Contents"
header:
  image: /assets/images/nanum.png
  caption: "**한글폰트** custom setting"
categories: [DEV]
tags:
  - takjakim
  - jekyll
  - font
  - blog
comments: true
breadcrumbs: true
---

## 들어가며


+ 이번에 `userid.github.io` 를 통한 홈페이지*(blog)* 를 구축하면서 찾아본 내용들을 아카이브하고자 남기는 글입니다.
+ 기본적으로 `macOS` 에서 개발할 경우 `safari` 에서는 한글font가 홈페이지와 괴리 없이 어울리지만 윈도우 및 기타 디바이스에서 확인할 경우 폰트가 이상한 경우가 있다.
+ 블로그 첫  `_post` 는 한글폰트(나눔고딕) 설정방법에 대해 알아보겠다.



## How to?

---

```scss
@import url(https://fonts.googleapis.com/earlyaccess/nanumgothiccoding.css);//google web font added
```

* 위의 코드를 복사(⌘+C) 한다
* `assets/css/main.scss` 파일에 위에서 복사한 코드를 붙여넣기(⌘+V)한다

~~~scss
---
# Only the main Sass file needs front matter (the dashes are enough)
---
@charset "utf-8";
@import "minimal-mistakes/skins/{{ site.minimal_mistakes_skin | default: 'default' }}"; // skin
@import "minimal-mistakes"; // main partials
@import url(https://fonts.googleapis.com/earlyaccess/nanumgothiccoding.css);//google web font added
~~~

## 주의할점

---

~~~scss
@import url(https://fonts.googleapis.com/earlyaccess/nanumgothiccoding.css);//google web font added
~~~

스크립트를 잘 보면 `https://fonts. ...` 로 구성되어 있다. SSL이 적용된 홈페이지의 경우 꼭 `https` 의 주소에서 `@import` 해야 원활하게 폰트를 가져올 수 있다



## reference

* [hesu.github.io](http://hesu.github.io/programming/jekyll/2016/04/08/jekyllblog-adding-fonts.html){: target="_blank" }

* [Minimal-mistakes](https://github.com/mmistakes/minimal-mistakes/issues/1352){: target="_blank" }

