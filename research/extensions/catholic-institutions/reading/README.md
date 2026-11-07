# Read the study in Jupyter notebooks

**Latest complete draft: 0.4.4-draft. Published development release: 0.4.1-dev.**

Start with the two notebooks below. They are the primary reading format for researchers, theologians, canonical advisers and institutional reviewers. The study notebook brings together the research and observations; the protocol notebook presents the complete methods and dated annexes in separate text cells. Neither requires code execution simply to read it.

| What you want to examine | Open the notebook |
| :--- | :--- |
| **The complete study, evidence and recorded observations** | [Study notebook, 0.4.4-draft](editions/0.4.4-draft/NodeNorm_Notebook_v0_4_4.ipynb) |
| **The complete research protocol and dated annexes** | [Protocol notebook, 0.4.4-draft content](notebooks/NodeNorm_Protocol_v0_4_4.ipynb) |

The current draft combines the study protocol, AI disclosure, citation-identity comparison, candidate institutional obligations and six live service responses. It does not claim independent validation, canonical applicability, ecclesial approval or deployment readiness. The core comparison protocol remains **0.3.0 and unfrozen**. Reading-edition numbers identify presentation snapshots, not new protocol approvals.

## Reading on GitHub

GitHub supports a static rendered view of `.ipynb` notebooks. Readers can inspect narrative, tables and saved outputs without installing Python. Running cells requires a suitable notebook environment. Arbitrary JavaScript interactions do not run in the repository preview. See [GitHub's notebook guidance](https://docs.github.com/en/repositories/working-with-files/using-files/working-with-non-code-files).

A `.html` file at a GitHub `/blob/` link is the stored source, not the hosted interactive website. A hosted HTML reading page requires a separate publication such as [GitHub Pages](https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages). This notebook-format update does not deploy a website. Use the notebook links above for reading directly in the repository.

The protocol notebook is a narrative document with no code cells. It preserves all source text, citations, tables, original section numbering and historical status statements. Its 55 source sections and two presentation notes are separately marked. Joining the source cells reproduces the archived Markdown bytes exactly. The source remains available for auditing; it is no longer the primary protocol-reading link.

## Inspect the research underneath the report

| Question | Notebook | Evidence and limits |
| :--- | :--- | :--- |
| What did the citation-identity procedures do? | [CIR-001 notebook](../scenario-batches/CB-001/CIR-001/study.ipynb) | [Results](../scenario-batches/CB-001/CIR-001/RESULTS.md), [pre-execution freeze](../scenario-batches/CB-001/CIR-001/FREEZE.md), [first-run receipt](../scenario-batches/CB-001/CIR-001/execution.json) |
| Which institutional responsibilities might apply? | [Obligations notebook](../scenario-batches/CB-001/obligations/study.ipynb) | [Source register](../scenario-batches/CB-001/obligations/sources.json), [provisional mappings](../scenario-batches/CB-001/obligations/mappings.json) |
| What did the external Q&A service actually return? | [Live-observation notebook](../scenario-batches/CB-001/PARISH-QA-001-R1/study.ipynb) | [Six captured responses](../scenario-batches/CB-001/PARISH-QA-001-R1/evidence.json), [freeze](../scenario-batches/CB-001/PARISH-QA-001-R1/FREEZE.md), [qualified-review worksheet](../scenario-batches/CB-001/PARISH-QA-001-R1/REVIEW.md) |

The compact notebooks above are distinct research instruments. The complete study notebook brings the chapters together. A model answer is evidence of an answer being returned, not evidence that its claims are correct. The recorded identity comparison found no admission advantage for the structured gate over the checklist on its constructed packet.

## Optional download and archival formats

| Format | Current draft |
| :--- | :--- |
| Interactive HTML to download and open in a browser | [Study and roadmap](editions/0.4.4-draft/NodeNorm_Study_v0_4_4.html) |
| PDF reading copy | [Study PDF](editions/0.4.4-draft/NodeNorm_Study_v0_4_4.pdf) |
| Protocol HTML to download | [Protocol HTML](editions/0.4.4-draft/NodeNorm_Protocol_v0_4_4.html) |
| Preserved protocol source for comparison | [Protocol Markdown](editions/0.4.4-draft/NodeNorm_Protocol_v0_4_4.md) |

These supporting formats remain preserved. The PDF summarizes the live run; all six complete answers and returned references remain in the study notebook, HTML and evidence JSON. Changing the preferred reading format does not erase earlier artifacts or revise research conclusions.

## Earlier editions remain available

| Edition | What it preserves | Notebook and files |
| :--- | :--- | :--- |
| 0.4.0-dev | Initial source-verification reader | [Notebook](NodeNorm_Notebook_v0_4_0.ipynb), [HTML](NodeNorm_Study_v0_4_0.html) |
| 0.4.1-dev | Substantive AI disclosure update | [Notebook](NodeNorm_Notebook_v0_4_1.ipynb), [published release](https://github.com/node-and-norm/control-evidence-corpus/releases/tag/catholic-pilot-v0.4.1-dev) |
| 0.4.2-draft | CIR-001 identity comparison | [Notebook](editions/0.4.2-draft/NodeNorm_Notebook_v0_4_2.ipynb), [archived files](editions/0.4.2-draft/) |
| 0.4.3-draft | Candidate obligations and authority mappings | [Notebook](editions/0.4.3-draft/NodeNorm_Notebook_v0_4_3.ipynb), [archived files](editions/0.4.3-draft/) |
| 0.4.4-draft | Six live Q&A observations | [Study notebook](editions/0.4.4-draft/NodeNorm_Notebook_v0_4_4.ipynb), [archived files](editions/0.4.4-draft/) |

The [v0.2 archive](../archive/v0.2/README.md), [evidence workbench](../evidence-workbench/README.md) and [course-alignment supplement](../evidence-workbench/course-alignment/README.md) retain earlier design and documentation. Their scope and dates remain historical; a later experiment does not rewrite an earlier statement about what was then pending.

## What is preserved and how

The twelve HTML, Markdown and notebook files in the three archived draft edition folders match the corresponding delivered package bytes. Notebook cell identities, metadata and saved outputs are retained. Validation executes separate temporary copies and leaves the archived outputs unchanged. The three PDFs are newly generated repository reading copies from those archived HTML files; they are **not claimed to match the original attachment PDF bytes**.

The [artifact index](ARTIFACT_INDEX.json) records paths, checksums, origin and offline replay status. [Archive support](archive-support/) supplies previously missing dependencies. [Archive policy](ARCHIVE_POLICY.md) explains version control, evidence boundaries and the retained build failure. Rebuilding the earlier editions no longer requires a ChatGPT attachment or an expiring workflow artifact. In a full clone with reading dependencies installed, run `python research/extensions/catholic-institutions/scripts/archive_readers.py --execute --pdf`.

### Notebook-first presentation addition

The new protocol notebook is an additional presentation of existing 0.4.4 content, outside the historical edition folders. The [conversion manifest](notebooks/protocol-notebook.json) identifies the exact source commit, source and notebook hashes, and source-preservation checks. The [builder](../scripts/build_protocol_notebook.py) uses only the Python standard library and makes no external requests. Rebuild with `python research/extensions/catholic-institutions/scripts/build_protocol_notebook.py`; add `--check` for read-only verification. Eight software checks cover text preservation, deterministic generation, unique cell identities, source offsets, pending review and absence of invented executions. These checks do not validate research claims.

The study notebook was already available and remains unchanged. The protocol notebook was added in response to the maintainer's preference for notebook reading rather than separate Markdown or HTML documents. No new study run, model response, approval, release or website deployment accompanies this presentation change. The root CEC README remains untouched.

Use this index for navigation. For a citation, record the exact Git commit and file path so a later branch update cannot silently change the cited version. New research requires a new run record; corrections to a delivered edition require a new edition or explicit supersession, not silent replacement.

**AI and review disclosure:** this archival and presentation maintenance was AI-assisted. Restoring or converting files, executing software checks and making material accessible do not constitute personal author verification, independent human review or theological approval. The [study disclosure](../AI_DISCLOSURE.md) and run-specific disclosures remain in force. Public documentation excludes secrets, unrelated private conversations, identifiable pastoral records and source content whose redistribution rights remain unresolved.
