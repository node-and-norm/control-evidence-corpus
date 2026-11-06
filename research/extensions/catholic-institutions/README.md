# Catholic Institutional AI Risk and Control Evidence Pilot

**Reading update 0.4.1-dev | Protocol 0.3.0 | AI disclosure 0.1.0**

This bounded CEC extension studies the evidence behind AI safeguards in pastoral assistance and Catholic education. The general CEC charter, schemas and independent empirical study remain unchanged. No institutional endorsement or independently validated safeguard finding is claimed.

## Read the current study

| Reader | Start here |
| :--- | :--- |
| Catholic leaders and general readers | [Visual study and roadmap](study-report.html), or the [disclosure-updated PDF](reading/NodeNorm_Study_v0_4_1.pdf) |
| Researchers and reviewers | [Self-contained Jupyter study](study-guide.ipynb), with offline results reconstruction and disclosure checks |
| Methodological scrutiny | [Protocol 0.3.0](PROTOCOL.md) and [browser-readable protocol](protocol.html), including the disclosure addendum |
| Source and theological scrutiny | [Scoping chapter](SCOPING.md), [18 provisional mappings](data/normative-crosswalk.json), and [captured source run](runs/SV-20261106-001/capture.json) |
| AI contributions and actual human review | [Study-specific disclosure](AI_DISCLOSURE.md), [contribution record](disclosure/record.json), and [guidance/access checks](disclosure/policy-checks.json) |

GitHub displays HTML source rather than a live webpage. Save the HTML and open it in a browser, or use the PDF. Generated current reading files and their disclosure manifest belong in `reading/`. A development snapshot records versions; it does not certify scientific validity, venue compliance or human review. Existing versioned releases must not be overwritten.

## Current evidence

Run SV-20261106-001 recorded two searches and two fetches without retries. The Antiqua et Nova target did not resolve by its returned identifier; the Magnifica Humanitas target returned paragraph 90 instead of 105. These two prior-informed checks provide no population reliability estimate or provider-defect attribution. The capture includes public metadata and explicit source-text omissions.

The 18 normative mappings remain subject to qualified independent review. Zero Catholic empirical cases have been admitted to CEC and no Catholic safeguard evaluation has been completed. The next gates are source clarification, qualified mapping review, and five scoped risk scenarios from a versioned upstream snapshot.

## AI assistance and human responsibility

Substantive AI assistance includes method proposals, source inspection, provisional interpretation, code, checks, diagrams and drafting. [The common disclosure](AI_DISCLOSURE.md) is generated from a single record across current readers. Author authorization, personal verification, independent review, theological review and submission approval have separate scopes. Specific checks must be recorded; no new human attestation is inferred.

The [October 27 guidance register](disclosure/historical-guidance-2026-10-27.json) preserves the user's historical wording and dates. [November 6 checks](disclosure/policy-checks.json) are separate and retain 403/redirect access limits. No venue is selected. The Cwik article is methodological context, not a compulsory standard. TAE's disclosure approach is reused without importing its model identities or approvals. See [implementation guidance](disclosure/README.md).

## Evidence and maintenance

The [evidence workbench](evidence-workbench/README.md) and [course alignment](evidence-workbench/course-alignment/README.md) remain supporting material. [Release inputs](release.json), [method amendment](METHOD_AMENDMENT.md), [decision record](DECISIONS.md), [change history](CHANGELOG.md), [disclosure change record](DISCLOSURE_CHANGELOG.md) and [release notes](RELEASE_NOTES.md) make the current state explicit. The unchanged [v0.2 package](archive/v0.2/README.md) preserves earlier bytes and supports historical checks.

From this directory, install `requirements-reading.txt` in an isolated environment and install Chromium for Playwright. Run `python scripts/build_release.py --execute --pdf --package`, then `python scripts/finalize_navigation.py`, then `python scripts/apply_ai_disclosure.py --execute --pdf --package`. Run `python scripts/test_release.py` and `python scripts/test_ai_disclosure.py`. The reading workflow performs those steps automatically. No research API calls occur. Generated outputs must accompany source changes; do not hand-edit them independently.

The PDF is a reading edition; the notebook embeds its versioned inputs and runs offline. Checksums establish byte correspondence, not truth or reviewer independence. The public export excludes credentials, sensitive institutional data and full source text with unresolved redistribution rights. The operator working copy has no established long-term archive custodian.

The root CEC README and Node & Norm website ingestion are preserved. Only this extension and its documentation/policy navigation change. Independent research and ecclesial-review gates remain open.
