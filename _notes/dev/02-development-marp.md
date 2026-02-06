# 마크다운쇼(Marp Editor) 개발

> [[01-planning|기획]]에서 정의한 요구사항을 실제로 구현하는 과정

## 프로젝트 구조

```
src/
├── app/
│   ├── page.tsx          # 메인 에디터 페이지
│   ├── globals.css       # 테마 CSS 변수
│   └── api/export/       # HTML 내보내기 API
├── components/
│   ├── Editor.tsx        # CodeMirror 에디터
│   ├── Preview.tsx       # 슬라이드 미리보기
│   ├── Filmstrip.tsx     # 슬라이드 썸네일 목록
│   ├── Toolbar.tsx       # 상단 툴바
│   ├── FloatingFormatBar.tsx  # 하단 포맷 바
│   ├── LayoutPanel.tsx   # 레이아웃 선택 모달
│   └── LayoutCard.tsx    # 레이아웃 카드 컴포넌트
└── lib/
    ├── marp-renderer.ts  # Marp 렌더링 로직
    ├── layouts.ts        # 62가지 레이아웃 정의
    ├── layout-thumbnails.ts  # SVG 썸네일 생성
    ├── export-pdf.ts     # PDF 내보내기
    └── export-pptx.ts    # PPTX 내보내기
```

## 핵심 구현

### 1. Marp 렌더링 엔진

Marp Core를 사용해 마크다운을 HTML+CSS로 변환합니다.

```typescript
// lib/marp-renderer.ts
import Marp from '@marp-team/marp-core';

export function renderSlides(markdown: string) {
  const marp = new Marp({
    html: true,
    math: true,
  });

  const { html, css } = marp.render(markdown);
  return { html, css };
}
```

### 2. 실시간 에디터 동기화

CodeMirror 6의 `onUpdate` 콜백으로 에디터 변경을 감지하고 미리보기를 업데이트합니다.

```typescript
// components/Editor.tsx
const handleChange = useCallback((value: string) => {
  onChange(value);
  // 디바운스로 성능 최적화
}, [onChange]);
```

슬라이드 구분자(`---`)를 기준으로 현재 커서 위치의 슬라이드를 자동으로 계산합니다.

### 3. 슬라이드 추가 로직

새 슬라이드 추가 시 현재 슬라이드 다음에 삽입됩니다.

```typescript
// app/page.tsx
const handleAddSlide = useCallback(() => {
  // 현재 슬라이드 끝 위치 계산
  const insertPos = calculateSlideEndPosition(markdown, currentSlide);

  // 15줄 빈 공간과 함께 새 슬라이드 삽입
  const newSlideContent = '\n\n---\n' + '\n'.repeat(15);

  const newMarkdown =
    markdown.substring(0, insertPos) +
    newSlideContent +
    markdown.substring(insertPos);

  setMarkdown(newMarkdown);
  setCurrentSlide(currentSlide + 1);
}, [markdown, currentSlide]);
```

![새 슬라이드 추가](./images/05-new-slide.png)

### 4. 레이아웃 프리셋 시스템

62가지 레이아웃은 카테고리별로 분류되어 있습니다.

```typescript
// lib/layouts.ts
export interface Layout {
  id: string;
  name: string;           // 한글 이름
  description: string;
  category: LayoutCategory;
  template: string;       // 마크다운 템플릿
}

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

### 부제목 또는 발표자 이름
`
  },
  // ... 61개 더
];
```

### 5. PDF 내보내기

Vercel 서버리스 환경에서 Puppeteer가 동작하지 않아 **브라우저 인쇄 다이얼로그**를 활용합니다.

```typescript
// lib/export-pdf.ts
export async function exportToPDFViaPrint(markdown: string) {
  const { html, css } = renderSlides(markdown);

  const printWindow = window.open('', '_blank');
  printWindow.document.write(`
    <!DOCTYPE html>
    <html>
      <head>
        <style>${css}</style>
        <style>
          @page { size: 1280px 720px landscape; margin: 0; }
          @media print {
            svg[data-marpit-svg] {
              page-break-after: always;
            }
          }
        </style>
      </head>
      <body>${html}</body>
    </html>
  `);

  printWindow.print();
}
```

### 6. PPTX 내보내기 (네이티브 텍스트)

이미지 캡처 대신 **마크다운 파싱 → 네이티브 텍스트**로 변환하여 PowerPoint에서 편집 가능합니다.

```typescript
// lib/export-pptx.ts
import PptxGenJS from 'pptxgenjs';

export async function exportToPPTXNative(markdown: string) {
  const pptx = new PptxGenJS();
  const slides = parseMarkdownSlides(markdown);

  for (const slideData of slides) {
    const slide = pptx.addSlide();

    // 마크다운 요소를 PowerPoint 객체로 변환
    if (slideData.title) {
      slide.addText(slideData.title, {
        x: 0.5, y: 0.5,
        fontSize: 32, bold: true
      });
    }
    // ... 본문, 리스트 등 처리
  }

  await pptx.writeFile('presentation.pptx');
}
```

## 테마 시스템

CSS 변수로 6가지 테마를 지원합니다.

| 테마 | 특징 |
|------|------|
| Dark (기본) | PowerPoint 스타일 다크 |
| Light | 밝은 배경 |
| Dracula | 보라색 계열 다크 |
| Sepia | 따뜻한 세피아 톤 |
| Nord | 북유럽 스타일 |
| GitHub | GitHub 스타일 라이트 |

```css
/* globals.css */
[data-theme="dark"] {
  --mp-bg: #1f1f1f;
  --mp-chrome: #2d2d2d;
  --mp-accent: #5a9bd5;
  /* ... */
}

[data-theme="dracula"] {
  --mp-bg: #282a36;
  --mp-chrome: #44475a;
  --mp-accent: #bd93f9;
  /* ... */
}
```

## 성능 최적화

1. **디바운스**: 에디터 변경 시 100ms 디바운스로 렌더링 횟수 감소
2. **메모이제이션**: `useMemo`로 슬라이드 파싱 결과 캐싱
3. **Dynamic Import**: PDF/PPTX 라이브러리 동적 로딩
4. **LocalStorage 저장**: 자동 저장으로 새로고침 시 복구

## 다음 단계

개발이 완료되면 [[03-deployment|배포]] 단계에서 Vercel에 배포하고 프로덕션 환경을 구성합니다.

---

**시리즈 목차**
1. [[01-planning|기획]]
2. **개발** (현재 글)
3. [[03-deployment|배포]]
