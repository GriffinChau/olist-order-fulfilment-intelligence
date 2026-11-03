"""Portfolio presentation regression checks: one main visual, no broken references."""
import re
import unittest
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
EXECUTIVE=ROOT/"evidence/executive_summary.svg"
WORKBOOK=ROOT/"workbook/Olist_Order_Fulfilment_Intelligence_Real_Data.xlsx"

class TestPortfolioPresentation(unittest.TestCase):
    def test_main_readme_uses_one_unified_visual(self):
        text=(ROOT/"README.md").read_text(encoding="utf-8")
        embeds=re.findall(r"!\[[^\]]*\]\(([^)]+)\)",text)
        self.assertEqual(embeds,["evidence/executive_summary.svg"])
        self.assertTrue(EXECUTIVE.is_file())
    def test_no_repeated_embeds_in_supporting_briefs(self):
        for path in ("docs/05_findings.md","docs/09_management_brief.md",
                     "docs/10_delivery_performance_findings.md","evidence/README.md"):
            with self.subTest(document=path):
                text=(ROOT/path).read_text(encoding="utf-8")
                self.assertNotRegex(text,r"!\[[^\]]*\]\([^)]+\)")
    def test_revised_visuals_are_valid_xml(self):
        for p in ("evidence/executive_summary.svg","evidence/customer_delivery_by_region.svg",
                  "evidence/freight_category_analysis.svg"):
            with self.subTest(image=p):
                root=ET.parse(ROOT/p).getroot()
                self.assertTrue(root.tag.endswith("svg"))
                self.assertIn("viewBox",root.attrib)
    def test_current_full_data_workbook_exists(self):
        self.assertTrue(WORKBOOK.is_file())
        with zipfile.ZipFile(WORKBOOK) as z:
            self.assertIsNone(z.testzip())
            sheets=[p for p in z.namelist() if p.startswith("xl/worksheets/sheet") and p.endswith(".xml")]
            self.assertGreaterEqual(len(sheets),16)

if __name__=="__main__":
    unittest.main()
