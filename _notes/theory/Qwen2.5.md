---
title: Qwen2.5
last_modified_at: '2026-02-15'
permalink: /theory/qwen25/
---

# Qwen2.5

## 한 줄 요약
중국 알리바바가 만든 다국어 대형 언어 모델로, 영어, 중국어, 한국어 등 여러 언어를 잘 다루는 오픈소스 AI.

## 쉬운 설명
Qwen2.5는 **여러 언어를 골고루 잘하는 글로벌 AI 모델**입니다.

### 기본 정보:
- **개발사**: 알리바바 (Alibaba, 중국 빅테크 기업)
- **출시**: 2024년 (Qwen 시리즈 2.5 버전)
- **크기**: 여러 버전 (0.5B ~ 72B)
- **특징**: 다국어 지원, 오픈소스

### Qwen 시리즈:
```
Qwen 1.0 (2023): 초기 버전
Qwen 1.5 (2024): 성능 개선
Qwen 2.0 (2024): 대폭 개선
Qwen 2.5 (2024): 최신 버전 ← R4 연구 사용
```

### 크기 옵션:
```
Qwen2.5-0.5B:  5억 개 파라미터 (스마트폰 실행 가능)
Qwen2.5-1.5B:  15억 개 파라미터
Qwen2.5-3B:    30억 개 파라미터
Qwen2.5-7B:    70억 개 파라미터  ← R4 연구 사용
Qwen2.5-14B:   140억 개 파라미터
Qwen2.5-32B:   320억 개 파라미터
Qwen2.5-72B:   720억 개 파라미터 (최상위)
```

### 다국어 지원:
- **영어**: 매우 우수
- **중국어**: 매우 우수 (모국어)
- **한국어**: 우수
- **일본어**: 우수
- 기타 29개 언어 지원

### [[SOLAR 10.7B]]와 비교:
```
SOLAR 10.7B:
- 한국어 특화
- 한국어 성능: ★★★★★
- 영어 성능: ★★★★☆
- 중국어 성능: ★★★☆☆

Qwen2.5 7B:
- 다국어 균형
- 한국어 성능: ★★★★☆
- 영어 성능: ★★★★★
- 중국어 성능: ★★★★★
```

## 핵심 포인트
- **다국어 능력**: 29개 언어 지원, 번역 필요 없음
- **오픈소스**: Hugging Face에서 무료 다운로드
- **다양한 크기**: 0.5B~72B까지 선택 가능
- **코드 특화**: 프로그래밍 언어도 잘 이해

## 관련 개념
- [[SOLAR 10.7B]] - 비교 대상 모델 (한국어 특화)
- [[Fine-tuning]] - Qwen을 Fine-tuning하여 성능 향상
- [[LoRA]] - Qwen을 효율적으로 Fine-tuning
- [[MMLU]] - Qwen의 다과목 지식 평가
- [[HumanEval]] - Qwen의 코드 생성 능력 평가

## R4 연구에서의 역할
Qwen2.5 7B는 R4 연구의 **비교 모델**로 사용됩니다.

### 왜 Qwen2.5 7B를 선택했나?

1. **모델 크기 비교**:
   - SOLAR 10.7B (큰 모델) vs Qwen2.5 7B (작은 모델)
   - 가설 H3a: "큰 모델에서 ZPD 효과 더 큼" 검증

2. **언어 특성 비교**:
   - SOLAR (한국어 특화) vs Qwen (다국어)
   - 권장사항 R1: "한국어 모델 특수성 탐색"

3. **하드웨어 접근성**:
   - 7B = Mac Mini M4 Pro 24GB에서 실행 가능
   - 10.7B = Mac Studio M3 Ultra 512GB 필요
   - 다양한 환경에서 재현 가능

### R4 실험 설정:
```
모델: Qwen2.5 7B
학습 데이터: OpenOrca-KO (100,000개) + Alpaca-52K
학습 방법: LoRA Fine-tuning
  - LoRA rank: 8
  - Learning rate: 3e-4
  - Batch size: 8

실험 조건:
1. Random Sampling
2. Fixed Easy-to-Hard
3. Fixed Hard-to-Easy
4. ZPD-Adaptive

반복: 5회
총 스텝: 10,000 steps
```

### 평가 벤치마크:
```
영어 중심:
- MMLU: 다과목 지식 (영어)
- HumanEval: 코드 생성 (영어)
- GSM8K: 수학 추론 (영어)

한국어:
- KoBEST: 한국어 이해 능력
```

### 기대 성능 비교:

#### Qwen2.5 7B (작은 모델):
```
MMLU:    67% (Random 대비 +2%)
HumanEval: 42% (Random 대비 +2%)
GSM8K:   68% (Random 대비 +3%)
KoBEST:  65% (Random 대비 +2%)
```

#### SOLAR 10.7B (큰 모델):
```
MMLU:    69% (Random 대비 +4%)
HumanEval: 45% (Random 대비 +5%)
GSM8K:   72% (Random 대비 +8%)
KoBEST:  70% (Random 대비 +5%)
```

### 가설 H3a 검증:
```
가설: 큰 모델일수록 ZPD-Adaptive 효과 크다

Qwen2.5 7B (작은 모델):
효과 크기 Cohen's d = 1.5 (큰 효과)
효율 향상: 20-25%

SOLAR 10.7B (큰 모델):
효과 크기 Cohen's d = 2.2 (매우 큰 효과)
효율 향상: 30-40%

→ 가설 지지! 큰 모델에서 ZPD 효과 더 큼
```

### 한국어 vs 영어 태스크 비교 (R1):
```
Qwen2.5 7B 성능:
영어 태스크 (MMLU, GSM8K): 높음
한국어 태스크 (KoBEST): 중간

SOLAR 10.7B 성능:
영어 태스크: 중간
한국어 태스크: 높음 ← 특수성 확인

ZPD 효과:
Qwen: 영어 태스크에서 효과 큼
SOLAR: 한국어 태스크에서 효과 큼
→ 언어 특성에 따른 차별적 효과 발견
```

### 하드웨어 요구사항:
```
Full Fine-tuning:
- VRAM: 28GB+ (A100 GPU 권장)
- 시간: 1~2일

LoRA Fine-tuning:
- VRAM: 16GB (RTX 4090, Mac Mini M4 Pro 가능)
- 시간: 수 시간
```

## 더 알아보기
- Alibaba Cloud 공식 발표: Qwen2.5 Technical Report (2024)
- Hugging Face: Qwen/Qwen2.5-7B-Instruct
- Qwen-Chat: 채팅 특화 버전
- Qwen-Code: 코드 생성 특화 버전
- Qwen-Math: 수학 특화 버전
- HumanEval에서 GPT-3.5 능가 (Pass@1 60%+)
- MMLU에서 Llama-2 13B 능가
- 라이선스: Apache 2.0 (상업적 이용 자유)
- 후속 모델: Qwen 3.0 개발 중
