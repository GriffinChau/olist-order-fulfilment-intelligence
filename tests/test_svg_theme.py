"""Keep the published SVG figures consistent with the Olist report theme."""
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NAMES = (
    "analysis_to_action",
    "customer_delivery_by_region",
    "customer_delivery_performance",
    "dashboard_overview",
    "delivery_and_reviews",
    "executive_summary",
    "freight_category_analysis",
    "seller_state_concentration",
    "top_seller_cities",
)


class TestPublishedSvgTheme(unittest.TestCase):
    def test_all_nine_svg_files_render_as_xml_and_use_the_green_report_theme(self):
        files = sorted((ROOT / "evidence").glob("*.svg"))
        self.assertEqual([p.stem for p in files], sorted(NAMES))
        for file in files:
            with self.subTest(file=file.name):
                root = ET.parse(file).getroot()
                self.assertEqual(root.attrib.get("viewBox"), "0 0 1440 1020")
                self.assertEqual(root.tag, "{http://www.w3.org/2000/svg}svg")
                source = file.read_text(encoding="utf-8")
                self.assertIn("OLIST", source)
                self.assertIn("#02473F", source)
                self.assertIn("#D9854C", source)
                self.assertNotIn("Pending data", source)
                self.assertNotIn("STATIC PDF PREVIEW", source)
                self.assertNotIn("No interactive slicers", source)

    def test_monthly_line_charts_use_exactly_20_cohorts_inside_plot(self):
        import csv
        with (ROOT / "data/processed/monthly_metrics.csv").open(newline="", encoding="utf-8") as f:
            metrics = {row["month"]: row for row in csv.DictReader(f)}

        cohort_months = [f"2017-{month:02d}" for month in range(1, 13)] + [
            f"2018-{month:02d}" for month in range(1, 9)
        ]
        self.assertEqual(len(cohort_months), 20)
        self.assertEqual(metrics["2018-03"]["on_time_delivery_pct"], "81.04")
        self.assertEqual(metrics["2018-08"]["on_time_delivery_pct"], "93.81")

        svg_ns = "{http://www.w3.org/2000/svg}"
        charts = {
            "executive_summary": (306, 771, 419, 570, "590"),
            "customer_delivery_performance": (326, 775, 440, 656, "676"),
        }
        ticks = ["17/01", "17/04", "17/07", "17/10",
                 "18/01", "18/03", "18/06", "18/08"]
        for name, (x0, x1, top, bottom, tick_y) in charts.items():
            with self.subTest(chart=name):
                root = ET.parse(ROOT / "evidence" / (name + ".svg")).getroot()
                lines = [
                    el for el in root.iter(svg_ns + "polyline")
                    if el.attrib.get("clip-path") == "url(#monthlyPlotClip)"
                ]
                self.assertEqual(len(lines), 1)
                points = [
                    tuple(float(v) for v in xy.split(","))
                    for xy in lines[0].attrib["points"].split()
                ]
                self.assertEqual(len(points), 20)
                for i, (x, y) in enumerate(points):
                    expected_x = x0 + i * (x1 - x0) / 19
                    rate = float(metrics[cohort_months[i]]["on_time_delivery_pct"])
                    expected_y = bottom - (rate - 78) / 22 * (bottom - top)
                    self.assertAlmostEqual(x, expected_x, delta=0.06)
                    self.assertAlmostEqual(y, expected_y, delta=0.06)
                    self.assertGreaterEqual(y, top)
                    self.assertLessEqual(y, bottom)
                self.assertAlmostEqual(points[-1][0], x1, delta=0.01)
                self.assertAlmostEqual(points[14][1],
                                       bottom - (81.04 - 78) / 22 * (bottom - top),
                                       delta=0.06)
                tick_labels = [
                    node.text for node in root.iter(svg_ns + "text")
                    if node.attrib.get("y") == tick_y
                ]
                self.assertEqual(tick_labels, ticks)

        # The second chart also needs Sep 2017 through Aug 2018,
        # not Oct 2017 through an empty Sep 2018 placeholder.
        root = ET.parse(
            ROOT / "evidence/customer_delivery_performance.svg"
        ).getroot()
        bars = [
            node for node in root.iter(svg_ns + "rect")
            if node.attrib.get("clip-path") == "url(#latePlotClip)"
        ]
        self.assertEqual(len(bars), 12)
        late_months = cohort_months[8:]
        for bar, month in zip(bars, late_months):
            expected_height = (float(metrics[month]["late_deliveries"]) / 1500) * 220
            self.assertAlmostEqual(float(bar.attrib["height"]),
                                   expected_height, delta=0.06)
            self.assertGreater(float(bar.attrib["height"]), 0)
        self.assertEqual(bars[6].attrib["fill"], "#D9854C")

    def test_critical_published_metrics_remain_visible(self):
        for name, expected in {
            "executive_summary": ("99,441", "93.23%", "6,534", "81.04%"),
            "customer_delivery_by_region": ("96,470", "95.51%", "87.89%"),
            "customer_delivery_performance": ("96,470", "1,328", "81.04%"),
            "delivery_and_reviews": ("4.29 / 5", "2.27 / 5", "62.36%"),
            "freight_category_analysis": ("13.59M", "2.26M", "112,650"),
            "seller_state_concentration": ("3,095", "1,849"),
            "top_seller_cities": ("694", "1,254"),
            "dashboard_overview": ("99,441", "93.23%"),
            "analysis_to_action": ("99,441", "96,470", "93.23%"),
        }.items():
            text = (ROOT / "evidence" / (name + ".svg")).read_text(encoding="utf-8")
            for value in expected:
                with self.subTest(file=name, value=value):
                    self.assertIn(value, text)


if __name__ == "__main__":
    unittest.main()
