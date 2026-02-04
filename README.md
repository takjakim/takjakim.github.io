# Digital Garden

> 투자 · 개발 · AI · Theory에 대한 생각과 기록을 연결하는 개인 지식 베이스

**Live Site**: [takjakim.kr](https://takjakim.kr)

## Features

- **Graph View** - 노트 간 연결을 시각화하는 인터랙티브 그래프 (카테고리별 색상 구분)
- **Bidirectional Links** - `[[노트명]]` 문법으로 노트 간 양방향 링크 자동 생성
- **Backlinks** - 현재 노트를 참조하는 다른 노트 자동 표시
- **Category System** - 투자, 개발, AI, Theory 4개 카테고리 분류
- **Modern UI** - 2026 트렌드 글래스모피즘 디자인
- **SEO Optimized** - sitemap.xml, robots.txt, JSON-LD 구조화 데이터
- **Responsive** - 모바일/데스크톱 반응형 레이아웃

## Tech Stack

- **Jekyll** - 정적 사이트 생성기
- **D3.js** - 그래프 시각화
- **SCSS** - 스타일링
- **GitHub Pages** - 호스팅
- **GitHub Actions** - CI/CD

## Structure

```
_notes/
├── investing/     # 투자 관련 노트
├── dev/           # 개발 관련 노트
├── ai/            # AI 관련 노트
└── theory/        # 이론/프레임워크 노트

_pages/            # 정적 페이지
_includes/         # 컴포넌트 (그래프, 헤더, 푸터)
_layouts/          # 레이아웃 템플릿
_sass/             # SCSS 스타일
_plugins/          # Jekyll 플러그인
```

## Local Development

```bash
# 의존성 설치
bundle install

# 로컬 서버 실행
bundle exec jekyll serve

# http://localhost:4000 에서 확인
```

## Deployment

GitHub Actions를 통해 `main` 브랜치 푸시 시 자동 배포됩니다.

## Credits

Based on [Digital Garden Jekyll Template](https://github.com/maximevaillancourt/digital-garden-jekyll-template) by Maxime Vaillancourt.

## License

MIT License
