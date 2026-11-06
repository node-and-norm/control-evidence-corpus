# Research decisions and amendment log

**Status:** open planning decisions. Items marked *proposed* are design recommendations, not approved or frozen choices.

| ID | Date | Decision | Status | Reason and consequence |
|---|---|---|---|---|
| D-001 | 2026-11-06 | Host the Catholic study as a scoped CEC research extension on a dedicated branch | Proposed / implemented in branch | Avoids a competing canonical corpus and keeps integration traceable |
| D-002 | 2026-11-06 | Use HTML as reader-facing report and a Jupyter notebook as reproducibility companion | Proposed / artifacts prepared | Supports mixed technical and nontechnical audiences; both read the same study manifest |
| D-003 | 2026-11-06 | Start with pastoral and catechetical AI assistants and Catholic education | Proposed | Limits normative and technical scope during initial feasibility work |
| D-004 | 2026-11-06 | Preserve 20–25 risks, 5–10 incidents and 3–5 tests as planning targets only | Proposed | Ingestion, eligibility and resource feasibility not yet established |
| D-005 | 2026-11-06 | Keep CEC's existing ~30 event pilot separate and unmodified | Proposed | Prevents contamination of original sample and measurement plan |
| D-006 | 2026-11-06 | Use no LangGraph orchestration in the design phase | Proposed | Deterministic scripts and human review are sufficient until benefit is tested |
| D-007 | 2026-11-06 | Defer Taylor / CDCF external presentation until reviewable pilot package exists | Proposed | Ownership, institutional alignment and qualified review need clear boundaries |

| D-008 | 2026-11-06 | Add official *Antiqua et Nova* and *Magnifica Humanitas* texts to the normative source layer | Implemented as unreviewed development crosswalk | Documents support source-located questions; no automatic canonical or technical-control requirement |
| D-009 | 2026-11-06 | Use Magisterium MCP for source discovery only until search/fetch locators and original texts agree | Implemented as acceptance rule; gaps open | Six exploratory tool interactions included two matches, three mismatches and one not-found; cause and prevalence unestablished |
| D-010 | 2026-11-06 | Keep source crosswalk and connector audit separate from empirical CEC intake | Implemented in development branch | Preserves original CEC release gates, source provenance and interpretive independence |

## Decisions still required

- Source snapshot dates, MIT/incident corpus eligibility and rights decisions.
- Review roles, credentials, conflicts, training, adjudication and holdout custody.
- Primary comparison outcome, minimum worthwhile difference, sample allocation and precision analysis.
- Qualified-review protocol, normative scope and source hierarchy; the source-fidelity procedure is drafted but not independently reviewed.
- Source-locator discrepancies: clarify which expected ref/fetched ref pairs qualify for citation admission; never impute a match.
- Artifact publication status, approval responsibility, correction procedure and exact citation version.

A later amendment must append a dated entry naming the affected sections, reason, decision owner, effect on comparability, and whether the change occurred before or after observing relevant data.
