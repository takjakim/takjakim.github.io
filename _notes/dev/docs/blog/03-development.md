---
title: "stats.takjakim.kr 개발기 (3): 개발"
last_modified_at: 2026-02-15
permalink: /dev/stats-method/development/
tags: [stats, education, implementation, pyodide, mdx, nextauth]
importance: 2
---

# stats.takjakim.kr 개발기 (3): 개발

> Method 개발기 시리즈 (3/4)

[← 이전: 설계](/dev/stats-method/design/) | [목차](/dev/stats-method/) | [다음: 배포 →](/dev/stats-method/deployment/)

---

## 개요

<!-- 다이어그램: ./images/development-diagram.excalidraw -->
![레슨 페이지](/assets/img/stats-method/lesson-mean.png)

이 파트에서는 핵심 기능 구현을 다룹니다:
- Pyodide를 통한 브라우저 내 Python 실행
- MDX 컴포넌트 시스템
- 반응형 모바일 UI
- 인증 및 진도 추적

---

## 1. 인터랙티브 Python 실행 (Pyodide)

### 1.1 Pyodide란?

![레슨 페이지](/assets/img/stats-method/dev-variance.png)

**Pyodide**는 Python을 WebAssembly로 컴파일하여 브라우저에서 실행할 수 있게 해주는 프로젝트입니다.

```
┌─────────────────────────────────────────┐
│              Browser                     │
│  ┌───────────────────────────────────┐  │
│  │         Pyodide (WASM)            │  │
│  │  ┌─────────┐  ┌──────────────┐   │  │
│  │  │ Python  │  │  Packages     │   │  │
│  │  │ 3.11    │  │  numpy        │   │  │
│  │  │         │  │  pandas       │   │  │
│  │  │         │  │  scipy        │   │  │
│  │  └─────────┘  └──────────────┘   │  │
│  └───────────────────────────────────┘  │
│           ↑                              │
│     No Server Needed!                    │
└─────────────────────────────────────────┘
```

### 1.2 InteractiveCode 컴포넌트

```tsx
// components/lesson/InteractiveCode.tsx

'use client';

import { useState, useEffect } from 'react';
import { usePyodide } from '@/hooks/usePyodide';
import CodeEditor from './CodeEditor';

interface InteractiveCodeProps {
  title?: string;
  description?: string;
  starterCode?: string;
  expectedValue?: number | string;
  tolerance?: number | string;
  resultVar?: string;
  difficulty?: 'easy' | 'medium' | 'hard';
}

export default function InteractiveCode({
  title,
  description,
  starterCode,
  expectedValue: expectedValueProp,
  tolerance: toleranceProp = 0.01,
  resultVar = 'result',
  difficulty = 'medium',
}: InteractiveCodeProps) {
  // MDX는 모든 prop을 문자열로 전달 → 숫자로 파싱
  const expectedValue = typeof expectedValueProp === 'string'
    ? parseFloat(expectedValueProp)
    : expectedValueProp;

  const tolerance = typeof toleranceProp === 'string'
    ? parseFloat(toleranceProp)
    : toleranceProp;

  // HTML 엔티티 (&#10;) → 실제 줄바꿈으로 변환
  const processedStarterCode = starterCode?.replace(/&#10;/g, '\n');

  const { pyodide, isLoading, error } = usePyodide();
  const [code, setCode] = useState(processedStarterCode || '');
  const [output, setOutput] = useState('');
  const [validation, setValidation] = useState<{
    isCorrect: boolean;
    message: string;
  } | null>(null);

  const runCode = async () => {
    if (!pyodide) return;

    try {
      // stdout 캡쳐
      pyodide.runPython(`
        import sys
        from io import StringIO
        sys.stdout = StringIO()
      `);

      // 사용자 코드 실행
      await pyodide.runPythonAsync(code);

      // 출력 가져오기
      const stdout = pyodide.runPython('sys.stdout.getvalue()');
      setOutput(stdout);

      // 결과 변수 검증
      if (expectedValue !== undefined) {
        const result = pyodide.globals.get(resultVar);
        const numResult = typeof result === 'number' ? result : result?.toJs?.();

        if (Math.abs(numResult - expectedValue) <= tolerance) {
          setValidation({
            isCorrect: true,
            message: '정답입니다! 🎉',
          });
        } else {
          setValidation({
            isCorrect: false,
            message: `오답입니다. 다시 시도해보세요.`,
          });
        }
      }
    } catch (err) {
      setOutput(`Error: ${err}`);
      setValidation(null);
    }
  };

  return (
    <div className="my-6 rounded-lg border bg-card">
      <div className="border-b px-4 py-3 flex items-center justify-between">
        <div>
          {title && <h3 className="font-semibold">{title}</h3>}
          {description && (
            <p className="text-sm text-muted-foreground">{description}</p>
          )}
        </div>
        <span className={`text-xs px-2 py-1 rounded ${
          difficulty === 'easy' ? 'bg-green-100 text-green-800' :
          difficulty === 'medium' ? 'bg-yellow-100 text-yellow-800' :
          'bg-red-100 text-red-800'
        }`}>
          {difficulty}
        </span>
      </div>

      <div className="p-4">
        <CodeEditor
          value={code}
          onChange={setCode}
          language="python"
        />

        <div className="mt-4 flex gap-2">
          <button
            onClick={runCode}
            disabled={isLoading}
            className="px-4 py-2 bg-primary text-primary-foreground rounded"
          >
            {isLoading ? '로딩 중...' : '실행'}
          </button>
          <button
            onClick={() => setCode(processedStarterCode || '')}
            className="px-4 py-2 border rounded"
          >
            초기화
          </button>
        </div>

        {output && (
          <pre className="mt-4 p-4 bg-muted rounded text-sm overflow-x-auto">
            {output}
          </pre>
        )}

        {validation && (
          <div className={`mt-4 p-4 rounded ${
            validation.isCorrect
              ? 'bg-green-50 text-green-800 border border-green-200'
              : 'bg-red-50 text-red-800 border border-red-200'
          }`}>
            {validation.message}
          </div>
        )}
      </div>
    </div>
  );
}
```

### 1.3 Pyodide 훅

```tsx
// hooks/usePyodide.ts

import { useState, useEffect } from 'react';

let pyodideInstance: any = null;
let pyodideLoading: Promise<any> | null = null;

export function usePyodide() {
  const [pyodide, setPyodide] = useState<any>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    const loadPyodide = async () => {
      // 이미 로드됨
      if (pyodideInstance) {
        setPyodide(pyodideInstance);
        setIsLoading(false);
        return;
      }

      // 로딩 중 (다른 컴포넌트가 먼저 요청)
      if (pyodideLoading) {
        pyodideInstance = await pyodideLoading;
        setPyodide(pyodideInstance);
        setIsLoading(false);
        return;
      }

      // 새로 로드
      try {
        pyodideLoading = window.loadPyodide({
          indexURL: 'https://cdn.jsdelivr.net/pyodide/v0.24.1/full/',
        });

        pyodideInstance = await pyodideLoading;

        // 통계 패키지 미리 로드
        await pyodideInstance.loadPackage([
          'numpy',
          'pandas',
          'scipy',
          'scikit-learn',
        ]);

        setPyodide(pyodideInstance);
        setIsLoading(false);
      } catch (err) {
        setError(err as Error);
        setIsLoading(false);
      }
    };

    loadPyodide();
  }, []);

  return { pyodide, isLoading, error };
}
```

---

## 2. MDX 컴포넌트 시스템

### 2.1 MDX 컴파일 설정

```tsx
// lib/mdx.ts

import { compileMDX } from 'next-mdx-remote/rsc';
import { readFile } from 'fs/promises';
import path from 'path';

// MDX 컴포넌트 매핑
import InteractiveCode from '@/components/lesson/InteractiveCode';
import BlurWord from '@/components/lesson/BlurWord';
import QuestionCard from '@/components/lesson/QuestionCard';
import RevealAnswer from '@/components/lesson/RevealAnswer';
import HiddenCode from '@/components/lesson/HiddenCode';

const components = {
  InteractiveCode,
  BlurWord,
  QuestionCard,
  RevealAnswer,
  HiddenCode,
};

export async function getLesson(locale: string, topic: string, lesson: string) {
  const filePath = path.join(
    process.cwd(),
    'content/lessons',
    locale,
    topic,
    `${lesson}.mdx`
  );

  const source = await readFile(filePath, 'utf-8');

  const { content, frontmatter } = await compileMDX<{
    title: string;
    description: string;
    difficulty: string;
    duration: number;
  }>({
    source,
    components,
    options: {
      parseFrontmatter: true,
    },
  });

  return { content, frontmatter };
}
```

### 2.2 BlurWord 컴포넌트

```tsx
// components/lesson/BlurWord.tsx

'use client';

import { useState } from 'react';

export default function BlurWord({ children }: { children: React.ReactNode }) {
  const [revealed, setRevealed] = useState(false);

  return (
    <span
      onClick={() => setRevealed(!revealed)}
      className={`
        cursor-pointer px-1 rounded transition-all
        ${revealed
          ? 'bg-yellow-100 dark:bg-yellow-900'
          : 'bg-gray-200 dark:bg-gray-700 blur-sm hover:blur-none'
        }
      `}
    >
      {children}
    </span>
  );
}
```

### 2.3 RevealAnswer 컴포넌트

```tsx
// components/lesson/RevealAnswer.tsx

'use client';

import { useState } from 'react';
import { ChevronDown, ChevronUp } from 'lucide-react';

export default function RevealAnswer({ children }: { children: React.ReactNode }) {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <div className="my-4">
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="flex items-center gap-2 text-primary hover:underline"
      >
        {isOpen ? <ChevronUp size={16} /> : <ChevronDown size={16} />}
        {isOpen ? '정답 숨기기' : '정답 보기'}
      </button>

      {isOpen && (
        <div className="mt-2 p-4 bg-muted rounded-lg border-l-4 border-primary">
          {children}
        </div>
      )}
    </div>
  );
}
```

---

## 3. 반응형 모바일 UI

### 3.1 사이드바 컴포넌트

![모바일 레슨](/assets/img/stats-method/dev-lesson-mobile.png)

```tsx
// components/learn/Sidebar.tsx

'use client';

import { useState, useEffect } from 'react';
import { usePathname } from 'next/navigation';
import { Menu, X } from 'lucide-react';
import { cn } from '@/lib/utils';

export default function Sidebar({ children }: { children: React.ReactNode }) {
  const [isOpen, setIsOpen] = useState(false);
  const pathname = usePathname();

  // 라우트 변경 시 사이드바 닫기
  useEffect(() => {
    setIsOpen(false);
  }, [pathname]);

  return (
    <>
      {/* 모바일 토글 버튼 */}
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="fixed top-4 left-4 z-50 p-2 bg-background border rounded-lg md:hidden"
        aria-label="메뉴 토글"
      >
        {isOpen ? <X size={24} /> : <Menu size={24} />}
      </button>

      {/* 오버레이 */}
      {isOpen && (
        <div
          className="fixed inset-0 bg-black/50 z-40 md:hidden"
          onClick={() => setIsOpen(false)}
        />
      )}

      {/* 사이드바 */}
      <aside
        className={cn(
          'fixed left-0 top-0 h-full w-72 bg-background border-r z-40',
          'transform transition-transform duration-300 ease-in-out',
          'md:sticky md:top-0 md:translate-x-0',
          isOpen ? 'translate-x-0' : '-translate-x-full'
        )}
      >
        <nav className="p-4 pt-16 md:pt-4 overflow-y-auto h-full">
          {children}
        </nav>
      </aside>
    </>
  );
}
```

### 3.2 반응형 브레이크포인트

```css
/* Tailwind CSS 기본 브레이크포인트 활용 */

/* 모바일: 기본 (< 768px) */
.sidebar {
  @apply fixed -translate-x-full;
}

/* 태블릿 이상: md (>= 768px) */
@screen md {
  .sidebar {
    @apply sticky translate-x-0;
  }
}
```

---

## 4. 인증 시스템

### 4.1 NextAuth.js v5 설정

![로그인 페이지](/assets/img/stats-method/dev-hypothesis.png)

```ts
// auth.ts

import NextAuth from 'next-auth';
import { PrismaAdapter } from '@auth/prisma-adapter';
import Google from 'next-auth/providers/google';
import Credentials from 'next-auth/providers/credentials';
import bcrypt from 'bcryptjs';
import { prisma } from '@/lib/prisma';

export const { handlers, auth, signIn, signOut } = NextAuth({
  adapter: PrismaAdapter(prisma),
  providers: [
    // Google OAuth
    Google({
      clientId: process.env.GOOGLE_CLIENT_ID!,
      clientSecret: process.env.GOOGLE_CLIENT_SECRET!,
    }),

    // 이메일/비밀번호
    Credentials({
      name: 'credentials',
      credentials: {
        email: { label: 'Email', type: 'email' },
        password: { label: 'Password', type: 'password' },
      },
      async authorize(credentials) {
        if (!credentials?.email || !credentials?.password) {
          return null;
        }

        const user = await prisma.user.findUnique({
          where: { email: credentials.email as string },
        });

        if (!user || !user.password) {
          return null;
        }

        const isValid = await bcrypt.compare(
          credentials.password as string,
          user.password
        );

        if (!isValid) {
          return null;
        }

        return {
          id: user.id,
          email: user.email,
          name: user.name,
        };
      },
    }),
  ],
  session: {
    strategy: 'jwt',
  },
  pages: {
    signIn: '/auth/signin',
    error: '/auth/error',
  },
});
```

### 4.2 회원가입 API

```ts
// app/api/auth/signup/route.ts

import { NextResponse } from 'next/server';
import bcrypt from 'bcryptjs';
import { prisma } from '@/lib/prisma';

export async function POST(req: Request) {
  try {
    const { email, password, name } = await req.json();

    // 이메일 중복 확인
    const existingUser = await prisma.user.findUnique({
      where: { email },
    });

    if (existingUser) {
      return NextResponse.json(
        { error: '이미 사용 중인 이메일입니다.' },
        { status: 400 }
      );
    }

    // 비밀번호 해시
    const hashedPassword = await bcrypt.hash(password, 12);

    // 사용자 생성
    const user = await prisma.user.create({
      data: {
        email,
        password: hashedPassword,
        name,
      },
    });

    return NextResponse.json({
      id: user.id,
      email: user.email,
      name: user.name,
    });
  } catch (error) {
    return NextResponse.json(
      { error: '회원가입 중 오류가 발생했습니다.' },
      { status: 500 }
    );
  }
}
```

---

## 5. 학습 진도 추적

### 5.1 진도 저장 API

![회귀분석 레슨](/assets/img/stats-method/dev-regression.png)

```ts
// app/api/progress/route.ts

import { NextResponse } from 'next/server';
import { auth } from '@/auth';
import { prisma } from '@/lib/prisma';

// 진도 조회
export async function GET(req: Request) {
  const session = await auth();

  if (!session?.user?.id) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
  }

  const progress = await prisma.progress.findMany({
    where: {
      userId: session.user.id,
      completed: true,
    },
    select: {
      lessonId: true,
    },
  });

  return NextResponse.json({
    completedLessons: progress.map((p) => p.lessonId),
  });
}

// 진도 저장
export async function POST(req: Request) {
  const session = await auth();

  if (!session?.user?.id) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
  }

  const { lessonId } = await req.json();

  const progress = await prisma.progress.upsert({
    where: {
      lessonId_userId: {
        lessonId,
        userId: session.user.id,
      },
    },
    create: {
      lessonId,
      userId: session.user.id,
      completed: true,
    },
    update: {
      completed: true,
    },
  });

  return NextResponse.json({ success: true, progress });
}
```

### 5.2 CompletionButton 컴포넌트

```tsx
// components/lesson/CompletionButton.tsx

'use client';

import { useState } from 'react';
import { useSession } from 'next-auth/react';
import { Check, Loader2 } from 'lucide-react';

interface CompletionButtonProps {
  lessonId: string;
  initialCompleted?: boolean;
}

export default function CompletionButton({
  lessonId,
  initialCompleted = false,
}: CompletionButtonProps) {
  const { data: session } = useSession();
  const [completed, setCompleted] = useState(initialCompleted);
  const [loading, setLoading] = useState(false);

  const handleComplete = async () => {
    if (!session) {
      // 로그인 유도
      return;
    }

    setLoading(true);

    try {
      const res = await fetch('/api/progress', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ lessonId }),
      });

      if (res.ok) {
        setCompleted(true);
      }
    } catch (error) {
      console.error('Failed to save progress:', error);
    } finally {
      setLoading(false);
    }
  };

  if (completed) {
    return (
      <div className="flex items-center gap-2 text-green-600">
        <Check size={20} />
        <span>완료됨</span>
      </div>
    );
  }

  return (
    <button
      onClick={handleComplete}
      disabled={loading || !session}
      className="flex items-center gap-2 px-4 py-2 bg-primary text-primary-foreground rounded hover:bg-primary/90 disabled:opacity-50"
    >
      {loading ? (
        <Loader2 size={20} className="animate-spin" />
      ) : (
        <Check size={20} />
      )}
      <span>학습 완료</span>
    </button>
  );
}
```

---

## 6. 연습문제 시스템

### 6.1 연습문제 페이지

![연습문제](/assets/img/stats-method/exercises.png)

![가설검정 레슨](/assets/img/stats-method/dev-hypothesis.png)

```tsx
// app/[locale]/learn/[topic]/[lesson]/exercises/page.tsx

import { getExercises } from '@/lib/exercises';
import ExerciseCard from '@/components/lesson/ExerciseCard';

export default async function ExercisesPage({
  params,
}: {
  params: { locale: string; topic: string; lesson: string };
}) {
  const exercises = await getExercises(params.topic, params.lesson);

  return (
    <div className="max-w-4xl mx-auto p-6">
      <h1 className="text-2xl font-bold mb-6">{exercises.title}</h1>
      <p className="text-muted-foreground mb-8">{exercises.description}</p>

      <div className="space-y-8">
        {exercises.exercises.map((exercise, index) => (
          <ExerciseCard
            key={exercise.id}
            exercise={exercise}
            number={index + 1}
          />
        ))}
      </div>
    </div>
  );
}
```

---

## 주요 기술적 도전

### MDX + next-mdx-remote 이슈

**문제**: MDX에서 JSX 표현식 `{value}`가 동작하지 않음

```mdx
<!-- 이건 안 됨 -->
<InteractiveCode expectedValue={27.625} />

<!-- 이건 됨 -->
<InteractiveCode expectedValue="27.625" />
```

**해결**: 모든 prop을 문자열로 받고 컴포넌트에서 파싱

### Python f-string 파싱 오류

**문제**: f-string 내 `{var:.2f}`가 JSX로 파싱됨

```python
# 이건 서버 에러 발생
print(f'결과: {result:.2f}')

# 이렇게 변경
print('결과:', round(result, 2))
```

---

[← 이전: 설계](/dev/stats-method/design/) | [목차](/dev/stats-method/) | [다음: 배포 →](/dev/stats-method/deployment/)
