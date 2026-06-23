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
import requests

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

SIGNAL_TICKERS = [
    "KRW=X",       # USD/KRW
    "^TNX",        # US 10Y yield index (Yahoo quotes yield * 10)
    "DX-Y.NYB",    # US Dollar Index
    "CL=F",        # WTI crude oil futures
    "005930.KS",   # Samsung Electronics
    "000660.KS",   # SK hynix
    "012450.KS",   # Hanwha Aerospace (defense)
    "247540.KQ",   # EcoPro BM (battery)
    "068270.KS",   # Celltrion (bio)
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


UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X)"}


def _yahoo_chart_closes(ticker: str, start: date, end: date) -> pd.Series:
    """Fetch daily close series for [start, end] inclusive via Yahoo chart endpoint."""
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}"
    # Using range is simpler; keep it small.
    # We request ~30 days to cover weekends/holidays.
    params = {"interval": "1d", "range": "30d"}
    r = requests.get(url, params=params, headers=UA, timeout=30)
    r.raise_for_status()
    j = r.json()
    result = (((j or {}).get("chart") or {}).get("result") or [None])[0]
    if not result:
        return pd.Series(dtype=float)

    ts = result.get("timestamp") or []
    quote = (((result.get("indicators") or {}).get("quote") or [None])[0]) or {}
    closes = quote.get("close") or []

    rows = []
    for t, c in zip(ts, closes):
        if c is None:
            continue
        # Yahoo daily timestamps are often intraday UTC values (e.g. US
        # indices at 13:30 UTC). Normalize before date filtering so the
        # requested end date is not accidentally excluded by a midnight
        # comparison.
        d = pd.to_datetime(int(t), unit="s").tz_localize(None).normalize()
        rows.append((d, float(c)))

    if not rows:
        return pd.Series(dtype=float)

    s = pd.Series({d: v for d, v in rows}).sort_index()
    s = s[(s.index >= pd.Timestamp(start)) & (s.index <= pd.Timestamp(end))]
    s.name = ticker
    return s


def download_closes(tickers: list[str], start: date, end: date) -> pd.DataFrame:
    # Yahoo endpoint is 1 request per ticker, but we only have a few indices.
    series = []
    for t in tickers:
        try:
            s = _yahoo_chart_closes(t, start, end)
        except Exception:
            s = pd.Series(dtype=float)
        s.name = t
        series.append(s)

    closes = pd.concat(series, axis=1)
    closes.index = pd.to_datetime(closes.index).tz_localize(None).normalize()
    closes = closes.sort_index()
    closes = closes.groupby(level=0).last()
    closes = closes.dropna(how="all")
    return closes


def plausible_index_close(ticker: str, close: float) -> bool:
    """Reject obviously bad vendor data before writing public notes.

    Yahoo occasionally returns corrupt / wrong-market values for Korean indices.
    Keep bounds intentionally broad so normal market moves do not get filtered.
    """
    bounds = {
        "^KS11": (1_000.0, 15_000.0),
        "^KQ11": (300.0, 3_000.0),
    }
    lo_hi = bounds.get(ticker)
    if lo_hi is None:
        return True
    lo, hi = lo_hi
    return lo <= close <= hi


def heatmap_asset_date(d: date, slug: str) -> str | None:
    """Return the nearest heatmap image date for a market slug.

    The heatmap workflow dates assets by UTC run date, while US index posts are
    dated by the prior US trading session. For Monday US closes the matching
    heatmap often appears under the next calendar day (e.g. 2026-06-16 for the
    2026-06-15 US post). Search a small forward/backward window and skip broken
    image links when no asset exists.
    """
    candidates = [d, d + timedelta(days=1), d - timedelta(days=1), d + timedelta(days=2)]
    for cand in candidates:
        rel = Path("assets") / "img" / "heatmaps" / cand.isoformat() / f"{slug}.png"
        if (ROOT / rel).exists():
            return cand.isoformat()
    return None


def compute_daily(closes: pd.DataFrame) -> pd.DataFrame:
    prev = closes.ffill().shift(1)
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

    return [a1, a2]


def daily_value(daily: pd.DataFrame | None, d: date, field: str, ticker: str) -> float | None:
    if daily is None:
        return None
    idx = pd.Timestamp(d)
    if idx not in daily.index or (field, ticker) not in daily.columns:
        return None
    value = daily.loc[idx, (field, ticker)]
    if pd.isna(value):
        return None
    return float(value)


def pct_phrase(label: str, pct: float | None) -> str:
    if pct is None:
        return f"{label} 데이터는 아직 비어 있어서 방향만 체크한다."
    direction = "상승" if pct >= 0 else "하락"
    return f"{label} {direction}({fmt_pct(pct)})"


def kr_next_session_checklist(
    d: date,
    kospi_pct: float,
    kosdaq_pct: float,
    signal_daily: pd.DataFrame | None = None,
) -> list[str]:
    usdkrw = daily_value(signal_daily, d, "pct", "KRW=X")
    us10y = daily_value(signal_daily, d, "pct", "^TNX")
    dxy = daily_value(signal_daily, d, "pct", "DX-Y.NYB")
    wti = daily_value(signal_daily, d, "pct", "CL=F")
    samsung = daily_value(signal_daily, d, "pct", "005930.KS")
    hynix = daily_value(signal_daily, d, "pct", "000660.KS")
    defense = daily_value(signal_daily, d, "pct", "012450.KS")
    battery = daily_value(signal_daily, d, "pct", "247540.KQ")
    bio = daily_value(signal_daily, d, "pct", "068270.KS")

    if usdkrw is None:
        fx_note = "**원/달러** — 환율 데이터가 비어 있어서, 다음 장에서는 원/달러가 재상승하는지 먼저 확인하자."
    elif usdkrw > 0.3:
        fx_note = f"**원/달러** — 원/달러가 {fmt_pct(usdkrw)} 상승했다. 다음 장에서도 오르면 외국인 수급과 코스피 대형주에는 부담으로 볼 수 있다."
    elif usdkrw < -0.3:
        fx_note = f"**원/달러** — 원/달러가 {fmt_pct(usdkrw)} 하락했다. 원화 강세가 이어지면 외국인 수급과 대형주 반등에는 우호적이다."
    else:
        fx_note = f"**원/달러** — 원/달러 변동이 {fmt_pct(usdkrw)}로 크지 않았다. 환율보다 업종/개별 테마 수급을 더 봐야 한다."

    risk_parts = [pct_phrase("미 10년물", us10y), pct_phrase("DXY", dxy), pct_phrase("WTI", wti)]
    if (us10y is not None and us10y > 1.0) or (dxy is not None and dxy > 0.4):
        macro_bias = "금리/달러가 다시 위로 가면 성장주·코스닥의 단기 변동성이 커질 수 있다."
    elif (us10y is not None and us10y < -1.0) or (dxy is not None and dxy < -0.4):
        macro_bias = "금리/달러가 내려가면 성장주와 코스닥 쪽 위험선호가 이어질 여지가 있다."
    elif wti is not None and wti < -3.0:
        macro_bias = "유가 하락은 한국 수입물가·항공/화학 마진 기대에는 우호적인 변수다."
    else:
        macro_bias = "방향성이 엇갈리면 지수보다 업종별 상대강도 확인이 더 중요하다."
    macro_note = f"**금리·달러·유가** — {'; '.join(risk_parts)}. {macro_bias}"

    semis = [x for x in [samsung, hynix] if x is not None]
    semis_avg = sum(semis) / len(semis) if semis else None
    theme_bits = []
    if samsung is not None:
        theme_bits.append(f"삼성전자 {fmt_pct(samsung)}")
    if hynix is not None:
        theme_bits.append(f"SK하이닉스 {fmt_pct(hynix)}")
    if defense is not None:
        theme_bits.append(f"방산(한화에어로) {fmt_pct(defense)}")
    if battery is not None:
        theme_bits.append(f"2차전지(에코프로비엠) {fmt_pct(battery)}")
    if bio is not None:
        theme_bits.append(f"바이오(셀트리온) {fmt_pct(bio)}")

    if semis_avg is not None and semis_avg > 1.0:
        theme_bias = "반도체가 지수 상승을 계속 끌고 가는지 확인하자."
    elif semis_avg is not None and semis_avg < -1.0:
        theme_bias = "반도체가 밀리면 코스피 랠리의 질이 약해질 수 있다."
    elif kosdaq_pct - kospi_pct > 1.0:
        theme_bias = "코스닥 우위가 이어지면 2차전지/바이오 같은 모멘텀 테마 확산을 보자."
    else:
        theme_bias = "주도주가 좁아지는지, 아니면 반도체 외 테마로 확산되는지 체크하자."

    theme_summary = "; ".join(theme_bits) if theme_bits else "대표 테마 데이터는 비어 있음"
    theme_note = f"**핵심 테마 수급** — {theme_summary}. {theme_bias}"

    breadth_note = (
        "**되돌림/확산** — 코스피가 코스닥보다 크게 앞섰다. 다음 장에서는 대형주 랠리가 중소형주로 확산되는지, 아니면 대형주만 버티는 장인지 구분하자."
        if kospi_pct - kosdaq_pct > 1.0
        else "**되돌림/확산** — 코스닥 탄력이 더 강하다. 급등 테마는 추격보다 거래대금 지속성과 눌림 강도를 보는 게 안전하다."
        if kosdaq_pct - kospi_pct > 1.0
        else "**되돌림/확산** — 코스피·코스닥 온도차가 크지 않다. 상승/하락 종목 수와 거래대금 확산 여부를 같이 보자."
    )

    return [fx_note, macro_note, theme_note, breadth_note]


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

    spx_heatmap_date = heatmap_asset_date(d, "us-spx")
    ndx_heatmap_date = heatmap_asset_date(d, "us-ndx")
    heatmap_lines = [
        "## 2) 히트맵으로 보는 분위기",
        "",
    ]
    if spx_heatmap_date:
        heatmap_lines.extend([
            "### S&P 500",
            f'![S&P 500 heatmap](/assets/img/heatmaps/{spx_heatmap_date}/us-spx.png)',
            "",
        ])
    if ndx_heatmap_date:
        heatmap_lines.extend([
            "### NASDAQ 100",
            f'![NASDAQ 100 heatmap](/assets/img/heatmaps/{ndx_heatmap_date}/us-ndx.png)',
            "",
        ])
    if not spx_heatmap_date and not ndx_heatmap_date:
        heatmap_lines.extend([
            "- 해당 날짜에 연결할 수 있는 히트맵 이미지가 아직 없다.",
            "",
        ])

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
            *heatmap_lines,
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


def write_kr_post(
    d: date,
    daily: pd.DataFrame,
    force: bool,
    signal_daily: pd.DataFrame | None = None,
) -> Path | None:
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
    if not plausible_index_close(KR_INDEXES[0].ticker, kospi_c):
        print(f"Skipping {d.isoformat()} Korea post: implausible KOSPI close {kospi_c:,.2f}")
        return None
    if not plausible_index_close(KR_INDEXES[1].ticker, kosdaq_c):
        print(f"Skipping {d.isoformat()} Korea post: implausible KOSDAQ close {kosdaq_c:,.2f}")
        return None

    last_mod = d.isoformat()
    one = kr_one_liner(kospi_p, kosdaq_p)
    ins = kr_insights(kospi_p, kosdaq_p)
    checklist = kr_next_session_checklist(d, kospi_p, kosdaq_p, signal_daily)

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
            "",
            "## 3) 다음 거래일 체크포인트",
            "",
            f"1. {checklist[0]}",
            f"2. {checklist[1]}",
            f"3. {checklist[2]}",
            f"4. {checklist[3]}",
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
    signal_closes = download_closes(SIGNAL_TICKERS, dl_start, end)

    us_daily = compute_daily(us_closes)
    kr_daily = compute_daily(kr_closes)
    signal_daily = compute_daily(signal_closes)

    wrote: list[Path] = []
    for d in daterange(start, end):
        p1 = write_us_post(d, us_daily, force=args.force)
        p2 = write_kr_post(d, kr_daily, force=args.force, signal_daily=signal_daily)
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
