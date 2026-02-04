#!/usr/bin/env python3
"""Generate ECharts treemap JSON for market heatmaps.

Outputs:
  assets/data/heatmaps/YYYY-MM-DD/{key}.json

Keys:
  us-ndx, us-spx, cn-csi300, hk-hsi, hk-hstech, all-sectors

Data:
- Daily % change + market cap via yfinance.
- Constituents:
  - US NDX/SPX: Wikipedia tables (best-effort)
  - CN/HK: pinned CSVs in data/constituents/*.csv (recommended)

This is designed to run in GitHub Actions.
"""

from __future__ import annotations

import datetime as dt
import json
from dataclasses import dataclass
from pathlib import Path

import pandas as pd
import requests
import yfinance as yf

ROOT = Path(__file__).resolve().parents[1]
UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X)"}


@dataclass
class IndexSpec:
    key: str
    label: str
    tickers: list[str]
    meta: dict


def wiki_tickers(url: str) -> pd.DataFrame:
    html = requests.get(url, headers=UA, timeout=30).text
    tables = pd.read_html(html)
    target = None
    ticker_col = None
    for t in tables:
        cols = [str(c).lower() for c in t.columns]
        for c in t.columns:
            lc = str(c).lower()
            if lc == "ticker" or "ticker" in lc or "symbol" in lc:
                target = t
                ticker_col = c
                break
        if target is not None:
            break
    if target is None or ticker_col is None:
        raise RuntimeError(f"Could not find ticker table on {url}")

    # best-effort name/sector
    def pick(cols, hints):
        low = {c: str(c).lower() for c in cols}
        for h in hints:
            hl = h.lower()
            for c, cl in low.items():
                if hl == cl or hl in cl:
                    return c
        return None

    name_col = pick(target.columns, ["Company", "Name", "Security", "Issuer"])
    sector_col = pick(target.columns, ["Sector", "Industry", "GICS Sector"])

    df = pd.DataFrame({
        "ticker": target[ticker_col].astype(str).str.strip().str.replace(".", "-", regex=False)
    })
    if name_col is not None:
        df["name"] = target[name_col].astype(str).str.strip()
    else:
        df["name"] = df["ticker"]

    if sector_col is not None:
        df["sector"] = target[sector_col].astype(str).str.strip()
    else:
        df["sector"] = ""

    df = df[df["ticker"].str.len() > 0].drop_duplicates("ticker")
    return df


def csv_constituents(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    for col in ["ticker", "name", "sector"]:
        if col not in df.columns:
            raise RuntimeError(f"Missing column {col} in {path}")
    df["ticker"] = df["ticker"].astype(str).str.strip().str.replace(".", "-", regex=False)
    df["name"] = df["name"].astype(str).str.strip()
    df["sector"] = df["sector"].astype(str).str.strip()
    return df.drop_duplicates("ticker")


def fetch_prices(tickers: list[str]) -> pd.DataFrame:
    return yf.download(
        tickers=tickers,
        period="7d",
        interval="1d",
        group_by="ticker",
        auto_adjust=False,
        threads=True,
        progress=False,
    )


def compute_pct_change(price_df: pd.DataFrame, tickers: list[str]) -> pd.Series:
    out = {}
    for t in tickers:
        try:
            if isinstance(price_df.columns, pd.MultiIndex):
                if (t, "Close") not in price_df.columns:
                    continue
                close = price_df[(t, "Close")].dropna()
            else:
                close = price_df["Close"].dropna()
            if len(close) < 2:
                continue
            last = float(close.iloc[-1])
            prev = float(close.iloc[-2])
            if prev <= 0:
                continue
            out[t] = (last / prev - 1.0) * 100.0
        except Exception:
            continue
    return pd.Series(out, name="pct")


def fetch_market_caps(tickers: list[str]) -> pd.Series:
    caps = {}
    tks = yf.Tickers(" ".join(tickers))
    for t in tickers:
        try:
            tk = tks.tickers.get(t) or yf.Ticker(t)
            cap = None
            fi = getattr(tk, "fast_info", None)
            if fi is not None:
                cap = fi.get("marketCap") or fi.get("market_cap")
            if cap is None:
                info = tk.info
                cap = info.get("marketCap")
            if cap is None:
                continue
            cap = float(cap)
            if cap <= 0:
                continue
            caps[t] = cap
        except Exception:
            continue
    return pd.Series(caps, name="mcap")


def build_payload(label: str, df_const: pd.DataFrame, pct: pd.Series, mcap: pd.Series, as_of: str, source: str):
    df = df_const.set_index("ticker").join(pct).join(mcap)
    df = df.dropna(subset=["pct", "mcap"])  # require both
    items = []
    for t, r in df.iterrows():
        items.append({
            "ticker": t,
            "name": r.get("name") or t,
            "sector": r.get("sector") or "",
            "pct": float(r["pct"]),
            "mcap_usd_b": float(r["mcap"]) / 1e9,
        })

    return {
        "label": label,
        "asOf": as_of,
        "source": source,
        "items": items,
    }


def write_json(path: Path, payload: dict):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def main():
    as_of = dt.datetime.now().strftime("%Y-%m-%d")
    out_dir = ROOT / "assets" / "data" / "heatmaps" / as_of
    out_dir.mkdir(parents=True, exist_ok=True)

    specs: list[tuple[str, str, pd.DataFrame]] = []

    # US
    ndx_df = wiki_tickers("https://en.wikipedia.org/wiki/Nasdaq-100")
    spx_df = wiki_tickers("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies")

    specs.append(("us-ndx", "US · NASDAQ 100", ndx_df))
    specs.append(("us-spx", "US · S&P 500", spx_df))

    # CN/HK pinned CSV
    cdir = ROOT / "data" / "constituents"
    cn_path = cdir / "cn_csi300.csv"
    hk_hsi_path = cdir / "hk_hsi.csv"
    hk_hstech_path = cdir / "hk_hstech.csv"

    if cn_path.exists():
        specs.append(("cn-csi300", "CN · CSI 300", csv_constituents(cn_path)))
    if hk_hsi_path.exists():
        specs.append(("hk-hsi", "HK · Hang Seng", csv_constituents(hk_hsi_path)))
    if hk_hstech_path.exists():
        specs.append(("hk-hstech", "HK · Hang Seng Tech", csv_constituents(hk_hstech_path)))

    # Fetch market data once for all tickers
    all_tickers = sorted({t for _, _, df in specs for t in df["ticker"].astype(str).tolist()})
    price_df = fetch_prices(all_tickers)
    pct = compute_pct_change(price_df, all_tickers)
    mcap = fetch_market_caps(all_tickers)

    # Write index payloads
    for key, label, df_const in specs:
        payload = build_payload(label, df_const, pct, mcap, as_of, source="yfinance (pct+market cap), Wikipedia/CSV constituents")
        write_json(out_dir / f"{key}.json", payload)

    # Build integrated sector heatmap (country buckets)
    # Aggregate market caps and cap-weighted pct by (country, sector)
    buckets = []
    for key, label, df_const in specs:
        country = key.split("-")[0].upper()
        df = df_const.set_index("ticker").join(pct).join(mcap)
        df = df.dropna(subset=["pct", "mcap"])
        if df.empty:
            continue
        df["country"] = country
        df["sector"] = df["sector"].replace({"": "(Unknown)"})
        buckets.append(df)

    if buckets:
        full = pd.concat(buckets)
        g = full.groupby(["country", "sector"], dropna=False)
        out_items = []
        for (country, sector), sub in g:
            m = float(sub["mcap"].sum())
            pct_w = float((sub["pct"] * sub["mcap"]).sum() / m) if m else 0.0
            out_items.append({
                "ticker": f"{country}-{sector}"[:64],
                "name": f"{country} {sector}",
                "sector": country,
                "pct": pct_w,
                "mcap_usd_b": m / 1e9,
            })

        payload = {
            "label": "통합 · 섹터 히트맵",
            "asOf": as_of,
            "source": "yfinance (pct+market cap), Wikipedia/CSV constituents",
            "items": out_items,
        }
        write_json(out_dir / "all-sectors.json", payload)


if __name__ == "__main__":
    main()
