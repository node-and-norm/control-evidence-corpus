# Reader generation and recovery

## Current archival status

The complete **0.4.4-draft** reader files and the preceding **0.4.2/0.4.3** editions are now archived in the repository. Start with the [reader and notebook index](../../../reading/README.md), the [complete notebook](../../../reading/editions/0.4.4-draft/NodeNorm_Notebook_v0_4_4.ipynb), or the [artifact manifest](../../../reading/ARTIFACT_INDEX.json).

The twelve text/notebook files match the delivered bytes, including notebook saved outputs. PDFs are newly rendered repository reading copies, not claimed identical to the original attachment PDFs. Previously missing base inputs are now recoverable using repository files and a pinned Git revision. See the [archive policy](../../../reading/ARCHIVE_POLICY.md). No new service queries or changes to this run's evidence occurred during archival maintenance.

## Earlier recovery record, preserved for context

The initial five 0.4.4-draft readers were delivered as conversation attachments and a ZIP. They combined the earlier 0.4.2 study, recovered OA-001 material and this live observation run. At that handoff the repository held only the compact notebook, evidence and builders; complete portable readers still depended on the delivered base package. The new archive resolves that distribution gap without rewriting the original result.

The previous handoff failed after the OA-001 source commit. Source files were recovered from GitHub Actions artifact 13552590033 for commit 180fcdc42b2d997277d9bf5af0ff194f7184ae4a. Its downloaded ZIP matched SHA-256 2a311d75a23c628e35f9775bb019b3d2c9ab2d553fbeb4b23b21ec61df556a90. The recovered builder and six-question draft matched their Git blob identifiers. The Actions artifact was a recovery mechanism, not the long-term archive.

## Reading and rebuilding

The study HTML and portable notebook expose all six exact answers and returned reference metadata. The PDF gives the narrative and observation summary; complete responses remain in the HTML, notebook and evidence JSON. The core comparison protocol stays 0.3.0 and unfrozen, and qualified judgments remain pending.

In a full clone, run `python research/extensions/catholic-institutions/scripts/archive_readers.py --execute --pdf` with the pinned reading dependencies and a Python kernel installed. The original chained builders remain available for inspection. Reading/replay makes no Magisterium call. New service queries would require a separate run record.

The published 0.4.1 release and root repository README are preserved. A GitHub file is not a live website deployment, a correctness certification or an ecclesial approval.
