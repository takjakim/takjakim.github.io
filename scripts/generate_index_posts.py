"""Generate narrative daily US/KR market posts for takjakim.github.io.

Outputs markdown notes under _notes/investing.

Usage:
  python scripts/generate_index_posts.py --start 2026-02-15 --end 2026-04-19 --force

Notes
- Uses yfinance daily closes.
- Skips non-trading days (no close).
- Writes only when --force, otherwise skips existing.
- Matches the structure of _notes/investing/2026-02-13-us.md but WITHOUT the
  "기사 인용" section.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from datetime import date, timedelta
from pathlib import Path

import pandas as pd
import yfinance as yf

ROOT = Path(__file__).resolve().parents[1]
OUTDIR = ROOT / "_notes" / "investing"


@dataclass(frozen=True)
class IndexSpec:
    label: str
    ticker: str
    wikilink: str


US_INDEXES = [
    IndexSpec("S&P 500", "^GSPC", "S&P 500"),
    IndexSpec("Dow Jones Industrial Average", "^DJI", "Dow Jones Industrial Average"),
    IndexSpec("Nasdaq Composite", "^IXIC", "Nasdaq Composite"),
]

KR_INDEXES = [
    IndexSpec("KOSPI", "^KS11", "KOSPI"),
    IndexSpec("KOSDAQ", "^KQ11", "KOSDAQ"),
]


def fmt_num(x: float) -> str:
    return f"{x:,.2f}"


def fmt_delta(delta: float) -> str:
    sign = "+" if delta >= 0 else "-"
    return f"{sign}{abs(delta):,.2f}"


def fmt_pct(p: float) -> str:
    sign = "+" if p >= 0 else "-"
    return f"{sign}{abs(p):.2f}%"


def to_datestr(d: date) -> str:
    return d.isoformat()


def daterange(start: date, end: date):
    d = start
    while d <= end:
        yield d
        d += timedelta(days=1)


def download_closes(tickers: list[str], start: date, end: date) -> pd.DataFrame:
    df = yf.download(
        tickers=tickers,
        start=to_datestr(start),
        end=to_datestr(end + timedelta(days=1)),
        interval="1d",
        auto_adjust=False,
        group_by="ticker",
        progress=False,
        threads=True,
    )

    if isinstance(df.columns, pd.MultiIndex):
        closes = pd.DataFrame({t: df[t]["Close"] for t in tickers})
    else:
        closes = df[["Close"]].rename(columns={"Close": tickers[0]})

    closes.index = pd.to_datetime(closes.index).tz_localize(None)
    closes = closes.sort_index()
    closes = closes.dropna(how="all")
    return closes


def compute_daily(closes: pd.DataFrame) -> pd.DataFrame:
    prev = closes.shift(1)
    delta = closes - prev
    pct = (delta / prev) * 100.0

    out = pd.concat({"close": closes, "delta": delta, "pct": pct}, axis=1)
    return out


def us_one_liner(spx: float, dji: float, ixic: float) -> str:
    avg = (spx + dji + ixic) / 3.0
    if avg >= 0.8:
        mood = "강한 리스크온"
    elif avg >= 0.2:
        mood = "완만한 리스크온"
    elif avg > -0.2:
        mood = "혼조/숨고르기"
    elif avg > -0.8:
        mood = "완만한 리스크오프"
    else:
        mood = "강한 리스크오프"

    # leadership
    if ixic >= spx and ixic >= dji:
        leader = "기술주(나스닥)"
    elif dji >= spx and dji >= ixic:
        leader = "다우(전통/가치)"
    else:
        leader = "시장 전반(S&P)"

    return f"해석 한 줄: **{mood}**. 오늘은 **{leader}** 흐름이 상대적으로 더 두드러졌다."


def us_insights(spx: float, dji: float, ixic: float) -> list[str]:
    avg = (spx + dji + ixic) / 3.0
    gap = ixic - spx

    a1 = (
        f"**리더십(나스닥 vs S&P) 체크** — 나스닥({fmt_pct(ixic)})과 S&P({fmt_pct(spx)})의 격차가 "
        f"{fmt_pct(gap).replace('+', '').replace('-', '')} 수준이라, 당일 수급이 **성장/가치 선호**로 갈렸을 수 있다."
        if abs(gap) >= 0.5
        else "**지수들이 같이 움직인 날** — 스타일보다 **매크로/금리/달러 같은 공통 요인**이 더 크게 작동했을 가능성이 높다."
    )

    if avg < -0.3:
        a2 = (
            "**리스크 관리 우선** — 지수 전반이 밀리면 좋은 종목도 같이 빠지기 쉬워서, "
            "단기에는 이벤트/포지셔닝/변동성 관리가 더 중요해진다."
        )
    elif avg > 0.3:
        a2 = (
            "**반등의 ‘연속성’이 중요** — 반등 구간에선 ‘왜 올랐나’보다 "
            "**무슨 섹터/팩터가 주도했는지**가 다음 날까지 이어지는지 관찰하는 게 실전에서 유리하다."
        )
    else:
        a2 = (
            "**진정/정리 구간** — 큰 방향성보다 전일의 과열/과매도에 대한 **포지션 조정**이 반영되기 쉽다."
        )

    a3 = (
        "**체크리스트 (다음 거래일)** — (1) 금리/달러가 다시 오르는지, "
        "(2) 빅테크 실적·가이던스 코멘트 변화, (3) 하락이 섹터 ‘확산’인지 ‘집중’인지 같이 보자."
    )

    return [a1, a2, a3]


def kr_one_liner(kospi: float, kosdaq: float) -> str:
    avg = (kospi + kosdaq) / 2.0
    if avg >= 1.0:
        mood = "강한 상승"
    elif avg >= 0.3:
        mood = "완만한 상승"
    elif avg > -0.3:
        mood = "혼조/횡보"
    elif avg > -1.0:
        mood = "완만한 하락"
    else:
        mood = "강한 하락"

    leader = "KOSDAQ"
    if kospi >= kosdaq:
        leader = "KOSPI"

    return f"해석 한 줄: **{mood}**. 오늘은 **{leader}** 쪽 변동이 상대적으로 더 컸다."


def kr_insights(kospi: float, kosdaq: float) -> list[str]:
    gap = kosdaq - kospi
    a1 = (
        f"**코스닥-코스피 격차** — 코스닥({fmt_pct(kosdaq)})이 코스피({fmt_pct(kospi)}) 대비 "
        f"{fmt_pct(gap)}p 만큼 더 움직여서, 중소형/모멘텀 쪽으로 수급이 쏠렸을 가능성이 있다."
        if abs(gap) >= 0.6
        else "**지수 간 격차가 크지 않음** — 테마보다 지수 전반(외국인/환율/금리) 요인이 더 크게 작동했을 수 있다."
    )

    a2 = (
        "**지수만 보면 놓치는 것** — 지수는 평균이라, 체감은 ‘상위 대형주’와 ‘변동 상위’에서 갈리는 경우가 많다. "
        "(가능하면 시총 상위/등락 상위를 같이 체크)"
    )

    a3 = (
        "**체크리스트 (다음 거래일)** — (1) 원/달러·금리 방향, (2) 반도체/2차전지/바이오 등 핵심 테마 수급, "
        "(3) 코스닥 변동이 과했는지(되돌림) 같이 보자."
    )

    return [a1, a2, a3]


def write_us_post(d: date, daily: pd.DataFrame, force: bool) -> Path | None:
    path = OUTDIR / f"{d.isoformat()}-us.md"
    if path.exists() and not force:
        return None

    idx = pd.Timestamp(d)
    if idx not in daily.index:
        return None
    row = daily.loc[idx]

    spx_c = float(row[("close", US_INDEXES[0].ticker)])
    dji_c = float(row[("close", US_INDEXES[1].ticker)])
    ixic_c = float(row[("close", US_INDEXES[2].ticker)])
    spx_p = float(row[("pct", US_INDEXES[0].ticker)])
    dji_p = float(row[("pct", US_INDEXES[1].ticker)])
    ixic_p = float(row[("pct", US_INDEXES[2].ticker)])

    if any(pd.isna(x) for x in [spx_c, dji_c, ixic_c, spx_p, dji_p, ixic_p]):
        return None

    last_mod = (d + timedelta(days=1)).isoformat()
    one = us_one_liner(spx_p, dji_p, ixic_p)
    ins = us_insights(spx_p, dji_p, ixic_p)

    md = "\n".join(
        [
            "---",
            f'title: "{d.isoformat()} 미국 증시 요약"',
            f"last_modified_at: {last_mod}",
            f"permalink: /investing/{d.isoformat()}-us/",
            "tags: [us, market, spx, ndx, dow, index]",
            "---",
            "",
            f"# {d.isoformat()} 미국 증시 요약",
            "",
            f"> 기준: {d.month}/{d.day} 미국장 종가. (투자 조언 아님)",
            "",
            "## 1) 지수 요약",
            "",
            f"- [[S&P 500]]: **{fmt_num(spx_c)} ({fmt_pct(spx_p)})**",
            f"- [[Dow Jones Industrial Average]]: **{fmt_num(dji_c)} ({fmt_pct(dji_p)})**",
            f"- [[Nasdaq Composite]]: **{fmt_num(ixic_c)} ({fmt_pct(ixic_p)})**",
            "",
            one,
            "",
            "## 2) 히트맵으로 보는 분위기",
            "",
            "### S&P 500",
            f'![S&P 500 heatmap](/assets/img/heatmaps/{d.isoformat()}/us-spx.png)',
            "",
            "### NASDAQ 100",
            f'![NASDAQ 100 heatmap](/assets/img/heatmaps/{d.isoformat()}/us-ndx.png)',
            "",
            "## 3) 인사이트 (내가 보는 포인트)",
            "",
            f"1. {ins[0]}",
            f"2. {ins[1]}",
            f"3. {ins[2]}",
            "",
            "## 연결",
            "",
            "- 지수 노트: [[S&P 500]] / [[NASDAQ 100]] / [[Nasdaq Composite]] / [[Dow Jones Industrial Average]]",
            "- 원칙/도구: [[해외 지수 분석 시작하기]]",
        ]
    )

    path.write_text(md + "\n", encoding="utf-8")
    return path


def write_kr_post(d: date, daily: pd.DataFrame, force: bool) -> Path | None:
    path = OUTDIR / f"{d.isoformat()}-korea.md"
    if path.exists() and not force:
        return None

    idx = pd.Timestamp(d)
    if idx not in daily.index:
        return None
    row = daily.loc[idx]

    kospi_c = float(row[("close", KR_INDEXES[0].ticker)])
    kosdaq_c = float(row[("close", KR_INDEXES[1].ticker)])
    kospi_d = float(row[("delta", KR_INDEXES[0].ticker)])
    kosdaq_d = float(row[("delta", KR_INDEXES[1].ticker)])
    kospi_p = float(row[("pct", KR_INDEXES[0].ticker)])
    kosdaq_p = float(row[("pct", KR_INDEXES[1].ticker)])

    if any(pd.isna(x) for x in [kospi_c, kosdaq_c, kospi_d, kosdaq_d, kospi_p, kosdaq_p]):
        return None

    last_mod = d.isoformat()
    one = kr_one_liner(kospi_p, kosdaq_p)
    ins = kr_insights(kospi_p, kosdaq_p)

    md = "\n".join(
        [
            "---",
            f'title: "{d.isoformat()} 한국 증시 요약 (KOSPI/KOSDAQ)"',
            f"last_modified_at: {last_mod}",
            f"permalink: /investing/{d.isoformat()}-korea/",
            "tags: [kr, market, kospi, kosdaq, index]",
            "---",
            "",
            f"# {d.isoformat()} 한국 증시 요약",
            "",
            "> 기준: 해당일 종가. (투자 조언 아님)",
            "",
            "## 1) 지수 요약",
            "",
            f"- **KOSPI**: {fmt_num(kospi_c)} ({fmt_delta(kospi_d)}, {fmt_pct(kospi_p)})",
            f"- **KOSDAQ**: {fmt_num(kosdaq_c)} ({fmt_delta(kosdaq_d)}, {fmt_pct(kosdaq_p)})",
            "",
            one,
            "",
            "## 2) 인사이트 (내가 보는 포인트)",
            "",
            f"1. {ins[0]}",
            f"2. {ins[1]}",
            f"3. {ins[2]}",
            "",
            "## 연결",
            "",
            "- 관련: [[지수 투자 시작하기]]",
        ]
    )

    path.write_text(md + "\n", encoding="utf-8")
    return path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--start", required=True)
    ap.add_argument("--end", required=True)
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args()

    start = date.fromisoformat(args.start)
    end = date.fromisoformat(args.end)

    OUTDIR.mkdir(parents=True, exist_ok=True)

    # Download a wider window so the first day in the requested range has a valid "prev close"
    # (pct/delta need the prior trading day).
    dl_start = start - timedelta(days=14)

    us_closes = download_closes([s.ticker for s in US_INDEXES], dl_start, end)
    kr_closes = download_closes([s.ticker for s in KR_INDEXES], dl_start, end)

    us_daily = compute_daily(us_closes)
    kr_daily = compute_daily(kr_closes)

    wrote: list[Path] = []
    for d in daterange(start, end):
        p1 = write_us_post(d, us_daily, force=args.force)
        p2 = write_kr_post(d, kr_daily, force=args.force)
        if p1:
            wrote.append(p1)
        if p2:
            wrote.append(p2)

    print(f"Wrote {len(wrote)} file(s).")
    for p in wrote[:10]:
        print("-", p.relative_to(ROOT))
    if len(wrote) > 10:
        print(f"... (+{len(wrote)-10} more)")


if __name__ == "__main__":
    main()
