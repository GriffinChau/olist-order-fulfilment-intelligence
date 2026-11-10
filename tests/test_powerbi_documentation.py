"""Validate published Power BI implementation notes without requiring Desktop."""
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs" / "powerbi"


class PowerBIDocumentationTests(unittest.TestCase):
    def test_measure_catalog_and_page_bindings(self):
        dax = (DOCS / "measures.dax").read_text(encoding="utf-8")
        names = set(re.findall(r"^'(Fact[A-Za-z]+)'\[([^\]]+)\] =\s*$", dax, re.M))
        self.assertEqual(len(names), 56, "Expected 56 distinct documented measures")
        self.assertEqual(
            {table for table, _ in names},
            {"FactMonthly", "FactRegion", "FactReviews", "FactCategory", "FactKpi"},
        )
        manifest = json.loads((DOCS / "page_manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["model"]["tables"], 9)
        self.assertEqual(manifest["model"]["relationships"], 4)
        self.assertEqual(manifest["model"]["measures"], 56)
        self.assertEqual(len(manifest["pages"]), 4)
        for page in manifest["pages"]:
            with self.subTest(page=page["title"]):
                self.assertEqual((page["canvas"]["width"], page["canvas"]["height"]), (1600, 900))
                self.assertEqual(len(page["cards"]), 4)
                self.assertEqual(len(page["charts"]), 2)
                for visual in page["cards"] + page["charts"]:
                    table, measure = visual["measure"].split(".", 1)
                    self.assertIn((table, measure), names)
                self.assertTrue(page["template_image"].endswith(".png"))

    def test_schema_and_theme_are_present(self):
        relation_text = (DOCS / "relationships.tmdl").read_text(encoding="utf-8")
        self.assertEqual(len(re.findall(r"^relationship\s", relation_text, re.M)), 4)
        for pair in (
            "FactMonthly.month", "DimMonth.month",
            "FactRegion.state", "DimState.state",
            "FactReviews.delivery_outcome", "DimDeliveryOutcome.delivery_outcome",
            "FactCategory.category", "DimCategory.category",
        ):
            self.assertIn(pair, relation_text)
        theme = json.loads((DOCS / "theme.json").read_text(encoding="utf-8"))
        self.assertEqual(theme["background"], "#F2F8F5")
        self.assertGreaterEqual(len(theme["dataColors"]), 4)

    def test_private_power_bi_project_not_in_documentation(self):
        for p in DOCS.rglob("*"):
            self.assertNotIn(p.suffix.lower(), {".pbix", ".pbip", ".pbir"})
        for name in ("README.md", "semantic_model.md", "kpi_dictionary.md", "report_pages.md"):
            self.assertTrue((DOCS / name).is_file(), name)


if __name__ == "__main__":
    unittest.main()
