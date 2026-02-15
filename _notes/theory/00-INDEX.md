---
title: R4 연구 Obsidian 노트 색인
last_modified_at: '2026-02-15'
permalink: /theory/r4-obsidian/
---

# R4 연구 Obsidian 노트 색인

## 개요
이 디렉토리는 **R4 연구: ZPD-inspired Adaptive Curriculum Learning**에 언급된 모든 이론, 방법론, 개념에 대한 Obsidian 형식 연계 노트를 포함한다.

**대상 독자**: 고등학생 수준
**형식**: Obsidian [[]] 백링크 형식
**총 노트 수**: 22개

---

## 1. 핵심 이론 (Core Theories)

### [[Curriculum Learning]]
- Bengio et al. (2009)의 핵심 이론
- R4 연구의 이론적 기반
- 쉬운 것→어려운 것 순서로 학습

### [[ZPD (근접발달영역)]]
- Vygotsky의 교육학 이론
- R4 연구의 영감의 원천
- "딱 적당히 어려운" 학습 영역

### [[Krashen i+1 가설]]
- 언어 습득 이론
- ZPD Window 설정의 이론적 근거
- "현재 수준 + 1단계"가 최적

---

## 2. 성능 측정 지표 (Performance Metrics)

### [[Perplexity (PPL)]]
- 언어 모델 성능 지표
- ZPD Window 계산의 기준
- 낮을수록 좋음

### [[Cross-entropy Loss]]
- AI 학습의 오차 점수
- PPL 계산의 기반
- 낮을수록 정확

### [[Confidence (신뢰도)]]
- 모델의 확신도 측정
- 복합 지표의 35% 차지
- 높을수록 확신함

### [[Entropy (엔트로피)]]
- 모델의 불확실성 측정
- 복합 지표의 25% 차지
- 높을수록 혼란스러움

---

## 3. 학습 기법 (Learning Techniques)

### [[Fine-tuning]]
- 사전학습 모델 미세조정
- R4 연구의 학습 단계
- Pre-training 후 2단계 학습

### [[LoRA]]
- Low-Rank Adaptation
- 효율적 Fine-tuning 기법
- 메모리/시간 90% 절감

### [[Chain-of-Thought (CoT)]]
- 단계별 추론 기법
- D2 (추론 단계 수) 측정에 사용
- 복잡한 문제 해결에 효과적

### [[EMA (Exponential Moving Average)]]
- 지수이동평균
- PPL 안정화에 사용
- 노이즈 제거, smoothing factor=0.9

---

## 4. 평가 벤치마크 (Evaluation Benchmarks)

### [[MMLU]]
- 57개 과목 종합 평가
- 추론 능력 측정
- 다중선택 4지선다

### [[HumanEval]]
- 코드 생성 능력 평가
- 생성 태스크 대표
- Python 함수 완성 164문제

### [[KoBEST]]
- 한국어 NLU 벤치마크
- 5개 태스크
- SOLAR 10.7B 평가용

### [[GSM8K]]
- 초등 수학 추론 벤치마크
- 8,000개 문제
- 다단계 추론 평가

---

## 5. 통계 분석 방법 (Statistical Methods)

### [[Ablation Study]]
- 제거 실험
- 구성 요소 중요도 검증
- R4: 8개 Ablation 조건

### [[ANOVA]]
- 분산분석
- 4개 조건 비교
- F-test, p<0.05

### [[Cohen's d]]
- 효과 크기 측정
- 실질적 중요성 평가
- 0.8 이상이면 큰 효과

---

## 6. 난이도 측정 지표 (Difficulty Metrics)

### [[Flesch-Kincaid Grade Level]]
- 가독성 지표
- D1 (언어적 복잡성) 측정
- 몇 학년 수준 텍스트인지 계산

### [[Type-Token Ratio (TTR)]]
- 어휘 다양성 측정
- D1의 30% 가중치
- 0~1 범위, 높을수록 다양

---

## 7. 실험 모델 (Experimental Models)

### [[SOLAR 10.7B]]
- 한국어 특화 LLM
- 업스테이지 개발
- R4 주요 실험 모델

### [[Qwen2.5]]
- 다국어 LLM
- 알리바바 개발
- R4 비교 모델 (7B)

---

## 노트 활용 가이드

### 1. 백링크로 탐색
- 각 노트에는 관련 개념이 [[]] 형식으로 링크됨
- Obsidian의 그래프 뷰에서 관계 시각화 가능

### 2. 학습 경로 추천

**초보자 경로**:
1. [[Curriculum Learning]] → 기본 개념
2. [[ZPD (근접발달영역)]] → 교육학 배경
3. [[Fine-tuning]] → 학습 방법
4. [[MMLU]] → 평가 방법

**중급자 경로**:
1. [[Perplexity (PPL)]] → 측정 지표
2. [[Confidence (신뢰도)]] → 복합 지표
3. [[Ablation Study]] → 실험 설계
4. [[ANOVA]] → 통계 분석

**고급자 경로**:
1. [[Chain-of-Thought (CoT)]] → 난이도 측정
2. [[EMA (Exponential Moving Average)]] → 안정화 기법
3. [[Cohen's d]] → 효과 크기
4. [[LoRA]] → 효율적 학습

### 3. 검색 팁
- Obsidian 검색창에서 키워드 검색
- 태그: 각 노트의 "R4 연구에서의 역할" 섹션 참고
- 그래프 뷰: 개념 간 연결 시각화

---

## 노트 작성 원칙

### 1. 쉬운 설명
- 고등학생도 이해 가능한 수준
- 비유와 예시 활용
- 전문 용어 최소화

### 2. 구조화
- 한 줄 요약
- 쉬운 설명 (3-5 문단)
- 핵심 포인트 (불릿 포인트)
- 관련 개념 (백링크)
- R4 연구에서의 역할
- 더 알아보기

### 3. 실용성
- R4 연구와의 연결 명시
- 실제 예시 제공
- 코드 스니펫 포함 (필요시)

---

## 업데이트 이력
- **2026-02-15**: 최초 작성 (22개 노트)

---

## 참고 자료
- 원본 계획: `/Users/takjakim_mbp/Projects/.omc/plans/research-4-zpd-curriculum-learning-v3.md`
- R4 연구 문서: 버전 3.0 (2026-02-15)
