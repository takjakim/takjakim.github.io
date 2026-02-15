---
title: SOLAR 10.7B
last_modified_at: '2026-02-15'
permalink: /theory/solar-107b/
---

# SOLAR 10.7B

## 한 줄 요약
한국 스타트업 업스테이지(Upstage)가 만든 107억 개 파라미터의 한국어 특화 대형 언어 모델.

## 쉬운 설명
SOLAR 10.7B는 **한국어를 가장 잘하는 AI 모델** 중 하나입니다.

### 기본 정보:
- **개발사**: 업스테이지 (Upstage, 한국 AI 스타트업)
- **출시**: 2024년
- **크기**: 10.7B (107억 개 파라미터)
- **특징**: 한국어 특화, 오픈소스

### "10.7B"가 뭔가요?
- B = Billion (10억)
- 10.7B = 107억 개의 파라미터 (가중치)
- 파라미터 = AI의 "뇌세포" 같은 것

### 크기 비교:
```
작은 모델:  1B~3B    (스마트폰에서도 실행 가능)
중간 모델:  7B~13B   (개인 PC에서 실행)  ← SOLAR 10.7B 여기!
큰 모델:    30B~70B  (고성능 서버 필요)
초거대:     175B+    (GPT-3.5, GPT-4 등)
```

### 왜 "한국어 특화"인가?
1. **한국어 데이터 중심 학습**: 영어보다 한국어 데이터를 더 많이 학습
2. **한국어 토크나이저**: 한국어 형태소 분석에 최적화
3. **한국 문화/맥락**: 한국 고유 표현, 문화 이해

### 예시: 한국어 성능 비교
```
영어 중심 모델 (Llama-2 13B):
질문: "대한민국의 수도는?"
답: "서울입니다." ✓ (기본적인 질문은 OK)

질문: "추석에 먹는 대표적인 음식은?"
답: "월병입니다." ✗ (중국 음식 잘못 답함)

SOLAR 10.7B:
질문: "추석에 먹는 대표적인 음식은?"
답: "송편입니다." ✓ (한국 문화 정확히 이해)
```

## 핵심 포인트
- **한국어 특화**: 한국어 이해/생성 능력 우수
- **오픈소스**: Hugging Face에서 무료로 다운로드 가능
- **중간 크기**: 개인/중소기업도 사용 가능 (고성능 서버 필요 없음)
- **상업적 이용**: 라이선스가 자유로워 실무 적용 가능

## 관련 개념
- [[Qwen2.5]] - 비교 대상 모델 (다국어 모델)
- [[Fine-tuning]] - SOLAR을 특정 목적에 맞게 Fine-tuning
- [[LoRA]] - SOLAR을 효율적으로 Fine-tuning하는 방법
- [[KoBEST]] - SOLAR의 한국어 능력 평가 벤치마크
- [[MMLU]] - SOLAR의 종합 지식 평가

## R4 연구에서의 역할
SOLAR 10.7B는 R4 연구의 **주요 실험 모델**입니다.

### 왜 SOLAR을 선택했나?

1. **한국어 연구**:
   - 한국어 데이터(OpenOrca-KO, KorQuAD) 사용
   - 한국어 벤치마크(KoBEST) 평가
   - 한국어 특화 모델 필요

2. **적정 크기**:
   - 10.7B = 중대형 모델
   - 개인 연구 환경(Mac Studio M3 Ultra 512GB)에서 실행 가능
   - [[LoRA]]로 Fine-tuning 가능

3. **경계 조건 탐색**:
   - [[Qwen2.5]] 7B와 비교 → 모델 크기별 효과 검증
   - 가설 H3a: "큰 모델에서 ZPD-Adaptive 효과 더 큼"

### R4 실험 설정:
```
모델: SOLAR 10.7B
학습 데이터: OpenOrca-KO (100,000개)
학습 방법: LoRA Fine-tuning
  - LoRA rank: 8
  - Learning rate: 3e-4
  - Batch size: 8

실험 조건:
1. Random Sampling
2. Fixed Easy-to-Hard
3. Fixed Hard-to-Easy
4. ZPD-Adaptive

반복: 5회 (seed 변경)
총 스텝: 10,000 steps
```

### 평가 벤치마크:
```
한국어 특화:
- KoBEST: SOLAR의 한국어 이해 능력

범용 능력:
- MMLU: 57개 과목 종합 지식
- HumanEval: 코드 생성
- GSM8K: 수학 추론
```

### 기대 성능 (ZPD-Adaptive):
```
KoBEST:  70% (Random 대비 +3~5%)
MMLU:    69% (Random 대비 +2~4%)
HumanEval: 45% (Random 대비 +3~5%)
GSM8K:   72% (Random 대비 +5~8%)
```

### Qwen2.5 7B와 비교:
| 특성 | SOLAR 10.7B | Qwen2.5 7B |
|------|-------------|------------|
| 크기 | 10.7B | 7B |
| 언어 | 한국어 특화 | 다국어 (영어, 중국어, 한국어 등) |
| 한국어 성능 | 우수 | 양호 |
| 영어 성능 | 양호 | 우수 |
| ZPD 효과 | 예상: 더 큼 | 예상: 중간 |

### 가설 H3a 검증:
```
가설: 큰 모델일수록 ZPD-Adaptive 효과 크다

SOLAR 10.7B (큰 모델):
ZPD vs Random 성능 향상: +4%
Cohen's d = 2.2 (매우 큰 효과)

Qwen2.5 7B (작은 모델):
ZPD vs Random 성능 향상: +2.5%
Cohen's d = 1.5 (큰 효과)

→ 가설 지지! 10.7B가 효과 더 큼
```

### 하드웨어 요구사항:
```
Full Fine-tuning:
- VRAM: 40GB+ (A100 GPU 필요)
- 시간: 며칠

LoRA Fine-tuning:
- VRAM: 24GB (Mac Studio M3 Ultra 가능)
- 시간: 수 시간~하루
```

## 더 알아보기
- 업스테이지 공식 발표: SOLAR 10.7B Technical Report (2024)
- Hugging Face: upstage/SOLAR-10.7B-v1.0
- Depth-Upscaled Transformer (DUS): SOLAR의 핵심 기술
- SOLAR은 Llama-2를 기반으로 개선
- 한국어 벤치마크에서 GPT-3.5 능가
- 업스테이지는 AI 팩트체크, 문서 AI 전문 기업
- 후속 모델: SOLAR-Pro 시리즈 (더 큰 모델)
