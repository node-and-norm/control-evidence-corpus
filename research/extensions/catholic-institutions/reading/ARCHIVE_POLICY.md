# Reader preservation and publication status

**Archive maintenance | 6 November 2026, America/New_York; build completed 7 November UTC**

This policy accompanies the [reviewer index](README.md) and [artifact inventory](ARTIFACT_INDEX.json). It governs reader preservation, not research approval.

## What this archive contains

Three complete draft reader editions are retained under `editions/`: 0.4.2, 0.4.3 and 0.4.4. Each has the study HTML, portable Jupyter notebook, protocol HTML, protocol Markdown and study PDF. The twelve text/notebook files match the corresponding previously delivered file bytes, including saved notebook outputs, cell identifiers and metadata. Checksums and byte counts are in ARTIFACT_INDEX.json. The three PDFs are new repository renders from those exact archived HTML files, rather than byte-identical copies of the original PDF attachments. Fonts and pagination can differ across rendering environments.

The prior 0.4.1-dev release, existing 0.4.0 readers and v0.2 archive remain intact. The stable top-level study-guide.ipynb, study-report.html and PROTOCOL.md still describe the published baseline; the reviewer index explicitly directs readers to the latest complete draft. This avoids silently presenting a development increment as the already published version.

## Evidence and reader versions are different

A reading edition combines and explains evidence; it does not create a new experimental run. The core comparative protocol remains 0.3.0 and unfrozen. Citation tests, candidate obligations and live responses retain their own identities and review limits. Archiving a negative or unresolved result does not change it. No canonical applicability decision, qualified review, new model call or institutional deployment occurred during this maintenance.

Git history preserves committed changes. Edition folders preserve specific delivered snapshots. Named releases preserve declared publication milestones. Draft branch files are accessible for scrutiny but are not automatically a new release. A citation should include the exact commit, file path, run ID where applicable, and evidence status.

## Rebuilding without chat attachments

The repository now contains the formerly missing CIR-001 reader builder, selected source-packet record, metrics, retained notebook metadata and digest-checked replay inputs. The archive builder retrieves prior source versions from the pinned baseline commit and recreates the three edition chains in temporary folders. It restores retained outputs from the delivered notebooks, verifies the resulting file hashes, and separately executes temporary notebook copies. Those replays are not new research observations, and they do not replace the original saved outputs.

Use a full Git clone, the extension's pinned reading requirements and a Python kernel. Run `python research/extensions/catholic-institutions/scripts/archive_readers.py --execute --pdf`. The build invokes no research or model service. It rejects modified archived files instead of replacing them. Installation of dependencies and a browser is a separate environment-preparation step.

CIR-001's reproducible input/output copies remain labelled replay copies and checked against the retained first-run digests. No missing HTTP captures, provider model identities, hidden instructions, human attestations or past timestamps are fabricated. Matching a checksum establishes correspondence of bytes; it does not establish truth, authorship or reviewer independence.

## Preserve the failed maintenance attempt

The first archive workflow, [run 42326743999](https://github.com/node-and-norm/control-evidence-corpus/actions/runs/42326743999), stopped while serializing restored notebook outputs. Nested JSON dictionaries required conversion to NotebookNode objects. The correction added that conversion without altering cell source, expected hashes, recorded outputs or research findings. The failed attempt published no archival asset commit.

The corrected [run 42326931275](https://github.com/node-and-norm/control-evidence-corpus/actions/runs/42326931275) successfully verified twelve text/notebook identities, replayed the three portable notebooks, rendered three PDFs, checked protected files and committed the archive at bcb72973120464c4c5043439d515dc56186190f2. Notebook replay counts were seven, nine and ten code cells for the successive editions. These checks are software and artifact checks, not independent scientific validation.

## Subsequent changes

Preserve completed evidence records. Correct errors through an explicit amendment or superseding edition, identifying the changed claim and its effect. Do not change an old edition merely because a newer finding exists. Keep a single reviewer entry point and update its latest-draft link. Each new delivered edition should have committed files or a verified release asset, a checksum manifest, supporting source/version references, disclosure and a clear review status before it is described as archived.

The public archive excludes credentials, unrelated private conversations, identifiable pastoral information and unlicensed full source works. Generated answers remain attributed to the service that returned them; preserved statements are not endorsed advice. This maintenance was AI-assisted. User authorization is distinct from personal source verification, qualified review and exact-text acceptance. See the [study AI disclosure](../AI_DISCLOSURE.md) and the run-specific disclosures.

The root CEC README, website ingestion, canonical CEC schemas and the published 0.4.1 release were not changed by this archive. All research review gates remain visible.
