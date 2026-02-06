---
title: "마크다운ㅎ글 개발기 (3) - 배포: Vercel 배포와 서버리스 환경 최적화"
last_modified_at: 2026-02-06
categories: [dev, project]
tags: [vercel, serverless, puppeteer, optimization, pdf-generation, 마크다운ㅎ글]
description: "Vercel 서버리스 환경에서 Puppeteer 돌리기, 메모리 초과 해결, 413 에러 트러블슈팅 - 실전 배포 삽질 기록"
permalink: /dev/markdown-hangul/part-3/
---

# 마크다운ㅎ글 개발기 (3) - 배포: Vercel 배포와 서버리스 환경 최적화

## 시리즈 목차

- [Part 1: 기획](/dev/markdown-hangul/part-1/)
- [Part 2: 개발](/dev/markdown-hangul/part-2/)
- **Part 3: 배포** (현재 글)

---

개발이 끝났으니 이제 배포할 차례입니다. 로컬에서는 잘 돌아가던 앱이 프로덕션 환경에서 갑자기 413 에러를 뱉거나, 메모리 초과로 죽거나, cold start에 10초씩 걸리는 경험, 다들 한 번쯤 있으시죠? 이번 글에서는 **마크다운ㅎ글**을 Vercel에 배포하면서 겪은 실전 문제들과 해결 과정을 공유합니다.

## 1. 왜 Vercel인가?

배포 플랫폼으로 Vercel을 선택한 이유는 명확했습니다.

### Next.js Native Support
Next.js를 만든 회사답게 설정이 거의 필요 없습니다. GitHub 레포지토리만 연결하면 자동으로 빌드 설정을 감지하고 배포합니다. `next.config.js`, `package.json`만 있으면 끝.

### Serverless Functions
API 라우트가 자동으로 서버리스 함수로 변환됩니다. PDF 생성처럼 CPU-intensive한 작업도 독립적인 함수로 실행되어 전체 서버에 영향을 주지 않습니다. 트래픽이 없으면 비용도 0원.

### Free Hobby Plan
개인 프로젝트에 충분한 스펙:
- 100GB bandwidth/월
- 1000개 serverless function invocations/일
- 각 함수당 최대 60초 실행 시간
- 메모리 1024MB (이게 나중에 발목을 잡습니다...)

### Global CDN
정적 파일(이미지, 폰트, JS 번들)이 전 세계 CDN 엣지에 캐싱됩니다. 한국 사용자는 한국 엣지에서, 미국 사용자는 미국 엣지에서 받습니다.

### Zero-Config Deployment
`git push`만 하면 자동으로 빌드 → 테스트 → 배포. Preview deployment로 PR마다 독립적인 환경이 생성됩니다. 이거 한 번 써보면 다른 플랫폼 못 씁니다.

## 2. Vercel 설정

프로젝트 루트에 `vercel.json` 파일을 만들어 서버리스 함수를 튜닝합니다.

```json
{
  "functions": {
    "src/app/api/convert/route.ts": {
      "maxDuration": 60,
      "memory": 1024
    },
    "src/app/api/preview/route.ts": {
      "memory": 1024
    },
    "src/app/api/warmup/route.ts": {
      "maxDuration": 30,
      "memory": 1024
    }
  }
}
```

### 주요 설정 설명

**maxDuration: 60**
- PDF 변환은 Puppeteer가 Chromium을 띄우고, HTML을 렌더링하고, PDF로 출력하는 과정이 필요합니다.
- 이미지가 많거나 문서가 길면 10-30초 걸립니다.
- Hobby plan 최대치인 60초로 설정.

**memory: 1024**
- Chromium 프로세스 자체가 메모리를 많이 먹습니다 (~200-300MB).
- 고해상도 이미지가 포함되면 메모리 사용량이 급증합니다.
- Hobby plan 최대치인 1024MB로 설정. (나중에 이것 때문에 고생합니다)

## 3. 서버리스 환경에서 Puppeteer 돌리기

로컬 개발 환경에서는 시스템에 설치된 Chrome을 사용하면 됩니다. 하지만 Vercel 같은 서버리스 환경에서는 문제가 있습니다.

### The Challenge: Chromium Binary Size
- 일반 Puppeteer가 다운로드하는 Chromium은 약 **280MB**
- AWS Lambda 배포 패키지 한계: **250MB**
- Vercel도 Lambda 기반이라 같은 제약이 있습니다

"그럼 어떻게 하지?" 🤔

### The Solution: @sparticuz/chromium

[@sparticuz/chromium](https://github.com/Sparticuz/chromium)은 서버리스 환경에 최적화된 Chromium 바이너리입니다.
- 용량: **~50MB** (압축 상태)
- 불필요한 기능 제거 (GUI, GPU 가속 등)
- Lambda/Vercel에서 바로 실행 가능

설치:
```bash
npm install @sparticuz/chromium
npm install puppeteer-core  # puppeteer 대신 사용
```

### 환경별 분기 처리

로컬에서는 시스템 Chrome, Vercel에서는 @sparticuz/chromium을 사용하도록 분기합니다.

```typescript
// src/lib/browser.ts
import puppeteer from 'puppeteer-core';
import chromium from '@sparticuz/chromium';

const IS_VERCEL = !!process.env.VERCEL || !!process.env.AWS_LAMBDA_FUNCTION_NAME;

export async function launchBrowser() {
  if (IS_VERCEL) {
    // Vercel/Lambda 환경
    return await puppeteer.launch({
      args: chromium.args,
      defaultViewport: chromium.defaultViewport,
      executablePath: await chromium.executablePath(),
      headless: chromium.headless,
    });
  } else {
    // 로컬 개발 환경
    return await puppeteer.launch({
      executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
      headless: 'new',
    });
  }
}
```

### Warmup API Endpoint

서버리스 함수는 처음 호출될 때 **cold start**가 발생합니다. Chromium 바이너리를 다운로드하고 압축을 풀고 초기화하는 데 5-10초 걸립니다. 사용자가 첫 변환 버튼을 누르고 10초 기다리면... 이탈합니다.

해결책: warmup 엔드포인트를 만들어 미리 Chromium을 초기화합니다.

```typescript
// src/app/api/warmup/route.ts
import { NextRequest, NextResponse } from 'next/server';
import { launchBrowser } from '@/lib/browser';

export async function GET(request: NextRequest) {
  try {
    const browser = await launchBrowser();
    await browser.close();
    return NextResponse.json({ status: 'warm' });
  } catch (error) {
    return NextResponse.json({ error: 'warmup failed' }, { status: 500 });
  }
}
```

클라이언트에서 페이지 로드 시 자동 호출:
```typescript
// src/app/page.tsx
useEffect(() => {
  // Background warmup call
  fetch('/api/warmup').catch(console.error);
}, []);
```

## 4. 삽질 기록: 실전 문제 해결

이제부터가 진짜입니다. 로컬에서는 완벽하게 동작하던 앱이 Vercel에 배포하자마자 연달아 문제가 터졌습니다.

### 문제 1: 413 Error - Request Entity Too Large

**증상**
- 이미지가 포함된 마크다운 변환 시 `413 Payload Too Large` 에러
- 개발자 도구 Network 탭: Request payload **10.2MB**

**원인 분석**
- 마크다운에 이미지를 삽입하면 base64로 인코딩됩니다
- `![alt](data:image/png;base64,iVBORw0KG...)` 형태
- 2MB 이미지 → base64 인코딩 → 약 2.7MB (33% 증가)
- 이미지 3-4개면 쉽게 10MB 돌파
- **Vercel의 요청 본문 크기 제한: 4.5MB**

**시도 1: 이미지를 별도 업로드?**
→ 복잡도 증가. S3 같은 스토리지 필요. Hobby plan으로는 무리.

**시도 2: gzip 압축 사용**
→ 브라우저 `fetch`는 자동 압축을 지원하지만, Vercel이 인식 못 함.

**최종 해결책: 클라이언트에서 직접 gzip 압축**

```typescript
// src/lib/compressed-fetch.ts
export async function compressedFetch(url: string, options: RequestInit = {}) {
  const body = options.body as string;

  // 100KB 이상일 때만 압축 (작은 요청은 오히려 손해)
  if (body && body.length > 100 * 1024) {
    const encoder = new TextEncoder();
    const stream = new ReadableStream({
      start(controller) {
        controller.enqueue(encoder.encode(body));
        controller.close();
      },
    });

    const cs = new CompressionStream('gzip');
    const compressedStream = stream.pipeThrough(cs);
    const compressedData = await new Response(compressedStream).arrayBuffer();

    return fetch(url, {
      ...options,
      body: compressedData,
      headers: {
        ...options.headers,
        'Content-Encoding': 'gzip',
        'Content-Type': 'application/json',
      },
    });
  }

  return fetch(url, options);
}
```

서버 측에서는 `Content-Encoding: gzip` 헤더를 확인하고 압축 해제:

```typescript
// src/app/api/convert/route.ts
import { gunzipSync } from 'zlib';

export async function POST(request: NextRequest) {
  const contentEncoding = request.headers.get('content-encoding');

  let body: string;
  if (contentEncoding === 'gzip') {
    const buffer = Buffer.from(await request.arrayBuffer());
    const decompressed = gunzipSync(buffer);
    body = decompressed.toString('utf-8');
  } else {
    body = await request.text();
  }

  const data = JSON.parse(body);
  // ... PDF 생성
}
```

**결과**
- 10.2MB → **1.8MB** (약 82% 감소)
- 413 에러 완전 해결
- 네트워크 전송 시간도 단축

### 문제 2: 메모리 초과 (OOM) - 1024MB 한계

**증상**
- 고해상도 이미지가 포함된 문서 변환 시 간헐적 실패
- Vercel 로그: `Function exceeded memory limit`
- Hobby plan 최대 메모리: **1024MB**

**원인 분석**
- Chromium 프로세스 자체: ~200-300MB
- 4K 이미지 (3840×2160) 디코딩 시 메모리: 약 **30MB per image**
- 이미지 5개만 있어도: 300MB + 150MB = 450MB
- 렌더링 과정에서 추가 메모리 사용
- Peak memory usage: **1100-1200MB** → OOM

**시도 1: 서버에서 이미지 리사이징?**
→ Sharp 라이브러리 사용하려 했지만, 이미 메모리 부족한 상황에서 추가 처리는 역효과.

**시도 2: Puppeteer 옵션 튜닝**
```typescript
await puppeteer.launch({
  args: ['--disable-dev-shm-usage', '--disable-gpu', '--single-process'],
});
```
→ 약간 도움되지만 근본적 해결 안 됨.

**최종 해결책: 클라이언트에서 이미지 압축**

이미지를 서버로 보내기 전에 Canvas API로 압축합니다.

```typescript
// src/lib/image-processor.ts
export function compressImage(dataUrl: string): Promise<string> {
  return new Promise((resolve) => {
    const img = new Image();
    img.onload = () => {
      const canvas = document.createElement('canvas');
      const ctx = canvas.getContext('2d')!;

      // 최대 너비 1920px (Full HD)
      const maxWidth = 1920;
      const scale = Math.min(1, maxWidth / img.width);

      canvas.width = img.width * scale;
      canvas.height = img.height * scale;

      ctx.drawImage(img, 0, 0, canvas.width, canvas.height);

      // WebP 85% 품질
      // WebP는 JPEG보다 25-35% 작으면서 품질 유사
      const compressed = canvas.toDataURL('image/webp', 0.85);
      resolve(compressed);
    };
    img.src = dataUrl;
  });
}
```

마크다운 에디터에서 이미지 붙여넣기 시 자동 압축:

```typescript
// src/components/MarkdownEditor.tsx
const handlePaste = async (e: ClipboardEvent) => {
  const items = e.clipboardData?.items;
  if (!items) return;

  for (const item of items) {
    if (item.type.startsWith('image/')) {
      e.preventDefault();
      const file = item.getAsFile();
      if (!file) continue;

      const reader = new FileReader();
      reader.onload = async (event) => {
        const dataUrl = event.target?.result as string;
        const compressed = await compressImage(dataUrl);  // 압축!
        insertImage(compressed);
      };
      reader.readAsDataURL(file);
    }
  }
};
```

**결과**
- 4K PNG (8.5MB) → WebP 1920px (0.8MB) - **90% 감소**
- 메모리 사용량: 1200MB → **600MB**
- OOM 에러 완전 해결
- 추가 보너스: 네트워크 전송도 빨라짐

### 문제 3: Cold Start 지연

**증상**
- 첫 PDF 변환 요청 시 10-15초 대기
- 이후 요청은 2-3초로 빠름

**원인**
- Serverless function cold start
- Chromium 바이너리 다운로드 및 압축 해제
- Node.js 런타임 초기화

**해결책**
앞서 설명한 warmup API + 클라이언트 자동 호출로 해결했습니다. 추가로:

```typescript
// Vercel Cron Jobs로 주기적 warmup (vercel.json)
{
  "crons": [
    {
      "path": "/api/warmup",
      "schedule": "*/5 * * * *"  // 5분마다
    }
  ]
}
```

단, Hobby plan에서는 cron job이 제한적이라 production에서만 사용.

## 5. 성능 최적화 팁

### Debounced Preview
실시간 미리보기는 사용자 경험에 좋지만, 타이핑할 때마다 API 호출하면 서버리스 함수 quota를 금방 소진합니다.

```typescript
// 300ms debounce
const debouncedPreview = useMemo(
  () => debounce((markdown: string) => {
    fetch('/api/preview', {
      method: 'POST',
      body: JSON.stringify({ markdown }),
    });
  }, 300),
  []
);
```

### Image Caching
같은 이미지를 여러 번 압축하지 않도록 캐싱:

```typescript
const imageCache = new Map<string, string>();

export async function compressImageCached(dataUrl: string): Promise<string> {
  if (imageCache.has(dataUrl)) {
    return imageCache.get(dataUrl)!;
  }
  const compressed = await compressImage(dataUrl);
  imageCache.set(dataUrl, compressed);
  return compressed;
}
```

### Next.js Code Splitting
Next.js는 자동으로 페이지별 코드 스플리팅을 합니다. 추가로 동적 import 사용:

```typescript
// Heavy library를 필요할 때만 로드
const PDFViewer = dynamic(() => import('@/components/PDFViewer'), {
  ssr: false,
  loading: () => <Spinner />,
});
```

### Font Loading
구글 폰트를 `next/font`로 최적화:

```typescript
// src/app/layout.tsx
import { Noto_Sans_KR } from 'next/font/google';

const notoSansKR = Noto_Sans_KR({
  subsets: ['latin'],
  weight: ['400', '700'],
  display: 'swap',  // FOUT 방지
});
```

## 6. 회고 및 개선점

### What Went Well ✅
- **컨셉 검증**: "마크다운 편의성 + HWP 스타일 PDF" 조합이 실제로 필요한 사람들이 있었습니다.
- **서버리스 아키텍처**: 트래픽 없으면 비용 0원. 스파이크 트래픽도 자동 스케일.
- **빠른 배포**: GitHub에 push만 하면 자동 배포. Preview deployment 덕분에 안전하게 테스트 가능.

### Challenges 😅
- **메모리 제한**: Hobby plan 1024MB는 PDF 작업에 빠듯합니다. Pro plan ($20/월)은 3008MB까지 가능하지만, 개인 프로젝트에는 부담.
- **Cold Start**: 5-10초는 여전히 긴 편. Vercel의 Edge Functions는 cold start가 빠르지만 Puppeteer를 못 돌립니다.
- **디버깅 난이도**: 서버리스 환경 특성상 로컬과 프로덕션 환경이 달라서 디버깅이 까다로웠습니다.

### Future Plans 🚀
- **Self-hosted 옵션**: Docker 이미지 제공해서 회사 내부망에서도 사용 가능하게
- **더 많은 템플릿**: 논문, 이력서, 제안서 등 용도별 스타일
- **협업 기능**: 실시간 공동 편집 (WebSocket + CRDT)
- **이미지 스토리지**: S3/Cloudflare R2 연동으로 대용량 이미지 처리

### Lessons Learned 💡

**1. 큰 문서로 일찍 테스트하라**
- 개발 초기부터 이미지 10개 + 50페이지 문서로 테스트했다면 메모리 문제를 일찍 발견했을 겁니다.
- "로컬에서 잘 돌아가네" → "배포했더니 OOM" 패턴은 정말 흔합니다.

**2. 압축은 서버리스의 친구**
- gzip, WebP, code splitting 등 모든 종류의 압축이 도움됩니다.
- 네트워크도 빨라지고, 메모리도 절약되고, 비용도 줄어듭니다.

**3. 클라이언트를 활용하라**
- 서버리스 함수는 비싸고 제한적입니다. 클라이언트 CPU/메모리는 공짜입니다.
- 이미지 압축, 데이터 검증, 캐싱 등 가능한 건 클라이언트에서 처리.

**4. Monitoring은 필수**
- Vercel Analytics로 함수 실행 시간, 메모리 사용량, 에러율 추적
- Sentry 같은 에러 트래킹 도구 연동
- 문제가 터지기 전에 징조를 파악할 수 있습니다

## 마치며

3부작 시리즈를 통해 **마크다운ㅎ글** 프로젝트의 기획부터 개발, 배포까지 전 과정을 공유했습니다.

- [Part 1](/dev/markdown-hangul/part-1/)에서는 "왜 만들었는가"
- [Part 2](/dev/markdown-hangul/part-2/)에서는 "어떻게 만들었는가"
- Part 3에서는 "어떻게 세상에 내놓았는가"

개인 프로젝트지만 실제 사용자들의 피드백을 받으며 개선하는 과정이 즐거웠습니다. 무엇보다 "이런 거 찾고 있었어요!"라는 반응이 가장 큰 보람이었습니다.

서버리스 환경은 제약도 많지만, 제대로 이해하고 최적화하면 개인 개발자에게 최고의 도구입니다. 여러분의 사이드 프로젝트도 Vercel에 올려보세요!

테스트 URL: <https://md.takjakim.kr>

질문이나 피드백은 편하게 메시지로 줘. 감사합니다.

---

## 🔗 연결 (백링크용)
- Part 1: [[마크다운ㅎ글 개발기 (1) - 기획: 마크다운으로 공문서 쓰기]]
- Part 2: [[마크다운ㅎ글 개발기 (2) - 개발: 기술 스택과 핵심 구현]]
- 허브: [[개발 노트 시작하기]]
