---
title: "stats.takjakim.kr 개발기 (4): 배포"
last_modified_at: 2026-02-15
permalink: /dev/stats-method/deployment/
tags: [stats, education, deployment, vercel, ci-cd]
importance: 2
---

# stats.takjakim.kr 개발기 (4): 배포

> Method 개발기 시리즈 (4/4)

[← 이전: 개발](/dev/stats-method/development/) | [목차](/dev/stats-method/)

---

## 개요

<!-- 다이어그램: ./images/deployment-diagram.excalidraw -->
![프로덕션 사이트](/assets/img/stats-method/deploy-production.png)

이 파트에서는 배포 및 운영을 다룹니다:
- Vercel 배포
- CI/CD 파이프라인
- 커스텀 도메인
- 모니터링

---

## 1. Vercel 배포

### 1.1 왜 Vercel인가?

| 기능 | Vercel | 다른 옵션 |
|------|--------|-----------|
| **Next.js 최적화** | 공식 지원 (만든 회사) | 추가 설정 필요 |
| **무료 티어** | 충분함 | 제한적 |
| **자동 CI/CD** | Git push로 끝 | 별도 설정 |
| **Edge Functions** | 기본 지원 | 제한적 |
| **Preview 배포** | PR마다 자동 | 수동 설정 |

### 1.2 배포 프로세스

```
┌─────────┐     ┌─────────┐     ┌─────────┐     ┌─────────┐
│  Code   │────▶│  Push   │────▶│  Build  │────▶│  Deploy │
│  Edit   │     │ GitHub  │     │ Vercel  │     │  Edge   │
└─────────┘     └─────────┘     └─────────┘     └─────────┘
                     │               │               │
                     │               │               ▼
                     │               │         ┌─────────┐
                     │               │         │  Live   │
                     │               │         │  Site   │
                     │               │         └─────────┘
                     │               │
                     │               ▼
                     │         ┌─────────┐
                     └────────▶│ Preview │ (PR 생성 시)
                               │  URL    │
                               └─────────┘
```

### 1.3 초기 설정

```bash
# 1. Vercel CLI 설치
npm i -g vercel

# 2. 로그인
vercel login

# 3. 프로젝트 연결
vercel link

# 4. 환경변수 설정
vercel env add DATABASE_URL
vercel env add NEXTAUTH_SECRET
vercel env add GOOGLE_CLIENT_ID
vercel env add GOOGLE_CLIENT_SECRET
vercel env add NEXTAUTH_URL

# 5. 프로덕션 배포
vercel --prod
```

### 1.4 vercel.json 설정

```json
{
  "framework": "nextjs",
  "regions": ["icn1"],
  "functions": {
    "app/api/**/*": {
      "maxDuration": 30
    }
  },
  "headers": [
    {
      "source": "/(.*)",
      "headers": [
        {
          "key": "X-Content-Type-Options",
          "value": "nosniff"
        },
        {
          "key": "X-Frame-Options",
          "value": "DENY"
        }
      ]
    }
  ]
}
```

---

## 2. CI/CD 파이프라인

### 2.1 자동 배포 흐름

```
┌──────────────────────────────────────────────────────────────┐
│                        GitHub Repository                      │
├──────────────────────────────────────────────────────────────┤
│                                                               │
│   ┌─────────┐                              ┌─────────────┐   │
│   │  main   │──── push ────────────────────▶│ Production  │   │
│   │ branch  │                              │   Deploy    │   │
│   └─────────┘                              └─────────────┘   │
│        ▲                                                      │
│        │ merge                                                │
│   ┌─────────┐                              ┌─────────────┐   │
│   │ feature │──── PR 생성 ─────────────────▶│  Preview    │   │
│   │ branch  │                              │   Deploy    │   │
│   └─────────┘                              └─────────────┘   │
│                                                               │
└──────────────────────────────────────────────────────────────┘
```

### 2.2 브랜치 전략

| 브랜치 | 용도 | 배포 환경 |
|--------|------|-----------|
| `main` | 프로덕션 코드 | Production |
| `feature/*` | 기능 개발 | Preview |
| `fix/*` | 버그 수정 | Preview |

### 2.3 Preview 배포

PR 생성 시 자동으로 Preview URL 생성:

```
https://method-git-feature-login-takjakim.vercel.app
```

- PR 코멘트에 자동으로 URL 추가
- 코드 리뷰 시 실제 동작 확인 가능
- PR 닫으면 자동 삭제

---

## 3. 환경변수 관리

### 3.1 환경별 변수

| 환경 | 용도 | 설정 위치 |
|------|------|-----------|
| **Development** | 로컬 개발 | `.env.local` |
| **Preview** | PR 테스트 | Vercel Dashboard |
| **Production** | 실서비스 | Vercel Dashboard |

### 3.2 필수 환경변수

```env
# Database (Supabase)
DATABASE_URL="postgresql://postgres:password@db.xxx.supabase.co:5432/postgres"

# NextAuth.js
NEXTAUTH_SECRET="your-secret-key-here"
NEXTAUTH_URL="https://stats.takjakim.kr"

# Google OAuth
GOOGLE_CLIENT_ID="xxx.apps.googleusercontent.com"
GOOGLE_CLIENT_SECRET="GOCSPX-xxx"
```

### 3.3 비밀값 관리

```bash
# Vercel CLI로 환경변수 추가 (암호화 저장)
vercel env add DATABASE_URL production

# 입력 프롬프트
? What's the value of DATABASE_URL? [hidden]
```

---

## 4. 커스텀 도메인

### 4.1 도메인 설정

```
┌──────────────────────────────────────────────────────────────┐
│                         DNS 설정                              │
├──────────────────────────────────────────────────────────────┤
│                                                               │
│   stats.takjakim.kr ──── CNAME ────▶ cname.vercel-dns.com    │
│                                                               │
└──────────────────────────────────────────────────────────────┘
```

### 4.2 설정 단계

1. **Vercel Dashboard** → Settings → Domains
2. `stats.takjakim.kr` 입력
3. DNS 레코드 안내 확인
4. **도메인 레지스트라**에서 CNAME 추가:
   - Host: `stats`
   - Value: `cname.vercel-dns.com`
5. SSL 인증서 자동 발급 (Let's Encrypt)

### 4.3 리다이렉트 설정

```js
// next.config.js
module.exports = {
  async redirects() {
    return [
      {
        source: '/',
        destination: '/ko',
        permanent: false,
      },
    ];
  },
};
```

---

## 5. 모니터링

### 5.1 Vercel Analytics

```
┌──────────────────────────────────────────────────────────────┐
│                     Vercel Analytics                          │
├──────────────────────────────────────────────────────────────┤
│                                                               │
│   Page Views        ████████████████████  12,345             │
│   Unique Visitors   ██████████████        8,234              │
│   Bounce Rate       ████████              32%                 │
│                                                               │
│   Top Pages:                                                  │
│   1. /ko/learn/descriptive-statistics/mean    2,345 views    │
│   2. /ko                                      1,890 views    │
│   3. /ko/learn                                1,456 views    │
│                                                               │
└──────────────────────────────────────────────────────────────┘
```

```tsx
// app/layout.tsx
import { Analytics } from '@vercel/analytics/react';

export default function RootLayout({ children }) {
  return (
    <html>
      <body>
        {children}
        <Analytics />
      </body>
    </html>
  );
}
```

### 5.2 Speed Insights

```tsx
import { SpeedInsights } from '@vercel/speed-insights/next';

export default function RootLayout({ children }) {
  return (
    <html>
      <body>
        {children}
        <SpeedInsights />
      </body>
    </html>
  );
}
```

### 5.3 Web Vitals

| 메트릭 | 타겟 | 현재 |
|--------|------|------|
| **LCP** (Largest Contentful Paint) | < 2.5s | 1.8s |
| **FID** (First Input Delay) | < 100ms | 45ms |
| **CLS** (Cumulative Layout Shift) | < 0.1 | 0.05 |
| **TTFB** (Time to First Byte) | < 800ms | 320ms |

### 5.4 Error Tracking (예정)

```tsx
// Sentry 설정 (예정)
import * as Sentry from '@sentry/nextjs';

Sentry.init({
  dsn: process.env.SENTRY_DSN,
  tracesSampleRate: 1.0,
});
```

---

## 6. 성능 최적화

### 6.1 이미지 최적화

```tsx
import Image from 'next/image';

// 자동 최적화
<Image
  src="/images/hero.png"
  alt="Hero"
  width={1200}
  height={630}
  priority // LCP 이미지
/>
```

### 6.2 폰트 최적화

```tsx
// app/layout.tsx
import { Noto_Sans_KR } from 'next/font/google';

const notoSansKr = Noto_Sans_KR({
  subsets: ['latin'],
  weight: ['400', '500', '700'],
  display: 'swap', // FOIT 방지
});
```

### 6.3 번들 분석

```bash
# 번들 사이즈 분석
ANALYZE=true npm run build
```

---

## 7. 배포 체크리스트

### 배포 전

- [ ] `npm run build` 성공
- [ ] `npm run lint` 경고 없음
- [ ] 환경변수 모두 설정
- [ ] 데이터베이스 마이그레이션 완료

### 배포 후

- [ ] 메인 페이지 로드 확인
- [ ] 로그인/로그아웃 동작 확인
- [ ] 레슨 페이지 Python 실행 확인
- [ ] 모바일 반응형 확인
- [ ] 진도 저장 동작 확인

---

## 결론 및 향후 계획

### 배운 점

1. **Vercel + Next.js**: 배포가 놀라울 정도로 간단
2. **Preview 배포**: PR 리뷰 효율 크게 향상
3. **Edge Functions**: 한국 리전(icn1) 선택으로 지연시간 최소화

### 향후 계획

- [ ] **Sentry** 연동 - 에러 트래킹
- [ ] **PWA** - 오프라인 지원
- [ ] **WebR** - R 언어 지원
- [ ] **AI 튜터** - Claude 연동
- [ ] **커뮤니티** - 댓글, 질문 기능

---

## 마무리

4개의 파트에 걸쳐 Method 프로젝트의 기획부터 배포까지 전 과정을 살펴보았습니다.

**핵심 요약:**
- **기획**: 환경 설정 없이 바로 통계 실습
- **설계**: Next.js 15 + Pyodide + Supabase
- **개발**: InteractiveCode, MDX, 인증
- **배포**: Vercel 자동 CI/CD

이 프로젝트가 통계를 배우는 분들께 도움이 되길 바랍니다.

---

**Links**
- Live: [stats.takjakim.kr](https://stats.takjakim.kr)
- GitHub: [github.com/takjakim/stat-method](https://github.com/takjakim/stat-method)
- Developer: 김재현 ([takjakim.kr](https://takjakim.kr))

---

[← 이전: 개발](/dev/stats-method/development/) | [목차](/dev/stats-method/)

*2026년 2월 작성*
