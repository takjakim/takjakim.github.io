#!/usr/bin/env python3
"""Bootstrap (one-time) constituents lists into data/constituents/*.csv.

Goal: free + relatively stable by pinning constituents into the repo.
- US indices (NDX/SPX) are derived daily from Wikipedia in the generator.
- CN/HK indices are bootstrapped here and then treated as static until you update.

Outputs (CSV columns): ticker,name,sector
"""

import csv
import sys
from pathlib import Path

import pandas as pd
import requests

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "data" / "constituents"
OUT_DIR.mkdir(parents=True, exist_ok=True)

UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X)"}


def write_csv(path: Path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["ticker", "name", "sector"])
        w.writeheader()
        for r in rows:
            w.writerow(r)


def scrape_wikipedia_table(url: str, ticker_col_hint=("Ticker", "Symbol"), name_col_hint=("Company", "Name"), sector_col_hint=("Industry", "Sector")):
    html = requests.get(url, headers=UA, timeout=30).text
    tables = pd.read_html(html)

    def pick_col(cols, hints):
        low = {c: str(c).lower() for c in cols}
        for h in hints:
            hl = h.lower()
            for c, cl in low.items():
                if hl == cl or hl in cl:
                    return c
        return None

    # Find a table that has a ticker-like column
    target = None
    tcol = None
    for t in tables:
        cols = list(t.columns)
        c = pick_col(cols, ticker_col_hint)
        if c is not None:
            target = t
            tcol = c
            break

    if target is None:
        raise RuntimeError(f"Could not find ticker table on {url}")

    ncol = pick_col(list(target.columns), name_col_hint)
    scol = pick_col(list(target.columns), sector_col_hint)

    rows = []
    for _, r in target.iterrows():
        ticker = str(r[tcol]).strip()
        if not ticker or ticker.lower() == "nan":
            continue
        # Normalize for Yahoo: BRK.B -> BRK-B
        ticker_yf = ticker.replace(".", "-")
        name = str(r[ncol]).strip() if ncol is not None else ticker
        sector = str(r[scol]).strip() if scol is not None else ""
        rows.append({"ticker": ticker_yf, "name": name, "sector": sector})

    # de-dupe
    seen = set()
    out = []
    for x in rows:
        if x["ticker"] in seen:
            continue
        out.append(x)
        seen.add(x["ticker"])
    return out


def main():
    # HK: Hang Seng Index constituents (Wikipedia has a constituents section)
    hsi_out = OUT_DIR / "hk_hsi.csv"
    if not hsi_out.exists():
        # This page typically includes a table of constituents.
        hsi_url = "https://en.wikipedia.org/wiki/Hang_Seng_Index"
        rows = scrape_wikipedia_table(hsi_url)
        write_csv(hsi_out, rows)
        print(f"Wrote {hsi_out} ({len(rows)} rows)")
    else:
        print(f"Skip (exists): {hsi_out}")

    # HK: Hang Seng Tech Index constituents
    hstech_out = OUT_DIR / "hk_hstech.csv"
    if not hstech_out.exists():
        hstech_url = "https://en.wikipedia.org/wiki/Hang_Seng_Tech_Index"
        rows = scrape_wikipedia_table(hstech_url)
        write_csv(hstech_out, rows)
        print(f"Wrote {hstech_out} ({len(rows)} rows)")
    else:
        print(f"Skip (exists): {hstech_out}")

    # CN: CSI 300 constituents
    csi_out = OUT_DIR / "cn_csi300.csv"
    if not csi_out.exists():
        # Free+stable constituents list is hard to source without an API.
        # Best-effort: try Wikipedia if it ever has a table; otherwise fail with instructions.
        csi_url = "https://en.wikipedia.org/wiki/CSI_300_Index"
        try:
            rows = scrape_wikipedia_table(csi_url)
        except Exception:
            rows = []
        if not rows:
            raise SystemExit(
                "Could not bootstrap CSI300 constituents from Wikipedia.\n"
                "Option A) provide a CSV list (ticker,name,sector) for CSI300, or\n"
                "Option B) allow using an API/free-tier source for CSI300.\n"
                f"Expected output path: {csi_out}"
            )
        write_csv(csi_out, rows)
        print(f"Wrote {csi_out} ({len(rows)} rows)")
    else:
        print(f"Skip (exists): {csi_out}")


if __name__ == "__main__":
    main()
