# CIR-001: first controlled identity comparison

**CITATION-GATE-001-R1 | Engineering feasibility | 6 November 2026**

## What the comparison found

The simple checklist and structured gate made identical admission decisions on the fixed 24-case packet. Each retained all eight constructed valid identities and held all sixteen invalid or unresolved cases. **The structured gate showed no admission advantage over the simple checklist.** Its additional per-dimension record may aid diagnosis; that benefit was not measured with human reviewers.

| Procedure | Valid identities retained | Positive signals/admissions on nonadmissible cases | Held/nonmatching | Meaning left unreviewed |
|---|---:|---:|---:|---:|
| Locator-only diagnostic, ablation | 7 / 8 | 11 / 16 signals | 6 / 24 | 24 / 24 |
| Simple checklist | 8 / 8 | 0 / 16 admissions | 16 / 24 | 24 / 24 |
| Structured gate | 8 / 8 | 0 / 16 admissions | 16 / 24 | 24 / 24 |

The locator-only output is a diagnostic label, not a production admission decision by the existing website or a Catholic institution. The checklist, not this ablation, is the primary comparator. Both complete procedures implement the same identity requirements, so this is a conformance comparison, not evidence of greater scientific validity from the structured format.

## What was actually executed

One local pass on **22 authored synthetic packets plus two historical metadata replays** produced 72 deterministic procedure outputs. No new Magisterium query, LLM inference, participant study or institutional deployment occurred. The same assistant authored the code and expected labels. The synthetic stratum includes eight valid and fourteen nonadmissible cases; the two historical cases are known failures. Do not pool them into a provider error-rate estimate.

Every output retains `semantic_support=unreviewed` and `answer_verified=false`. This deliberate limitation is not a semantic-accuracy result. The run demonstrates that the identity component does not upgrade its own checks into doctrinal approval.

## Two cases to inspect

**CG-10:** the returned document changes while paragraph number44 remains. The locator-only diagnostic signals a match; both complete procedures hold the packet. Paragraph equality alone cannot establish document identity.

**CG-07:** the identity matches, while the synthetic input contains an AI assertion of support. Both complete procedures retain the identity and leave the interpretation unreviewed. Source correspondence cannot replace a qualified judgment about meaning.

CG-05 permits an explicitly declared benign paragraph prefix; CG-06 permits declared whitespace normalization. Cases CG-09–22 test changed identities, collisions, missing fields, payload mismatch, editions, language, host and request binding. CG-23–24 replay known earlier failures, with no unseen-data claim.

## Inspect and reproduce

The scope and frozen input/engine hashes were committed in [FREEZE.md](FREEZE.md) at `ec08b3efd74187fff948e22ebffbb623ecaa7015` before the first execution. [plan.json](plan.json) and [execution.json](execution.json) retain the fixed design and first-run receipt. The first-run runner was hashed locally before invocation; it was not part of the prior remote freeze. No outcomes were used to tune the engine or change case membership.

[engine.py](engine.py) is the frozen tested implementation. [prepare_inputs.py](prepare_inputs.py) materializes the exact authored input bytes from a transparent recipe and the existing public historical capture, then checks the original input digests. [reproduce.py](reproduce.py) produces a **replay copy** of all 72 outputs and checks it against the retained first-run output digest. It writes a case-by-case CSV and a receipt in a new directory, never overwriting prior evidence.

From this directory run `python reproduce.py --output /path/to/new/cir001-replay`. No API credentials or network calls are needed. The first-run flat files and raw outputs are also included in the downloadable reading package supplied with this study continuation. Reconstructed outputs must retain their replay label, even when their bytes match.

## What remains open

This is a component-level engineering feasibility result, not one of the independently evaluated institutional safeguards or the H1 human representation comparison. No statistical generalization, provider defect, theological validity, independent gold standard or user benefit is established. The full five-scenario batch remains incomplete. Qualified interpretation, external case preparation and live integration remain gates.

The practical decision is to keep the simple checklist as the admission baseline and retain the structured trace for inspection without claiming a measured benefit. A later, independently prepared set and review study can test whether that trace actually helps people diagnose errors or preserve uncertainty.

## AI disclosure

One ChatGPT assistant inspected selected primary-source sections, designed the packet, wrote code and fixture expectations, ran the local comparison and drafted the report. Exact provider build metadata remain unestablished. User authorization is not personal source verification, independent review or exact-text approval. No AI team was executed. The study's existing TAE-aligned [AI disclosure](../../../AI_DISCLOSURE.md) remains applicable; this contribution extends it without changing any human attestation.
