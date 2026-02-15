# Method 개발기

> **stats.takjakim.kr** - 대학(원)생을 위한 인터랙티브 통계학 학습 플랫폼

![Method 홈페이지](../images/home.png)

---

## 시리즈 목차

이 개발기는 4개의 파트로 구성되어 있습니다:

| # | 파트 | 내용 | 핵심 키워드 |
|---|------|------|------------|
| 1 | [기획](./01-planning.md) | 문제 인식, 솔루션 컨셉, 타겟 사용자 | Problem-Solution Fit |
| 2 | [설계](./02-design.md) | 기술 스택, 시스템 아키텍처, 데이터 모델 | Architecture |
| 3 | [개발](./03-development.md) | Pyodide, MDX, 인증, 진도 추적 | Implementation |
| 4 | [배포](./04-deployment.md) | Vercel, CI/CD, 모니터링 | DevOps |

---

## 프로젝트 요약

### 핵심 기능
- **인터랙티브 Python 실행** - Pyodide 기반 브라우저 내 실행
- **체계적인 커리큘럼** - 기술통계 → 회귀분석 → 고급 방법론
- **20+ 레슨 & 170+ 연습문제**
- **학습 진도 저장** - 로그인 후 진행률 추적

### 기술 스택
```
Frontend: Next.js 15 + React 19 + TypeScript
Styling:  Tailwind CSS + shadcn/ui
Content:  MDX + next-mdx-remote v6
Python:   Pyodide (WebAssembly)
Database: Supabase (PostgreSQL) + Prisma
Auth:     NextAuth.js v5
Deploy:   Vercel
```

### 스크린샷

<table>
  <tr>
    <td><img src="../images/home.png" alt="홈페이지" /></td>
    <td><img src="../images/learn.png" alt="학습 페이지" /></td>
  </tr>
  <tr>
    <td><img src="../images/lesson-mean.png" alt="레슨" /></td>
    <td><img src="../images/exercises.png" alt="연습문제" /></td>
  </tr>
</table>

---

**Links**
- Live: [stats.takjakim.kr](https://stats.takjakim.kr)
- GitHub: [github.com/takjakim/stat-method](https://github.com/takjakim/stat-method)
- Developer: 김재현 ([takjakim.kr](https://takjakim.kr))

*2026년 2월 작성*
