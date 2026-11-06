# AI assistance and disclosure records

This is the Catholic study's implementation of [Node & Norm research-integrity commitments](https://nodeandnorm.org/about/research-integrity/) and [CEC's existing AI-use policy](../../../../docs/policies/AI_USE_POLICY.md). It adapts [TAE's November disclosure](https://github.com/node-and-norm/trust-autonomy-evidence/blob/a8bd6a13cf8f24a1abe15885df7195ca20465a25/paper/revisions/2026-11-01/main.tex#L1466-L1480), without importing TAE-specific model identities, findings or approvals.

## One record, multiple reading formats

[record.json](record.json) is the source for the study's disclosure statement and six artifact-scoped contribution entries. [AI_DISCLOSURE.md](../AI_DISCLOSURE.md) and the current reading editions are generated from it. [policy-checks.json](policy-checks.json) records fresh checks and access limitations; [historical-guidance-2026-10-27.json](historical-guidance-2026-10-27.json) preserves the user-supplied earlier register. Neither is a universal standard or a compliance certificate.

Run `python scripts/apply_ai_disclosure.py --execute --pdf --package` from the study directory after its existing reader build. The command makes no research-service calls. It generates disclosure-updated 0.4.1 reading copies, leaving old version-named reading files and archive/history bytes intact. Run `python scripts/test_ai_disclosure.py` for software checks. A passing check does not attest human verification.

## Human checks and publication

The user authorized applying this approach. Specific personal source verification, independent review, theological review and final submission acceptance are separate. No new human attestation has been supplied. When one exists, record reviewer, role, exact artifact and claim scope, method, AI exposure, conflicts, decision, limitations and date. Do not sign on someone's behalf or infer a full review from general authorization.

A target venue remains unselected. Recheck publisher and venue instructions before submission, and reconcile where the disclosure belongs and what methods details are required. Unknown model snapshots stay unknown. AI tools receive no authorship, independent-human-review or ecclesial-authority status.

Material future AI uses must identify affected artifacts and retained input/output references. Historical gaps remain gaps. Public transparency excludes credentials, unrelated conversations, protected institutional data, and sealed holdouts. Document redactions and their effect on reproducibility. Current readers link to this record; historical editions retain their original disclosures and are qualified through this dated addendum.
