# Separating Evidence Traceability from Model Comparability: A Case-Based Audit of Meta-KAN for Transformer Oil-Temperature Forecasting

**Pagidimarri Krishna**  
Independent Researcher, Hyderabad, India  
Corresponding author: pagidimarrikrishna1@gmail.com  
ORCID: [0009-0007-0352-0887](https://orcid.org/0009-0007-0352-0887)

### Citation

Manuscript prepared for consideration by ComputO. Publication details and DOI will be added if and when formally assigned.

### Project overview

This repository accompanies a retrospective, case-based study of the Evidence-Traceability and Comparability Protocol (ETCP), applied to a previously reported Meta-KAN study on transformer oil-temperature forecasting.

ETCP separates the evidence status of an individual research claim from the eligibility of two experimental results for direct comparison. The accompanying Python prototype processes structured claim and comparison records and produces inspectable audit outputs.

### Repository contents

- `etcp_audit.py` — audit implementation.
- `ETCP_File_9_run_audit.py` and `run_audit.py` — runner scripts. The intended canonical entry point and equivalence of these scripts should be verified before release.
- `ETCP_File_8_test_etcp_audit.py` and `test_etcp_audit.py` — test scripts. Their equivalence and execution status should be verified before release.
- `Claims.csv` and `claims.csv` — claim-related records. Their contents, capitalization, and possible duplication should be checked before release.
- `comparisons.csv` — experimental-comparison records.
- `environment.yml` — environment specification.
- `etcp_results.csv` and `etcp_comparison_results.csv` — recorded audit outputs; regeneration and consistency with the source records remain to be verified.
- `etcp_validation.txt` — recorded validation output; the results should be regenerated and checked before claiming successful execution.
- `main.qmd` and `references.bib` — article source and bibliography.
- Other repository files may contain supplementary configuration, checksums, tests, and documentation.

### Evidence and reproducibility limitations

The historical Meta-KAN metrics are documented in the preserved manuscript but have not been independently reproduced in this reassessment. Corrected LSTM records use a different experimental configuration and do not establish a controlled comparison with Meta-KAN.

The prototype evaluates supplied records; it does not independently verify all underlying experimental artifacts, establish inter-assessor reliability, or demonstrate that ETCP is a validated general-purpose standard. Software validation results must not be interpreted as reproduction of the forecasting experiments.

### Reproducibility

The repository provides source code, structured evidence records, an environment specification, tests, and recorded outputs. Before claiming full reproducibility, the code and tests must be run in a clean environment, generated outputs must be checked against the manuscript, and relevant source artifacts must be verified.

### Research integrity

Unresolved or conflicting evidence is explicitly identified rather than inferred. Historical metrics are distinguished from independently reproduced results, and direct model comparisons are permitted only when the relevant experimental conditions and provenance support them.

### License and publication status

The repository's licensing and publication metadata should reflect the actual selected license and the journal's formal publication status. No journal DOI or publication badge is claimed here.
