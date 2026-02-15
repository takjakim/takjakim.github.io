# Curriculum Learning

## 한 줄 요약
사람이 쉬운 것부터 배우듯이, AI도 쉬운 데이터부터 어려운 데이터 순서로 학습시키면 더 효율적으로 배운다는 기계학습 방법론.

## 쉬운 설명
여러분이 수학을 배울 때를 생각해보세요. 갑자기 미적분부터 시작하지 않고, 덧셈→뺄셈→곱셈→나눗셈 순서로 배우죠? 이게 바로 Curriculum Learning의 핵심 아이디어입니다.

2009년에 Yoshua Bengio라는 유명한 AI 학자가 제안한 방법인데, 신경망(AI 모델)을 학습시킬 때도 데이터를 **난이도 순서대로** 제공하면 훨씬 빨리 배운다는 것을 발견했어요.

예를 들어, 강아지와 고양이를 구분하는 AI를 만든다고 해봅시다:
- **잘못된 방법**: 모든 사진을 무작위로 섞어서 학습
- **Curriculum Learning**: 먼저 선명한 정면 사진 → 측면 사진 → 흐릿한 사진 → 일부만 보이는 사진 순서로 학습

마치 운전을 배울 때 주차장에서 먼저 연습하고 나중에 고속도로로 나가는 것처럼, AI도 단계적으로 배우면 더 안정적으로 학습이 됩니다.

## 핵심 포인트
- **점진적 학습**: 쉬운 예제에서 어려운 예제로 점진적으로 난이도를 높임
- **수렴 가속**: 적절한 학습 순서를 정하면 목표 성능에 더 빨리 도달함 (20-40% 빠름)
- **안정성 향상**: 처음부터 어려운 문제를 주면 학습이 불안정하거나 실패할 수 있음
- **Local Minima 회피**: 쉬운 예제로 좋은 출발점을 잡으면, 나쁜 함정(Local Minima)에 빠지는 것을 방지

## 관련 개념
- [[ZPD (근접발달영역)]] - 교육학 이론에서 온 영감
- [[Krashen i+1 가설]] - 언어 습득에서의 유사한 원리
- [[Fine-tuning]] - Curriculum Learning이 주로 적용되는 학습 단계
- [[Perplexity (PPL)]] - 난이도 측정에 사용되는 지표
- [[Ablation Study]] - Curriculum Learning 효과를 검증하는 방법

## R4 연구에서의 역할
R4 연구의 **핵심 이론적 기반**입니다. Bengio의 Curriculum Learning을 기초로 삼고, 여기에 [[ZPD (근접발달영역)]]이라는 교육학 이론의 통찰을 더해서 "적응형(Adaptive)" Curriculum Learning을 만들었습니다.

기존 Curriculum Learning은 난이도 순서가 **고정**되어 있었는데, R4 연구는 모델이 학습하는 동안 **실시간으로 난이도를 조정**하는 것이 특징입니다. 마치 좋은 선생님이 학생 수준을 보면서 문제 난이도를 바꿔주는 것처럼요.

## 더 알아보기
- Bengio, Y., Louradour, J., Collobert, R., & Weston, J. (2009). Curriculum learning. *Proceedings of the 26th International Conference on Machine Learning*, 41-48.
- 원문에서는 수학적 정의를 제공: "W*(T) = argmin_W Σ L(f(x;W), y) × Q_T(x,y)" - Q_T가 시간에 따라 쉬운 예제에서 어려운 예제로 가중치를 조정하는 역할
