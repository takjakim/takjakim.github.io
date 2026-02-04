#!/usr/bin/env python3
"""Generate daily market report JSON + Markdown.

Creates:
- assets/data/heatmaps/YYYY-MM-DD/daily.json
- _notes/investing/YYYY-MM-DD-daily.md

Data sources:
- Indices: Stooq for NDX/SPX/HSI; yfinance for CSI300 (000300.SS) fallback
- Items: Stooq per-ticker daily CSV for the 30-ticker watchlist
- News: web fetch (best-effort). If parsing fails, leaves empty arrays.

Designed to run locally (Clawdbot cron) after US close (KST 06:00+).
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
from pathlib import Path

import requests

try:
    import yfinance as yf
except Exception:
    yf = None

ROOT = Path(__file__).resolve().parents[1]
UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X)"}

STOOQ_DAILY = "https://stooq.com/q/d/l/?s={sym}&i=d"

WATCHLIST = {
    "US": [
        ("aapl.us", "AAPL", "Apple", "Technology"),
        ("msft.us", "MSFT", "Microsoft", "Technology"),
        ("nvda.us", "NVDA", "NVIDIA", "Technology"),
        ("googl.us", "GOOGL", "Alphabet", "Technology"),
        ("amzn.us", "AMZN", "Amazon", "Consumer"),
        ("meta.us", "META", "Meta", "Technology"),
        ("tsla.us", "TSLA", "Tesla", "Automotive"),
        ("avgo.us", "AVGO", "Broadcom", "Semiconductor"),
        ("brk-b.us", "BRK-B", "Berkshire", "Financials"),
        ("jpm.us", "JPM", "JPMorgan", "Financials"),
        ("lly.us", "LLY", "Eli Lilly", "Healthcare"),
        ("v.us", "V", "Visa", "Financials"),
        ("unh.us", "UNH", "UnitedHealth", "Healthcare"),
        ("xom.us", "XOM", "ExxonMobil", "Energy"),
        ("ma.us", "MA", "Mastercard", "Financials"),
    ],
    "HK": [
        ("0700.hk", "0700.HK", "Tencent", "Technology"),
        ("9988.hk", "9988.HK", "Alibaba", "Technology"),
        ("0005.hk", "0005.HK", "HSBC", "Financials"),
        ("1299.hk", "1299.HK", "AIA", "Insurance"),
        ("0941.hk", "0941.HK", "China Mobile", "Telecom"),
        ("2318.hk", "2318.HK", "Ping An", "Insurance"),
        ("0388.hk", "0388.HK", "HKEX", "Financials"),
        ("0939.hk", "0939.HK", "CCB", "Financials"),
        ("1398.hk", "1398.HK", "ICBC", "Financials"),
        ("3690.hk", "3690.HK", "Meituan", "Technology"),
    ],
    "CN": [
        ("600519.cn", "600519.SS", "귀주모태", "Consumer"),
        ("601318.cn", "601318.SS", "핑안보험", "Insurance"),
        ("000858.cn", "000858.SZ", "오량액", "Consumer"),
        ("600036.cn", "600036.SS", "초상은행", "Financials"),
        ("601166.cn", "601166.SS", "흥업은행", "Financials"),
    ],
}


def stooq_last_two_closes(sym: str, date: str | None = None):
    """Return (close, prev_close, effective_date) for given symbol.

    If date is given, tries to find that row; otherwise uses last row.
    """
    url = STOOQ_DAILY.format(sym=sym)
    txt = requests.get(url, headers=UA, timeout=30).text
    if "Exceeded the daily hits limit" in txt:
        raise RuntimeError("stooq_daily_hits_limit")
    lines = [ln for ln in txt.splitlines() if ln.strip()]
    if not lines or not lines[0].startswith("Date,"):
        raise RuntimeError(f"no_csv_for_{sym}")

    def parse_row(ln):
        parts = ln.split(",")
        return parts[0], float(parts[4])

    if date:
        # scan from end
        for i in range(len(lines) - 1, 0, -1):
            d, c = parse_row(lines[i])
            if d == date:
                dprev, cprev = parse_row(lines[i - 1])
                return c, cprev, d
        raise RuntimeError(f"date_not_found_{sym}_{date}")

    # last two rows
    d1, c1 = parse_row(lines[-1])
    d0, c0 = parse_row(lines[-2])
    return c1, c0, d1


def pct_change(close: float, prev: float) -> float:
    return (close - prev) / prev * 100.0 if prev else 0.0


def fetch_indices(target_date: str):
    """Fetch 4 indices. Prefer Stooq, fall back to yfinance when Stooq is rate-limited."""
    indices = {}

    mapping = {
        "NDX": "^ndx",
        "SPX": "^spx",
        "HSI": "^hsi",
    }

    stooq_ok = True
    for k, sym in mapping.items():
        try:
            close, prev, eff = stooq_last_two_closes(sym, date=target_date)
            indices[k] = {"close": round(close, 2), "pct": round(pct_change(close, prev), 2), "date": eff}
        except Exception as e:
            stooq_ok = False
            indices[k] = {"close": None, "pct": None, "date": None}

    # CSI300: Stooq unreliable; yfinance single-ticker
    if yf is not None:
        try:
            df = yf.download("000300.SS", start=(dt.date.fromisoformat(target_date) - dt.timedelta(days=7)).isoformat(), end=(dt.date.fromisoformat(target_date) + dt.timedelta(days=2)).isoformat(), interval="1d", progress=False, threads=False)
            if not df.empty:
                df.index = df.index.tz_localize(None)
                t = dt.datetime.fromisoformat(target_date)
                if t in df.index:
                    i = list(df.index).index(t)
                    if i > 0:
                        close = float(df["Close"].iloc[i])
                        prev = float(df["Close"].iloc[i - 1])
                        indices["CSI300"] = {"close": round(close, 2), "pct": round(pct_change(close, prev), 2), "date": target_date}
        except Exception:
            pass

    indices.setdefault("CSI300", {"close": None, "pct": None, "date": None})

    # If Stooq is rate-limited, try yfinance for US/HK indices too (few calls)
    if (not stooq_ok) and yf is not None:
        yf_map = {
            "NDX": "^NDX",
            "SPX": "^GSPC",
            "HSI": "^HSI",
        }
        for k, sym in yf_map.items():
            if indices.get(k, {}).get("close") is not None:
                continue
            try:
                df = yf.download(sym, start=(dt.date.fromisoformat(target_date) - dt.timedelta(days=7)).isoformat(), end=(dt.date.fromisoformat(target_date) + dt.timedelta(days=2)).isoformat(), interval="1d", progress=False, threads=False)
                if df.empty:
                    continue
                df.index = df.index.tz_localize(None)
                t = dt.datetime.fromisoformat(target_date)
                if t in df.index:
                    i = list(df.index).index(t)
                    if i > 0:
                        close = float(df["Close"].iloc[i])
                        prev = float(df["Close"].iloc[i - 1])
                        indices[k] = {"close": round(close, 2), "pct": round(pct_change(close, prev), 2), "date": target_date}
            except Exception:
                continue

    return indices


def fetch_items(target_date: str):
    items = []
    sess = requests.Session()

    for market, rows in WATCHLIST.items():
        for stooq_sym, ticker, name, sector in rows:
            try:
                url = STOOQ_DAILY.format(sym=stooq_sym)
                txt = sess.get(url, headers=UA, timeout=30).text
                if "Exceeded the daily hits limit" in txt:
                    raise RuntimeError("stooq_daily_hits_limit")
                lines = [ln for ln in txt.splitlines() if ln.strip()]
                if not lines or not lines[0].startswith("Date,"):
                    continue
                # find date row
                prev_close = None
                cur_close = None
                for i in range(len(lines) - 1, 0, -1):
                    parts = lines[i].split(",")
                    if parts[0] == target_date:
                        cur_close = float(parts[4])
                        prev_close = float(lines[i - 1].split(",")[4])
                        break
                if cur_close is None or prev_close is None:
                    continue
                p = pct_change(cur_close, prev_close)
                items.append({
                    "ticker": ticker,
                    "name": name,
                    "sector": sector,
                    "pct": round(p, 2),
                    "market": market,
                })
            except Exception:
                continue

    return items


def pick_top(items, n=10):
    gainers = sorted(items, key=lambda x: x.get("pct", 0), reverse=True)[:n]
    losers = sorted(items, key=lambda x: x.get("pct", 0))[:n]
    return gainers, losers


def fetch_news_best_effort():
    # We cannot use web_search (no Brave key). Best-effort scrape via readability is unreliable.
    # We'll leave placeholders to be filled later.
    return [], []


def make_insight(indices, items):
    # Very lightweight heuristic.
    ndx = indices.get("NDX", {}).get("pct")
    spx = indices.get("SPX", {}).get("pct")
    hsi = indices.get("HSI", {}).get("pct")
    csi = indices.get("CSI300", {}).get("pct")

    word = "변동성"
    if ndx is not None and spx is not None and abs(ndx - spx) >= 0.7:
        word = "디커플링"
    elif ndx is not None and ndx > 0.8 and spx is not None and spx > 0.5:
        word = "리스크온"
    elif ndx is not None and ndx < -0.8 and spx is not None and spx < -0.5:
        word = "리스크오프"

    # one-line summary
    summary = "미국은 혼조, 아시아는 정책/수급 이슈에 따라 따로 노는 흐름."
    if ndx is not None and spx is not None and ndx < 0 and spx < 0 and (hsi is not None and hsi > 0):
        summary = "미국은 조정, 홍콩/중국은 반등 — 하루 만에 표정이 바뀐 장."

    return word, summary


def fmt_idx_row(label, close, pct):
    if close is None or pct is None:
        return f"| {label} | 조회 실패 | 조회 실패 |"
    sign = "+" if pct > 0 else ""
    return f"| {label} | {close:,.2f} | {sign}{pct:.2f}% |"


def write_outputs(date: str, indices, items, gainers, losers, us_news, asia_news):
    out_dir = ROOT / "assets" / "data" / "heatmaps" / date
    out_dir.mkdir(parents=True, exist_ok=True)

    daily = {
        "date": date,
        "indices": {
            "NDX": {"close": indices["NDX"]["close"], "pct": indices["NDX"]["pct"]},
            "SPX": {"close": indices["SPX"]["close"], "pct": indices["SPX"]["pct"]},
            "HSI": {"close": indices["HSI"]["close"], "pct": indices["HSI"]["pct"]},
            "CSI300": {"close": indices["CSI300"]["close"], "pct": indices["CSI300"]["pct"]},
        },
        "items": items,
        "top_gainers": [{k: x[k] for k in ("ticker", "name", "pct", "market")} for x in gainers],
        "top_losers": [{k: x[k] for k in ("ticker", "name", "pct", "market")} for x in losers],
        "news": {"us": us_news, "asia": asia_news},
    }

    (out_dir / "daily.json").write_text(json.dumps(daily, ensure_ascii=False, indent=2), encoding="utf-8")

    word, one_line = make_insight(indices, items)

    md_path = ROOT / "_notes" / "investing" / f"{date}-daily.md"

    def table_rows(items_list):
        lines = []
        for i, x in enumerate(items_list, 1):
            sign = "+" if x["pct"] > 0 else ""
            lines.append(f"| {i} | {x['ticker']} ({x['name']}) | {sign}{x['pct']:.2f}% | {x['market']} |")
        return "\n".join(lines)

    us_lines = "\n".join([f"{i+1}. **{n.get('title','(제목 없음)')}** - {n.get('summary','')} _(CNBC)_" for i, n in enumerate(us_news)]) or "- (뉴스 수집 미설정)"
    asia_lines = "\n".join([f"{i+1}. **{n.get('title','(제목 없음)')}** - {n.get('summary','')} _(SCMP)_" for i, n in enumerate(asia_news)]) or "- (뉴스 수집 미설정)"

    md = f"""---
title: \"{date} 시장 리포트\"
last_modified_at: {date}
---

# {date} 시장 리포트

## 📌 한줄 요약
> {one_line}

---

## 📈 주요 지수

| 지수 | 종가 | 등락률 |
|------|------|--------|
{fmt_idx_row('🇺🇸 NASDAQ 100', indices['NDX']['close'], indices['NDX']['pct'])}
{fmt_idx_row('🇺🇸 S&P 500', indices['SPX']['close'], indices['SPX']['pct'])}
{fmt_idx_row('🇭🇰 항셍지수', indices['HSI']['close'], indices['HSI']['pct'])}
{fmt_idx_row('🇨🇳 CSI 300', indices['CSI300']['close'], indices['CSI300']['pct'])}

---

## 🚀 상승 Top 10

| 순위 | 종목 | 등락률 | 시장 |
|------|------|--------|------|
{table_rows(gainers) if gainers else '| - | - | - | - |'}

---

## 📉 하락 Top 10

| 순위 | 종목 | 등락률 | 시장 |
|------|------|--------|------|
{table_rows(losers) if losers else '| - | - | - | - |'}

---

## 🗺️ 히트맵
<div class=\"market-heatmap\" data-file=\"daily\" data-as-of=\"{date}\"></div>

---

## 📰 오늘의 뉴스

### 미국
{us_lines}

### 아시아
{asia_lines}

---

## ✍️ 인사이트

### 오늘 시장을 한 단어로? **{word}**
- (짧은 이유를 내일 더 다듬자)

### 내일 주목 포인트
1. 금리/달러 방향
2. 빅테크 실적/가이던스
3. 중화권 정책/수급

---

## 🔗 연결 노트
- 투자 원칙: [[지수 투자 시작하기]]
- 분석 도구: [[AI 투자 분석 활용하기]]
"""

    md_path.write_text(md, encoding="utf-8")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", required=True, help="YYYY-MM-DD")
    args = ap.parse_args()

    date = args.date

    indices = fetch_indices(date)
    items = fetch_items(date)
    gainers, losers = pick_top(items, 10)
    us_news, asia_news = fetch_news_best_effort()

    write_outputs(date, indices, items, gainers, losers, us_news, asia_news)


if __name__ == "__main__":
    main()
