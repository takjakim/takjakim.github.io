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
# yfinance often rate-limits in GitHub Actions / CI. Prefer Yahoo chart endpoint via requests.
# import yfinance as yf

ROOT = Path(__file__).resolve().parents[1]
UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X)"}

STOOQ_BASE = "https://stooq.com/q/d/l/"


@dataclass
class IndexSpec:
    key: str
    label: str
    tickers: list[str]
    meta: dict


def wiki_tickers(url: str) -> pd.DataFrame:
    # pd.read_html on large pages can be surprisingly slow; constrain parsing.
    from io import StringIO

    html = requests.get(url, headers=UA, timeout=30).text
    # Use StringIO to avoid deprecation and match to reduce work.
    tables = pd.read_html(StringIO(html), match=r"(?i)(ticker|symbol)")
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

    t = df["ticker"].astype(str).str.strip()

    # Normalize HK tickers coming from Wikipedia like "SEHK: 5" -> "0005.HK"
    if path.name.startswith("hk_"):
        # extract digits
        dig = t.str.extract(r"(\d+)", expand=False)
        t = dig.fillna("")
        t = t.apply(lambda x: x.zfill(4) if x else x)
        t = t.where(t == "", t + ".HK")

    # Normalize Yahoo-style dot tickers for internal consistency
    t = t.str.replace(".", "-", regex=False)

    df["ticker"] = t
    df["name"] = df["name"].astype(str).str.strip()
    df["sector"] = df["sector"].astype(str).str.strip()
    df = df[df["ticker"].str.len() > 0]
    return df.drop_duplicates("ticker")


def fetch_prices_yf(tickers: list[str], start: str, end: str) -> pd.DataFrame:
    return yf.download(
        tickers=tickers,
        start=start,
        end=end,
        interval="1d",
        group_by="ticker",
        auto_adjust=False,
        threads=True,
        progress=False,
    )


def stooq_symbol(ticker: str) -> str:
    """Best-effort mapping from common tickers to Stooq symbols."""
    t = ticker.strip()
    # HK: 0700.HK -> 0700.hk
    if t.upper().endswith(".HK"):
        return t[:-3].lower() + ".hk"
    # China: 600519.SS / 300750.SZ -> 600519.cn
    if t.upper().endswith(".SS") or t.upper().endswith(".SZ"):
        return t[:-3].lower() + ".cn"
    # US default: aapl -> aapl.us
    return t.lower() + ".us"


def fetch_pct_change_stooq(tickers: list[str], as_of: str) -> pd.Series:
    """Compute pct change for each ticker on as_of using Stooq daily CSV.

    WARNING: This does 1 HTTP request per ticker and can be slow/fragile.
    Prefer yfinance batch when possible.
    """
    out = {}
    target = as_of

    sess = requests.Session()

    for t in tickers:
        sym = stooq_symbol(t)
        url = f"{STOOQ_BASE}?s={sym}&i=d"
        try:
            txt = sess.get(url, headers=UA, timeout=15).text
            if not txt.startswith("Date,"):
                continue
            lines = [ln for ln in txt.splitlines() if ln.strip()]
            prev_close = None
            cur_close = None
            for i in range(len(lines) - 1, 0, -1):
                parts = lines[i].split(",")
                if len(parts) < 5:
                    continue
                if parts[0] == target:
                    cur_close = float(parts[4])
                    p2 = lines[i - 1].split(",")
                    if len(p2) >= 5:
                        prev_close = float(p2[4])
                    break
            if cur_close is None or prev_close is None or prev_close <= 0:
                continue
            out[t] = (cur_close / prev_close - 1.0) * 100.0
        except Exception:
            continue

    return pd.Series(out, name="pct")


def fetch_pct_change_yahoo(tickers: list[str], as_of: str) -> pd.Series:
    """Compute pct change for each ticker on as_of using Yahoo public chart endpoint.

    This avoids yfinance and is more reliable in CI, but it is 1 request per ticker.
    We keep ticker counts capped upstream.
    """
    import requests

    target = pd.to_datetime(as_of)
    out = {}

    sess = requests.Session()

    def last_two_closes(t: str):
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{t}"
        params = {"interval": "1d", "range": "14d"}
        r = sess.get(url, params=params, headers=UA, timeout=8)
        if r.status_code == 429:
            raise RuntimeError("rate_limited")
        r.raise_for_status()
        j = r.json()
        result = (((j or {}).get("chart") or {}).get("result") or [None])[0]
        if not result:
            return None
        ts = result.get("timestamp") or []
        quote = (((result.get("indicators") or {}).get("quote") or [None])[0]) or {}
        closes = quote.get("close") or []
        rows = []
        for tt, c in zip(ts, closes):
            if c is None:
                continue
            d = pd.to_datetime(int(tt), unit="s").tz_localize(None)
            rows.append((d, float(c)))
        if len(rows) < 2:
            return None
        rows.sort(key=lambda x: x[0])
        rows = [rc for rc in rows if rc[0] <= target]
        if len(rows) < 2:
            return None
        return rows[-1], rows[-2]

    for t in tickers:
        try:
            r = last_two_closes(t)
            if r is None:
                continue
            (d_last, last_close), (d_prev, prev_close) = r
            if prev_close <= 0:
                continue
            out[t] = (last_close / prev_close - 1.0) * 100.0
            # Avoid slow runs in cron/CI; if we get rate-limited we fall back to Stooq anyway.
        except Exception:
            continue

    return pd.Series(out, name="pct")


def fetch_market_caps_cached(tickers: list[str]) -> pd.Series:
    """Market-cap cache (USD).

    Free sources rate-limit quickly. We'll keep a cached file and update it separately.
    If missing, fall back to 1 so heatmap still renders (sizes become roughly uniform).
    """
    cache_path = ROOT / "data" / "mcap_cache.json"
    cache = {}
    if cache_path.exists():
        try:
            cache = json.loads(cache_path.read_text(encoding="utf-8"))
        except Exception:
            cache = {}

    out = {}
    for t in tickers:
        v = cache.get(t)
        if v is None:
            continue
        try:
            out[t] = float(v)
        except Exception:
            continue
    return pd.Series(out, name="mcap")


def build_payload(label: str, df_const: pd.DataFrame, pct: pd.Series, mcap: pd.Series, as_of: str, source: str):
    df = df_const.set_index("ticker").join(pct).join(mcap)
    # Keep items even if pct is missing (treat as 0) so the heatmap always renders.
    df["pct"] = df["pct"].fillna(0.0)

    if "mcap" in df.columns:
        # If we don't have market caps, use a neutral default so treemap still renders.
        # 1e9 => 1B USD-sized tiles (uniform).
        df["mcap"] = df["mcap"].fillna(1e9)
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
    import argparse

    ap = argparse.ArgumentParser()
    ap.add_argument("--date", help="as-of date (YYYY-MM-DD)")
    args = ap.parse_args()

    as_of = args.date or dt.datetime.now().strftime("%Y-%m-%d")
    out_dir = ROOT / "assets" / "data" / "heatmaps" / as_of
    out_dir.mkdir(parents=True, exist_ok=True)

    # fetch window: include previous trading day
    start = (pd.to_datetime(as_of) - pd.Timedelta(days=14)).strftime("%Y-%m-%d")
    end = (pd.to_datetime(as_of) + pd.Timedelta(days=2)).strftime("%Y-%m-%d")

    specs: list[tuple[str, str, pd.DataFrame]] = []

    # US
    # NOTE: yfinance can rate-limit (429 / connection resets) when requesting too many tickers.
    # Keep SPX capped by default for reliability on free endpoints.
    ndx_df = wiki_tickers("https://en.wikipedia.org/wiki/Nasdaq-100")
    spx_df = wiki_tickers("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies")

    os = __import__("os")
    MAX_NDX = int(os.environ.get("MAX_NDX", "40"))
    MAX_SPX = int(os.environ.get("MAX_SPX", "40"))

    if len(ndx_df) > MAX_NDX:
        ndx_df = ndx_df.head(MAX_NDX)
    if len(spx_df) > MAX_SPX:
        spx_df = spx_df.head(MAX_SPX)

    specs.append(("us-ndx", f"US · NASDAQ 100 (sample {len(ndx_df)})", ndx_df))
    specs.append(("us-spx", f"US · S&P 500 (sample {len(spx_df)})", spx_df))

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

    # Daily % change: use Yahoo public chart endpoint (more reliable in CI than yfinance).
    pct = fetch_pct_change_yahoo(all_tickers, as_of=as_of)
    if pct.empty:
        # Fallback: Stooq per-ticker.
        pct = fetch_pct_change_stooq(all_tickers, as_of=as_of)
    if pct.empty:
        # Last resort: neutral colors.
        pct = pd.Series({t: 0.0 for t in all_tickers}, name="pct")

    # Market cap via local cache (optional). If missing, fill with 1 (uniform size).
    mcap = fetch_market_caps_cached(all_tickers)
    if mcap.empty:
        mcap = pd.Series({t: 1e9 for t in all_tickers}, name="mcap")

    # Write index payloads
    source = "Stooq (daily % change) + local mcap cache (if available); constituents via Wikipedia/CSV"
    for key, label, df_const in specs:
        # join requires mcap for sizing; ensure fill
        payload = build_payload(label, df_const, pct, mcap, as_of, source=source)
        write_json(out_dir / f"{key}.json", payload)

    # Build integrated sector heatmap (country buckets)
    # Aggregate market caps and cap-weighted pct by (country, sector)
    buckets = []
    for key, label, df_const in specs:
        country = key.split("-")[0].upper()
        df = df_const.set_index("ticker").join(pct).join(mcap)
        # Keep rows even if pct is missing; treat as 0 so integrated heatmap stays renderable.
        df["pct"] = df["pct"].fillna(0.0)
        if "mcap" in df.columns:
            df["mcap"] = df["mcap"].fillna(1.0)
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
            "source": "Yahoo chart (pct) + Wikipedia/CSV constituents",
            "items": out_items,
        }
        write_json(out_dir / "all-sectors.json", payload)


if __name__ == "__main__":
    main()
