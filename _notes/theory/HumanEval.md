---
title: HumanEval
last_modified_at: '2026-02-15'
permalink: /theory/humaneval/
---

# HumanEval

## 한 줄 요약
AI가 프로그래밍 문제를 얼마나 잘 푸는지 평가하는 코딩 테스트로, 실제로 실행 가능한 코드를 작성하는지 확인한다.

## 쉬운 설명
HumanEval은 AI의 **코딩 능력**을 평가하는 벤치마크입니다. "Human-level Evaluation"에서 이름이 왔어요.

### 어떻게 평가하나?
1. **문제 제공**: Python 함수를 완성하는 문제 164개
2. **AI가 코드 작성**: 모델이 함수 내용을 자동 생성
3. **테스트 실행**: 실제로 코드를 실행해서 정답 확인
4. **정답률 계산**: 몇 %가 통과하는지 측정

### 예시 문제:
```python
# 문제: 두 수의 최대공약수를 구하는 함수 완성
def greatest_common_divisor(a: int, b: int) -> int:
    """ Returns the greatest common divisor of a and b
    >>> greatest_common_divisor(12, 8)
    4
    >>> greatest_common_divisor(21, 14)
    7
    """
    # AI가 여기를 채워야 함!
```

### AI 답변 예시:
```python
def greatest_common_divisor(a: int, b: int) -> int:
    while b != 0:
        a, b = b, a % b
    return a
```

### 평가 방법:
- 테스트 케이스를 **실제로 실행**
- 모든 테스트를 통과하면 정답
- 하나라도 실패하면 오답

## 핵심 포인트
- **164개 문제**: 다양한 난이도와 유형 (정렬, 수학, 문자열 처리 등)
- **실행 기반 평가**: 코드 스타일이 아닌 **실제 동작** 평가
- **Pass@k 메트릭**: k개 생성해서 1개만 통과해도 정답 (예: Pass@1, Pass@10)
- **실용적**: 실제 개발자가 하는 일과 유사

## 관련 개념
- [[MMLU]] - 지식 평가 (HumanEval은 코드 생성 평가)
- [[Fine-tuning]] - 코드 생성 능력 향상을 위한 Fine-tuning
- [[Chain-of-Thought (CoT)]] - 복잡한 코딩 문제 해결 시 단계별 추론
- [[GSM8K]] - 수학 추론 평가 (수식 vs 코드의 차이)

## R4 연구에서의 역할
HumanEval은 R4 연구의 **생성 태스크** 평가에 사용됩니다.

### 왜 HumanEval이 중요한가?
R4 연구는 **태스크 유형별 효과 차이**를 검증합니다 (가설 H3b):
- **추론 태스크** (MMLU, GSM8K): ZPD-Adaptive 효과 **큼**
- **생성 태스크** (HumanEval): ZPD-Adaptive 효과 **중간**

코드 생성은 "정답이 여러 개"일 수 있어서, 난이도 정의가 추론 태스크보다 모호합니다.
예: 최대공약수 함수를 구현하는 방법은 여러 가지 (유클리드 호제법, 반복문, 재귀 등)

### R4 연구의 HumanEval 사용:
- **평가 주기**: 매 500 스텝마다 측정
- **메트릭**: Pass@1 (1번 생성해서 통과 여부)
- **기대 결과**:
  - Random 대비 +3~5% 향상
  - Fixed E→H 대비 +1~3% 향상

### 실험 조건별 예상 HumanEval Pass@1:
```
Random:           40%
Fixed E→H:        42%
Fixed H→E:        38%
ZPD-Adaptive:     45%  ← R4 제안 방법
```

### 태스크 유형 비교:
| 태스크 | 벤치마크 | 난이도 정의 | ZPD 효과 |
|--------|---------|------------|---------|
| 추론 | MMLU, GSM8K | 명확 (단계 수, 지식량) | **큼** |
| 생성 | HumanEval | 모호 (여러 정답 가능) | 중간 |

## 더 알아보기
- Chen, M., et al. (2021). Evaluating Large Language Models Trained on Code. *arXiv preprint*.
- 공개 데이터셋: https://github.com/openai/human-eval
- GPT-4 점수: Pass@1 67%, Pass@10 88%
- Codex (2021) 점수: Pass@1 28.8%
- AlphaCode 점수: 경쟁 프로그래밍 문제에서 상위 54%
- GitHub Copilot의 기반 기술이 바로 Codex
- 후속 벤치마크: MBPP (Mostly Basic Python Problems, 974개 문제)
