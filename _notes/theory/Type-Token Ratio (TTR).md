---
title: Type-Token Ratio (TTR)
last_modified_at: '2026-02-15'
permalink: /theory/type-token-ratio-ttr/
---

# Type-Token Ratio (TTR)

## 한 줄 요약
텍스트에서 "다양한 단어 (Type)"와 "전체 단어 (Token)"의 비율로 어휘 다양성을 측정하는 지표.

## 쉬운 설명
TTR은 **"얼마나 다양한 단어를 사용하는가"**를 측정합니다.

### 핵심 개념:
- **Type (유형)**: 중복 제거한 고유 단어 수
- **Token (토큰)**: 전체 단어 수 (중복 포함)

### 쉬운 예시:

**텍스트 A** (어휘 다양성 낮음):
```
"나는 학교에 간다. 나는 집에 간다. 나는 친구 집에 간다."
Token (전체 단어): 12개
Type (고유 단어): 나는, 학교에, 간다, 집에, 친구 = 5개
TTR = 5/12 = 0.42
```

**텍스트 B** (어휘 다양성 높음):
```
"나는 학교에 간다. 철수는 도서관으로 향한다. 영희는 공원을 산책한다."
Token (전체 단어): 12개
Type (고유 단어): 나는, 학교에, 간다, 철수는, 도서관으로, 향한다, 영희는, 공원을, 산책한다 = 9개
TTR = 9/12 = 0.75
```

### 계산 방법:
```
TTR = (고유 단어 수) / (전체 단어 수)

범위: 0~1
- 0에 가까움: 같은 단어 반복 (단조로움)
- 1에 가까움: 모든 단어가 다름 (다양함)
```

## 핵심 포인트
- **0~1 범위**: 1에 가까울수록 어휘가 다양함
- **텍스트 길이 의존성**: 긴 텍스트일수록 TTR 낮아지는 경향 (한계)
- **어휘 풍부성**: 작문 능력, 언어 발달 수준 지표
- **난이도 관련**: 일반적으로 TTR 높으면 읽기 어려움

## 관련 개념
- [[Flesch-Kincaid Grade Level]] - 함께 언어적 복잡성 측정
- [[Curriculum Learning]] - TTR로 텍스트 난이도 분류
- [[Perplexity (PPL)]] - AI가 느끼는 텍스트 난이도
- [[Entropy (엔트로피)]] - 단어 분포의 불확실성 (TTR과 유사 개념)

## R4 연구에서의 역할
TTR은 R4 연구의 **D1 (언어적 복잡성)** 계산에 사용됩니다.

### D1 계산 방법 (복습):
```python
def compute_linguistic_complexity(text):
    # 1. Flesch-Kincaid Grade Level
    fk_grade = flesch_kincaid_grade(text)  # 40% 가중치

    # 2. Type-Token Ratio (어휘 다양성)
    tokens = tokenize(text)
    ttr = len(set(tokens)) / len(tokens)   # 30% 가중치 ← 여기!

    # 3. 종속절 비율
    subordinate_ratio = count_subordinate_clauses(text) / len(sentences)  # 30% 가중치

    # 종합
    D1 = 0.4 × normalize(fk_grade) + 0.3 × ttr + 0.3 × subordinate_ratio
    return D1
```

### 왜 TTR이 중요한가?
어휘 다양성은 텍스트 난이도의 중요한 지표:

```
낮은 TTR (0.3~0.5):
- 같은 단어 반복
- 단순한 표현
- 쉬운 텍스트
예: "나는 간다. 너는 간다. 우리는 간다."

중간 TTR (0.5~0.7):
- 적당한 어휘 다양성
- 일반적 텍스트
예: 뉴스 기사, 일반 설명문

높은 TTR (0.7~0.9):
- 다양한 어휘 사용
- 복잡한 표현
- 어려운 텍스트
예: 학술 논문, 문학 작품
```

### 난이도 분류에 활용:
```
OpenOrca-KO 데이터셋 분석:
쉬운 데이터: TTR < 0.5, D1 낮음
중간 데이터: TTR 0.5~0.7, D1 중간
어려운 데이터: TTR > 0.7, D1 높음
```

### ZPD Window 적용:
```
현재 모델이 TTR 0.6 텍스트를 잘 이해함
→ ZPD 범위: TTR 0.6~0.75 선택
→ TTR < 0.5는 너무 쉬움 (제외)
→ TTR > 0.8은 너무 어려움 (제외)
```

### TTR의 한계와 대응:
**문제**: 텍스트가 길수록 TTR 낮아짐
```
짧은 텍스트 (20단어): TTR = 0.9 가능
긴 텍스트 (1000단어): TTR = 0.5 정도
→ 길이가 다른 텍스트 비교 어려움
```

**대응**: 정규화된 TTR 변형 사용
- **MATTR** (Moving Average TTR): 일정 윈도우(예: 100단어)마다 계산
- **Root TTR**: √(Type / Token)
- R4 연구에서는 비슷한 길이의 텍스트만 비교

## 더 알아보기
- Lexical Diversity: TTR의 학술적 용어
- Yule's K: TTR의 대안 지표 (길이 독립적)
- MTLD (Measure of Textual Lexical Diversity): 최신 지표
- 아동 언어 발달 연구에서 TTR 활용 (연령별 TTR 증가)
- 작문 평가: TTR 높음 = 더 풍부한 표현력
- 기계 번역 평가: TTR로 번역 품질 측정
- 한국어 TTR: 조사, 어미 처리 방법에 따라 달라짐
