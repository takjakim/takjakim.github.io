# Cross-entropy Loss

## 한 줄 요약
AI 모델의 예측과 정답이 얼마나 다른지 측정하는 "오차 점수"로, 낮을수록 모델이 정확하다는 의미.

## 쉬운 설명
Cross-entropy Loss(교차 엔트로피 손실)는 AI가 학습할 때 **"얼마나 틀렸는지"** 계산하는 공식입니다.

### 시험 점수로 비유하면:
- **정답률 (Accuracy)**: 100점 만점에 80점 → 우리가 익숙한 점수
- **Loss**: "틀린 정도"를 특별한 방법으로 계산 → 낮을수록 좋음

### 왜 Cross-entropy를 사용하나?
단순히 "맞았다/틀렸다"보다 **"얼마나 확신했는지"**도 중요하기 때문입니다.

예를 들어:
```
문제: 다음 단어는? "나는 학교에 ___"

모델 A 예측:
- "간다": 90% 확률 ← 확신함, 정답!
- "온다": 5%
- "먹는다": 5%
→ Loss: 매우 낮음 (잘함)

모델 B 예측:
- "간다": 40% ← 자신 없음, 정답이긴 하지만...
- "온다": 35%
- "먹는다": 25%
→ Loss: 높음 (운으로 맞춤)
```

Cross-entropy Loss는 **확신하고 정답 맞추기**를 권장합니다.

### 수학적으로는:
```
Loss = -log(정답 확률)

정답 확률이 90% → Loss = -log(0.9) = 0.105 (낮음, 좋음)
정답 확률이 40% → Loss = -log(0.4) = 0.916 (높음, 나쁨)
정답 확률이 10% → Loss = -log(0.1) = 2.303 (매우 높음, 매우 나쁨)
```

## 핵심 포인트
- **낮을수록 좋음**: Loss가 0에 가까우면 거의 완벽
- **확률 기반**: 정답 확률이 높을수록 Loss 낮음
- **로그 사용**: 작은 확률 차이도 크게 반영 (0.9 vs 0.99는 큰 차이)
- **미분 가능**: AI가 학습할 때 "어느 방향으로 수정"할지 계산 가능

## 관련 개념
- [[Perplexity (PPL)]] - PPL = exp(평균 Loss)
- [[Confidence (신뢰도)]] - 정답 확률 = 모델의 확신도
- [[Entropy (엔트로피)]] - 전체 예측 분포의 불확실성
- [[Fine-tuning]] - Loss를 낮추는 것이 학습의 목표
- [[Curriculum Learning]] - Loss 기반으로 난이도 측정

## R4 연구에서의 역할
Cross-entropy Loss는 R4 연구에서 **세 가지 역할**을 합니다.

### 1. 학습 목표 함수:
모델이 학습할 때 Loss를 최소화하도록 파라미터 업데이트
```python
for step in range(10000):
    loss = compute_loss(model, batch)
    loss.backward()  # Loss를 줄이는 방향 계산
    optimizer.step()  # 파라미터 업데이트
```

### 2. 현재 능력 측정 (복합 지표의 일부):
```
Competence = 0.4 × (1 - Loss) + 0.35 × Confidence + 0.25 × (1 - Entropy)
```
Loss가 낮을수록 Competence 높음

### 3. PPL 계산:
```
PPL = exp(평균 Loss)
```
ZPD Window는 PPL 기반으로 설정:
```
ZPD 범위 = [PPL × 1.1, PPL × 1.3]
```

### 학습 곡선 예시:
```
Step 0:    Loss = 3.5 (처음, 모델이 무지함)
Step 1000: Loss = 2.1 (배우는 중)
Step 5000: Loss = 0.8 (많이 배움)
Step 10000: Loss = 0.3 (거의 완벽)
```

### Ablation Study (A1):
R4 연구는 "Loss만 사용" vs "복합 지표" 비교:
- A1 (Loss-only): Competence = Loss만 사용
- Full model: Competence = Loss + Confidence + Entropy
→ 복합 지표가 더 정확한 ZPD 탐지

## 더 알아보기
- 정보 이론에서 유래: 두 확률 분포 간 차이 측정
- Binary Cross-entropy: 2개 선택지 (예: 개/고양이 분류)
- Categorical Cross-entropy: 다중 선택지 (예: 1만 개 단어 중 예측)
- Focal Loss: 어려운 예제에 더 집중하는 변형 (불균형 데이터용)
- KL Divergence: Cross-entropy와 유사하지만 대칭적
- 음의 로그 우도 (Negative Log-Likelihood): Cross-entropy의 다른 이름
