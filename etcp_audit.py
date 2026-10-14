#!/usr/bin/env python3
"""Small deterministic proof of concept for ETCP.

This script classifies supplied records. It does not inspect source artifacts,
reproduce forecasting metrics, or validate ETCP as a general scientific standard.
Requires Python 3.10+ and pandas.
"""
from pathlib import Path
import hashlib
import platform
import sys
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent if (Path(__file__).resolve().parent.parent / "data").exists() else Path(__file__).resolve().parent
DATA = ROOT / "data" if (ROOT / "data").exists() else ROOT

def classify_claim(row):
    status = str(row["evidence_status"]).strip()
    if status not in {"D", "A", "R", "U", "X"}:
        raise ValueError(f"Invalid evidence status for {row['claim_id']}: {status}")
    return status

def classify_comparison(row):
    # Conservative deterministic rules: a known task-contract mismatch blocks direct comparison.
    if int(row["feature_count_a"]) != int(row["feature_count_b"]):
        return "ineligible"
    if int(row["horizon_a"]) != int(row["horizon_b"]):
        return "ineligible"
    if row["target_alignment"] != "same":
        return "ineligible"
    if row["preprocessing_alignment"] != "same":
        return "ineligible"
    if row["provenance"] != "complete":
        return "conditional"
    return "eligible"

def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def main():
    claims_in = pd.read_csv(DATA / "claims.csv", dtype=str).fillna("")
    comps_in = pd.read_csv(DATA / "comparisons.csv", dtype=str).fillna("")
    claims_out = claims_in.copy()
    claims_out["computed_status"] = claims_out.apply(classify_claim, axis=1)
    claims_out["rationale_generated"] = claims_out["evidence_status"].map({
        "D": "Documented in the identified source; not independently reproduced by this script.",
        "A": "Artifact-level record was reported in the supplied register; the script does not inspect the source artifact.",
        "R": "Marked as independently reproduced in the supplied register; this script does not independently reproduce the underlying result.",
        "U": "Material evidence remains unresolved in the supplied register.",
        "X": "The supplied register does not support the claim as stated."
    })
    comps_out = comps_in.copy()
    comps_out["computed_decision"] = comps_out.apply(classify_comparison, axis=1)
    comps_out["validation"] = comps_out.apply(
        lambda r: "PASS" if r["computed_decision"] == r["expected_decision"] else "FAIL", axis=1
    )
    claims_out.to_csv(ROOT / "etcp_results.csv", index=False)
    comps_out.to_csv(ROOT / "etcp_comparison_results.csv", index=False)

    checks = []
    checks.append(("claim_rows_preserved", len(claims_in) == len(claims_out)))
    checks.append(("comparison_rows_preserved", len(comps_in) == len(comps_out)))
    checks.append(("historical_vs_corrected_ineligible", comps_out.loc[comps_out.comparison_id == "P01", "computed_decision"].iloc[0] == "ineligible"))
    checks.append(("aligned_toy_pair_eligible", comps_out.loc[comps_out.comparison_id == "P04", "computed_decision"].iloc[0] == "eligible"))
    checks.append(("toy_horizon_mismatch_ineligible", comps_out.loc[comps_out.comparison_id == "P05", "computed_decision"].iloc[0] == "ineligible"))
    checks.append(("all_expected_decisions_match", bool((comps_out["validation"] == "PASS").all())))

    lines = [
        "ETCP proof-of-concept validation report",
        f"Python: {platform.python_version()}",
        f"pandas: {pd.__version__}",
        f"Claim rows: {len(claims_in)}",
        f"Comparison rows: {len(comps_in)}",
        ""
    ]
    for name, passed in checks:
        lines.append(f"{name}: {'PASS' if passed else 'FAIL'}")
    lines.append("")
    lines.append(f"Checks passed: {sum(ok for _, ok in checks)}/{len(checks)}")
    lines.append("Scope: software behavior on supplied records only; no model training or scientific validation.")
    (ROOT / "etcp_validation.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    (ROOT / "environment.txt").write_text(
        f"Python {platform.python_version()}\npandas {pd.__version__}\n"
        f"Platform {platform.platform()}\nNo network access required.\n", encoding="utf-8"
    )
    if not all(ok for _, ok in checks):
        raise SystemExit("One or more validation checks failed.")
    print("\n".join(lines))

if __name__ == "__main__":
    main()
