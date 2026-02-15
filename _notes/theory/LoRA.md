# LoRA

## 한 줄 요약
거대 언어 모델을 학습시킬 때 전체 파라미터 대신 작은 "부품"만 업데이트해서 메모리와 시간을 획기적으로 절약하는 기법.

## 쉬운 설명
LoRA는 "Low-Rank Adaptation"의 약자입니다. 이름이 어려워 보이지만, 핵심 아이디어는 매우 간단해요.

### 비유로 이해하기
거대한 백과사전(GPT 같은 대형 모델)이 있다고 상상해보세요. 새로운 정보를 추가하려면:

**기존 방법 (Full Fine-tuning)**:
- 백과사전 전체를 다시 쓰기
- 시간: 몇 주
- 비용: 매우 비쌈
- 메모리: 수백 GB 필요

**LoRA 방법**:
- 백과사전은 그대로 두고, 포스트잇(작은 메모)만 붙이기
- 시간: 몇 시간
- 비용: 1/10 이하
- 메모리: 수 GB만 필요

LoRA는 거대 모델의 **핵심 부분(W)은 그대로 두고**, **작은 업데이트 행렬(A, B)만 학습**합니다.

### 수학적으로는:
```
기존 가중치: W (예: 10억 개 파라미터)
LoRA 추가: W' = W + A × B
  여기서 A, B는 매우 작음 (예: 100만 개 파라미터)
```

## 핵심 포인트
- **메모리 절약**: 전체 모델의 0.1~1%만 학습 → GPU 메모리 90% 이상 절감
- **속도 향상**: 업데이트할 파라미터가 적어서 학습 3~5배 빠름
- **성능 유지**: 놀랍게도 Full Fine-tuning과 비슷한 성능
- **다중 태스크**: 베이스 모델 하나에 여러 LoRA 모듈을 붙여서 다양한 태스크 수행 가능

## 관련 개념
- [[Fine-tuning]] - LoRA가 주로 사용되는 학습 단계
- [[Curriculum Learning]] - LoRA와 결합하여 더 효율적인 학습 가능
- [[SOLAR 10.7B]] - LoRA를 사용하여 Fine-tuning하는 대표적 모델
- [[Qwen2.5]] - LoRA 지원하는 또 다른 모델

## R4 연구에서의 역할
R4 연구는 **LoRA를 사용하여 Fine-tuning**을 진행합니다. 왜냐하면:

1. **하드웨어 제약**:
   - SOLAR 10.7B 모델을 Full Fine-tuning하려면 A100 80GB GPU 여러 장 필요
   - LoRA 사용 시 Mac Studio M3 Ultra 512GB로도 가능

2. **실험 효율성**:
   - 4개 조건 × 5번 반복 = 20번 실험
   - Full Fine-tuning: 1번에 며칠 소요 → 전체 몇 달
   - LoRA: 1번에 몇 시간 → 전체 2주 이내

3. **ZPD-Adaptive Curriculum과의 호환**:
   - 500 스텝마다 ZPD 재계산 필요
   - LoRA는 계산이 빨라서 실시간 적응에 유리

### R4에서 사용하는 LoRA 설정 (예상):
```python
LoRA_config = {
    "r": 8,              # Rank (낮을수록 파라미터 적음, 보통 4~16)
    "lora_alpha": 16,    # Scaling factor
    "target_modules": ["q_proj", "v_proj"],  # 적용할 모듈
    "lora_dropout": 0.05
}
```

## 더 알아보기
- Hu, E. J., et al. (2021). LoRA: Low-Rank Adaptation of Large Language Models. *ICLR 2022*.
- Rank(r) 선택이 중요: 너무 작으면 성능 하락, 너무 크면 메모리 이득 감소
- QLoRA: LoRA + Quantization (양자화)를 결합하여 더욱 효율적
- 실제 사례: Llama-2 70B 모델을 16GB GPU에서 LoRA로 Fine-tuning 가능
- Hugging Face PEFT 라이브러리에서 쉽게 사용 가능
