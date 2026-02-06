---
title: "마크다운ㅎ글 개발기 (2) - 개발: 기술 스택과 핵심 구현"
last_modified_at: 2026-02-06
categories: [dev, project]
tags: [markdown-hangul, nextjs, puppeteer, typescript, react, 마크다운ㅎ글]
description: "마크다운을 한글 HWP 스타일 PDF로 변환하는 웹 앱의 기술 스택 선정과 핵심 구현 과정을 상세히 소개합니다."
image: /assets/images/dev/markdown-hangul/02-editor-with-content.png
permalink: /dev/markdown-hangul/part-2/
---

# 마크다운ㅎ글 개발기 (2) - 개발: 기술 스택과 핵심 구현

[Part 1: 기획](/dev/markdown-hangul/part-1/)에서 한글 HWP 스타일 PDF 생성이라는 목표를 정했습니다. 이제 본격적인 개발 이야기를 시작합니다.

## 1. 기술 스택 선정

### 1.1 프레임워크: Next.js 16 (App Router)

**선택 이유:**
- **SSR + API Routes 통합**: 프리뷰 HTML 생성과 PDF 변환 API를 하나의 프레임워크에서 처리
- **React 19 + TypeScript 5**: 최신 React 기능과 타입 안정성
- **Vercel 최적화**: 서버리스 배포 시 자동 최적화 및 엣지 캐싱 지원
- **App Router**: 파일 기반 라우팅으로 API 엔드포인트 구조화가 직관적

### 1.2 스타일링: Tailwind CSS 4

**선택 이유:**
- **Utility-First 패러다임**: 컴포넌트 스타일을 빠르게 작성
- **CSS 변수 통합**: 테마별 폰트/크기/여백을 CSS 변수로 관리하여 동적 변경 용이
- **JIT (Just-In-Time)**: 사용하는 클래스만 빌드하여 최종 CSS 크기 최소화

### 1.3 마크다운 파싱: markdown-it v14 생태계

**핵심 플러그인:**

```typescript
// markdown-renderer.ts
const md = new MarkdownIt({
  html: true,       // HTML 태그 허용
  breaks: true,     // 줄바꿈을 <br>로 변환
  linkify: true,    // URL 자동 링크 변환
  highlight(str: string, lang: string) {
    if (lang && hljs.getLanguage(lang)) {
      return hljs.highlight(lang, str, true).value;
    }
    return md.utils.escapeHtml(str);
  },
})
  .use(require('markdown-it-katex'))         // LaTeX 수식 ($inline$, $$block$$)
  .use(require('markdown-it-emoji'))         // :smile: → 😊
  .use(require('markdown-it-checkbox'))      // - [ ] → 체크박스
  .use(require('markdown-it-container'))     // ::: warning :::
  .use(require('markdown-it-mark'))          // ==highlight==
  .use(require('markdown-it-named-headers')); // # Heading → id="heading"
```

**플러그인 선정 기준:**
- **KaTeX**: 수식 렌더링 품질과 성능 (MathJax보다 빠름)
- **Emoji**: 이모티콘 지원 (선택적 활성화)
- **Checkbox**: 작업 목록 (`- [ ]`, `- [x]`)
- **Container**: 커스텀 블록 (경고, 팁 등)
- **Mark**: 하이라이트 표시 (`==text==`)
- **Named Headers**: TOC 앵커 링크용 ID 자동 생성

### 1.4 PDF 생성: Puppeteer + @sparticuz/chromium

**왜 Puppeteer인가?**
- **완벽한 CSS 지원**: HTML/CSS를 그대로 PDF로 렌더링 (표, Flexbox, Grid 등)
- **헤더/푸터 템플릿**: 페이지 번호, 문서 제목 자동 삽입
- **JavaScript 실행**: TOC 페이지 번호 계산 로직을 클라이언트 사이드에서 실행

**서버리스 최적화: @sparticuz/chromium**
- Vercel/AWS Lambda에서 Chromium 바이너리를 포함한 경량 패키지
- 로컬 개발 시 시스템 Chrome 사용, 배포 시 자동 전환

```typescript
// pdf-generator.ts
async function getExecPathAndArgs() {
  if (IS_VERCEL) {
    const chromium = await import('@sparticuz/chromium');
    return {
      executablePath: await chromium.default.executablePath(),
      args: chromium.default.args
    };
  }
  // 로컬: 시스템 Chrome 경로 탐색
  return { executablePath: '/Applications/Google Chrome.app/...', args: [...] };
}
```

### 1.5 보조 라이브러리

| 라이브러리 | 용도 |
|-----------|------|
| **gray-matter** | YAML frontmatter 파싱 (제목, 저자, 날짜 등) |
| **cheerio** | 서버사이드 HTML DOM 조작 (TOC 생성, 간지 페이지 삽입) |
| **highlight.js** | 코드 블록 구문 강조 (130+ 언어 지원) |

## 2. 아키텍처: 데이터 흐름

![에디터와 프리뷰](/assets/images/dev/markdown-hangul/02-editor-with-content.png)

### 2.1 전체 흐름도

```
┌──────────────┐
│ Markdown 입력 │
└──────┬───────┘
       │
       v
┌─────────────────┐
│  Editor.tsx     │  ← 클라이언트 컴포넌트 (줄 번호, 설정 패널)
│  - Settings UI  │
│  - File Browser │
└──────┬──────────┘
       │
       v
  ┌────┴────┐
  │         │
  v         v
┌──────────────┐     ┌──────────────┐
│ /api/preview │     │ /api/convert │
│  (HTML)      │     │  (PDF)       │
└──────┬───────┘     └──────┬───────┘
       │                    │
       v                    v
┌─────────────────────┐  ┌─────────────────┐
│ markdown-renderer.ts│  │ pdf-generator.ts│
│  (Parse MD)         │  │  (Puppeteer)    │
└──────┬──────────────┘  └────────┬────────┘
       │                          │
       v                          v
┌────────────────┐          ┌─────────────┐
│ html-builder.ts│          │ PDF Buffer  │
│  (Assemble)    │          │  (Download) │
└──────┬─────────┘          └─────────────┘
       │
       v
┌────────────────┐
│ css-pipeline.ts│
│  (Styling)     │
└──────┬─────────┘
       │
       v
┌──────────────────┐
│ Preview.tsx      │  ← iframe으로 렌더링
│  (HTML Preview)  │
└──────────────────┘
```

### 2.2 핵심 파일과 역할

| 파일 | 역할 | 주요 기능 |
|------|------|----------|
| `markdown-renderer.ts` | 마크다운 → HTML 변환 | markdown-it 플러그인 체인 구성 |
| `html-builder.ts` | HTML 문서 조립 | 표지, 목차, 간지 페이지 생성 |
| `css-pipeline.ts` | 동적 CSS 생성 | 설정 기반 스타일 주입 (폰트, 여백, 테마) |
| `pdf-generator.ts` | HTML → PDF 변환 | Puppeteer 실행, 페이지 번호 계산 |
| `settings.ts` | 설정 타입 정의 | 58개 설정 항목 TypeScript 타입 |

## 3. 핵심 구현 포인트

### 3.1 마크다운 렌더링 파이프라인

markdown-it는 체인 패턴으로 플러그인을 순차 적용합니다:

```typescript
// markdown-renderer.ts
export function convertMarkdownToHtml(text: string, settings: Settings): string {
  const grayMatter = require('gray-matter');
  const matterParts = grayMatter(text);

  const md = new MarkdownIt({
    html: true,
    breaks: matterParts.data.breaks ?? settings.breaks,
    highlight(str, lang) {
      if (lang && hljs.getLanguage(lang)) {
        return hljs.highlight(lang, str, true).value;
      }
      return md.utils.escapeHtml(str);
    },
  })
    .use(require('markdown-it-checkbox'))
    .use(require('markdown-it-emoji'), { defs: emojiDefs })
    .use(require('markdown-it-named-headers'), { slugify: Slug })
    .use(require('markdown-it-container'))
    .use(require('markdown-it-katex'))
    .use(require('markdown-it-mark'));

  return md.render(matterParts.content);
}
```

**특징:**
- **Frontmatter 우선**: 문서별 `breaks`, `emoji` 설정이 전역 설정을 오버라이드
- **에러 핸들링**: `highlight.js`가 언어를 인식 못 하면 HTML 이스케이프로 폴백
- **플러그인 순서**: `named-headers` → `container` → `katex` → `mark` 순으로 적용

### 3.2 HTML 조립: 표지/목차/간지 페이지

`html-builder.ts`는 세 가지 특수 페이지를 자동 생성합니다.

#### 3.2.1 표지 페이지 (Cover Page)

```typescript
// html-builder.ts
if (settings.coverPage && frontMatter) {
  content += '<div class="hwp-cover-page">';
  if (frontMatter.organization)
    content += `<div class="hwp-cover-org">${frontMatter.organization}</div>`;
  content += `<div class="hwp-cover-title">${frontMatter.title}</div>`;
  if (frontMatter.subtitle)
    content += `<div class="hwp-cover-subtitle">${frontMatter.subtitle}</div>`;
  content += '<div class="hwp-cover-meta">';
  content += `<div class="hwp-cover-date">${frontMatter.date}</div>`;
  content += `<div class="hwp-cover-author">${frontMatter.author}</div>`;
  content += '</div></div>';
}
```

**CSS 레이아웃:**
```css
.hwp-cover-page {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  page-break-after: always; /* PDF 페이지 구분 */
}
```

#### 3.2.2 목차 페이지 (TOC)

cheerio로 HTML에서 헤딩을 추출하고 점선 리더와 페이지 번호를 추가합니다:

```typescript
// html-builder.ts
const $ = cheerio.load(data);
const tocItems: { level: number; text: string; id: string }[] = [];

$('h1, h2, h3').each(function () {
  const level = parseInt(this.tagName.replace('h', ''));
  const text = $(this).text();
  const id = $(this).attr('id') || '';
  tocItems.push({ level, text, id });
});

content += '<div class="hwp-toc-page">';
content += '<div class="hwp-toc-heading">목  차</div>';
tocItems.forEach(item => {
  content += `
    <div class="hwp-toc-item">
      <a href="#${item.id}">${item.text}</a>
      <span class="hwp-toc-page-num" data-target="${item.id}"></span>
    </div>`;
});
content += '</div>';
```

**점선 리더 CSS:**
```css
.hwp-toc-item::after {
  content: "";
  flex: 1;
  border-bottom: 1px dotted #999;
  margin: 0 0.4em;
}
```

#### 3.2.3 간지 페이지 (Divider)

H1 헤딩 앞에 전체 페이지 간지를 삽입합니다:

```typescript
// html-builder.ts
if (settings.dividerPage) {
  const $ = cheerio.load(data);
  $('h1').each(function () {
    const heading = $(this).text();
    const divider = `<div class="hwp-divider-page">
                       <div class="hwp-divider-title">${heading}</div>
                     </div>`;
    $(this).before(divider);
  });
  data = $.html();
}
```

#### 3.2.4 번호 박스 헤딩 (Numbered Box)

![설정 패널](/assets/images/dev/markdown-hangul/03-settings-panel.png)

한글 HWP의 시그니처 스타일인 "1.2.3" 번호 박스:

```typescript
// html-builder.ts
const counters = [0, 0, 0, 0, 0, 0];
$('h1, h2, h3').each(function () {
  const level = parseInt(this.tagName.replace('h', ''));
  counters[level - 1]++;
  for (let r = level; r < 6; r++) counters[r] = 0; // 하위 레벨 리셋

  const numStr = counters.slice(0, level).join('.'); // "1.2.3"
  const text = $(this).html();
  const id = $(this).attr('id') || '';

  const replacement = `
    <div class="hwp-heading-box hwp-heading-box-${level}" id="${id}">
      <span class="hwp-heading-num">${numStr}</span>
      <span class="hwp-heading-text">${text}</span>
    </div>`;
  $(this).replaceWith(replacement);
});
```

**CSS 스타일:**
```css
.hwp-heading-box {
  display: flex;
  align-items: stretch;
}
.hwp-heading-num {
  background: #1a1a1a;
  color: #fff;
  padding: 0.3em 0.8em;
  font-weight: bold;
}
.hwp-heading-text {
  border: 1px solid #1a1a1a;
  border-left: none;
  padding: 0.3em 0.7em;
  flex: 1;
}
```

### 3.3 동적 CSS 생성 (css-pipeline.ts)

설정 값을 CSS 변수로 변환하여 테마를 동적으로 적용합니다.

#### 3.3.1 Base Styles 로드

```typescript
// css-pipeline.ts
export function readStyles(settings: Settings): string {
  let style = '';

  // 1. markdown.css (기본 마크다운 스타일)
  if (settings.includeDefaultStyles) {
    style += makeCss('./public/styles/markdown.css');
  }

  // 2. highlight.js 테마
  if (settings.highlight) {
    const hljsPath = require.resolve(`highlight.js/styles/${settings.highlightStyle}`);
    style += makeCss(hljsPath);
  }

  // 3. hwp.css (한글 HWP 스타일)
  style += makeCss('./public/styles/hwp.css');

  return style;
}
```

#### 3.3.2 CSS 변수 주입

```typescript
// css-pipeline.ts
const fontFamilyMap: Record<string, string> = {
  'nanum-gothic': "'NanumGothic', 'Nanum Gothic', sans-serif",
  'nanum-myeongjo': "'NanumMyeongjo', 'Nanum Myeongjo', serif",
  'pretendard': "'Pretendard Variable', sans-serif",
  'noto-serif-kr': "'Noto Serif KR', serif",
};

style += `
<style>
:root {
  --hwp-font-family: ${fontFamilyMap[settings.fontFamily]};
  --hwp-font-size: ${settings.fontSize}pt;
  --hwp-line-height: ${settings.lineHeight};
  --hwp-word-break: ${settings.wordBreak};
}
</style>
`;
```

#### 3.3.3 테이블 스타일 변형

HWP 기본 → APA/Minimal/None 스타일로 전환:

```typescript
// css-pipeline.ts
if (settings.tableStyle === 'apa') {
  style += `
    <style>
    table {
      border-top: 2px solid #000;
      border-bottom: 2px solid #000;
    }
    table > thead > tr > th {
      border-bottom: 1px solid #000;
    }
    </style>`;
}
```

### 3.4 PDF 생성의 난제: TOC 페이지 번호 계산

**문제 상황:**
- TOC는 문서 최상단에 위치하지만, 각 헤딩의 페이지 번호는 전체 HTML 렌더링 후에야 알 수 있음
- Puppeteer가 PDF를 생성할 때 요소의 절대 위치를 기준으로 페이지를 나눔

**해결 전략:**
1. HTML에서 TOC 페이지 번호를 빈 `<span data-target="heading-id"></span>`으로 생성
2. Puppeteer로 HTML을 로드한 후 JavaScript를 실행하여 각 헤딩의 Y 좌표를 계산
3. Y 좌표를 A4 페이지 높이(297mm = 1122.52px)로 나누어 페이지 번호 산출
4. `span` 태그에 페이지 번호 주입
5. 최종 PDF 생성

```typescript
// pdf-generator.ts
await page.evaluate(() => {
  const pageHeight = 297 * 3.7795275591; // A4 mm → px 변환
  const tocNums = document.querySelectorAll('.hwp-toc-page-num');

  tocNums.forEach((span) => {
    const targetId = span.getAttribute('data-target');
    const target = document.getElementById(targetId);
    if (!target) return;

    const rect = target.getBoundingClientRect();
    const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
    const absTop = rect.top + scrollTop;
    const pageNum = Math.floor(absTop / pageHeight) + 1;

    span.textContent = String(pageNum); // 페이지 번호 주입
  });
});
```

**왜 3.7795275591인가?**
- 1mm = 3.7795275591px (CSS 단위 변환)
- A4 세로 = 297mm × 3.7795275591 = 1122.52px

### 3.5 헤더/푸터 페이지 번호 로직

Puppeteer의 `headerTemplate`/`footerTemplate`에서 특수 페이지를 건너뛰는 로직:

```typescript
// pdf-generator.ts
let skipPages = 0;
if (settings.coverPage) skipPages += 1;
if (settings.tocPage) skipPages += 1;
if (settings.dividerPage) {
  const dividerCount = (html.match(/class="hwp-divider-page"/g) || []).length;
  skipPages += dividerCount;
}

// settings.ts
export function buildFooterTemplate(settings: Settings, skipPages: number): string {
  if (!settings.footerPageNumber) return '<div></div>';

  const showFrom = 1 + skipPages;
  return `
    <div style="width: 100%; text-align: center; font-size: 9pt;">
      <span class="pageNumber"
            style="visibility: calc(
              (var(--webkit-page-number) >= ${showFrom}) * 1
            ) ? visible : hidden;">
        <span class="pageNumber"></span>
      </span>
    </div>`;
}
```

**핵심 아이디어:**
- `--webkit-page-number`: Puppeteer가 제공하는 현재 페이지 번호 (1부터 시작)
- `visibility` 조건: `pageNumber >= showFrom`일 때만 표시
- 표지/목차/간지 페이지에서는 페이지 번호 숨김

### 3.6 이미지 처리: 로컬 폴더 통합

**File System Access API 활용:**

```typescript
// Editor.tsx
const handleFolderSelect = async () => {
  const dirHandle = await window.showDirectoryPicker();
  const files = await readFilesRecursively(dirHandle);
  setFolderFiles(files);
};

async function readFilesRecursively(dirHandle: FileSystemDirectoryHandle) {
  const files: FileEntry[] = [];
  for await (const entry of dirHandle.values()) {
    if (entry.kind === 'file' && /\.(png|jpg|jpeg|gif|webp)$/i.test(entry.name)) {
      const file = await entry.getFile();
      files.push({ name: entry.name, file });
    }
  }
  return files;
}
```

**Canvas API 압축:**

Vercel 요청 크기 제한(4.5MB)을 피하기 위해 이미지를 WebP로 압축:

```typescript
// image-compressor.ts
async function compressImage(file: File): Promise<string> {
  return new Promise((resolve) => {
    const img = new Image();
    img.onload = () => {
      const canvas = document.createElement('canvas');
      const maxDim = 1920;
      const scale = Math.min(1, maxDim / Math.max(img.width, img.height));

      canvas.width = img.width * scale;
      canvas.height = img.height * scale;

      const ctx = canvas.getContext('2d')!;
      ctx.drawImage(img, 0, 0, canvas.width, canvas.height);

      canvas.toBlob((blob) => {
        const reader = new FileReader();
        reader.onloadend = () => resolve(reader.result as string);
        reader.readAsDataURL(blob);
      }, 'image/webp', 0.85);
    };
    img.src = URL.createObjectURL(file);
  });
}
```

**압축 전략:**
- 최대 1920px로 리사이즈
- WebP 포맷, 85% 품질
- Base64로 인코딩하여 HTML에 인라인 삽입

## 4. 설정 시스템: 58개 옵션의 TypeScript 관리

### 4.1 타입 정의

```typescript
// settings.ts
export interface Settings {
  // 폰트
  fontFamily: 'nanum-gothic' | 'nanum-myeongjo' | 'pretendard' | 'noto-serif-kr' | 'custom';
  customFontFamily?: string;
  fontSize: number;
  lineHeight: number;
  wordBreak: 'keep-all' | 'break-word' | 'normal';

  // 레이아웃
  margin: { top: string; right: string; bottom: string; left: string };
  scale: number;
  printBackground: boolean;

  // 헤딩
  headingStyle: 'default' | 'numbered-box' | 'apa';
  headingBoxDepth: number;
  headingSizeH1: string;
  headingSizeH2: string;
  // ... H3-H6

  // 특수 페이지
  coverPage: boolean;
  tocPage: boolean;
  tocDepth: number;
  dividerPage: boolean;

  // 테이블
  tableStyle: 'hwp' | 'apa' | 'minimal' | 'none';

  // 코드 하이라이트
  highlight: boolean;
  highlightStyle: string;

  // 기타
  breaks: boolean;
  emoji: boolean;
  textIndent: string;
  // ... 총 58개
}
```

### 4.2 localStorage 영속화

```typescript
// Editor.tsx
const loadSettings = () => {
  const saved = localStorage.getItem('hwp-settings');
  return saved ? JSON.parse(saved) : defaultSettings;
};

const saveSettings = (newSettings: Settings) => {
  localStorage.setItem('hwp-settings', JSON.stringify(newSettings));
  setSettings(newSettings);
};
```

### 4.3 프리셋 저장/불러오기

```typescript
// SettingsPanel.tsx
const handleExportPreset = () => {
  const json = JSON.stringify(settings, null, 2);
  const blob = new Blob([json], { type: 'application/json' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `preset-${Date.now()}.json`;
  a.click();
};

const handleImportPreset = async (file: File) => {
  const text = await file.text();
  const imported = JSON.parse(text);
  saveSettings({ ...defaultSettings, ...imported });
};
```

## 5. API Routes: 프리뷰와 변환

### 5.1 프리뷰 API (`/api/preview`)

```typescript
// app/api/preview/route.ts
export async function POST(req: Request) {
  const { markdown, settings } = await req.json();

  const html = convertMarkdownToHtml(markdown, settings);
  const grayMatter = require('gray-matter');
  const { data: frontMatter } = grayMatter(markdown);

  const fullHtml = makeHtml(html, settings, frontMatter, false);
  return new Response(fullHtml, {
    headers: { 'Content-Type': 'text/html; charset=utf-8' }
  });
}
```

**특징:**
- `forPdf: false` → 브라우저 프리뷰용 헤더/푸터 삽입
- iframe에서 실시간 렌더링

### 5.2 변환 API (`/api/convert`)

```typescript
// app/api/convert/route.ts
export async function POST(req: Request) {
  const { markdown, settings } = await req.json();

  const html = convertMarkdownToHtml(markdown, settings);
  const { data: frontMatter } = grayMatter(markdown);
  const fullHtml = makeHtml(html, settings, frontMatter, true); // forPdf: true

  const pdfBuffer = await generatePdf(fullHtml, settings);

  return new Response(pdfBuffer, {
    headers: {
      'Content-Type': 'application/pdf',
      'Content-Disposition': 'attachment; filename="document.pdf"',
    },
  });
}
```

**특징:**
- `forPdf: true` → Puppeteer용 헤더/푸터 제거 (Puppeteer가 자체 템플릿 사용)
- 30초 타임아웃 설정

## 6. 주요 기술적 도전과 해결

### 6.1 Vercel 메모리 제한 (1024MB)

**문제:** Puppeteer + Chromium이 512MB 사용, 대용량 문서 변환 시 OOM

**해결:**
```typescript
// pdf-generator.ts
browser = await puppeteer.launch({
  args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage'],
  defaultViewport: { width: 1920, height: 1080 },
  headless: true,
});
```
- `--disable-dev-shm-usage`: 공유 메모리 대신 `/tmp` 사용

### 6.2 요청 본문 크기 제한 (4.5MB)

**문제:** 이미지 포함 마크다운이 Vercel Body Size Limit 초과

**해결:**
```typescript
// app/api/convert/route.ts
import { parseBody } from '@/lib/parse-body';

export async function POST(req: Request) {
  const body = await parseBody(req); // gzip 압축 해제
  // ...
}
```

```typescript
// lib/parse-body.ts
import { gunzipSync } from 'zlib';

export async function parseBody(req: Request) {
  const raw = await req.arrayBuffer();
  const encoding = req.headers.get('Content-Encoding');

  if (encoding === 'gzip') {
    const decompressed = gunzipSync(Buffer.from(raw));
    return JSON.parse(decompressed.toString('utf-8'));
  }
  return JSON.parse(new TextDecoder().decode(raw));
}
```

**클라이언트 압축:**
```typescript
// Editor.tsx
const compressed = pako.gzip(JSON.stringify({ markdown, settings }));
fetch('/api/convert', {
  method: 'POST',
  headers: { 'Content-Encoding': 'gzip', 'Content-Type': 'application/json' },
  body: compressed,
});
```

### 6.3 한글 폰트 로딩 지연

**문제:** 웹폰트 로딩 전 PDF 생성 시 폰트 깨짐

**해결:**
```typescript
// html-builder.ts
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Nanum+Gothic:wght@400;700;800&display=swap" rel="stylesheet">
```

Puppeteer의 `waitUntil: 'networkidle0'` 옵션으로 폰트 로딩 대기.

## 7. 성능 최적화

### 7.1 CSS 캐싱

```typescript
// css-pipeline.ts
const cachedStyles = new Map<string, string>();

function makeCss(filePath: string): string {
  if (cachedStyles.has(filePath)) {
    return cachedStyles.get(filePath)!;
  }
  const css = fs.readFileSync(filePath, 'utf-8');
  cachedStyles.set(filePath, css);
  return css;
}
```

### 7.2 Warm-up API

```typescript
// app/api/warmup/route.ts
export async function GET() {
  const chromium = await import('@sparticuz/chromium');
  await chromium.default.executablePath(); // Chromium 바이너리 사전 로드
  return new Response('OK');
}
```

Vercel Cron으로 5분마다 호출하여 Cold Start 방지.

## 8. 개발 과정에서 배운 것

### 8.1 Puppeteer의 CSS 렌더링 한계
- `page-break-inside: avoid`가 일부 요소에서 무시됨 → `page-break-after: avoid`로 우회
- Flexbox의 `flex: 1`이 PDF에서 제대로 계산되지 않음 → 고정 너비로 대체

### 8.2 markdown-it 플러그인 호환성
- 일부 플러그인이 ESM/CJS 혼용으로 `default` export 처리 필요
- `markdown-it-emoji` v3는 `full`, `bare`, `light` 세 가지 버전 제공

### 8.3 TypeScript 타입 추론
- `Settings` 타입의 58개 필드를 일일이 타이핑하는 대신 `Record<string, any>`로 시작했다가, 버그 추적이 어려워져 결국 모두 명시적으로 정의

## 마무리

Part 2에서는 Next.js 16 + Puppeteer 스택으로 마크다운 → HWP 스타일 PDF 변환 파이프라인을 구현하는 과정을 살펴봤습니다. 특히 TOC 페이지 번호 계산, 동적 CSS 생성, 이미지 압축 등 까다로운 기술적 문제들을 해결하는 과정이 흥미로웠습니다.

[Part 3: 배포](/dev/markdown-hangul/part-3/)에서는 Vercel 서버리스 환경에 배포하면서 겪은 메모리 제한, Cold Start, 보안 설정 등의 이슈와 해결책을 다룹니다.

---

## 🔗 연결 (백링크용)
- 이전: [[마크다운ㅎ글 개발기 (1) - 기획: 마크다운으로 공문서 쓰기]]
- 다음: [[마크다운ㅎ글 개발기 (3) - 배포: Vercel 배포와 서버리스 환경 최적화]]
- 허브: [[개발 노트 시작하기]]

**테스트 URL:** <https://md.takjakim.kr>
