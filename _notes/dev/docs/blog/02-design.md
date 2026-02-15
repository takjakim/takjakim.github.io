---
title: "stats.takjakim.kr 개발기 (2): 설계"
last_modified_at: 2026-02-15
permalink: /dev/stats-method/design/
tags: [stats, education, architecture, nextjs, supabase]
importance: 2
---

# stats.takjakim.kr 개발기 (2): 설계

> Method 개발기 시리즈 (2/4)

[← 이전: 기획](/dev/stats-method/planning/) | [목차](/dev/stats-method/) | [다음: 개발 →](/dev/stats-method/development/)

---

## 개요

<!-- 다이어그램: ./images/architecture-diagram.excalidraw -->
![학습 페이지](/assets/img/stats-method/design-curriculum.png)

이 파트에서는 Method 프로젝트의 설계를 다룹니다:
- 기술 스택 선정
- 시스템 아키텍처
- 데이터 모델
- 콘텐츠 구조

---

## 1. 기술 스택 선정

### 1.1 프론트엔드

| 기술 | 버전 | 선택 이유 |
|------|------|-----------|
| **Next.js** | 15 | App Router, React Server Components |
| **React** | 19 | 최신 기능 (Suspense, Streaming) |
| **TypeScript** | 5.0 | 타입 안정성, DX |
| **Tailwind CSS** | 3.4 | 빠른 스타일링, 반응형 |
| **shadcn/ui** | - | 접근성, 커스터마이징 |

### 1.2 콘텐츠

| 기술 | 선택 이유 |
|------|-----------|
| **MDX** | 마크다운 + React 컴포넌트 |
| **next-mdx-remote v6** | RSC 지원, 동적 로딩 |

### 1.3 Python 실행

| 기술 | 선택 이유 |
|------|-----------|
| **Pyodide** | 서버 없이 브라우저 내 실행 |
| **WebAssembly** | 네이티브급 성능 |

### 1.4 백엔드

| 기술 | 선택 이유 |
|------|-----------|
| **Supabase** | PostgreSQL + Auth + 무료 티어 |
| **Prisma** | Type-safe ORM |
| **NextAuth.js v5** | Google OAuth + Credentials |

### 1.5 인프라

| 기술 | 선택 이유 |
|------|-----------|
| **Vercel** | Next.js 최적화, 자동 CI/CD |
| **GitHub** | 코드 저장소, PR Preview |

---

## 2. 시스템 아키텍처

### 2.1 전체 아키텍처

```
┌──────────────────────────────────────────────────────────────────────┐
│                         CLIENT (Browser)                              │
│  ┌────────────────┐  ┌────────────────┐  ┌────────────────────────┐  │
│  │    React       │  │     MDX        │  │   Pyodide (WASM)       │  │
│  │  Components    │  │   Lessons      │  │  numpy, pandas, scipy  │  │
│  │  (shadcn/ui)   │  │  (RSC render)  │  │  scikit-learn          │  │
│  └────────────────┘  └────────────────┘  └────────────────────────┘  │
└──────────────────────────────────────────────────────────────────────┘
                                │
                    ┌───────────┴───────────┐
                    │        HTTPS          │
                    └───────────┬───────────┘
                                ▼
┌──────────────────────────────────────────────────────────────────────┐
│                    NEXT.JS 15 SERVER (Vercel Edge)                    │
│  ┌────────────────┐  ┌────────────────┐  ┌────────────────────────┐  │
│  │   App Router   │  │  API Routes    │  │   next-mdx-remote      │  │
│  │  (File-based)  │  │  /api/auth     │  │   (RSC compile)        │  │
│  │                │  │  /api/progress │  │                        │  │
│  └────────────────┘  └────────────────┘  └────────────────────────┘  │
└──────────────────────────────────────────────────────────────────────┘
                                │
                    ┌───────────┴───────────┐
                    │      Prisma ORM       │
                    └───────────┬───────────┘
                                ▼
┌──────────────────────────────────────────────────────────────────────┐
│                           SUPABASE                                    │
│  ┌────────────────┐  ┌────────────────┐  ┌────────────────────────┐  │
│  │   PostgreSQL   │  │     Auth       │  │      Storage           │  │
│  │  Users, Progress │  │   (OAuth)      │  │   (Future: Files)     │  │
│  └────────────────┘  └────────────────┘  └────────────────────────┘  │
└──────────────────────────────────────────────────────────────────────┘
```

### 2.2 데이터 흐름

```
┌─────────┐     ┌─────────┐     ┌─────────┐     ┌─────────┐
│  User   │────▶│ Next.js │────▶│ Prisma  │────▶│Supabase │
│ Browser │◀────│ Server  │◀────│  ORM    │◀────│   DB    │
└─────────┘     └─────────┘     └─────────┘     └─────────┘
     │
     │ Pyodide (Client-side only)
     ▼
┌─────────┐
│ Python  │ ← 서버 통신 없음
│  WASM   │
└─────────┘
```

### 2.3 인증 흐름

```
┌─────────┐     ┌─────────────┐     ┌──────────┐
│  User   │────▶│  NextAuth   │────▶│  Google  │
│         │◀────│   v5        │◀────│  OAuth   │
└─────────┘     └──────┬──────┘     └──────────┘
                       │
                       ▼
                ┌─────────────┐
                │   Prisma    │
                │   Adapter   │
                └──────┬──────┘
                       │
                       ▼
                ┌─────────────┐
                │  Supabase   │
                │  PostgreSQL │
                └─────────────┘
```

---

## 3. 데이터 모델

### 3.1 ERD

```
┌─────────────────────┐       ┌─────────────────────┐
│        User         │       │       Progress       │
├─────────────────────┤       ├─────────────────────┤
│ id         (PK)     │──┐    │ id         (PK)     │
│ email      (UNIQUE) │  │    │ lessonId            │
│ name                │  │    │ completed           │
│ password?           │  └───▶│ userId     (FK)     │
│ emailVerified?      │       │ createdAt           │
│ image?              │       │ updatedAt           │
│ createdAt           │       └─────────────────────┘
│ updatedAt           │
└─────────────────────┘
         │
         │ NextAuth.js Relations
         ▼
┌─────────────────────┐       ┌─────────────────────┐
│       Account       │       │       Session       │
├─────────────────────┤       ├─────────────────────┤
│ provider            │       │ sessionToken        │
│ providerAccountId   │       │ expires             │
│ type                │       │ userId     (FK)     │
│ access_token        │       └─────────────────────┘
│ userId     (FK)     │
└─────────────────────┘
```

### 3.2 Prisma 스키마

```prisma
// prisma/schema.prisma

model User {
  id            String    @id @default(cuid())
  name          String?
  email         String    @unique
  emailVerified DateTime?
  image         String?
  password      String?   // 이메일/비밀번호 가입 시

  accounts      Account[]
  sessions      Session[]
  progress      Progress[]

  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt
}

model Progress {
  id        String   @id @default(cuid())
  lessonId  String   // "descriptive-statistics/mean"
  completed Boolean  @default(false)
  userId    String
  user      User     @relation(fields: [userId], references: [id], onDelete: Cascade)

  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt

  @@unique([lessonId, userId])
  @@index([userId])
}

// NextAuth.js 관련 모델들...
```

---

## 4. 콘텐츠 구조

### 4.1 디렉토리 구조

```
content/
├── lessons/
│   ├── ko/                              # 한국어 레슨
│   │   ├── descriptive-statistics/      # 기술통계
│   │   │   ├── mean.mdx                 # 평균
│   │   │   ├── median.mdx               # 중앙값
│   │   │   ├── variance.mdx             # 분산
│   │   │   └── correlation.mdx          # 상관관계
│   │   │
│   │   ├── probability-distributions/   # 확률분포
│   │   │   ├── probability-basics.mdx
│   │   │   ├── binomial-distribution.mdx
│   │   │   └── normal-distribution.mdx
│   │   │
│   │   ├── inferential-statistics/      # 추론통계
│   │   │   ├── sampling.mdx
│   │   │   ├── central-limit-theorem.mdx
│   │   │   ├── confidence-intervals.mdx
│   │   │   └── hypothesis-testing.mdx
│   │   │
│   │   ├── regression-analysis/         # 회귀분석
│   │   │   ├── simple-regression.mdx
│   │   │   └── multiple-regression.mdx
│   │   │
│   │   ├── factor-analysis/             # 요인분석
│   │   │   ├── exploratory-factor-analysis.mdx
│   │   │   └── confirmatory-factor-analysis.mdx
│   │   │
│   │   ├── advanced-regression/         # 고급 회귀
│   │   │   ├── hierarchical-regression.mdx
│   │   │   ├── logistic-regression.mdx
│   │   │   ├── moderated-mediation.mdx
│   │   │   └── mediated-moderation.mdx
│   │   │
│   │   └── sem/                         # 구조방정식
│   │       └── structural-equation-modeling.mdx
│   │
│   └── en/                              # 영어 레슨
│       └── ... (미러 구조)
│
└── exercises/
    ├── descriptive-statistics/
    │   ├── mean.json                    # 평균 연습문제
    │   ├── median.json
    │   └── ...
    └── ...
```

### 4.2 레슨 파일 구조 (MDX)

```mdx
---
title: "평균 (Mean)"
description: "데이터의 중심을 나타내는 가장 기본적인 측도"
difficulty: "beginner"
duration: 15
prerequisites: []
---

# 평균이란?

평균은 <BlurWord>모든 관측값의 합</BlurWord>을 개수로 나눈 값입니다.

## 수식

$$
\bar{x} = \frac{1}{n}\sum_{i=1}^{n}x_i
$$

## 실습

<InteractiveCode
  title="평균 계산하기"
  expectedValue="27.625"
  starterCode="import numpy as np&#10;data = [15, 18, 21, 19, 17, 20, 16, 95]&#10;result = np.mean(data)"
/>

## 퀴즈

<QuestionCard>
이상치가 있을 때 평균의 특성은?
</QuestionCard>

<RevealAnswer>
이상치에 민감하여 왜곡될 수 있음
</RevealAnswer>
```

### 4.3 연습문제 파일 구조 (JSON)

```json
{
  "title": "평균 연습문제",
  "description": "평균 계산 실습",
  "exercises": [
    {
      "id": "mean-001",
      "type": "code",
      "difficulty": "easy",
      "question": "주어진 데이터의 산술평균을 계산하세요.",
      "starterCode": "import numpy as np\ndata = [10, 20, 30, 40, 50]\nresult = ___",
      "expectedValue": 30,
      "tolerance": 0.01,
      "hints": ["np.mean() 함수를 사용하세요"]
    },
    {
      "id": "mean-002",
      "type": "code",
      "difficulty": "medium",
      "question": "가중평균을 계산하세요.",
      "starterCode": "weights = [0.3, 0.3, 0.4]\nvalues = [80, 90, 85]\nresult = ___",
      "expectedValue": 85,
      "tolerance": 0.01
    }
  ]
}
```

---

## 5. 라우팅 설계

### 5.1 App Router 구조

```
app/
├── [locale]/                    # i18n (ko, en)
│   ├── page.tsx                 # 홈페이지 /
│   ├── layout.tsx               # 공통 레이아웃
│   │
│   ├── learn/
│   │   ├── page.tsx             # 학습 목록 /learn
│   │   └── [topic]/
│   │       └── [lesson]/
│   │           ├── page.tsx     # 레슨 /learn/descriptive-statistics/mean
│   │           └── exercises/
│   │               └── page.tsx # 연습문제 /learn/.../mean/exercises
│   │
│   ├── dashboard/
│   │   └── page.tsx             # 대시보드 /dashboard
│   │
│   └── auth/
│       ├── signin/
│       │   └── page.tsx         # 로그인 /auth/signin
│       ├── signup/
│       │   └── page.tsx         # 회원가입 /auth/signup
│       └── error/
│           └── page.tsx         # 에러 /auth/error
│
└── api/
    ├── auth/
    │   └── [...nextauth]/
    │       └── route.ts         # NextAuth API
    └── progress/
        └── route.ts             # 진도 저장 API
```

### 5.2 URL 설계

| URL | 페이지 | 인증 필요 |
|-----|--------|----------|
| `/ko` | 홈페이지 | X |
| `/ko/learn` | 학습 목록 | X |
| `/ko/learn/[topic]/[lesson]` | 레슨 | X |
| `/ko/learn/.../exercises` | 연습문제 | X |
| `/ko/dashboard` | 대시보드 | O |
| `/ko/auth/signin` | 로그인 | X |
| `/ko/auth/signup` | 회원가입 | X |

---

## 설계 원칙

### Server-First
- React Server Components 우선 사용
- 클라이언트 컴포넌트는 인터랙션 필요한 곳만

### Type-Safety
- 모든 곳에 TypeScript
- Prisma로 DB 타입 자동 생성

### Progressive Enhancement
- 비로그인도 학습 가능
- 로그인 시 진도 저장 추가

---

[← 이전: 기획](/dev/stats-method/planning/) | [목차](/dev/stats-method/) | [다음: 개발 →](/dev/stats-method/development/)
