---
title: Entropy (엔트로피)
last_modified_at: '2026-02-15'
permalink: /theory/entropy/
---

# Entropy (엔트로피)

## 한 줄 요약
AI의 예측이 얼마나 "혼란스러운지" 측정하는 불확실성 지표로, 높을수록 모델이 갈팡질팡한다는 의미.

## 쉬운 설명
Entropy(엔트로피)는 원래 물리학과 정보 이론에서 나온 개념으로, **"무질서도" 또는 "불확실성"**을 측정합니다.

### 쉬운 비유:
여러분이 주사위 게임을 한다고 상상해보세요.

**낮은 Entropy (확실함)**:
- 주사위: 조작된 주사위, 항상 6이 나옴
- 확률 분포: [0%, 0%, 0%, 0%, 0%, 100%]
- "다음에 뭐 나올지 뻔함!" → Entropy 낮음

**높은 Entropy (불확실함)**:
- 주사위: 공정한 주사위, 모든 면이 똑같이 나옴
- 확률 분포: [16.7%, 16.7%, 16.7%, 16.7%, 16.7%, 16.7%]
- "다음에 뭐 나올지 전혀 모름!" → Entropy 높음

### AI 예측에서의 Entropy:
```
예측 A (낮은 Entropy = 확신):
- "서울": 95%
- "부산": 2%
- "인천": 2%
- "대구": 1%
→ 거의 "서울"로 확신 → Entropy 낮음

예측 B (높은 Entropy = 혼란):
- "서울": 30%
- "부산": 25%
- "인천": 25%
- "대구": 20%
→ 뭐가 정답인지 모르겠음 → Entropy 높음
```

### 수학적으로:
```
Entropy = -Σ p(i) × log(p(i))

여기서 p(i)는 각 선택지의 확률
```

## 핵심 포인트
- **높을수록 불확실**: Entropy 높음 = 혼란스러움
- **낮을수록 확실**: Entropy 낮음 = 확신함
- **정보량 측정**: "평균적으로 몇 비트의 정보가 필요한가"
- **최대값**: 모든 선택지가 동일 확률일 때 (완전 무작위)

## 관련 개념
- [[Confidence (신뢰도)]] - Entropy와 반대 관계 (Entropy ↑ → Confidence ↓)
- [[Perplexity (PPL)]] - PPL은 지수화된 Entropy와 유사
- [[Cross-entropy Loss]] - Loss 계산에 Entropy 개념 사용
- [[Curriculum Learning]] - Entropy로 데이터 난이도 측정
- [[ZPD (근접발달영역)]] - 적정 Entropy 범위 = ZPD

## R4 연구에서의 역할
Entropy는 R4 연구에서 **모델의 불확실성 측정**에 사용됩니다.

### 복합 지표에서의 역할 (25% 가중치):
```
Competence = 0.4 × (1-Loss) + 0.35 × Confidence + 0.25 × (1-Entropy)
```

주의: **(1 - Entropy)** 사용!
- Entropy 높음 → 불확실 → Competence 낮음
- Entropy 낮음 → 확실 → Competence 높음

### 왜 Entropy가 필요한가?
Confidence만으로는 부족한 경우:

```
예측 A:
- Top-1: 51%  ← Confidence = 0.51
- Top-2: 49%
→ Confidence는 51%지만, 실제로는 매우 불확실!
→ Entropy가 높게 나와서 이를 포착

예측 B:
- Top-1: 51%  ← Confidence = 0.51 (동일)
- Top-2: 10%
→ Top-1이 압도적, 비교적 확신
→ Entropy가 낮음
```

### Entropy 기반 ZPD 탐지:
```
현재 Held-out set 평균 Entropy = 1.2

ZPD 범위 설정:
- 너무 낮은 Entropy (<0.5): 너무 쉬움 → 제외
- 적정 Entropy (0.8~1.5): 적당히 불확실 → 선택!
- 너무 높은 Entropy (>2.0): 너무 어려움 → 제외
```

### EDCO (2026) 연구와의 비교:
R4 연구는 EDCO의 한계를 보완:
- **EDCO**: Entropy 단일 지표만 사용
- **R4**: Entropy + Loss + Confidence 복합 지표
→ 더 정확한 난이도 측정

### Ablation Study (A3):
```
A3 (Entropy-only): w1=0, w2=0, w3=1
→ Entropy만으로 ZPD 탐지
→ Full model과 비교하여 복합 지표의 중요성 검증
```

### 학습 과정별 Entropy 변화:
```
Step 0:    평균 Entropy = 3.5 (완전 혼란)
Step 1000: 평균 Entropy = 2.2 (조금씩 확신)
Step 5000: 평균 Entropy = 1.0 (많이 확신)
Step 10000: 평균 Entropy = 0.4 (거의 확실)
```

## 더 알아보기
- Shannon Entropy: 정보 이론의 창시자 Claude Shannon이 제안
- 물리학 엔트로피: 무질서도 (비슷한 개념, 다른 분야)
- KL Divergence: 두 확률 분포 간 Entropy 차이
- Cross-Entropy: Entropy의 확장 개념
- Maximum Entropy: 모든 선택지가 동일 확률 (log(N))
- Conditional Entropy: 조건부 엔트로피 (맥락 고려)
- Mutual Information: 두 변수의 상호 정보량 (Entropy 기반)
