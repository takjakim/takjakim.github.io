---
title: KoBEST
last_modified_at: '2026-02-15'
permalink: /theory/kobest/
---

# KoBEST

## 한 줄 요약
한국어 AI가 한국어를 얼마나 잘 이해하는지 평가하는 5가지 태스크로 구성된 종합 한국어 벤치마크.

## 쉬운 설명
KoBEST는 "Korean Benchmark Suite of Tasks"의 약자입니다. 쉽게 말해 **한국어판 종합 평가 시험**이에요.

[[MMLU]]가 영어로 된 57개 과목 시험이라면, KoBEST는 한국어로 된 5개 영역 시험입니다.

### 왜 KoBEST가 필요한가요?
영어 벤치마크(MMLU, HumanEval)만으로는 **한국어 능력**을 제대로 평가할 수 없어요. 왜냐하면:
- 한국어 특유의 문법 (조사, 어미 등)
- 한국 문화 맥락 (역사, 관용어 등)
- 한국어 데이터로 학습한 모델의 성능 측정 필요

### KoBEST의 5가지 태스크:
1. **Boolean Question (BoolQ-KO)**: 참/거짓 판단
   ```
   지문: 서울은 대한민국의 수도이다.
   질문: 서울이 수도인가?
   답: True
   ```

2. **Choice of Plausible Alternatives (COPA-KO)**: 원인/결과 추론
   ```
   상황: 아이가 울었다.
   질문: 원인은?
   A) 장난감이 부서졌다  ← 정답
   B) 날씨가 좋았다
   ```

3. **Words-in-Context (WiC-KO)**: 단어 의미 파악
   ```
   문장1: 사과를 먹었다.
   문장2: 잘못을 사과했다.
   질문: 두 "사과"의 의미가 같은가? → False
   ```

4. **HellaSwag-KO**: 이야기 다음 문장 예측
   ```
   상황: 남자가 운동장에서 뛰고 있다. 갑자기 발을 헛디뎠다.
   다음 문장은?
   A) 그는 넘어졌다  ← 정답
   B) 그는 하늘을 날았다
   ```

5. **Sentiment Negation Recognition (SentiNeg-KO)**: 부정 표현 이해
   ```
   문장: "이 영화는 별로 안 좋지 않았어"
   감정: 긍정 ← 이중부정 이해 필요
   ```

## 핵심 포인트
- **5개 태스크**: 한국어 이해의 다양한 측면 평가
- **한국어 특화**: 한국어 문법, 맥락, 문화 반영
- **5-shot 평가**: 예시 5개 제공 후 평가
- **공개 데이터**: 한국 AI Hub에서 제공

## 관련 개념
- [[MMLU]] - 영어 다과목 평가 (KoBEST는 한국어 버전)
- [[Fine-tuning]] - 한국어 데이터로 Fine-tuning 후 KoBEST로 평가
- [[SOLAR 10.7B]] - 한국어 특화 모델, KoBEST 성능 우수
- [[Perplexity (PPL)]] - 한국어 난이도 측정

## R4 연구에서의 역할
KoBEST는 R4 연구에서 **한국어 능력 평가** 지표로 사용됩니다.

### 왜 KoBEST를 사용하나?
1. **SOLAR 10.7B 평가**: 한국어 특화 모델이므로 한국어 벤치마크 필수
2. **다차원 평가**: 5개 태스크로 다양한 언어 이해 능력 측정
3. **추론 능력 평가**: 단순 번역이 아닌 추론, 맥락 이해 필요

### R4 연구의 KoBEST 사용:
- **평가 주기**: 매 500 스텝마다 측정
- **평가 방법**: 5-shot
- **기대 결과**: 다른 벤치마크와 유사하게 ZPD-Adaptive가 우수

### 모델별 특성:
| 모델 | 언어 특성 | 영어 벤치마크 | 한국어 벤치마크 |
|------|----------|--------------|----------------|
| SOLAR 10.7B | 한국어 특화 | MMLU, HumanEval | **KoBEST** ← 강점 |
| Qwen2.5 7B | 다국어 | MMLU, HumanEval | KoBEST |

### 연구 가설 검증 (R1):
KoBEST는 권장 수정사항 R1 "한국어 모델 특수성 탐색"에 활용:
- SOLAR 10.7B의 KoBEST 성능 vs MMLU 성능 비교
- 한국어 태스크에서 ZPD-Adaptive 효과가 더 큰지 분석

## 더 알아보기
- 한국 AI Hub에서 공개: https://aihub.or.kr
- KLUE (Korean Language Understanding Evaluation)와 함께 대표적인 한국어 벤치마크
- GPT-4의 KoBEST 점수: 약 75-80% (영어 MMLU보다 낮음)
- 한국어 특화 모델들이 영어 모델보다 KoBEST에서 우수한 경향
- 5개 태스크 외에도 확장 버전에는 NER(개체명 인식), QA(질의응답) 등 추가
