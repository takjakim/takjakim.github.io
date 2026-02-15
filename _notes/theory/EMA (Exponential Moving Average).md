---
title: EMA (Exponential Moving Average)
last_modified_at: '2026-02-15'
permalink: /theory/ema-exponential-moving-average/
---

# EMA (Exponential Moving Average)

## 한 줄 요약
최근 값에 더 많은 가중치를 주고 과거 값은 점점 줄이면서 평균을 계산하는 방법으로, 잡음을 제거하고 추세를 부드럽게 보여준다.

## 쉬운 설명
EMA는 "지수 이동 평균"으로, **"최근 것이 더 중요해!"**라는 철학으로 평균을 계산합니다.

### 단순 평균 vs EMA:

**단순 평균 (Simple Moving Average)**:
```
최근 5일 주가: [100, 102, 105, 103, 104]
평균 = (100 + 102 + 105 + 103 + 104) / 5 = 102.8원
→ 모든 값이 동일한 중요도
```

**EMA (Exponential Moving Average)**:
```
최근 5일 주가: [100, 102, 105, 103, 104]
EMA = 0.1×100 + 0.15×102 + 0.2×105 + 0.25×103 + 0.3×104
    ≈ 103.2원
→ 최근 값(104)에 더 큰 가중치(0.3)
→ 과거 값(100)에 작은 가중치(0.1)
```

### 쉬운 비유: 성적 관리
**단순 평균**: 1학기, 2학기, 3학기 성적을 똑같이 반영
**EMA**: 3학기(최근) 성적을 가장 중요하게, 1학기는 조금만 반영
→ "최근 실력이 더 중요하니까!"

### 계산 방법:
```
EMA_new = α × 현재값 + (1-α) × EMA_old

α (알파) = smoothing factor (보통 0.1~0.3)
- α가 클수록: 최근 값에 민감
- α가 작을수록: 부드러운 곡선
```

## 핵심 포인트
- **최근 값 중시**: 오래된 값은 지수적으로 가중치 감소
- **노이즈 제거**: 잡음이 많은 데이터를 부드럽게 만듦
- **트렌드 파악**: 장기 추세를 명확하게 보여줌
- **메모리 효율**: 과거 모든 값 저장 불필요

## 관련 개념
- [[Perplexity (PPL)]] - PPL을 EMA로 평활화하여 안정적 측정
- [[Curriculum Learning]] - 학습 곡선 평활화에 EMA 사용
- [[Confidence (신뢰도)]] - Confidence 추이를 EMA로 모니터링
- [[Cross-entropy Loss]] - Loss 값을 EMA로 평활화

## R4 연구에서의 역할
R4 연구는 EMA를 **PPL 안정화**에 사용합니다.

### 문제 상황:
모델 학습 중 PPL이 불안정하게 변동:
```
Step 0:   PPL = 35.2
Step 100: PPL = 32.1
Step 200: PPL = 33.8 (갑자기 올라감!)
Step 300: PPL = 30.5
Step 400: PPL = 31.2 (또 올라감!)
```
→ PPL이 왔다갔다하면 ZPD Window도 계속 바뀜
→ 학습이 불안정해질 수 있음

### EMA 적용:
```python
class ZPDCurriculumScheduler:
    def __init__(self, smoothing_factor=0.9):
        self.smoothing_factor = 0.9  # α = 1 - 0.9 = 0.1
        self.current_ppl = None

    def compute_current_competence(self, model, held_out_set):
        loss = compute_average_loss(model, held_out_set)
        ppl = math.exp(loss)

        # EMA smoothing
        if self.current_ppl is None:
            self.current_ppl = ppl  # 첫 값은 그대로
        else:
            self.current_ppl = (self.smoothing_factor * self.current_ppl +
                               (1 - self.smoothing_factor) * ppl)

        return self.current_ppl
```

### EMA 효과:
```
원본 PPL (노이즈 많음):
Step 0:   35.2 → EMA: 35.2
Step 100: 32.1 → EMA: 34.9 (천천히 감소)
Step 200: 33.8 → EMA: 34.8 (급등 무시)
Step 300: 30.5 → EMA: 34.4 (계속 감소)
Step 400: 31.2 → EMA: 34.1 (안정적)

→ 부드러운 곡선, 급격한 변동 억제
```

### Smoothing Factor 선택:
R4 연구는 **0.9**를 사용:
```
α = 1 - 0.9 = 0.1

의미:
- 새 값(PPL) 가중치: 10%
- 기존 EMA 가중치: 90%
→ 매우 보수적, 안정적 변화
```

왜 0.9인가?
- **너무 높음 (0.95)**: 변화에 너무 둔감, ZPD 적응 느림
- **적정 (0.9)**: 노이즈 제거 + 적절한 적응 속도
- **너무 낮음 (0.7)**: 노이즈에 민감, EMA 효과 약함

### ZPD Window 안정화:
```
EMA 없이:
Step 100: PPL=32, ZPD=[35.2, 41.6]
Step 200: PPL=34, ZPD=[37.4, 44.2] (갑자기 확 바뀜!)
→ 데이터 선별 기준이 불안정

EMA 적용:
Step 100: EMA_PPL=34.9, ZPD=[38.4, 45.4]
Step 200: EMA_PPL=34.8, ZPD=[38.3, 45.2] (거의 안 바뀜)
→ 안정적인 데이터 선별
```

### 학습 안정성 향상:
```
Loss Variance (학습 안정성 지표):
EMA 없음: Variance = 0.25 (불안정)
EMA 적용: Variance = 0.12 (안정적, 52% 감소)
```

### Ablation Study 관련:
만약 EMA를 제거하면?
```
No EMA 조건:
- PPL 노이즈에 민감
- ZPD Window 자주 변경
- Fallback 전략 호출 빈도 증가
- 학습 안정성 하락
예상 성능: -8~12% 하락
```

## 더 알아보기
- 주식 투자: MACD (Moving Average Convergence Divergence) 지표
- 시계열 분석: Holt-Winters EMA 확장 (계절성 포함)
- 딥러닝 Optimizer: Adam의 모멘텀이 EMA 사용
- Network Traffic: 네트워크 부하 평활화
- EMA vs SMA (Simple Moving Average): EMA가 더 빠르게 반응
- Double EMA: EMA를 다시 EMA (더 부드러움)
- α 선택: 일반적으로 2/(N+1), N=20이면 α≈0.095
