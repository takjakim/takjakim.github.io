# Confidence (신뢰도)

## 한 줄 요약
AI가 자신의 답에 얼마나 확신하는지 나타내는 확률 값으로, 높을수록 "나 이거 맞다고 확신해!"라는 의미.

## 쉬운 설명
Confidence(신뢰도, 확신도)는 AI가 답을 제시할 때 **"얼마나 자신 있는지"** 보여주는 숫자입니다.

### 쉬운 비유:
시험에서 객관식 문제를 풀 때:
- **높은 Confidence**: "이건 100% A번이야!" (확신)
- **낮은 Confidence**: "음... A번 같기도 하고 B번 같기도 하고..." (불확실)

### AI 예측 예시:
```
질문: "서울의 수도는?"

모델의 예측:
- "대한민국": 95% ← Confidence = 0.95 (매우 확신)
- "한국": 3%
- "부산": 1%
- "인천": 1%

Confidence = Top-1 확률 = 95%
```

### 또 다른 예시:
```
질문: "양자역학의 창시자는?"

모델의 예측:
- "하이젠베르크": 35% ← Confidence = 0.35 (불확실)
- "슈뢰딩거": 30%
- "아인슈타인": 25%
- "보어": 10%

Confidence = Top-1 확률 = 35%
→ 잘 모르겠다는 신호!
```

### Confidence vs Accuracy (정확도):
- **Accuracy**: 실제로 맞췄는지 (정답 여부)
- **Confidence**: 모델이 자신 있는지 (주관적 확신)

좋은 모델은 이 둘이 일치:
- 확신할 때 맞고 (High Confidence + Correct)
- 불확실할 때 틀림 (Low Confidence + Wrong)

## 핵심 포인트
- **0~1 범위**: 0% (전혀 확신 없음) ~ 100% (완전 확신)
- **Top-1 확률**: 가장 높은 확률을 가진 답의 확률
- **Calibration**: 잘 훈련된 모델은 Confidence와 Accuracy가 일치
- **Over-confidence**: 틀렸는데 확신하는 문제 (위험!)

## 관련 개념
- [[Cross-entropy Loss]] - Confidence가 높을수록 Loss 낮음
- [[Entropy (엔트로피)]] - Confidence와 반대 개념 (불확실성)
- [[Perplexity (PPL)]] - 평균 Confidence와 관련
- [[Curriculum Learning]] - Confidence로 모델 현재 수준 측정
- [[ZPD (근접발달영역)]] - 적정 Confidence 범위가 ZPD

## R4 연구에서의 역할
Confidence는 R4 연구에서 **현재 능력 수준 측정**의 핵심 지표 중 하나입니다.

### 복합 지표에서의 역할 (35% 가중치):
```
Competence = 0.4 × (1-Loss) + 0.35 × Confidence + 0.25 × (1-Entropy)
```

왜 Confidence가 중요한가?
- **Loss**: 사후적 평가 (이미 틀린 후 측정)
- **Confidence**: 사전적 신호 (모델이 스스로 "잘 모르겠다" 신호)

### Confidence 기반 ZPD 탐지:
```
현재 Held-out set 평균 Confidence = 0.75

해석:
- 0.75 = "대체로 자신 있음, 하지만 완벽하지 않음"
- 너무 쉬운 데이터: Confidence > 0.9 → 제외
- 적정 난이도: Confidence 0.6~0.8 → 선택!
- 너무 어려운 데이터: Confidence < 0.4 → 제외
```

### Calibration 검증 (Guo et al., 2017):
R4 연구는 Guo et al. (2017)의 Calibration 연구를 참고:
- **Well-calibrated 모델**: Confidence 75% → 실제 정답률 75%
- **Over-confident 모델**: Confidence 90% → 실제 정답률 60% (위험!)

Fine-tuning 과정에서 Calibration이 깨지지 않도록 모니터링

### Ablation Study (A2):
```
A2 (Confidence-only): w1=0, w2=1, w3=0
→ Confidence만으로 ZPD 탐지
→ Full model (복합 지표)과 비교
```

### 학습 과정별 Confidence 변화:
```
Step 0:    평균 Confidence = 0.15 (거의 모름)
Step 1000: 평균 Confidence = 0.45 (조금씩 배움)
Step 5000: 평균 Confidence = 0.72 (많이 배움)
Step 10000: 평균 Confidence = 0.88 (거의 완벽)
```

## 더 알아보기
- Guo, C., et al. (2017). On Calibration of Modern Neural Networks. *ICML*.
- Temperature Scaling: Confidence 조정 기법 (Over-confidence 해결)
- Expected Calibration Error (ECE): Calibration 측정 지표
- Softmax Confidence: 신경망 출력층의 확률 분포
- Ensemble Uncertainty: 여러 모델 예측 비교로 Confidence 측정
- Bayesian Neural Networks: 불확실성을 직접 모델링
