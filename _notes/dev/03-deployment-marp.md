---
title: "마크다운쇼 개발기 3편: 배포"
last_modified_at: 2026-02-07
categories: [dev, project]
tags: [marp, markdown, presentation, nextjs, vercel, deployment, 마크다운쇼, 개발기]
description: "마크다운쇼 Vercel 배포기. 빌드 실패, Puppeteer 삽질, 번들 최적화까지 프로덕션 배포 과정의 트러블슈팅."
permalink: /dev/marp-editor/devlog-3/
image: /assets/images/dev/marp-editor/final-view.png
---

# 마크다운쇼 개발기 3편: 배포

> [[마크다운쇼 개발기 2편: 개발]]을 마치고 세상에 공개하는 시간. 예상치 못한 이슈들과의 싸움.

## Vercel 배포는 쉽다 (원래는)

```bash
npm i -g vercel
vercel
```

끝. GitHub 저장소 연결하면 푸시할 때마다 자동 배포된다.

...라고 생각했다.

## 첫 번째 이슈: 빌드 실패

로컬에서 `npm run build` 잘 되는데 Vercel에서 터졌다.

```
Error: Cannot find module '@marp-team/marp-core'
```

### 원인

`package.json`에서 `dependencies`와 `devDependencies`를 구분 안 하고 다 `devDependencies`에 넣었다.

Vercel은 프로덕션 빌드 시 `devDependencies`를 설치 안 한다.

### 해결

```bash
npm install @marp-team/marp-core pptxgenjs --save
```

`dependencies`로 옮기니까 해결.

## 두 번째 이슈: Puppeteer의 배신

[[02-development|개발편]]에서도 언급했지만, 서버 사이드 PDF 생성이 Vercel에서 안 됐다.

```
Error: spawn ENOEXEC
```

Chromium 바이너리가 실행이 안 되는 거다.

시도해본 것들:
1. `@sparticuz/chromium` 버전 변경 → 실패
2. `puppeteer-core` 버전 다운그레이드 → 실패
3. Vercel 환경변수로 메모리 늘리기 → 실패

결국 **서버 사이드 PDF 생성을 포기**했다.

### 최종 해결책

클라이언트에서 브라우저 인쇄 다이얼로그를 띄우는 방식으로 변경.

```typescript
const printWindow = window.open('', '_blank');
printWindow.document.write(html);
printWindow.print();
```

오히려 이게 더 깔끔했다:
- 서버 부하 없음
- Marp CSS 100% 적용
- Cold start 걱정 없음

## 세 번째 이슈: 폰트 깨짐

배포하고 보니 한글이 이상하게 보였다. 기본 폰트로 렌더링되고 있었다.

### 해결

Google Fonts를 명시적으로 로드.

```typescript
// export-pdf.ts
const printHTML = `
  <!DOCTYPE html>
  <html>
    <head>
      <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;600;700&display=swap" rel="stylesheet">
      <style>${css}</style>
    </head>
    <body>${html}</body>
  </html>
`;
```

## 네 번째 이슈: 번들 사이즈

첫 배포 후 Lighthouse 돌려봤더니 성능 점수가 낮았다.

```
First Contentful Paint: 3.2s
Largest Contentful Paint: 4.8s
```

원인은 **모든 라이브러리가 초기 로딩에 포함**되고 있었다.

### 해결: Dynamic Import

PDF, PPTX 내보내기 라이브러리는 버튼 클릭할 때만 로드하도록 변경.

```typescript
// Before (안 좋음)
import { exportToPDF } from '@/lib/export-pdf';

// After (좋음)
const handleExportPDF = async () => {
  const { exportToPDFViaPrint } = await import('@/lib/export-pdf');
  await exportToPDFViaPrint(markdown);
};
```

jsPDF, pptxgenjs 같은 무거운 라이브러리가 초기 번들에서 빠지니까 로딩이 빨라졌다.

## 배포 결과

```
Route (app)
┌ ○ /                    (Static)
├ ○ /_not-found          (Static)
└ ƒ /api/export          (Dynamic)

○  (Static)   prerendered as static content
ƒ  (Dynamic)  server-rendered on demand
```

메인 페이지는 Static으로 빌드되어 CDN에서 서빙된다. 빠르다.

## CI/CD 파이프라인

GitHub + Vercel 조합의 장점:

```
[커밋] → [푸시] → [Vercel 자동 감지] → [빌드] → [배포]
                                            ↓
                                    [프리뷰 URL 생성]
```

PR 열면 프리뷰 환경이 자동으로 만들어진다:
```
https://marp-editor-git-feature-xxx.vercel.app
```

코드 리뷰하면서 실제로 돌려볼 수 있어서 편하다.

## 모니터링

Vercel 대시보드에서 확인 가능한 것들:

- **빌드 로그**: 빌드 실패 시 원인 파악
- **함수 로그**: API 호출 기록
- **분석**: 방문자 수, 페이지 조회
- **성능**: Core Web Vitals

무료 플랜인데도 웬만한 건 다 된다.

## 최종 아키텍처

```
[사용자] ──────────────────────────────────────────────────
           │
           ▼
    ┌──────────────┐
    │   Vercel     │
    │   (CDN)      │
    └──────┬───────┘
           │
           ▼
    ┌──────────────┐
    │  Next.js     │
    │  Static Page │  ← 서버 사이드 렌더링 없음
    └──────┬───────┘
           │
           ▼
    ┌──────────────────────────────────────────┐
    │              클라이언트                   │
    ├──────────────┬───────────────────────────┤
    │  CodeMirror  │  Marp Core                │
    │  (에디터)     │  (슬라이드 렌더링)          │
    ├──────────────┼───────────────────────────┤
    │  pptxgenjs   │  Browser Print API        │
    │  (PPTX 생성)  │  (PDF 생성)               │
    └──────────────┴───────────────────────────┘
```

서버 의존성을 최소화했다. 대부분의 로직이 클라이언트에서 돌아간다.

## 회고

### 잘한 것

1. **서버리스 제약을 빨리 파악함**: Puppeteer 안 되는 거 알고 바로 클라이언트로 전환
2. **Dynamic Import 적극 활용**: 초기 로딩 속도 개선
3. **LocalStorage 자동 저장**: 사용자 데이터 보호

### 아쉬운 것

1. **Puppeteer 삽질에 시간 낭비**: 처음부터 클라이언트 방식 갔으면 3일 아꼈음
2. **테스트 코드 없음**: 시간에 쫓겨서 테스트 작성 못함
3. **접근성 미흡**: 키보드 네비게이션이 불완전함

### 배운 것

- Vercel 서버리스 환경의 제약 (바이너리 실행 제한)
- 브라우저 API만으로도 꽤 많은 게 가능함
- Next.js App Router 사용법

## 완성!

![최종 결과물](/assets/images/dev/marp-editor/final-view.png)

- **GitHub**: [takjakim/marp_editor](https://github.com/takjakim/marp_editor)
- **Live Demo**: Vercel 배포 URL

## 앞으로

MVP는 완성했다. 추가하고 싶은 기능들:

- [ ] 협업 기능 (Yjs + WebRTC)
- [ ] 클라우드 저장 (Supabase)
- [ ] 발표자 노트
- [ ] 키보드 단축키 개선
- [ ] 모바일 반응형

하나씩 천천히 해볼 예정이다.

---

**마크다운쇼 개발기 시리즈**
1. [[마크다운쇼 개발기 1편: 기획]]
2. [[마크다운쇼 개발기 2편: 개발]]
3. **배포** ← 현재 글

읽어주셔서 감사합니다!
