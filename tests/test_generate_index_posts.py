import tempfile
import unittest
from datetime import date
from pathlib import Path

import pandas as pd

import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import scripts.generate_index_posts as gip


class GenerateIndexPostsTests(unittest.TestCase):
    def test_download_closes_normalizes_intraday_timestamps_to_date(self):
        original = gip._yahoo_chart_closes
        try:
            def fake_chart(ticker, start, end):
                return pd.Series(
                    [100.0, 101.0],
                    index=[pd.Timestamp("2026-06-15 13:30:00"), pd.Timestamp("2026-06-16 13:30:00")],
                    name=ticker,
                )

            gip._yahoo_chart_closes = fake_chart
            closes = gip.download_closes(["^GSPC"], date(2026, 6, 15), date(2026, 6, 16))

            self.assertIn(pd.Timestamp("2026-06-15"), closes.index)
            self.assertIn(pd.Timestamp("2026-06-16"), closes.index)
            self.assertNotIn(pd.Timestamp("2026-06-15 13:30:00"), closes.index)
        finally:
            gip._yahoo_chart_closes = original

    def test_heatmap_asset_date_falls_back_to_next_available_calendar_day(self):
        original_root = gip.ROOT
        with tempfile.TemporaryDirectory() as tmp:
            gip.ROOT = Path(tmp)
            try:
                img = Path(tmp) / "assets" / "img" / "heatmaps" / "2026-06-16" / "us-spx.png"
                img.parent.mkdir(parents=True)
                img.write_bytes(b"fake")

                found = gip.heatmap_asset_date(date(2026, 6, 15), "us-spx")

                self.assertEqual(found, "2026-06-16")
            finally:
                gip.ROOT = original_root

    def test_write_kr_post_skips_implausible_index_values(self):
        original_outdir = gip.OUTDIR
        with tempfile.TemporaryDirectory() as tmp:
            gip.OUTDIR = Path(tmp)
            try:
                idx = pd.Timestamp("2026-06-15")
                columns = pd.MultiIndex.from_product(
                    [["close", "delta", "pct"], ["^KS11", "^KQ11"]]
                )
                daily = pd.DataFrame(
                    [[8545.98, 1034.03, 422.36, 4.98, 5.20, 0.48]],
                    index=[idx],
                    columns=columns,
                )

                written = gip.write_kr_post(date(2026, 6, 15), daily, force=True)

                self.assertIsNone(written)
                self.assertFalse((Path(tmp) / "2026-06-15-korea.md").exists())
            finally:
                gip.OUTDIR = original_outdir


if __name__ == "__main__":
    unittest.main()
