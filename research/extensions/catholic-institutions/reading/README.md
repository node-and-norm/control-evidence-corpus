# Study readers and notebook archive

**Latest complete draft: 0.4.4-draft. Published development release: 0.4.1-dev.**

This is the entry point for researchers, theologians, canonical advisers and institutional reviewers. The current draft combines the study protocol, AI disclosure, citation-identity comparison, candidate institutional obligations and six live service responses. It does not claim independent validation, canonical applicability, ecclesial approval or deployment readiness.

## Start with the complete study

| Format | Current draft |
| :--- | :--- |
| Jupyter notebook, with retained outputs | [NodeNorm_Notebook_v0_4_4.ipynb](editions/0.4.4-draft/NodeNorm_Notebook_v0_4_4.ipynb) |
| Interactive HTML, including expandable response records | [Study and roadmap](editions/0.4.4-draft/NodeNorm_Study_v0_4_4.html) |
| PDF reading copy | [Study PDF](editions/0.4.4-draft/NodeNorm_Study_v0_4_4.pdf) |
| Browser-readable protocol and dated annexes | [Protocol HTML](editions/0.4.4-draft/NodeNorm_Protocol_v0_4_4.html) |
| Editable protocol and dated annexes | [Protocol Markdown](editions/0.4.4-draft/NodeNorm_Protocol_v0_4_4.md) |

The core comparison protocol remains **0.3.0 and unfrozen**. Reading-edition numbers identify presentation snapshots, not new protocol approvals. GitHub stores HTML as a file; save it and open it in a browser for its interactive controls. The notebook can be read without executing it and replayed locally without model credentials. The PDF summarizes the live run; all six complete answers and returned references remain in the HTML, notebook and evidence JSON.

## Inspect the research underneath the report

| Question | Notebook | Evidence and limits |
| :--- | :--- | :--- |
| What did the citation-identity procedures do? | [CIR-001 notebook](../scenario-batches/CB-001/CIR-001/study.ipynb) | [Results](../scenario-batches/CB-001/CIR-001/RESULTS.md), [pre-execution freeze](../scenario-batches/CB-001/CIR-001/FREEZE.md), [first-run receipt](../scenario-batches/CB-001/CIR-001/execution.json) |
| Which institutional responsibilities might apply? | [Obligations notebook](../scenario-batches/CB-001/obligations/study.ipynb) | [Source register](../scenario-batches/CB-001/obligations/sources.json), [provisional mappings](../scenario-batches/CB-001/obligations/mappings.json) |
| What did the external Q&A service actually return? | [Live-observation notebook](../scenario-batches/CB-001/PARISH-QA-001-R1/study.ipynb) | [Six captured responses](../scenario-batches/CB-001/PARISH-QA-001-R1/evidence.json), [freeze](../scenario-batches/CB-001/PARISH-QA-001-R1/FREEZE.md), [qualified-review worksheet](../scenario-batches/CB-001/PARISH-QA-001-R1/REVIEW.md) |

The compact notebooks above are distinct research instruments. The complete reader notebook brings the chapters together. A model answer is evidence of an answer being returned, not evidence that its claims are correct. The recorded identity comparison found no admission advantage for the structured gate over the checklist on its constructed packet.

## Earlier editions remain available

| Edition | What it preserves | Notebook and files |
| :--- | :--- | :--- |
| 0.4.0-dev | Initial source-verification reader | [Notebook](NodeNorm_Notebook_v0_4_0.ipynb), [HTML](NodeNorm_Study_v0_4_0.html) |
| 0.4.1-dev | Substantive AI disclosure update | [Notebook](NodeNorm_Notebook_v0_4_1.ipynb), [published release](https://github.com/node-and-norm/control-evidence-corpus/releases/tag/catholic-pilot-v0.4.1-dev) |
| 0.4.2-draft | CIR-001 identity comparison | [Notebook](editions/0.4.2-draft/NodeNorm_Notebook_v0_4_2.ipynb), [all five files](editions/0.4.2-draft/) |
| 0.4.3-draft | Candidate obligations and authority mappings | [Notebook](editions/0.4.3-draft/NodeNorm_Notebook_v0_4_3.ipynb), [all five files](editions/0.4.3-draft/) |
| 0.4.4-draft | Six live Q&A observations | [Notebook](editions/0.4.4-draft/NodeNorm_Notebook_v0_4_4.ipynb), [all five files](editions/0.4.4-draft/) |

The [v0.2 archive](../archive/v0.2/README.md), [evidence workbench](../evidence-workbench/README.md) and [course-alignment supplement](../evidence-workbench/course-alignment/README.md) retain earlier design and documentation. Their scope and dates remain historical; a later experiment does not rewrite an earlier statement about what was then pending.

## What is preserved and how

The twelve HTML, Markdown and notebook files in the three draft edition folders match the corresponding delivered package bytes. Notebook cell identities, metadata and saved outputs are retained. Validation executes separate temporary copies and leaves the archived outputs unchanged. The three PDFs are newly generated repository reading copies from those archived HTML files; they are **not claimed to match the original attachment PDF bytes**.

The [artifact index](ARTIFACT_INDEX.json) records paths, checksums, origin and offline replay status. [Archive support](archive-support/) supplies previously missing dependencies. [Archive policy](ARCHIVE_POLICY.md) explains version control, evidence boundaries and the retained build failure. Rebuilding no longer requires a ChatGPT attachment or an expiring workflow artifact. In a full clone with reading dependencies installed, run `python research/extensions/catholic-institutions/scripts/archive_readers.py --execute --pdf`.

Use this index for navigation. For a citation, record the exact Git commit and file path so a later branch update cannot silently change the cited version. New research requires a new run record; corrections to a delivered edition require a new edition or explicit supersession, not silent replacement.

**AI and review disclosure:** this archival maintenance was AI-assisted. Restoring files, executing software checks and making material accessible do not constitute personal author verification, independent human review or theological approval. The [study disclosure](../AI_DISCLOSURE.md) and run-specific disclosures remain in force. Public documentation excludes secrets, unrelated private conversations, identifiable pastoral records and source content whose redistribution rights remain unresolved.
