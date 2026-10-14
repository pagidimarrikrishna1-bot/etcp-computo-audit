#!/usr/bin/env python3
"""Regression tests for the ETCP proof-of-concept audit rules.

Run from the repository root with:
    python -m unittest -v test_etcp_audit.py

These tests verify deterministic software behavior on supplied records only.
They do not validate ETCP as a general scientific standard or reproduce model results.
"""
import unittest
from pathlib import Path
import sys
import pandas as pd

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
import etcp_audit  # noqa: E402


class TestETCPAudit(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.claims = pd.read_csv(ROOT / "claims.csv", dtype=str).fillna("")
        cls.comparisons = pd.read_csv(ROOT / "comparisons.csv", dtype=str).fillna("")

    def test_claim_rows_preserved(self):
        self.assertEqual(len(self.claims), 8)

    def test_comparison_rows_preserved(self):
        self.assertEqual(len(self.comparisons), 5)

    def test_historical_and_corrected_tasks_are_ineligible(self):
        row = self.comparisons.loc[self.comparisons.comparison_id == "P01"].iloc[0]
        self.assertEqual(etcp_audit.classify_comparison(row), "ineligible")

    def test_aligned_toy_pair_is_eligible(self):
        row = self.comparisons.loc[self.comparisons.comparison_id == "P04"].iloc[0]
        self.assertEqual(etcp_audit.classify_comparison(row), "eligible")

    def test_horizon_mismatch_is_ineligible(self):
        row = self.comparisons.loc[self.comparisons.comparison_id == "P05"].iloc[0]
        self.assertEqual(etcp_audit.classify_comparison(row), "ineligible")

    def test_partial_provenance_is_conditional(self):
        row = self.comparisons.loc[self.comparisons.comparison_id == "P02"].iloc[0]
        self.assertEqual(etcp_audit.classify_comparison(row), "conditional")

    def test_all_expected_decisions_match(self):
        actual = self.comparisons.apply(etcp_audit.classify_comparison, axis=1).tolist()
        expected = self.comparisons["expected_decision"].tolist()
        self.assertEqual(actual, expected)

    def test_invalid_claim_status_raises(self):
        row = self.claims.iloc[0].copy()
        row["evidence_status"] = "INVALID"
        with self.assertRaises(ValueError):
            etcp_audit.classify_claim(row)


if __name__ == "__main__":
    unittest.main()
