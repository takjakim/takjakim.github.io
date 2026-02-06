---
title: "마크다운쇼 개발기 2편: 개발"
last_modified_at: 2026-02-07
categories: [dev, project]
tags: [marp, markdown, presentation, nextjs, codemirror, pdf, pptx, 마크다운쇼, 개발기]
description: "마크다운쇼 개발 삽질기. Marp 렌더링, CodeMirror 동기화, PDF/PPTX 내보내기까지 4가지 삽질과 해결 과정."
permalink: /dev/marp-editor/devlog-2/
image: /assets/images/dev/marp-editor/sketch-component-structure.png
---

# 마크다운쇼 개발기 2편: 개발

> [[마크다운쇼 개발기 1편: 기획]]에서 그린 그림을 실제로 만들어보자. 삽질 포함.

## 프로젝트 초기 세팅

```bash
npx create-next-app@latest marp-editor --typescript --tailwind --app
cd marp-editor
npm install @marp-team/marp-core @codemirror/lang-markdown
```

여기까지는 순조로웠다.

## 폴더 구조

[[01-planning-marp|기획편]]에서 그렸던 컴포넌트 구조를 실제로 만들었다.

![컴포넌트 구조 스케치](/assets/images/dev/marp-editor/sketch-component-structure.png)

```
src/
├── app/
│   ├── page.tsx          # 메인 페이지 (여기에 다 때려박음)
│   ├── globals.css       # 테마 CSS 변수
│   └── api/export/       # 내보내기 API
├── components/
│   ├── Editor.tsx        # CodeMirror 래퍼
│   ├── Preview.tsx       # Marp 렌더링 결과 표시
│   ├── Filmstrip.tsx     # 좌측 슬라이드 목록
│   ├── Toolbar.tsx       # 상단 툴바
│   ├── FloatingFormatBar.tsx  # 하단 포맷 바
│   └── LayoutPanel.tsx   # 레이아웃 선택 모달
└── lib/
    ├── marp-renderer.ts  # Marp 렌더링 유틸
    ├── layouts.ts        # 62가지 레이아웃 정의
    ├── export-pdf.ts     # PDF 내보내기
    └── export-pptx.ts    # PPTX 내보내기
```

## 첫 번째 삽질: Marp 렌더링

Marp Core를 import하는데 에러가 터졌다.

```
Module not found: Can't resolve 'fs'
```

Marp는 Node.js용 라이브러리인데 Next.js 클라이언트에서 돌리려니 문제가 생긴 거다.

### 해결

`next.config.js`에서 webpack 설정을 건드렸다.

```javascript
webpack: (config, { isServer }) => {
  if (!isServer) {
    config.resolve.fallback = {
      fs: false,
      path: false,
    };
  }
  return config;
}
```

이제 렌더링은 된다.

```typescript
// lib/marp-renderer.ts
import Marp from '@marp-team/marp-core';

export function renderSlides(markdown: string) {
  const marp = new Marp({ html: true, math: true });
  const { html, css } = marp.render(markdown);
  return { html, css };
}
```

## 실시간 미리보기 구현

에디터에서 타이핑할 때마다 미리보기가 업데이트되어야 한다.

```typescript
// page.tsx (간략화)
const [markdown, setMarkdown] = useState(initialContent);

const handleEditorChange = useCallback((value: string) => {
  setMarkdown(value);
}, []);

// 렌더링은 useMemo로 캐싱
const { html, css } = useMemo(() => {
  return renderSlides(markdown);
}, [markdown]);
```

근데 문제가 있었다. 타이핑할 때마다 렌더링하니까 **렉이 걸린다**.

### 해결: 디바운스

```typescript
const debouncedMarkdown = useDebounce(markdown, 100);

const { html, css } = useMemo(() => {
  return renderSlides(debouncedMarkdown);
}, [debouncedMarkdown]);
```

100ms 딜레이를 주니까 훨씬 부드러워졌다.

## 두 번째 삽질: 슬라이드 네비게이션

Marp는 `---`로 슬라이드를 구분한다. 현재 커서가 몇 번째 슬라이드에 있는지 계산해야 했다.

```typescript
function getCurrentSlideIndex(markdown: string, cursorPos: number): number {
  const beforeCursor = markdown.substring(0, cursorPos);
  // frontmatter 제외하고 '---' 개수 세기
  const slides = beforeCursor.split(/\n---\n/);
  return Math.max(0, slides.length - 1);
}
```

근데 YAML frontmatter 때문에 첫 번째 `---`가 슬라이드 구분자인지 frontmatter인지 구분이 안 됐다.

### 해결

frontmatter를 먼저 파싱해서 제거한 뒤 계산했다.

```typescript
function parseSlides(markdown: string) {
  // frontmatter 제거
  const withoutFrontmatter = markdown.replace(/^---[\s\S]*?---\n/, '');

  // 슬라이드 분리
  return withoutFrontmatter.split(/\n---\n/).map(content => content.trim());
}
```

![필름스트립 사이드바](/assets/images/dev/marp-editor/filmstrip-sidebar.png)

이제 좌측 필름스트립에서 슬라이드를 클릭하면 해당 위치로 에디터가 스크롤된다.

## 세 번째 삽질: PDF 내보내기

처음에는 서버에서 Puppeteer로 PDF를 생성하려 했다.

```typescript
// 이 코드는 결국 쓰지 않았다
import puppeteer from 'puppeteer-core';
import chromium from '@sparticuz/chromium';

export async function generatePDF(html: string) {
  const browser = await puppeteer.launch({
    executablePath: await chromium.executablePath(),
    args: chromium.args,
  });
  // ...
}
```

로컬에서는 잘 돌아갔다. 그런데 **Vercel에 배포하니까 터졌다**.

```
Error: spawn ENOEXEC
```

Vercel 서버리스 환경에서 Chromium 바이너리가 제대로 실행이 안 되는 거다. 디버깅만 3일.

### 해결: 브라우저 인쇄 다이얼로그

결국 서버 사이드 렌더링을 포기하고 **브라우저 인쇄 기능**을 활용했다.

```typescript
// lib/export-pdf.ts
export async function exportToPDFViaPrint(markdown: string) {
  const { html, css } = renderSlides(markdown);

  // 새 창 열어서 인쇄
  const printWindow = window.open('', '_blank');
  printWindow.document.write(`
    <!DOCTYPE html>
    <html>
      <head>
        <style>
          ${css}
          @page { size: 1280px 720px landscape; margin: 0; }
        </style>
      </head>
      <body>${html}</body>
    </html>
  `);

  printWindow.print();
}
```

장점: Marp CSS가 100% 적용됨. 서버 부하 없음.
단점: 사용자가 "PDF로 저장"을 직접 선택해야 함.

트레이드오프였지만, CSS가 완벽하게 적용되는 게 더 중요했다.

## 네 번째 삽질: PPTX 내보내기

PDF는 해결했는데, PPTX는 또 다른 문제였다.

처음에는 html2canvas로 슬라이드를 이미지로 캡처해서 PPTX에 넣으려 했다.

```typescript
// 이것도 결국 쓰지 않았다
const canvas = await html2canvas(slideElement);
slide.addImage({ data: canvas.toDataURL() });
```

결과물이 **흐릿했다**. 그리고 SVG foreignObject가 렌더링이 안 됐다.

### 해결: 네이티브 텍스트 변환

마크다운을 파싱해서 PowerPoint 네이티브 객체로 변환했다.

```typescript
// lib/export-pptx.ts
export async function exportToPPTXNative(markdown: string) {
  const pptx = new PptxGenJS();
  const slides = parseMarkdownSlides(markdown);

  for (const slideData of slides) {
    const slide = pptx.addSlide();

    // 제목 추출
    const titleMatch = slideData.match(/^#\s+(.+)$/m);
    if (titleMatch) {
      slide.addText(titleMatch[1], {
        x: 0.5, y: 0.5,
        fontSize: 32, bold: true
      });
    }

    // 본문, 리스트 등 처리...
  }

  await pptx.writeFile('presentation.pptx');
}
```

이제 PowerPoint에서 텍스트 편집이 가능하다!

## 레이아웃 프리셋 시스템

62가지 레이아웃을 손으로 다 만들었다. 노가다였다.

```typescript
// lib/layouts.ts
export const LAYOUTS: Layout[] = [
  {
    id: 'cover-centered',
    name: '중앙 표지',
    description: '제목과 부제목이 중앙 정렬된 표지',
    category: 'structure',
    template: `---
class: cover
---

# 프레젠테이션 제목

### 부제목
`
  },
  // ... 61개 더
];
```

카테고리별로 정리해서 모달에서 탭으로 전환할 수 있게 했다.

![레이아웃 패널](/assets/images/dev/marp-editor/layout-panel-full.png)

## 테마 시스템

6가지 테마를 CSS 변수로 구현했다.

```css
[data-theme="dark"] {
  --mp-bg: #1f1f1f;
  --mp-chrome: #2d2d2d;
  --mp-accent: #5a9bd5;
}

[data-theme="dracula"] {
  --mp-bg: #282a36;
  --mp-chrome: #44475a;
  --mp-accent: #bd93f9;
}
```

![테마 드롭다운](/assets/images/dev/marp-editor/theme-dropdown.png)

테마 변경은 `document.documentElement.setAttribute('data-theme', theme)`로 간단하게.

## 자동 저장

새로고침해도 작업 내용이 날아가면 안 된다.

```typescript
// 저장
useEffect(() => {
  localStorage.setItem('markdown-editor-content', markdown);
}, [markdown]);

// 로드
const [markdown, setMarkdown] = useState(() => {
  if (typeof window !== 'undefined') {
    return localStorage.getItem('markdown-editor-content') || initialContent;
  }
  return initialContent;
});
```

간단하지만 사용자 경험에 큰 차이를 만든다.

## 새 슬라이드 추가

요청이 있어서 슬라이드 추가 시 15줄 빈 공간을 넣었다.

```typescript
const handleAddSlide = useCallback(() => {
  const insertPos = calculateSlideEndPosition(markdown, currentSlide);
  const newSlideContent = '\n\n---\n' + '\n'.repeat(15);

  setMarkdown(
    markdown.substring(0, insertPos) +
    newSlideContent +
    markdown.substring(insertPos)
  );
}, [markdown, currentSlide]);
```

![슬라이드 추가](/assets/images/dev/marp-editor/slide-added.png)

## 현재 코드 라인 수

```bash
$ find src -name "*.tsx" -o -name "*.ts" | xargs wc -l
  450 src/app/page.tsx
  180 src/components/Editor.tsx
  220 src/components/Filmstrip.tsx
  370 src/components/FloatingFormatBar.tsx
  280 src/components/LayoutPanel.tsx
  150 src/lib/marp-renderer.ts
 1200 src/lib/layouts.ts
  270 src/lib/export-pdf.ts
  200 src/lib/export-pptx.ts
 ----
 3320 total
```

생각보다 많이 썼다.

## 다음 편 예고

코드는 완성됐다. [[마크다운쇼 개발기 3편: 배포]]에서는 Vercel에 배포하고, 발생한 문제들을 해결하는 과정을 다룬다.

---

**마크다운쇼 개발기 시리즈**
1. [[마크다운쇼 개발기 1편: 기획]]
2. **개발** ← 현재 글
3. [[마크다운쇼 개발기 3편: 배포]]
