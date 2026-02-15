# Flesch-Kincaid Grade Level

## 한 줄 요약
텍스트를 읽으려면 몇 학년 수준의 교육이 필요한지 계산하는 가독성(읽기 쉬움) 지표.

## 쉬운 설명
Flesch-Kincaid Grade Level은 **"이 글은 몇 학년생이 읽을 수 있을까?"**를 숫자로 보여주는 공식입니다.

### 예시:
```
점수 5.0: 초등학교 5학년 수준
점수 8.0: 중학교 2학년 수준
점수 12.0: 고등학교 3학년 수준
점수 16.0: 대학교 4학년 수준
점수 20.0: 대학원 수준
```

### 무엇을 측정하나?
1. **문장 길이**: 문장이 길수록 어려움
2. **단어 길이**: 단어의 음절 수가 많을수록 어려움

### 계산 공식:
```
Grade Level = 0.39 × (총 단어 수 / 총 문장 수)
            + 11.8 × (총 음절 수 / 총 단어 수)
            - 15.59
```

### 쉬운 예시:
**텍스트 A** (쉬운 글):
```
"나는 학교에 간다. 친구를 만난다. 점심을 먹는다."
- 짧은 문장
- 짧은 단어
→ Grade Level: 3.0 (초등학교 3학년)
```

**텍스트 B** (어려운 글):
```
"교육학적 관점에서 근접발달영역은 학습자의 잠재적 발달 수준과 실제적 발달 수준 간의 괴리를 설명하는 이론적 프레임워크이다."
- 긴 문장
- 복잡한 단어 (음절 많음)
→ Grade Level: 16.0 (대학교 수준)
```

## 핵심 포인트
- **0~20+ 범위**: 숫자가 클수록 어려움
- **객관적 측정**: 사람 판단 없이 자동 계산
- **교육 표준**: 미국 교육 체계 기준 (K-12 + College)
- **가독성 개선**: 점수 낮추기 = 더 많은 사람이 읽을 수 있음

## 관련 개념
- [[Type-Token Ratio (TTR)]] - 어휘 다양성 측정 (난이도와 관련)
- [[Curriculum Learning]] - 낮은 Grade Level → 높은 Grade Level 순서로 학습
- [[Perplexity (PPL)]] - AI가 느끼는 텍스트 난이도

## R4 연구에서의 역할
Flesch-Kincaid는 R4 연구의 **D1 (언어적 복잡성)** 측정에 사용됩니다.

### 다차원 난이도 정의:
R4 연구는 데이터 난이도를 3차원으로 측정:
- **D1: 언어적 복잡성** ← Flesch-Kincaid 사용
- **D2: 추론 단계 수**
- **D3: 도메인 지식 요구량**

### D1 계산 방법:
```python
def compute_linguistic_complexity(text):
    # 1. Flesch-Kincaid Grade Level
    fk_grade = flesch_kincaid_grade(text)

    # 2. Type-Token Ratio (어휘 다양성)
    ttr = len(set(tokens)) / len(tokens)

    # 3. 종속절 비율
    subordinate_ratio = count_subordinate_clauses(text) / len(sentences)

    # 종합
    D1 = 0.4 × normalize(fk_grade) + 0.3 × ttr + 0.3 × subordinate_ratio
    return D1
```

### 난이도 분류 예시:
```
쉬운 데이터 (D1 < 0.3):
- Grade Level: 5~8 (초중등)
- 짧은 문장, 간단한 단어
예: "서울은 대한민국의 수도입니다."

중간 데이터 (D1 = 0.3~0.7):
- Grade Level: 9~12 (고등학교)
- 중간 길이 문장, 일반 어휘
예: "민주주의는 국민이 주권을 가지고 정치에 참여하는 제도이다."

어려운 데이터 (D1 > 0.7):
- Grade Level: 13+ (대학+)
- 긴 문장, 전문 용어
예: "양자역학의 불확정성 원리는 입자의 위치와 운동량을 동시에 정확히 측정할 수 없음을 시사하는 fundamental limitation이다."
```

### ZPD Window 적용:
```
현재 모델이 Grade Level 10 텍스트를 잘 이해함
→ ZPD 범위: Grade Level 11~13 선택
→ Grade Level 5~9는 너무 쉬움 (제외)
→ Grade Level 14+는 너무 어려움 (제외)
```

### 인간 인지 난이도 상관관계 검증:
R4 연구는 Flesch-Kincaid가 실제 인간이 느끼는 난이도와 일치하는지 검증:
```
전문가 라벨링 (200개 샘플):
- 교육학 전문가 3인이 "읽기 난이도" 5점 척도 평가
- Flesch-Kincaid 점수와 상관분석
- 기대: Pearson r > 0.6 (중간 이상 상관)
```

## 더 알아보기
- Flesch Reading Ease: 0~100 범위 (높을수록 쉬움, Grade Level과 반대)
- SMOG Index: 복잡한 단어(3+ 음절) 중심 가독성 지표
- Gunning Fog Index: 복잡한 단어 비율 기반
- Coleman-Liau Index: 문자 수 기반 (영어 특화)
- 한국어 가독성: 문장 길이, 조사/어미 복잡도, 한자어 비율 등
- Microsoft Word, Google Docs에 기본 탑재
- 신문: Grade Level 8~10 목표 (일반 대중)
- 학술 논문: Grade Level 15~18 (전문가)
