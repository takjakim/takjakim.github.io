# 마크다운쇼(Marp Editor) 배포

> [[02-development|개발]]이 완료된 프로젝트를 Vercel에 배포하는 과정

## 배포 환경

| 항목 | 값 |
|------|-----|
| 플랫폼 | Vercel |
| 프레임워크 | Next.js 15 |
| 런타임 | Node.js 20 (Edge 호환) |
| 도메인 | Vercel 기본 도메인 |

## Vercel 배포 설정

### 1. 프로젝트 연결

```bash
# Vercel CLI 설치
npm i -g vercel

# 프로젝트 연결 및 배포
vercel
```

GitHub 저장소를 연결하면 `main` 브랜치 푸시 시 자동 배포됩니다.

### 2. vercel.json 설정

```json
{
  "framework": "nextjs",
  "buildCommand": "npm run build",
  "outputDirectory": ".next"
}
```

### 3. 환경 변수

이 프로젝트는 외부 API 없이 클라이언트 사이드로 동작하므로 별도의 환경 변수가 필요하지 않습니다.

## 서버리스 제약 극복

### 문제: Puppeteer 사용 불가

처음에는 서버 사이드에서 Puppeteer로 PDF를 생성하려 했습니다.

```typescript
// 원래 계획 (실패)
import puppeteer from 'puppeteer-core';
import chromium from '@sparticuz/chromium';

export async function generatePDF(html: string) {
  const browser = await puppeteer.launch({
    executablePath: await chromium.executablePath(),
    // ...
  });
}
```

하지만 Vercel 서버리스 환경에서 `spawn ENOEXEC` 에러가 발생했습니다. Chromium 바이너리가 제대로 실행되지 않는 문제입니다.

### 해결: 클라이언트 사이드 내보내기

**PDF**: 브라우저 인쇄 다이얼로그 활용
- 장점: Marp CSS가 완벽하게 적용됨
- 장점: 서버 부하 없음
- 단점: 사용자가 "PDF로 저장" 선택 필요

**PPTX**: pptxgenjs로 클라이언트에서 직접 생성
- 장점: 네이티브 텍스트로 편집 가능
- 장점: 서버 의존성 없음

```typescript
// 현재 구현 (클라이언트 사이드)
const handleExportPDF = async () => {
  const { exportToPDFViaPrint } = await import('@/lib/export-pdf');
  await exportToPDFViaPrint(markdown);
};

const handleExportPPTX = async () => {
  const { exportToPPTXNative } = await import('@/lib/export-pptx');
  await exportToPPTXNative(markdown);
};
```

## 빌드 최적화

### Dynamic Import로 번들 분리

PDF/PPTX 라이브러리는 용량이 크므로 필요할 때만 로드합니다.

```typescript
// 동적 임포트로 초기 로딩 최적화
const handleExportPDF = async () => {
  const { exportToPDFViaPrint } = await import('@/lib/export-pdf');
  await exportToPDFViaPrint(markdown);
};
```

### 빌드 결과

```
Route (app)
┌ ○ /                    (Static)
├ ○ /_not-found          (Static)
└ ƒ /api/export          (Dynamic)

○  (Static)   prerendered as static content
ƒ  (Dynamic)  server-rendered on demand
```

메인 페이지는 정적으로 빌드되어 CDN에서 빠르게 서빙됩니다.

## 배포 파이프라인

```
[코드 작성] → [커밋/푸시] → [Vercel 자동 감지]
                              ↓
                        [빌드 & 배포]
                              ↓
                        [프리뷰 URL 생성]
                              ↓
                        [프로덕션 배포]
```

### 프리뷰 배포

PR을 열면 자동으로 프리뷰 환경이 생성됩니다.

```
https://marp-editor-git-feature-xxx.vercel.app
```

### 프로덕션 배포

`main` 브랜치에 머지되면 자동으로 프로덕션에 배포됩니다.

## 모니터링

Vercel 대시보드에서 확인 가능한 항목:

- **빌드 로그**: 빌드 성공/실패 여부
- **함수 로그**: API 호출 로그
- **분석**: 방문자 수, 페이지 조회 수
- **성능**: Core Web Vitals

## 트러블슈팅

### 1. 폰트 로딩 이슈

Marp 슬라이드에서 한글 폰트가 제대로 표시되지 않는 문제가 있었습니다.

**해결**: Google Fonts를 HTML에 직접 포함

```html
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;600;700&display=swap" rel="stylesheet">
```

### 2. SVG foreignObject 렌더링

html2canvas로 SVG를 캡처할 때 foreignObject 내부 요소가 렌더링되지 않는 문제가 있었습니다.

**해결**: 브라우저 인쇄 기능 사용

브라우저 렌더링 엔진이 직접 처리하므로 모든 CSS가 정확하게 적용됩니다.

### 3. CORS 이슈

외부 이미지를 슬라이드에 포함할 때 CORS 에러가 발생할 수 있습니다.

**권장**: 이미지는 Base64로 인라인 삽입하거나 같은 도메인에서 호스팅

## 완성된 프로젝트

![완성된 에디터](./images/01-editor-full.png)

- **GitHub**: [takjakim/marp_editor](https://github.com/takjakim/marp_editor)
- **Live Demo**: Vercel 배포 URL

## 시리즈 마무리

3편의 글을 통해 마크다운쇼의 전체 개발 과정을 살펴봤습니다.

1. [[01-planning|기획]]: 요구사항 정의와 기술 스택 선정
2. [[02-development|개발]]: 핵심 기능 구현과 아키텍처
3. **배포** (현재 글): Vercel 배포와 트러블슈팅

마크다운으로 프레젠테이션을 만들고 싶다면 지금 바로 사용해 보세요!

---

**시리즈 목차**
1. [[01-planning|기획]]
2. [[02-development|개발]]
3. **배포** (현재 글)
