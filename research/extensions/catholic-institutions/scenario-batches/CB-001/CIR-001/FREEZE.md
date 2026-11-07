# CITATION-GATE-001: pre-execution freeze

**Run:** CITATION-GATE-001-R1  
**Scenario:** CIR-001  
**Recorded locally:** 2026-11-06T23:33:07.767230+00:00  
**Governing protocol:** 0.3.0, main comparative study still unfrozen.

This commit precedes execution of the procedures on the prepared packet. It is a development freeze, not independent preregistration or unseen evaluation. The same assistant prepared the code and constructed reference labels. No independent human or theological reviewer has participated.

## Bounded question

Can the identity-admission component reject inconsistent citation packets while retaining valid identity matches and preserving semantic support as unreviewed?

The broader CIR-001 scenario includes interpretation. This first run tests only document, paragraph, edition, language, identifier binding and payload correspondence. It does not evaluate doctrinal truth, ecclesial authority, human performance or institutional effectiveness.

## Fixed packet and procedures

The input order and membership are fixed: 24 cases, comprising 22 authored synthetic packets and two previously observed Magisterium metadata replays from SV-20261106-001. There are eight identity-admissible constructed reference cases and sixteen negative or unresolved cases. Invented payloads are explicitly marked synthetic; they are not quotations from Church documents. The two historical cases are known regressions, not new calls or holdout examples.

Primary comparison: (1) a simple short-circuit checklist and (2) a structured per-dimension gate, both implementing the same criteria and receiving identical evidence. A third, locator-only diagnostic adapts the literal reference-field comparison in the existing build_release.py derive() function. That diagnostic is an ablation, not a deployed source-admission policy. Do not manufacture an institutional effectiveness claim from its behavior.

All procedures return semantic_support=unreviewed and answer_verified=false. An identity-consistent packet never becomes a verified theological answer merely because it passed these checks.

Criteria: request binding; available fetch and response binding; intended document and paragraph in search/fetch URLs and metadata; registered locator receipt; edition and language; no conflicting ID bindings in the retained search response; normalized payload correspondence. Body normalization is Unicode NFC plus collapsed whitespace. Paragraph normalization accepts numeric or para-prefixed numeric references. The pointer contract accepts HTTPS www.magisterium.com, no credentials and no non-443 port. No fuzzy matching.

Case coverage includes exact matches, harmless formatting changes, unresolved/model-asserted semantic support, wrong paragraph, same-number wrong document, unavailable fetch, identifier collision, contradictory metadata, absent fields/reference receipts, missing or changed payload, edition/language mismatch, lookalike host and incorrect request binding.

## Predeclared outcomes and stopping rules

Report incorrect identity admissions / 16 nonadmissible cases; retained identity matches / 8 admissible cases; holds / 24; checklist/gate disagreement / 24; and semantic uncertainty preservation. Locator-positive signals on nonadmissible cases must be called misleading signals, not actual admissions. Keep synthetic and historical strata visible. No inference to population error rates or statistical independence. No measured human cost, time or effectiveness claim.

One complete local pass per procedure, no network/model calls, retries, tuning or exclusions. Stop and preserve any exception, malformed required record or hash failure. Report any checklist/gate difference before changing anything. A corrected implementation or amended packet requires a new run.

## Frozen byte identities

| Artifact | SHA-256 |
|---|---|
| plan.json | 202a69cb2d1fa7e6c944f6e4fd5a189d5ae90162e64296edf578360fdbb2bd37 |
| engine.py | 489e076b9aa54c0019d0b48c6be319baab9dbb0b23ce4aacdefa5dc87277e26b |
| cases.json | e6d249868c9f2c9d409e554bd7cf6f32a376e4e5f77cc382ed99ebdc539b7337 |
| registry.json | 8f57ce5d891bc639e4918f0e4a48c2b5086975b9c795a8b7970cf3b9f10bd22e |
| legacy-capture.json | 23067e41b01c184f29ab6fcdff2a86d46fa797609e4e8331455b6d443f01ec82 |

These files were prepared locally before this commit and will accompany the execution record. Hashes establish byte correspondence, not source truth or independence.

## Source and rights boundary

The source packet inspects NIST AI 600-1 section 2.2 (printed p.6; PDF page10) and actions MS-2.5-001 and MS-2.5-003 (printed p.31; PDF page35), plus the official Antiqua et Nova paragraphs44–46 and Magnifica Humanitas paragraphs105–106. These provide technical motivation and provisional institutional context, not a prescribed implementation or qualified interpretation. Inspection is assistant-assisted and limited to the named sections. No whole-paper systematic review is claimed.

No new redistribution of the full Vatican documents or NIST PDF is included. The public packet contains source links, bounded paraphrases, declared metadata omissions, original code, invented fixtures and the prior public metadata capture. Original-byte downloads failed in this environment, so original-file hashes are not fabricated. Full source verification and qualified interpretation remain separate gates.

## Disclosure

One ChatGPT assistant prepared sources, methods, fixtures, code and documentation under the maintainer's authorization. Exact-text author review and independent validation remain pending. No AI team or paid model experiment is claimed. Existing TAE-aligned disclosure requirements apply. The root README, current released reader files, canonical CEC schema and upstream ingestion are unchanged by this freeze.
