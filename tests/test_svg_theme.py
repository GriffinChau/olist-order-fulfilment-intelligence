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
