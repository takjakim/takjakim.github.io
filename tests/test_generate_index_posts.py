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
    def test_yahoo_chart_closes_keeps_intraday_timestamp_on_end_date(self):
        class FakeResponse:
            def raise_for_status(self):
                return None

            def json(self):
                return {
                    "chart": {
                        "result": [{
                            "timestamp": [1782135000],  # 2026-06-22 13:30:00 UTC
                            "indicators": {"quote": [{"close": [7472.79]}]},
                        }]
                    }
                }

        original_get = gip.requests.get
        try:
            gip.requests.get = lambda *args, **kwargs: FakeResponse()
            closes = gip._yahoo_chart_closes("^GSPC", date(2026, 6, 22), date(2026, 6, 22))

            self.assertIn(pd.Timestamp("2026-06-22"), closes.index)
            self.assertEqual(float(closes.loc[pd.Timestamp("2026-06-22")]), 7472.79)
        finally:
            gip.requests.get = original_get

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

    def test_download_closes_names_empty_vendor_series(self):
        original = gip._yahoo_chart_closes
        try:
            def fake_chart(ticker, start, end):
                return pd.Series(dtype=float)

            gip._yahoo_chart_closes = fake_chart
            closes = gip.download_closes(["KRW=X", "^TNX"], date(2026, 6, 15), date(2026, 6, 16))

            self.assertEqual(list(closes.columns), ["KRW=X", "^TNX"])
        finally:
            gip._yahoo_chart_closes = original

    def test_download_closes_collapses_duplicate_normalized_dates(self):
        original = gip._yahoo_chart_closes
        try:
            def fake_chart(ticker, start, end):
                return pd.Series(
                    [100.0, 101.0],
                    index=[pd.Timestamp("2026-06-15 00:30:00"), pd.Timestamp("2026-06-15 13:30:00")],
                    name=ticker,
                )

            gip._yahoo_chart_closes = fake_chart
            closes = gip.download_closes(["KRW=X"], date(2026, 6, 15), date(2026, 6, 16))

            self.assertEqual(len(closes.index), 1)
            self.assertEqual(float(closes.loc[pd.Timestamp("2026-06-15"), "KRW=X"]), 101.0)
        finally:
            gip._yahoo_chart_closes = original

    def test_compute_daily_uses_previous_non_null_close_per_column(self):
        closes = pd.DataFrame(
            {
                "^TNX": [4.487, None, 4.500],
                "KRW=X": [None, 1509.5, 1513.31],
            },
            index=[pd.Timestamp("2026-06-12"), pd.Timestamp("2026-06-14"), pd.Timestamp("2026-06-15")],
        )

        daily = gip.compute_daily(closes)

        self.assertAlmostEqual(float(daily.loc[pd.Timestamp("2026-06-15"), ("pct", "^TNX")]), (4.5 - 4.487) / 4.487 * 100)
        self.assertAlmostEqual(float(daily.loc[pd.Timestamp("2026-06-15"), ("pct", "KRW=X")]), (1513.31 - 1509.5) / 1509.5 * 100)

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

    def test_write_kr_post_accepts_2026_kospi_range(self):
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

                self.assertEqual(written, Path(tmp) / "2026-06-15-korea.md")
                self.assertTrue((Path(tmp) / "2026-06-15-korea.md").exists())

            finally:
                gip.OUTDIR = original_outdir

    def test_kr_next_session_checklist_uses_macro_and_theme_signals(self):
        idx = pd.Timestamp("2026-06-15")
        columns = pd.MultiIndex.from_product(
            [["close", "delta", "pct"], ["KRW=X", "^TNX", "DX-Y.NYB", "CL=F", "005930.KS", "000660.KS"]]
        )
        signal_daily = pd.DataFrame(
            [[
                1380.0, 4.5, 105.0, 76.0, 70000.0, 230000.0,
                -8.0, 0.1, -0.4, -5.0, 800.0, 8400.0,
                -0.6, 2.3, -0.4, -6.2, 1.2, 3.8,
            ]],
            index=[idx],
            columns=columns,
        )

        lines = gip.kr_next_session_checklist(date(2026, 6, 15), 5.20, 0.48, signal_daily)

        joined = "\n".join(lines)
        self.assertIn("원/달러", joined)
        self.assertIn("금리", joined)
        self.assertIn("반도체", joined)
        self.assertIn("SK하이닉스", joined)

    def test_write_kr_post_includes_next_session_checkpoints(self):
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
                text = written.read_text(encoding="utf-8")

                self.assertIn("## 3) 다음 거래일 체크포인트", text)
                self.assertIn("원/달러", text)
                self.assertIn("핵심 테마", text)
            finally:
                gip.OUTDIR = original_outdir

    def test_write_kr_post_skips_extreme_vendor_errors(self):
        original_outdir = gip.OUTDIR
        with tempfile.TemporaryDirectory() as tmp:
            gip.OUTDIR = Path(tmp)
            try:
                idx = pd.Timestamp("2026-06-15")
                columns = pd.MultiIndex.from_product(
                    [["close", "delta", "pct"], ["^KS11", "^KQ11"]]
                )
                daily = pd.DataFrame(
                    [[50000.0, 1034.03, 422.36, 4.98, 5.20, 0.48]],
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
