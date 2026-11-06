# Catholic Institutional AI Risk and Control Evidence Pilot

**Reading package 0.4.0-dev | Protocol 0.3.0 | Source-verification pilot initiated**

This bounded CEC extension studies the evidence behind AI safeguards in pastoral assistance and Catholic education. The general CEC charter, schemas and independent empirical study remain unchanged. No institutional endorsement or independently validated safeguard finding is claimed.

## Read the current study

| Reader | Start here |
| :--- | :--- |
| Catholic leaders and general readers | [Visual study and roadmap](study-report.html), or the [PDF reading copy](reading/NodeNorm_Study_v0_4_0.pdf) |
| Researchers and reviewers | [Self-contained Jupyter study](study-guide.ipynb), with offline results reconstruction |
| Methodological scrutiny | [Protocol 0.3.0](PROTOCOL.md) and [browser-readable protocol](protocol.html) |
| Source and theological scrutiny | [Scoping chapter](SCOPING.md), [18 provisional mappings](data/normative-crosswalk.json), and [captured source run](runs/SV-20261106-001/capture.json) |

GitHub displays HTML source rather than a live webpage. Save the HTML and open it in a browser, or use the PDF. The [development release](https://github.com/node-and-norm/control-evidence-corpus/releases/tag/catholic-pilot-v0.4.0-dev) supplies the five reading files and complete package. A release is a versioned development snapshot, not an empirical approval.

## Current evidence

Run SV-20261106-001 recorded two searches and two fetches without retries. The Antiqua et Nova target did not resolve by its returned identifier; the Magnifica Humanitas target returned paragraph 90 instead of 105. These two prior-informed checks provide no population reliability estimate or provider-defect attribution. The capture includes public metadata and explicit source-text omissions.

The 18 normative mappings remain subject to qualified independent review. Zero Catholic empirical cases have been admitted to CEC and no Catholic safeguard evaluation has been completed. The next gates are source clarification, qualified mapping review, and five scoped risk scenarios from a versioned upstream snapshot.

## Evidence and maintenance

The [evidence workbench](evidence-workbench/README.md) and [course alignment](evidence-workbench/course-alignment/README.md) remain supporting material. [Release inputs](release.json), [method amendment](METHOD_AMENDMENT.md), [decision record](DECISIONS.md), [change history](CHANGELOG.md), and [release notes](RELEASE_NOTES.md) make the current state explicit. The unchanged [v0.2 package](archive/v0.2/README.md) preserves earlier bytes and supports historical checks.

From this directory, install `requirements-reading.txt` in an isolated environment, install Chromium for Playwright, then run `python scripts/build_release.py --execute --pdf --package`. This regenerates the five reading files without research API calls. `scripts/build_study.py` delegates to that same builder. Run `python scripts/test_release.py` for integrity checks. Generated outputs must accompany their source update; do not hand-edit them independently.

The PDF is a reading edition; the notebook embeds its versioned inputs and runs offline. Checksums establish byte correspondence, not truth or reviewer independence. The public export excludes credentials, sensitive institutional data, and full source text with unresolved redistribution rights. The operator working copy has no established long-term archive custodian.

The root CEC README and Node & Norm website ingestion are preserved. Only this extension and its documentation navigation change. Independent research and ecclesial-review gates remain open.
