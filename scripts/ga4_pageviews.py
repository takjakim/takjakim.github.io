#!/usr/bin/env python3
"""Fetch GA4 page views and write to _data/pageviews.json

Designed for GitHub Actions (daily cron).

Secrets expected:
- GA4_PROPERTY_ID: numeric GA4 property id
- GA4_SERVICE_ACCOUNT_JSON: service account JSON (as a single-line string)

Output schema (example):
{
  "meta": {"generated_at": "...", "range": "last_30_days"},
  "paths": {"/investing/2026-02-13-us/": {"views": 123}}
}
"""

import json
import os
from datetime import datetime, timezone


def main():
    prop = os.environ.get("GA4_PROPERTY_ID", "").strip()
    sa_json = os.environ.get("GA4_SERVICE_ACCOUNT_JSON", "").strip()
    out_path = os.environ.get("OUTPUT_PATH", "_data/pageviews.json")

    if not prop:
        raise SystemExit("Missing GA4_PROPERTY_ID")
    if not sa_json:
        raise SystemExit("Missing GA4_SERVICE_ACCOUNT_JSON")

    # Lazy import so local runs don't require the dependency unless used.
    from google.analytics.data_v1beta import BetaAnalyticsDataClient
    from google.analytics.data_v1beta.types import DateRange, Dimension, Metric, RunReportRequest
    from google.oauth2 import service_account

    creds_info = json.loads(sa_json)
    credentials = service_account.Credentials.from_service_account_info(
        creds_info,
        scopes=["https://www.googleapis.com/auth/analytics.readonly"],
    )

    client = BetaAnalyticsDataClient(credentials=credentials)

    # Use eventCount filtered to page_view for maximum compatibility.
    # (Some properties may not return screenPageViews depending on configuration.)
    from google.analytics.data_v1beta.types import FilterExpression, Filter, FilterExpressionList

    req = RunReportRequest(
        property=f"properties/{prop}",
        dimensions=[Dimension(name="pagePath")],
        metrics=[Metric(name="eventCount")],
        dimension_filter=FilterExpression(
            filter=Filter(
                field_name="eventName",
                string_filter=Filter.StringFilter(value="page_view", match_type=Filter.StringFilter.MatchType.EXACT),
            )
        ),
        # Include today so the counter isn't empty right after installation.
        date_ranges=[DateRange(start_date="30daysAgo", end_date="today")],
        limit=100000,
    )

    resp = client.run_report(req)

    paths = {}
    for row in resp.rows:
        path = row.dimension_values[0].value
        views = int(float(row.metric_values[0].value))
        # Normalize: ensure trailing slash for site paths
        if path and not path.endswith("/"):
            path = path + "/"
        paths[path] = {"views": views}

    payload = {
        "meta": {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "range": "last_30_days_including_today",
            "property_id": prop,
            "note": "GA4 Data API can lag hours; empty result right after install may be normal.",
        },
        "paths": paths,
    }

    # Safeguard: if GA4 returns 0 rows, keep previous non-empty data (avoid wiping UI).
    if len(paths) == 0 and os.path.exists(out_path):
        try:
            prev = json.load(open(out_path, "r", encoding="utf-8"))
            prev_paths = prev.get("paths", {}) if isinstance(prev, dict) else {}
            if isinstance(prev_paths, dict) and len(prev_paths) > 0:
                payload["paths"] = prev_paths
                payload["meta"]["note"] += " Kept previous snapshot because new result was empty."
        except Exception:
            pass

    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2, sort_keys=True)
        f.write("\n")

    print(f"Wrote {len(payload['paths'])} paths to {out_path}")


if __name__ == "__main__":
    main()
