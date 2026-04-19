"""Generate daily US/KR index summary posts for takjakim.github.io.

Outputs markdown notes under _notes/investing.

Usage:
  /Users/jahkim/clawd/.venv-market/bin/python scripts/generate_index_posts.py --start 2026-02-15 --end 2026-04-19

Notes:
- Uses yfinance for index closes.
- Creates/overwrites files only when --force is set; otherwise skips existing.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from pathlib import Path

import pandas as pd
import yfinance as yf

ROOT = Path(__file__).resolve().parents[1]
OUTDIR = ROOT / "_notes" / "investing"


@dataclass(frozen=True)
class IndexSpec:
    label: str
    ticker: str


US_INDEXES = [
    IndexSpec("S&P 500", "^GSPC"),
    IndexSpec("Dow Jones Industrial Average", "^DJI"),
    IndexSpec("Nasdaq Composite", "^IXIC"),
]

KR_INDEXES = [
    IndexSpec("KOSPI", "^KS11"),
    IndexSpec("KOSDAQ", "^KQ11"),
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


def download_closes(tickers: list[str], start: date, end: date) -> pd.DataFrame:
    # yfinance end is exclusive in many cases; add 1 day to be safe.
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

    # Normalize to a DataFrame of closes with columns=tickers, index=date
    if isinstance(df.columns, pd.MultiIndex):
        closes = pd.DataFrame({t: df[t]["Close"] for t in tickers})
    else:
        # Single ticker
        closes = df[["Close"]].rename(columns={"Close": tickers[0]})

    closes.index = pd.to_datetime(closes.index).tz_localize(None)
    closes = closes.sort_index()
    closes = closes.dropna(how="all")
    return closes


def compute_daily(closes: pd.DataFrame) -> pd.DataFrame:
    prev = closes.shift(1)
    delta = closes - prev
    pct = (delta / prev) * 100.0

    out = pd.concat(
        {
            "close": closes,
            "delta": delta,
            "pct": pct,
        },
        axis=1,
    )
    return out


def write_us_post(d: date, daily: pd.DataFrame, force: bool) -> Path | None:
    fname = f"{d.isoformat()}-us.md"
    path = OUTDIR / fname
    if path.exists() and not force:
        return None

    # Extract row
    idx = pd.Timestamp(d)
    if idx not in daily.index:
        return None

    row = daily.loc[idx]

    def line(spec: IndexSpec, wikilink: str, tag: str) -> str:
        c = float(row[("close", spec.ticker)])
        p = float(row[("pct", spec.ticker)])
        # Some days pct can be NaN (first row) -> skip
        if pd.isna(p):
            return ""
        return f"- [[{wikilink}]]: **{fmt_num(c)} ({fmt_pct(p)})**"

    lines = [
        line(US_INDEXES[0], "S&P 500", "spx"),
        line(US_INDEXES[1], "Dow Jones Industrial Average", "dow"),
        line(US_INDEXES[2], "Nasdaq Composite", "ixic"),
    ]
    lines = [l for l in lines if l]
    if not lines:
        return None

    last_mod = (d + timedelta(days=1)).isoformat()

    md = "\n".join(
        [
            "---",
            f'title: "{d.isoformat()} 미국 증시 지수 요약"',
            f"last_modified_at: {last_mod}",
            f"permalink: /investing/{d.isoformat()}-us/",
            "tags: [us, market, index, spx, dji, ixic]",
            "---",
            "",
            f"# {d.isoformat()} 미국 증시 지수 요약",
            "",
            "> 기준: 해당일 미국장 종가. (투자 조언 아님)",
            "",
            "## 1) 지수 요약",
            "",
            *lines,
            "",
            "## 2) 히트맵으로 보는 분위기",
            "",
            "### S&P 500",
            f'<div class="market-heatmap" data-country="us" data-index="spx" data-as-of="{d.isoformat()}"></div>',
            "",
            "### NASDAQ 100",
            f'<div class="market-heatmap" data-country="us" data-index="ndx" data-as-of="{d.isoformat()}"></div>',
            "",
            "## 연결",
            "",
            "- 지수 노트: [[S&P 500]] / [[Nasdaq Composite]] / [[Dow Jones Industrial Average]]",
        ]
    )

    path.write_text(md + "\n", encoding="utf-8")
    return path


def write_kr_post(d: date, daily: pd.DataFrame, force: bool) -> Path | None:
    fname = f"{d.isoformat()}-korea.md"
    path = OUTDIR / fname
    if path.exists() and not force:
        return None

    idx = pd.Timestamp(d)
    if idx not in daily.index:
        return None

    row = daily.loc[idx]

    def line(spec: IndexSpec) -> str:
        c = float(row[("close", spec.ticker)])
        dd = float(row[("delta", spec.ticker)])
        pp = float(row[("pct", spec.ticker)])
        if pd.isna(pp) or pd.isna(dd):
            return ""
        return f"- **{spec.label}**: {fmt_num(c)} ({fmt_delta(dd)}, {fmt_pct(pp)})"

    lines = [line(KR_INDEXES[0]), line(KR_INDEXES[1])]
    lines = [l for l in lines if l]
    if not lines:
        return None

    last_mod = d.isoformat()

    md = "\n".join(
        [
            "---",
            f'title: "{d.isoformat()} 한국 증시 지수 요약 (KOSPI/KOSDAQ)"',
            f"last_modified_at: {last_mod}",
            f"permalink: /investing/{d.isoformat()}-korea/",
            "tags: [kr, market, index, kospi, kosdaq]",
            "---",
            "",
            f"# {d.isoformat()} 한국 증시 지수 요약",
            "",
            "> 기준: 해당일 종가. (투자 조언 아님)",
            "",
            "## 1) 지수 요약",
            "",
            *lines,
            "",
            "## 연결",
            "",
            "- 관련: [[지수 투자 시작하기]]",
        ]
    )

    path.write_text(md + "\n", encoding="utf-8")
    return path


def daterange(start: date, end: date):
    d = start
    while d <= end:
        yield d
        d += timedelta(days=1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--start", required=True)
    ap.add_argument("--end", required=True)
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args()

    start = date.fromisoformat(args.start)
    end = date.fromisoformat(args.end)

    OUTDIR.mkdir(parents=True, exist_ok=True)

    us_closes = download_closes([s.ticker for s in US_INDEXES], start, end)
    kr_closes = download_closes([s.ticker for s in KR_INDEXES], start, end)

    us_daily = compute_daily(us_closes)
    kr_daily = compute_daily(kr_closes)

    wrote = []
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
