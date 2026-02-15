# Cohen's d

## 한 줄 요약
두 그룹의 평균 차이가 "통계적으로 유의미"한지를 넘어서 "실질적으로 얼마나 큰 차이"인지 측정하는 효과 크기 지표.

## 쉬운 설명
Cohen's d는 **"차이의 크기"**를 표준화된 숫자로 나타냅니다.

### 쉬운 비유: 키 차이
상황 1: 성인 남성 vs 성인 여성
- 남성 평균: 175cm
- 여성 평균: 162cm
- 차이: 13cm
- **Cohen's d = 1.2** (큰 차이)

상황 2: A반 학생 vs B반 학생 (모두 남성)
- A반 평균: 175cm
- B반 평균: 174cm
- 차이: 1cm
- **Cohen's d = 0.1** (작은 차이)

같은 1cm 차이라도:
- 성별 간: 큰 의미
- 같은 성별 내: 작은 의미

Cohen's d는 이런 **상대적 크기**를 측정합니다.

### 계산 방법:
```
Cohen's d = (평균1 - 평균2) / 합동 표준편차

예:
그룹 A: 평균 80, 표준편차 10
그룹 B: 평균 70, 표준편차 10

Cohen's d = (80 - 70) / 10 = 1.0
```

### 해석 기준 (Cohen, 1988):
| Cohen's d | 크기 | 의미 |
|-----------|------|------|
| 0.2 | 작음 (Small) | 겨우 알아차릴 정도 |
| 0.5 | 중간 (Medium) | 분명히 느껴지는 차이 |
| 0.8 | 큼 (Large) | 매우 큰 차이 |
| 1.2+ | 매우 큼 | 압도적 차이 |

## 핵심 포인트
- **표준화된 척도**: 단위가 다른 지표도 비교 가능
- **p-value와 독립적**: 통계적 유의성 ≠ 실질적 중요성
- **효과 크기**: 차이가 얼마나 "중요한지" 평가
- **실용적 의미**: 연구 결과의 실무 적용 가능성 판단

## 관련 개념
- [[ANOVA]] - ANOVA 후 Cohen's d로 효과 크기 측정
- [[Ablation Study]] - Ablation 조건 간 효과 크기 비교
- [[Curriculum Learning]] - Curriculum 효과의 실질적 크기 평가

## R4 연구에서의 역할
R4 연구는 Cohen's d로 **실질적 효과 크기**를 평가합니다.

### 왜 Cohen's d가 중요한가?
p-value만으로는 부족:

```
상황 1: 샘플 수 작음 (N=10)
평균 차이: 5점, p=0.12 (유의하지 않음)
Cohen's d = 0.9 (큰 효과!)
→ 실질적으로 중요하지만 샘플이 적어서 p-value가 높음

상황 2: 샘플 수 많음 (N=1000)
평균 차이: 0.5점, p=0.001 (유의함!)
Cohen's d = 0.05 (거의 없는 효과)
→ 통계적으로는 유의하지만 실질적으로 의미 없음
```

### R4의 Cohen's d 사용:

#### 1. 조건 간 비교:
```
ZPD-Adaptive vs Random:
MMLU 점수: 69% vs 65% (차이 4%)
표준편차: 2%
Cohen's d = 4/2 = 2.0 (매우 큰 효과!)

ZPD-Adaptive vs Fixed E→H:
MMLU 점수: 69% vs 67% (차이 2%)
표준편차: 2%
Cohen's d = 2/2 = 1.0 (큰 효과)
```

#### 2. 모델 규모별 효과 크기 (H3a):
```
가설 H3a: 효과 크기는 큰 모델에서 더 큼

SOLAR 10.7B:
Cohen's d (ZPD vs Random) = 2.2

Qwen2.5 7B:
Cohen's d (ZPD vs Random) = 1.5

→ 가설 지지! 큰 모델에서 효과 더 큼
```

#### 3. 태스크 유형별 효과 크기 (H3b):
```
가설 H3b: 추론 태스크에서 효과 더 큼

추론 태스크 (MMLU):
Cohen's d = 2.0 (매우 큰 효과)

생성 태스크 (HumanEval):
Cohen's d = 1.2 (큰 효과)

→ 가설 지지! 추론 태스크에서 효과 더 큼
```

#### 4. Ablation Study 효과 크기:
```
Full model vs A1 (Loss-only):
Cohen's d = 1.5 (큰 효과)
→ 복합 지표가 실질적으로 중요함

Full model vs A6 (Fixed Window):
Cohen's d = 1.2 (큰 효과)
→ 적응성이 실질적으로 중요함
```

### 실무 적용 판단:
```
Cohen's d < 0.5: 실무 적용 가치 낮음
Cohen's d 0.5~0.8: 실무 적용 고려 가능
Cohen's d > 0.8: 실무 적용 강력 권고
Cohen's d > 1.5: 즉시 적용 권장
```

## 더 알아보기
- Cohen, J. (1988). Statistical Power Analysis for the Behavioral Sciences.
- Hedges' g: Cohen's d의 보정 버전 (작은 샘플 크기용)
- Glass's Δ: 통제 집단 표준편차만 사용
- η² (Eta-squared): ANOVA에서의 효과 크기 (0~1 범위)
- r (상관계수): Cohen's d와 상호 변환 가능
- Overlap: 두 분포가 겹치는 정도 (d=0.8일 때 약 53% 겹침)
- NNT (Number Needed to Treat): 의학 연구의 효과 크기
