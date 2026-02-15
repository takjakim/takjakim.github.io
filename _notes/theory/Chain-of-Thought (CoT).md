---
title: Chain-of-Thought (CoT)
last_modified_at: '2026-02-15'
permalink: /theory/chain-of-thought-cot/
---

# Chain-of-Thought (CoT)

## 한 줄 요약
AI에게 답만 요구하는 게 아니라 "단계별로 생각하는 과정"을 보여주게 하면 복잡한 문제를 더 잘 푼다는 추론 기법.

## 쉬운 설명
Chain-of-Thought(사고의 연쇄)는 **"과정을 보여주면서 생각하기"**이다.

### 쉬운 비유: 수학 문제 풀이
**일반적인 방법 (Direct Answer)**:
```
질문: 철수는 사과 12개를 가지고 있었고, 3개를 먹고 5개를 더 받았습니다. 지금 몇 개?
AI: 14개
```
→ 답만 내고 끝

**Chain-of-Thought**:
```
질문: 철수는 사과 12개를 가지고 있었고, 3개를 먹고 5개를 더 받았습니다. 지금 몇 개?

AI:
1단계: 처음 사과는 12개였습니다.
2단계: 3개를 먹었으므로, 12 - 3 = 9개 남았습니다.
3단계: 5개를 더 받았으므로, 9 + 5 = 14개입니다.
답: 14개
```
→ **과정을 보여주면서** 답을 냄

### 왜 CoT가 효과적인가?
1. **중간 단계 검증**: 어디서 틀렸는지 찾기 쉬움
2. **복잡한 문제 해결**: 한 번에 못 풀어도 단계별로 나누면 가능
3. **신뢰성 향상**: 과정이 맞으면 답도 맞을 확률 높음
4. **인간과 유사**: 우리도 어려운 문제는 단계별로 풀잖아요!

### Few-shot CoT vs Zero-shot CoT:
**Few-shot CoT**: 예시를 먼저 보여줌
```
예시 1:
Q: 2 + 3 × 4는?
A: 먼저 곱셈: 3 × 4 = 12, 그 다음 덧셈: 2 + 12 = 14

예시 2:
Q: 100 - 50 ÷ 2는?
A: 먼저 나눗셈: 50 ÷ 2 = 25, 그 다음 뺄셈: 100 - 25 = 75

이제 풀어봐:
Q: 8 + 6 × 2는?
```

**Zero-shot CoT**: "단계별로 생각해봐"라고만 요청
```
Q: 8 + 6 × 2는? Let's think step by step.
A: 1단계: 곱셈 먼저... 2단계: 덧셈...
```

## 핵심 포인트
- **중간 추론 과정**: 답만이 아닌 사고 과정 생성
- **성능 향상**: 복잡한 추론 문제에서 20~50% 정확도 향상
- **디버깅 가능**: 어느 단계에서 틀렸는지 파악 가능
- **신뢰성 증가**: 과정이 논리적이면 답 신뢰도 상승

## 관련 개념
- [[GSM8K]] - CoT가 필수적인 수학 추론 벤치마크
- [[MMLU]] - 일부 어려운 과목에서 CoT 적용
- [[HumanEval]] - 코드 생성에서도 CoT 유사 방법 사용
- [[Curriculum Learning]] - CoT 단계 수로 난이도 측정 가능

## R4 연구에서의 역할
CoT는 R4 연구의 **D2 (추론 단계 수)** 측정에 핵심적으로 사용된다.

### D2 (추론 단계 수) 계산:
```python
def compute_reasoning_steps(question, answer):
    # GPT-4를 사용한 Chain-of-Thought 분해
    prompt = f"""
    Question: {question}
    Answer: {answer}

    Break down the reasoning into individual logical steps.
    Output each step on a new line, numbered.
    """

    cot = gpt4_generate(prompt)
    steps = parse_numbered_steps(cot)

    d2 = len(steps)  # 단계 수가 난이도
    return normalize(d2, max_steps=10)
```

### 난이도 분류 예시:

**쉬운 문제 (1~2 단계)**:
```
Q: 5 + 3은?
CoT:
1단계: 5 + 3 = 8
답: 8
→ D2 = 1 (매우 쉬움)
```

**중간 문제 (3~4 단계)**:
```
Q: 철수는 12개, 영희는 8개, 민수는 15개의 사탕을 가지고 있다. 평균은?
CoT:
1단계: 전체 개수 = 12 + 8 + 15 = 35개
2단계: 사람 수 = 3명
3단계: 평균 = 35 ÷ 3 = 11.67개
답: 11.67개
→ D2 = 3 (중간)
```

**어려운 문제 (5~7 단계)**:
```
Q: 어떤 수의 2배에서 5를 빼면 15가 된다. 이 수에 3을 곱하면?
CoT:
1단계: x의 2배에서 5를 빼면 15 → 2x - 5 = 15
2단계: 양변에 5 더하기 → 2x = 20
3단계: 양변을 2로 나누기 → x = 10
4단계: 이 수에 3을 곱하기 → 10 × 3
5단계: 계산 → 30
답: 30
→ D2 = 5 (어려움)
```

### 다차원 난이도에서의 역할:
```
종합 난이도 = 0.3 × D1 (언어 복잡성)
            + 0.5 × D2 (추론 단계 수) ← 가장 높은 가중치!
            + 0.2 × D3 (도메인 지식)
```

왜 D2가 50%로 가장 높은가?
- **추론 능력**이 LLM의 핵심 능력
- 단계 수가 많을수록 실질적으로 어려움
- 객관적 측정 가능 (CoT 분해 후 카운트)

### ZPD Window 적용:
```
현재 모델이 3단계 문제까지 잘 풀음
→ ZPD 범위: 3~4단계 문제 선택
→ 1~2단계는 너무 쉬움 (제외)
→ 5단계 이상은 너무 어려움 (제외)
```

### 가설 H3b 검증:
```
가설 H3b: 추론 중심 태스크에서 ZPD-Adaptive 효과가 더 큼

추론 태스크 (GSM8K, MMLU):
- CoT 단계 수로 명확한 난이도 구분 가능
- ZPD Window 적용 효과적
- 효과 크기: Cohen's d > 1.5

생성 태스크 (HumanEval):
- CoT 단계 수 측정 모호 (여러 풀이 방법)
- ZPD Window 적용 제한적
- 효과 크기: Cohen's d ≈ 1.0
```

## 더 알아보기
- Wei, J., et al. (2022). Chain-of-Thought Prompting Elicits Reasoning in Large Language Models. *NeurIPS 2022*.
- Zero-shot CoT: "Let's think step by step" 추가만으로 효과
- Self-Consistency: 여러 번 CoT 생성 후 다수결
- Tree of Thoughts (ToT): CoT를 트리 구조로 확장
- Program-aided Language Models (PAL): CoT를 코드로 생성
- Least-to-Most Prompting: 쉬운 것부터 단계적으로 CoT
- GPT-4 MMLU 점수: CoT 없음 70% → CoT 적용 86%
