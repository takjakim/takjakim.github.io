---
title: Fine-tuning
last_modified_at: '2026-02-15'
permalink: /theory/fine-tuning/
---

# Fine-tuning

## 한 줄 요약
이미 훈련된 AI 모델을 특정 목적에 맞게 추가로 학습시켜 성능을 높이는 과정.

## 쉬운 설명
Fine-tuning(미세조정)은 AI 모델 학습의 **2단계 전략**에서 두 번째 단계이다.

### 요리로 비유하면:
1. **Pre-training (사전학습)**: 요리학원에서 기본기 배우기
   - 칼질, 불 조절, 기본 레시피 등
   - 방대한 데이터(인터넷 전체)로 학습
   - 시간: 몇 주~몇 달
   - 비용: 수억~수천억 원

2. **Fine-tuning (미세조정)**: 특정 요리(예: 일식) 전문가 되기
   - 이미 배운 기본기를 활용
   - 특정 분야 데이터로 추가 학습
   - 시간: 몇 시간~며칠
   - 비용: 수십만~수백만 원

### 왜 Fine-tuning을 하나요?
처음부터 모델을 학습시키는 것(Pre-training)은:
- 돈이 너무 많이 듦 (GPT-4 학습비: 수백억 원)
- 시간이 너무 오래 걸림 (몇 달)
- 엄청난 데이터 필요 (인터넷 전체)

대신, 이미 학습된 모델(예: GPT-3.5, Llama-2)을 가져와서:
- 내 목적에 맞는 작은 데이터로 추가 학습
- 훨씬 저렴하고 빠름

### 예시:
- **의료 챗봇 만들기**:
  - ❌ 처음부터 학습: 불가능 (비용 문제)
  - ✅ GPT 모델 + 의료 문서로 Fine-tuning: 가능!

- **법률 문서 분석 AI**:
  - ❌ 처음부터 학습: 수십억 원
  - ✅ Llama-2 + 법률 판례로 Fine-tuning: 수백만 원

## 핵심 포인트
- **전이학습**: Pre-training에서 배운 지식을 새 태스크에 전이(Transfer)
- **데이터 효율성**: 적은 데이터(수천~수만 개)로도 좋은 성능
- **비용 효율성**: Pre-training의 1/100~1/1000 비용
- **도메인 특화**: 특정 분야(의료, 법률, 금융 등)에 최적화 가능

## 관련 개념
- [[LoRA]] - Fine-tuning을 효율적으로 하는 기법
- [[Curriculum Learning]] - Fine-tuning의 학습 효율을 높이는 방법
- [[Perplexity (PPL)]] - Fine-tuning 성능 측정 지표
- [[MMLU]] - Fine-tuning 후 성능 평가 벤치마크
- [[HumanEval]] - 코드 생성 Fine-tuning 평가

## R4 연구에서의 역할
R4 연구는 **Fine-tuning 단계에서 Curriculum Learning을 적용**한다.

### 기존 Fine-tuning (Random):
```
1. 학습 데이터를 무작위로 섞음
2. 순서 상관없이 학습
3. 10,000 스텝 완료
```

### ZPD-Adaptive Fine-tuning (R4 연구):
```
1. 현재 모델 수준 측정 (PPL, Confidence, Entropy)
2. "딱 적당히 어려운" 데이터만 선별 (ZPD Window)
3. 학습
4. 500 스텝마다 1-3 반복
5. 25-40% 빠르게 목표 성능 도달!
```

### R4 연구의 실험 설정:
- **모델**: SOLAR 10.7B, Qwen2.5 7B
- **데이터**: OpenOrca-KO (100,000개)
- **방법**: LoRA Fine-tuning
- **비교 조건**:
  1. Random (기존 방법)
  2. Fixed Easy-to-Hard (쉬운 것→어려운 것 고정 순서)
  3. Fixed Hard-to-Easy (어려운 것→쉬운 것)
  4. ZPD-Adaptive (실시간 난이도 조정) ← **R4 제안 방법**

### 기대 효과:
- 학습 스텝 25-40% 단축
- 최종 성능 MMLU +2~4% 향상
- GPU 시간 20-35% 절감

## 더 알아보기
- Fine-tuning vs Transfer Learning: 거의 같은 의미로 사용됨
- Instruction Tuning: 사용자 지시사항 따르도록 Fine-tuning (ChatGPT가 이 방식)
- RLHF (Reinforcement Learning from Human Feedback): 인간 선호도로 Fine-tuning
- Catastrophic Forgetting: Fine-tuning 시 이전 지식을 잊어버리는 문제 (주의 필요)
- Domain Adaptation: Fine-tuning의 학술적 용어
