> **Notebook reading home:** [Open the Catholic pilot book](../../../CATHOLIC_PILOT.ipynb). The files below remain the historical source and evidence workspace.

# Catholic Institutional AI Risk and Control Evidence Pilot

**Latest complete draft: 0.4.4-draft | Published reading release: 0.4.1-dev | Core protocol: 0.3.0, unfrozen**

This bounded CEC extension studies the evidence behind AI safeguards in pastoral assistance and Catholic education. The general CEC charter, schemas and independent empirical study remain unchanged. No institutional endorsement or independently validated safeguard finding is claimed.

**[Start here: study readers, research notebooks and version archive](reading/README.md).** This entry point links the complete current draft to its evidence, limitations and earlier editions. The root repository README and its visual theme remain unchanged.

## Read the current draft

| Reader | Start here |
| :--- | :--- |
| Researchers and reviewers | [Complete 0.4.4 Jupyter study](reading/editions/0.4.4-draft/NodeNorm_Notebook_v0_4_4.ipynb), with retained outputs and offline replay |
| Catholic leaders and general readers | [Visual study and roadmap](reading/editions/0.4.4-draft/NodeNorm_Study_v0_4_4.html), or [PDF reading copy](reading/editions/0.4.4-draft/NodeNorm_Study_v0_4_4.pdf) |
| Methodological scrutiny | [Protocol with dated annexes](reading/editions/0.4.4-draft/NodeNorm_Protocol_v0_4_4.md) and [browser-readable edition](reading/editions/0.4.4-draft/NodeNorm_Protocol_v0_4_4.html) |
| Source and theological scrutiny | [Candidate obligations](scenario-batches/CB-001/obligations/README.md), [six captured answers](scenario-batches/CB-001/PARISH-QA-001-R1/evidence.json), and [review worksheet](scenario-batches/CB-001/PARISH-QA-001-R1/REVIEW.md) |
| AI contributions and actual human review | [Study disclosure](AI_DISCLOSURE.md), [contribution record](disclosure/record.json), and each experiment's disclosure |

GitHub stores HTML as a file rather than deploying a live webpage. Save it and open it in a browser for interactive sections. A development snapshot records versions; it does not certify scientific validity, venue compliance or human review. The notebook can be read without running code. Replaying it does not repeat external service queries.

## Current evidence and its limits

The [CB-001 status record](scenario-batches/CB-001/STATUS.json) distinguishes five scenario drafts, one bounded citation-identity comparison, candidate obligations and six live Q&A observations.

The [CIR-001 comparison](scenario-batches/CB-001/CIR-001/RESULTS.md) used 22 assistant-authored synthetic packets and two known metadata replays. The checklist and structured gate made the same identity-admission decisions; no advantage for the structured gate was established. The [obligations records](scenario-batches/CB-001/obligations/README.md) propose institutional applications of sources while leaving qualified review and actual applicability pending.

The [live observation run](scenario-batches/CB-001/PARISH-QA-001-R1/README.md) retained six Magisterium AI answer/reference objects. Its 40 reference entries at 38 distinct URLs are returned metadata, not 40 verified authorities. All semantic and canonical assessments remain pending qualified review. No effectiveness, compliance, or doctrinal-accuracy score is assigned.

The [earlier source-verification capture](runs/SV-20261106-001/capture.json) and its unsuccessful target retrievals remain unchanged. The 18 inherited teaching mappings also remain provisional. Zero independently reviewed Catholic safeguard studies and zero canonical CEC admissions are established. Source verification, independently prepared cases, qualified interpretation and institutional transfer remain distinct gates.

## Published baseline and earlier versions

The [0.4.1 development release](https://github.com/node-and-norm/control-evidence-corpus/releases/tag/catholic-pilot-v0.4.1-dev) remains the published snapshot. Its [study notebook](study-guide.ipynb), [HTML](study-report.html), [protocol](PROTOCOL.md) and [disclosure-updated PDF](reading/NodeNorm_Study_v0_4_1.pdf) are preserved. The top-level files are not silently substituted with a newer draft.

Use the [reader archive](reading/README.md#earlier-editions-remain-available) for 0.4.2, 0.4.3 and 0.4.4. The [v0.2 archive](archive/v0.2/README.md), [evidence workbench](evidence-workbench/README.md) and [course alignment](evidence-workbench/course-alignment/README.md) retain their historical scope. The [artifact index](reading/ARTIFACT_INDEX.json) records exact text/notebook hashes, regenerated PDF origins and replay checks.

## AI assistance and human responsibility

Substantive AI assistance includes method proposals, source inspection, provisional interpretation, code, checks, diagrams and drafting. The [common disclosure](AI_DISCLOSURE.md) is retained in the reader chain, with run-specific contributions added as the study advances. Author authorization, personal verification, independent review, theological review and submission approval have separate scopes. Specific checks must be recorded; no new human attestation is inferred.

The [October 27 guidance register](disclosure/historical-guidance-2026-10-27.json) preserves the supplied historical wording and dates. [November 6 policy checks](disclosure/policy-checks.json) retain their separate access qualifications. No venue is selected. TAE's disclosure approach is reused without importing its model identities or approvals. See [implementation guidance](disclosure/README.md).

## Reproduction and maintenance

Install `requirements-reading.txt` in an isolated environment. The [archive policy](reading/ARCHIVE_POLICY.md) explains how to recreate all current draft editions from repository sources and Git history, without chat attachments. The [archive builder](scripts/archive_readers.py) verifies original delivered hashes, replays temporary copies and refuses to overwrite changed archived files. Full source control history is needed for the pinned baseline.

For the preserved 0.4.1 baseline, the existing build sequence remains `python scripts/build_release.py --execute --pdf --package`, `python scripts/finalize_navigation.py`, then `python scripts/apply_ai_disclosure.py --execute --pdf --package`. Generated files must accompany source changes. These builders make no research API calls. Run-specific reproduction scripts remain separate from reader generation.

Checksums establish byte correspondence, not truth or reviewer independence. The public record excludes credentials, sensitive institutional data and full source text with unresolved redistribution rights. Missing historical captures remain identified as missing.

[Decisions](DECISIONS.md), [change history](CHANGELOG.md), [disclosure changes](DISCLOSURE_CHANGELOG.md), [release notes](RELEASE_NOTES.md), and the draft PR retain the maintenance and publication trail. This navigation update and reader archive do not change research hypotheses, prior results, the root README or website ingestion.
