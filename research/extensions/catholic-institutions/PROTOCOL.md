# Catholic Institutional AI Risk and Control Evidence Pilot

**Research protocol 0.1.0 | Working design | 6 November 2026**  
**Research owner:** Node & Norm  
**Host infrastructure:** Control Evidence Corpus (CEC), development research extension  
**Study authority:** Independent Node & Norm research; no approval or endorsement from CDCF, Leonum, MIT, any diocese, or a Catholic institution is implied.  
**Current state:** Unfrozen protocol. No Catholic risk records have been independently coded, no Catholic incident cohort adjudicated, no Catholic pilot evaluations completed, and no empirical claim is made by this document.

> **What this protocol is for.** It fixes the questions and boundaries we can specify before the risk and incident intake finishes. Sample selection, reviewer recruitment, quantitative thresholds, and confirmatory tests remain decisions to be made and logged before relevant data are coded or unblinded. Protocol amendments will be dated and explained.

## 1. Problem and decision relevance

General AI risk databases identify possible failures; incident trackers collect accounts of reported events. Neither, on its own, establishes which risk mechanisms apply to a particular Catholic institutional workflow or whether a safeguard actually operated. Normative guidance can identify institutional obligations, but a doctrinal principle is not a technical test result. Institutional leaders need to know what was claimed, what was observed, what remains unknown, and who has authority to act.

This study examines whether an evidence-first method can connect four distinct propositions: (a) a technical failure is plausible in a specified workflow; (b) a documented event or controlled test supplies relevant evidence; (c) a candidate safeguard addresses the failure mechanism; and (d) available records warrant a bounded conclusion about the safeguard's operation. These propositions must never be collapsed into a single risk score or compliance claim.

## 2. Principal research question

**Can a source-traceable, event-control evidence method improve the support and reproducibility of AI risk and safeguard assessments in Catholic institutional settings, compared with simpler narrative and checklist representations?**

Secondary questions:

1. Which general AI failure mechanisms apply to a clearly specified Catholic institutional workflow, and on what evidence?
2. How reliably can independent reviewers map a technical risk to an institutional responsibility while distinguishing explicit normative requirements from an analyst's inference?
3. Where do direct Catholic incidents, analogous external incidents, and synthetic evaluations each support or fail to support risk-control claims?
4. Which control claims can be reconstructed from public evidence, and which remain `not_reported`, `not_observable`, `unknown`, or `conflicting`?
5. What incremental evidentiary benefit, if any, justifies the annotation cost of a CEC representation?

## 3. Proposed contribution and competing explanation

**Contribution hypothesis.** A versioned, Catholic institutional crosswalk joined to CEC's event-control observations may increase the proportion of correctly supported, traceable conclusions and improve preservation of uncertainty, relative to source-linked narratives and a well-designed simple checklist using the same evidence.

The contribution is **not** a new universal risk taxonomy, a new Catholic moral doctrine, a general incident database, a certification system, or proof that a mitigation is universally effective. MIT's repository and existing Catholic guidelines remain indispensable prior work. CEC already anticipates provenance, missingness, source-dependence, and control opportunities; domain adaptation alone is not evidence of novelty.

A credible rival explanation is that a simpler representation, given identical sources and careful coding instructions, performs as well with lower reviewer burden. The study must be allowed to support that conclusion. A prior validated Catholic institutional resource of comparable scope would also narrow the novelty claim.

## 4. Hypotheses and estimands

**H1, comparative representation (candidate primary hypothesis):** On matched, rights-reviewed evidence packets, eligible reviewers using a CEC-structured representation will make fewer unsupported affirmative/negative control-operation claims than reviewers using a source-linked narrative or an uncertainty-aware checklist. **Candidate primary outcome:** unsupported categorical conclusions per applicable control opportunity, determined under an independently reviewed documentary-support rubric. **Additional outcomes:** correctly retained unresolved states, documented provenance, time to complete and workload.

**H2, mapping feasibility (exploratory):** Independent technical and qualified Catholic-domain reviewers can apply the proposed institutional crosswalk with sufficiently stable category definitions to justify a frozen codebook. **Outcomes:** agreement before adjudication, item-level disagreements, unclassifiable cases, and revision burden. There is no presumption of a positive result.

**H3, control evaluation (exploratory):** On specifically frozen test cases, a defined safeguard will reduce a predeclared failure outcome relative to a defined baseline, without unacceptable failures on negative controls or benign tasks. **Outcomes:** rates and uncertainty per test condition, false positives, preserved raw model responses, retry and validation status. These are laboratory findings, not evidence about real deployments.

**H4, observability (descriptive):** Some claims about control operation will remain unresolved because public evidence lacks the specific records needed for reconstruction. This estimates an **evidence-availability result** under a fixed retrieval procedure, not actual population control effectiveness.

**Unresolved before confirmatory work:** primary endpoint adjudication criteria, minimum meaningful difference, allocation and blinding, inter-rater metric selection, sample-size/precision rationale, and a sealed holdout procedure. Do not retrospectively fix these after inspecting results.

## 5. Units and study boundaries

| Object | Definition | What it cannot establish alone |
|---|---|---|
| Risk scenario | A specified technical failure mechanism in a Catholic institutional workflow | That the failure occurred or is prevalent |
| Documented incident | A sourced account of a consequential event, either direct Catholic or external analogue | That controls failed or that causal attribution is established |
| CEC event-control observation | One event × control objective × opportunity × relevant period, with evidence and annotation | Full institutional compliance or control effectiveness in general |
| Controlled evaluation | An intentionally designed test with frozen stimuli, conditions and observed outputs | Real-world effectiveness or human-review reliability |
| Normative mapping | An attributable interpretation of relevant Church teaching, canon law, or institutional obligation | A legal finding or official ecclesial judgment without qualified authority |

The initial **institutional settings** are (i) pastoral and catechetical AI assistants, and (ii) Catholic educational AI systems. Chancery and tribunal administration, Catholic charitable services, and healthcare are deferred unless an explicit protocol amendment justifies expansion.

Candidate **study targets**, not representativeness claims: 20–25 risk scenarios; 5–10 incident records; 3–5 controlled evaluations. A small initial set of five risk scenarios will test the schema before any scale-up. CEC's separate ~30-event exploratory pilot and ~200-event main planning target remain distinct, unchanged, and not satisfied by this extension.

## 6. Source population, screening, and selection

The Node & Norm homepage map is a **discovery layer**, not an authoritative empirical corpus. Its editorial selection and the pending MIT/AIID ingestion are upstream candidates. Preserve exact source snapshot, retrieval date, source identifiers, licensing, known dependence and exclusion rationale. Screens based only on the map's highlighted records would bias the study toward editorially salient cases.

A candidate risk is eligible for the crosswalk only when (1) its source and technical mechanism can be located; (2) the institutional workflow is specified; (3) a potential consequence and exposed person/asset are identifiable; and (4) the Catholic relevance is stated as a reviewable proposition rather than presumed. Screen direct Catholic and analogous external incidents in separate strata. Allegations, near misses, successful interventions and synthetic tests retain separate labels. Do not infer risk prevalence from raw incident counts.

Data rights must be determined at the source and field level. AIID source-text restrictions, MIT attribution, and publisher rights continue to apply. A source mention is not permission to reproduce full reports. Prevent ingestion of identifiable confessional, pastoral-counseling, minor/student, or beneficiary records; public availability alone does not make sensitive reproduction ethically appropriate.

## 7. Data model and interoperability

The Catholic extension owns candidate `risk_scenario`, `institutional_workflow`, `normative_source`, `normative_mapping`, `risk_control_link`, `selection_decision`, and `review_status` records. It links via immutable source/version identifiers to the upstream homepage intake and via event/control IDs to a **CEC-approved release** when one exists. No new fields are appended silently to canonical CEC event/control schemas (which prohibit additional properties). A hypothetical `cec_event_id` is null until valid CEC intake occurs.

Minimum trace for each scenario: study ID; source risk ID and exact snapshot; technical mechanism; affected workflow/population; direct versus analogous relevance; candidate control; applicable normative source with paragraph/canon locator; interpretive reviewer and status; supporting evidence IDs and source family; missingness; rights decision; version, timestamps and corrections. An original document's teaching and a researcher's interpretation are distinct evidence objects.

## 8. Reproducible method

**Stage A, plan and evidence intake.** Record protocol decisions; obtain source rights; freeze candidate frame and stratification; preserve missing and excluded candidates.

**Stage B, independent enumeration.** Reviewers independently identify relevant controls and opportunities before seeing suggested labels. Preserve unmatched controls and adjudicate matches separately from coding dimensions.

**Stage C, three-view comparison.** Present identical evidence to groups receiving (a) a narrative with source links, (b) a simple checklist with explicit unresolved values, or (c) CEC event-control records. Balance assignments; prevent cross-exposure to the same case; track time and preparation cost. Support-assessment reviewers apply a common documented rubric and retain all initial decisions.

**Stage D, controlled evaluations.** For 3–5 selected mechanisms, predeclare system/version, prompt and policy configuration, baseline, safeguard, controlled perturbations, benign controls, failure/abstention rules, retries, and statistical summary. Keep synthetic evidence and model-authored reference answers separate from authoritative human judgments. Preserve invalid model outputs rather than silently repairing them.

**Stage E, qualified normative review.** Technical annotation and Catholic interpretation are reviewed separately. Qualified theological or canonical reviewers confirm the accuracy and applicability of any proposed doctrinal or canonical mapping; disagreements and jurisdictional limits remain visible.

**Stage F, release review.** Report results with failure cases, source coverage, reviewer reliability, uncertainty, licensing, privacy, code/schema versions, and the exact evidence cutoff. No compliance badge or official Church endorsement is authorized.

## 9. Evidence status and prohibited inference

Use CEC's distinctions: `yes`, `no`, `partial`, `conflicting`, `unknown`, `not_reported`, `not_observable`, `not_applicable`. Silence in a report is `not_reported`, not `no`. Missing control logs do not prove the control did not exist. Multiple articles copied from one announcement do not constitute independent confirmation. A case classification is not a causal finding. A synthetic evaluation is not an incident. A doctrinal citation is not an empirical validation. The existence of a human approver is not proof of practical intervention capacity.

## 10. AI use, reviewer authority, and research integrity

AI may assist literature triage, source discovery, extraction proposals, deduplication candidates, notebook formatting, and consistency checks. Every material use must be attributable by tool, version, prompt class, date and affected artifacts. AI cannot serve as an independent human rater or ecclesial authority. Eligible human assessors make sealed initial judgments before seeing other ratings or AI suggestions. Reviewer conflicts and exposure are recorded. Author involvement must be declared. No analysis of confidential ecclesial records is authorized in this public-data pilot.

## 11. Decision gates and stop conditions

| Gate | Required evidence | Current state |
|---|---|---|
| G0 Protocol readiness | Open methodological decisions, source plan, responsibility and amendment rule recorded | Drafted, unfrozen |
| G1 Source/rights readiness | Candidate source frame and source-specific rights decisions reviewed | Pending upstream ingestion and review |
| G2 Mapping feasibility | Five pilot risk records and independent category review | Not started |
| G3 Comparison readiness | Frozen comparator views, packet rules, support rubric, independent roles | Not started |
| G4 Evaluation readiness | Frozen test definitions, negative controls, integrity checks | Not started |
| G5 Research review | Independent assessment, uncertainty/negative results, reproducibility and rights audit | Not started |
| G6 External engagement | Clear ownership, conflict disclosure and bounded review question for CDCF/Leonum | Deferred |

The proposed representation fails its value test if the narrative/checklist performs comparably with lower burden, if reviewers cannot reliably enumerate control opportunities, if missingness is repeatedly confused with negative evidence, or if the domain mapping requires unresolvable normative judgments. Report such findings; do not redesign them away after outcome inspection.

## 12. Planned dissemination and institutional boundaries

The primary public-facing format is a versioned, accessible HTML report. A Jupyter notebook is a companion for methods, reproducible code, tables, diagrams, and later analyses. A machine-readable manifest is the shared source for the roadmap status. These are reading and reproducibility layers, **not** substitutes for the canonical evidence record or independent review.

CDCF C1–C8 can be used for a **clearly labeled internal readiness assessment**. CDCF's published criteria are a community-review draft; self-assessment is not institutional vetting, approval, or a theological imprimatur. CDCF project classifications and IP terms require separate consideration before any formal submission. Independent study ownership remains with Node & Norm unless a documented agreement changes it.

## 13. Open decisions to resolve before protocol freeze

1. Select exact source snapshots, screening frame, and attribution/redistribution conditions after upstream ingestion ends.
2. Complete targeted comparison of nearest prior work and domain-specific Catholic governance resources; do not claim to be first.
3. Recruit independent technical assessors, a Catholic normative reviewer, an adjudicator, and a holdout custodian; document roles, eligibility and conflicts.
4. Define primary outcome, support rubric, reliability statistic, allocation, minimum useful effect, and precision target.
5. Select pilot records without using outcome knowledge; freeze and version the chosen sample.
6. Define public-data safety, corrections, exact report release status, and update approval rules.

## 14. Selected source anchors (to be verified per record)

- MIT AI Risk Repository: https://airisk.mit.edu/risks
- MIT AI Incident Tracker overview: https://airisk.mit.edu/about
- *Antiqua et Nova* (28 January 2025), official Vatican text: https://www.vatican.va/roman_curia/congregations/cfaith/documents/rc_ddf_doc_20250128_antiqua-et-nova_en.html
- CDCF Project Vetting Criteria v0.2 draft: https://catholicdigitalcommons.org/governance/project-governance/project-vetting-criteria
- CEC Research Charter: https://github.com/node-and-norm/control-evidence-corpus/blob/main/RESEARCH_CHARTER.md
- CEC Comparative Pilot Design: https://github.com/node-and-norm/control-evidence-corpus/blob/main/research/COMPARATIVE_PILOT_DESIGN.md
- Node & Norm homepage map and source limitations: https://nodeandnorm.org/

## 15. Change record

| Version | Date | Decision | Evidence status |
|---|---|---|---|
| 0.1.0 | 2026-11-06 | Created an exploratory Catholic institutional extension to CEC with explicit comparison, normative review, risks and release gates | Planning only; no results |