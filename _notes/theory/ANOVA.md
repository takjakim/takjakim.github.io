---
title: ANOVA
last_modified_at: '2026-02-15'
permalink: /theory/anova/
---

# ANOVA

## 한 줄 요약
3개 이상의 그룹 평균을 비교해서 "이 차이가 진짜 차이인지 우연인지" 통계적으로 판단하는 분석 방법.

## 쉬운 설명
ANOVA는 "Analysis of Variance"의 약자로, 한국어로는 **"분산분석"**입니다.

### 쉬운 비유: 세 학교 수학 평균 비교
A 학교: 평균 80점
B 학교: 평균 75점
C 학교: 평균 85점

질문: "진짜 A 학교가 더 잘하는 거야, 아니면 우연히 이번에만 그런 거야?"

**ANOVA가 답해주는 것**:
- "이 차이는 통계적으로 의미 있음" (p < 0.05) → 진짜 차이!
- "이 차이는 우연일 수 있음" (p > 0.05) → 그냥 운일 수도...

### 왜 t-test가 아닌 ANOVA를 쓰나?
- **t-test**: 2개 그룹 비교 (A vs B)
- **ANOVA**: 3개 이상 그룹 비교 (A vs B vs C vs D)

만약 4개 그룹을 t-test로 비교하면:
- A vs B, A vs C, A vs D, B vs C, B vs D, C vs D
- 총 6번 검정 → 오류 확률 증가!

ANOVA는 **한 번에 모든 그룹 비교** → 오류 확률 통제

### ANOVA의 핵심 아이디어:
```
전체 차이 = 그룹 간 차이 + 그룹 내 차이

F-비율 = 그룹 간 분산 / 그룹 내 분산

F가 크면 (예: F=10) → 그룹 간 차이가 진짜 큼!
F가 작으면 (예: F=1.2) → 그룹 간 차이가 우연일 수도...
```

## 핵심 포인트
- **F-통계량**: 그룹 간 차이를 나타내는 숫자 (클수록 차이 큼)
- **p-value**: 이 차이가 우연일 확률 (보통 p<0.05면 유의미)
- **귀무가설**: "모든 그룹의 평균이 같다" (기본 가정)
- **대립가설**: "적어도 한 그룹은 다르다"

## 관련 개념
- [[Cohen's d]] - ANOVA 후 효과 크기 측정
- [[Ablation Study]] - ANOVA로 Ablation 결과 검증
- [[Curriculum Learning]] - 4개 Curriculum 조건 비교에 ANOVA 사용

## R4 연구에서의 역할
R4 연구는 **4-Arm 실험 설계**이므로 ANOVA가 핵심 통계 기법입니다.

### R4의 4개 조건:
1. Random Sampling
2. Fixed Easy-to-Hard
3. Fixed Hard-to-Easy
4. ZPD-Adaptive ← **R4 제안 방법**

### ANOVA 분석 예시:
```
연구 문제 1 (RQ1): "4개 조건 간 학습 효율성 차이가 있는가?"

귀무가설 (H0): μ1 = μ2 = μ3 = μ4 (모든 조건의 평균 성능 동일)
대립가설 (H1): 적어도 한 조건은 다름

ANOVA 결과:
F(3, 36) = 12.5, p = 0.001

해석:
- F = 12.5 (큰 값) → 그룹 간 차이 큼
- p = 0.001 < 0.05 → 통계적으로 유의미
- 결론: "4개 조건은 진짜 다르다!"
```

### Post-hoc Test (사후 검정):
ANOVA는 "적어도 한 그룹은 다르다"만 알려줌.
**어떤 그룹이 다른지**는 Tukey HSD로 확인:

```
Tukey HSD 결과:
ZPD-Adaptive vs Random:      p = 0.001 (유의미 차이)
ZPD-Adaptive vs Fixed E→H:   p = 0.023 (유의미 차이)
ZPD-Adaptive vs Fixed H→E:   p < 0.001 (유의미 차이)
Fixed E→H vs Random:         p = 0.145 (차이 없음)
```

### Two-way ANOVA (2원 분산분석):
R4 연구는 **조절 효과**도 검증:
- 독립변인 1: Curriculum Type (4수준)
- 독립변인 2: Model Size (2수준: 7B vs 10.7B)
- **상호작용**: Curriculum × Model Size

```
Two-way ANOVA 결과:
Main effect of Curriculum:     F(3,72)=15.2, p<0.001
Main effect of Model Size:     F(1,72)=8.3, p=0.005
Interaction (Curriculum×Size): F(3,72)=3.1, p=0.032

해석:
- Curriculum 효과 있음
- Model 크기 효과 있음
- 상호작용 있음 → 큰 모델에서 ZPD 효과 더 큼!
```

### 분석 절차:
```
1. One-way ANOVA (Curriculum Type 비교)
   → F-test로 전체 차이 검증

2. Tukey HSD (사후 검정)
   → 어떤 조건 간 차이인지 확인

3. Two-way ANOVA (조절 효과)
   → Curriculum × Model Size 상호작용

4. Effect Size (효과 크기)
   → Cohen's d로 실질적 의미 평가
```

## 더 알아보기
- One-way ANOVA: 독립변인 1개 (예: Curriculum Type)
- Two-way ANOVA: 독립변인 2개 (예: Curriculum × Model Size)
- Repeated Measures ANOVA: 동일 대상 반복 측정 (예: 시간에 따른 변화)
- MANOVA: 종속변인이 여러 개일 때
- 가정: 정규성, 등분산성, 독립성 (위반 시 Kruskal-Wallis 사용)
- Effect Size: η² (에타 제곱) 또는 ω² (오메가 제곱)
- Bonferroni Correction: 다중 비교 시 오류 조정
