# Ablation Study

## 한 줄 요약
복잡한 시스템에서 특정 부품을 하나씩 제거해보면서 "이게 정말 필요한지" 확인하는 실험 방법.

## 쉬운 설명
Ablation Study(제거 실험)는 **"이 부품 없으면 어떻게 될까?"**를 확인하는 과학적 방법입니다.

### 쉬운 비유: 자동차 성능 테스트
자동차가 빠른 이유를 알고 싶다면:
1. **원본**: 터보 엔진 + 경량 바디 + 고급 타이어 → 시속 250km
2. **터보 엔진 제거**: 일반 엔진 + 경량 바디 + 고급 타이어 → 시속 180km
3. **경량 바디 제거**: 터보 엔진 + 일반 바디 + 고급 타이어 → 시속 220km
4. **고급 타이어 제거**: 터보 엔진 + 경량 바디 + 일반 타이어 → 시속 240km

결론:
- 터보 엔진이 가장 중요 (70km 차이)
- 경량 바디도 중요 (30km 차이)
- 고급 타이어는 별로 안 중요 (10km 차이)

### AI 연구에서의 Ablation Study:
복잡한 AI 시스템을 만들 때, 각 요소가 정말 필요한지 검증해야 합니다.

예를 들어, "복합 지표 기반 ZPD 탐지"가 좋다고 주장하려면:
1. **Full model**: Loss + Confidence + Entropy → 성능 A
2. **Loss만 사용**: Confidence, Entropy 제거 → 성능 B
3. **Confidence만 사용**: Loss, Entropy 제거 → 성능 C
4. **Entropy만 사용**: Loss, Confidence 제거 → 성능 D

만약 A가 B, C, D보다 훨씬 좋다면 → "복합 지표가 필수!"라고 증명됨

## 핵심 포인트
- **체계적 제거**: 하나씩 빼보면서 효과 측정
- **인과관계 확인**: 상관관계가 아닌 진짜 원인 파악
- **중요도 순위**: 어떤 요소가 가장 중요한지 정량적으로 평가
- **과학적 근거**: "이게 좋다"라는 주장을 객관적으로 증명

## 관련 개념
- [[ANOVA]] - Ablation 결과 통계적 유의성 검증
- [[Cohen's d]] - Ablation 조건 간 효과 크기 측정
- [[Curriculum Learning]] - Ablation으로 Curriculum 구성 요소 검증
- [[Fine-tuning]] - Ablation으로 Fine-tuning 기법 검증

## R4 연구에서의 역할
R4 연구는 **8개 Ablation 조건**을 체계적으로 실험합니다.

### R4의 Ablation Study 계획:

| Ablation | 제거/변경 내용 | 검증 목적 |
|----------|---------------|-----------|
| **A1: Loss-only** | Confidence, Entropy 제거 → Loss만 사용 | Loss 단일 지표로도 충분한가? |
| **A2: Confidence-only** | Loss, Entropy 제거 → Confidence만 사용 | Confidence만으로 ZPD 탐지 가능한가? |
| **A3: Entropy-only** | Loss, Confidence 제거 → Entropy만 사용 | Entropy만으로 불확실성 측정 충분한가? |
| **A4: No Upper Bound** | β=∞ (ZPD 상한 제거) | "너무 어려운" 데이터 걸러내기 필요한가? |
| **A5: No Lower Bound** | α=1.0 (ZPD 하한 제거) | "너무 쉬운" 데이터 걸러내기 필요한가? |
| **A6: Fixed Window** | α, β 고정, 적응 제거 | 실시간 적응이 정말 중요한가? |
| **A7: Faster Update** | 갱신 주기 500→100 | 더 자주 갱신하면 더 좋은가? |
| **A8: Slower Update** | 갱신 주기 500→1000 | 덜 자주 갱신해도 괜찮은가? |

### 예상 결과:
```
Full model (복합 지표 + 적응):  성능 100 (기준)
A1 (Loss-only):                  성능 85  (15% 하락)
A2 (Confidence-only):            성능 80  (20% 하락)
A3 (Entropy-only):               성능 75  (25% 하락)
A4 (No Upper Bound):             성능 90  (10% 하락)
A5 (No Lower Bound):             성능 92  (8% 하락)
A6 (Fixed Window):               성능 88  (12% 하락)
A7 (Faster Update):              성능 98  (2% 하락)
A8 (Slower Update):              성능 95  (5% 하락)
```

### 결론 도출 예시:
1. **복합 지표 필요성**: A1, A2, A3 모두 Full model보다 낮음 → 복합 지표 필수
2. **상한 중요성**: A4 10% 하락 → 너무 어려운 데이터 제외 중요
3. **하한 중요성**: A5 8% 하락 → 너무 쉬운 데이터 제외도 중요
4. **적응 필요성**: A6 12% 하락 → 실시간 적응이 핵심
5. **갱신 주기 최적화**: A7 vs A8 → 500 스텝이 적정

### 통계적 검증:
각 Ablation 조건을 5번 반복 실험 → ANOVA로 유의성 검증
```python
# 예시
F-test: Full vs A1 (Loss-only)
p < 0.05 → 통계적으로 유의미한 차이
Cohen's d = 0.8 → 큰 효과 크기
```

## 더 알아보기
- 의학 연구: 약물의 특정 성분 효과 검증
- 신경과학: 뇌의 특정 영역 손상 효과 연구 (실제 ablation)
- 컴퓨터 비전: CNN의 특정 레이어 제거 효과
- NLP: Transformer의 Attention head 제거 효과
- A/B Testing: Ablation의 실무 버전
- Feature Importance: 머신러닝에서 변수 중요도 측정
