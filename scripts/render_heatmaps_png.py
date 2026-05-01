#!/usr/bin/env python3
"""Render static heatmap images (PNG) from generated JSON.

Inputs:
  assets/data/heatmaps/YYYY-MM-DD/{key}.json

Outputs:
  assets/img/heatmaps/YYYY-MM-DD/{key}.png

This is intended to run in GitHub Actions so mobile Safari doesn't need Plotly.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd

# plotly + kaleido are optional runtime deps; required in CI
import plotly.graph_objects as go

ROOT = Path(__file__).resolve().parents[1]


def load_items(json_path: Path) -> tuple[str, list[dict]]:
    obj = json.loads(json_path.read_text(encoding="utf-8"))
    label = obj.get("label") or obj.get("title") or json_path.stem

    if "items" in obj and isinstance(obj["items"], list):
        # current schema
        items = obj["items"]
        return label, items

    # legacy schema (labels/parents/values/changes) can't be reliably re-grouped by sector.
    # We'll convert leaves only if possible.
    raise RuntimeError(f"Unsupported heatmap schema in {json_path}")


def build_treemap(label: str, items: list[dict]) -> go.Figure:
    df = pd.DataFrame(items)
    if df.empty:
        raise RuntimeError("No items")

    # Normalize
    df["sector"] = df.get("sector", "Other").fillna("Other").astype(str)
    df["ticker"] = df.get("ticker", "N/A").fillna("N/A").astype(str)
    df["pct"] = pd.to_numeric(df.get("pct", 0), errors="coerce").fillna(0.0)
    # mcap_usd_b used as size; fallback to 1.0
    df["mcap_usd_b"] = pd.to_numeric(df.get("mcap_usd_b", 1), errors="coerce").fillna(1.0)
    df.loc[df["mcap_usd_b"] <= 0, "mcap_usd_b"] = 1.0

    root_id = "root"
    sectors = sorted(df["sector"].unique().tolist())

    ids: list[str] = [root_id]
    labels: list[str] = [label]
    parents: list[str] = [""]
    values: list[float] = [0.0]
    colors: list[float] = [0.0]

    # sectors
    sector_ids = {}
    for s in sectors:
        sid = f"sector:{s}"
        sector_ids[s] = sid
        ids.append(sid)
        labels.append(s)
        parents.append(root_id)
        # sector value = sum mcap
        sub = df[df["sector"] == s]
        m = float(sub["mcap_usd_b"].sum())
        w = float((sub["pct"] * sub["mcap_usd_b"]).sum() / m) if m else 0.0
        values.append(m)
        colors.append(w)
        values[0] += m

    # leaves
    for r in df.itertuples(index=False):
        tid = f"leaf:{r.sector}:{r.ticker}"
        ids.append(tid)
        labels.append(r.ticker)
        parents.append(sector_ids.get(r.sector, root_id))
        values.append(float(r.mcap_usd_b))
        colors.append(float(r.pct))

    fig = go.Figure(
        go.Treemap(
            ids=ids,
            labels=labels,
            parents=parents,
            values=values,
            branchvalues="total",
            marker=dict(
                colors=colors,
                colorscale=[
                    [0, "#dc2626"],
                    [0.35, "#f87171"],
                    [0.5, "#f5f5f5"],
                    [0.65, "#4ade80"],
                    [1, "#16a34a"],
                ],
                cmid=0,
                cmin=-5,
                cmax=5,
                showscale=True,
                colorbar=dict(title="등락률 (%)", ticksuffix="%"),
            ),
            customdata=colors,
            texttemplate="<b>%{label}</b><br>%{customdata:+.1f}%",
            hovertemplate="<b>%{label}</b><br>등락률: %{customdata:+.2f}%<extra></extra>",
        )
    )

    fig.update_layout(
        margin=dict(t=30, l=5, r=5, b=5),
        paper_bgcolor="white",
        plot_bgcolor="white",
        title=dict(text=label, font=dict(size=14)),
    )
    return fig


def render_one(date_str: str, key: str | None = None):
    in_dir = ROOT / "assets" / "data" / "heatmaps" / date_str
    out_dir = ROOT / "assets" / "img" / "heatmaps" / date_str
    out_dir.mkdir(parents=True, exist_ok=True)

    paths = sorted(in_dir.glob("*.json"))
    if key:
        paths = [in_dir / f"{key}.json"]

    for jp in paths:
        if not jp.exists():
            continue
        label, items = load_items(jp)
        fig = build_treemap(label, items)
        png_path = out_dir / f"{jp.stem}.png"
        fig.write_image(str(png_path), width=900, height=520, scale=2)
        print("wrote", png_path.relative_to(ROOT))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", required=True, help="YYYY-MM-DD")
    ap.add_argument("--key", help="heatmap key, e.g. us-spx")
    args = ap.parse_args()

    render_one(args.date, args.key)


if __name__ == "__main__":
    main()
