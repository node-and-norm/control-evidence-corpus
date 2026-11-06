# Catholic Institutional AI Risk and Control Evidence Pilot

**Research protocol 0.3.0 | Main comparative design unfrozen | 6 November 2026**  
**Research owner:** Node & Norm  
**Host infrastructure:** Control Evidence Corpus (CEC), development research extension  
**Study authority:** Independent Node & Norm research; no approval or endorsement from CDCF, Leonum, MIT, any diocese, or a Catholic institution is implied.  
**Current state:** Source-verification pilot initiated with one bounded run. No Catholic safeguard test, independent normative review, or canonical empirical admission has been completed. The 18 mappings remain provisional. See Section 15 for the new run and capture limits.

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

Minimum trace for each scenario: study ID; source risk ID and exact snapshot; technical mechanism; affected workflow/population; direct versus analogous relevance; candidate control; applicable normative source with paragraph/canon locator; interpretive reviewer and status; supporting evidence IDs and source family; missingness; rights decision; version, timestamps and corrections. An original document's teaching and a researcher's interpretation are distinct evidence objects. A search index hit is a discovery result until its locator and authoritative text have been checked.

### 7A. Primary Catholic source protocol and Magisterium MCP integration (development amendment)

The normative source layer begins with two **distinct primary publications**:

- **Dicastery for the Doctrine of the Faith and Dicastery for Culture and Education, *Antiqua et Nova* (28 January 2025).** Initial locations: §§34, 39, 42, 44–46, 93, 110.
- **Pope Leo XIV, *Magnifica Humanitas* (signed 15 May 2026; officially presented 25 May 2026).** Initial locations: §§95, 99, 102, 104–106, 108–109, 145, 164.

The selected paragraphs support **18 researcher-authored, provisional source-to-CEC mapping candidates**, held in `data/normative-crosswalk.json`. These are *source concepts and questions*, not 18 observed AI risks, 18 church-law requirements, approved mitigation controls, or empirical annotations. They neither satisfy the 20–25 risk-scenario target nor change the canonical CEC study population. Each candidate records the official source and paragraph, a bounded source paraphrase, a proposed evidence question, compatible CEC dimensions, and review status. Proposals may be rejected or amended by qualified reviewers.

**Authority and reliability rule:** Treat the official Vatican publication as the textual authority. Magisterium AI's connected MCP `search` and `fetch` tools may be used for discovery, lookup and source triage, provided tool responses retain their returned IDs, URLs, metadata, retrieval date and any inconsistency. Magisterium is not assigned independent doctrinal authority. The Explore vector visualization is exploratory discovery infrastructure; vector proximity does not establish doctrine, agreement, or a technical requirement. The current tool contract has not established bulk export rights, stable full-corpus access, or full-vector index access.

**Acceptance test for a retrieved passage:** (1) record search query and exact result ID, title and URL; (2) fetch that exact ID; (3) inspect `found`, returned document title, author, reference, URL and opening passage; (4) compare search and fetch locators; (5) locate the same paragraph in the authoritative Vatican publication; (6) retain the matched status or record the discrepancy with no silent repair; (7) have a qualified reviewer assess the Catholic interpretation and institutional applicability independently of the machine retrieval. A source can be indexed for discovery while its retrieved paragraph remains excluded from a verified quotation or mapping.

On 6 November 2026, an exploratory **six-row selected locator comparison** observed two consistent *Antiqua et Nova* search/fetch pairs, three *Magnifica Humanitas* search/fetch paragraph mismatches and one *Magnifica Humanitas* `fetch` result of `found=false` after a search result. These observations are retained in `data/magisterium-locator-audit.json` with exact IDs and URLs. They do not establish the frequency, mechanism or cause of an MCP problem. No provider defect claim or general reliability estimate follows. All mapped *Magnifica Humanitas* paragraphs rely on the Vatican original for their locators until a separate verified Magisterium fetch succeeds.

**Research boundary:** A Magisterium passage, a Vatican paragraph, an analyst's normative reading and a testable CEC control dimension occupy different evidentiary roles. *Antiqua et Nova* and *Magnifica Humanitas* establish a strong reason to investigate questions of dignity, oversight, responsibility, rights and remedy. They do not, by themselves, impose a specific software-control implementation or prove a technical safeguard effective. Canonical applicability, doctrinal interpretation and pastoral judgment require appropriately qualified independent review. Claims of compliance, sacramental validity, or diocesan authorization remain outside this pilot's remit.


## 8. Reproducible method

**Stage A, plan and evidence intake.** Record protocol decisions; obtain source rights; freeze candidate frame and stratification; preserve missing and excluded candidates.

**Stage B, independent enumeration.** Reviewers independently identify relevant controls and opportunities before seeing suggested labels. Preserve unmatched controls and adjudicate matches separately from coding dimensions.

**Stage C, three-view comparison.** Present identical evidence to groups receiving (a) a narrative with source links, (b) a simple checklist with explicit unresolved values, or (c) CEC event-control records. Balance assignments; prevent cross-exposure to the same case; track time and preparation cost. Support-assessment reviewers apply a common documented rubric and retain all initial decisions.

**Stage D, controlled evaluations.** For 3–5 selected mechanisms, predeclare system/version, prompt and policy configuration, baseline, safeguard, controlled perturbations, benign controls, failure/abstention rules, retries, and statistical summary. Keep synthetic evidence and model-authored reference answers separate from authoritative human judgments. Preserve invalid model outputs rather than silently repairing them.

**Stage E, qualified normative review.** Magisterium discovery is checked against Vatican originals before independent interpretation. Technical annotation and Catholic interpretation are reviewed separately. Qualified theological or canonical reviewers confirm the accuracy and applicability of any proposed doctrinal or canonical mapping; disagreements and jurisdictional limits remain visible.

**Stage F, release review.** Report results with failure cases, source coverage, reviewer reliability, uncertainty, licensing, privacy, code/schema versions, and the exact evidence cutoff. No compliance badge or official Church endorsement is authorized.

## 9. Evidence status and prohibited inference

Use CEC's distinctions: `yes`, `no`, `partial`, `conflicting`, `unknown`, `not_reported`, `not_observable`, `not_applicable`. Silence in a report is `not_reported`, not `no`. Missing control logs do not prove the control did not exist. Multiple articles copied from one announcement do not constitute independent confirmation. A case classification is not a causal finding. A synthetic evaluation is not an incident. A doctrinal citation is not an empirical validation. The existence of a human approver is not proof of practical intervention capacity.

## 10. AI use, reviewer authority, and research integrity

AI may assist literature triage, source discovery, extraction proposals, deduplication candidates, notebook formatting, and consistency checks. Every material use must be attributable by tool, version, prompt class, date and affected artifacts. AI cannot serve as an independent human rater or ecclesial authority. Eligible human assessors make sealed initial judgments before seeing other ratings or AI suggestions. Reviewer conflicts and exposure are recorded. Author involvement must be declared. No analysis of confidential ecclesial records is authorized in this public-data pilot.

## 11. Decision gates and stop conditions

| Gate | Required evidence | Current state |
|---|---|---|
| G0 Protocol readiness | Open methodological decisions, source plan, locator QA, responsibility and amendment rule recorded | v0.2 draft and 18 unreviewed source candidates; protocol unfrozen |
| G1 Source/rights readiness | Candidate source frame and source-specific rights decisions reviewed | Pending upstream ingestion and review |
| G2 Mapping feasibility | Five pilot risk records, verified normative locators and independent category review | 18 source concepts drafted; zero reviewed risk records |
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
7. Independently review the source mapping and decide which Magisterium locator states are acceptable; retain and report the observed search/fetch mismatches without silently resolving them.

## 14. Selected source anchors (to be verified per record)

- MIT AI Risk Repository: https://airisk.mit.edu/risks
- MIT AI Incident Tracker overview: https://airisk.mit.edu/about
- *Antiqua et Nova* (28 January 2025), official Vatican text: https://www.vatican.va/roman_curia/congregations/cfaith/documents/rc_ddf_doc_20250128_antiqua-et-nova_en.html
- *Magnifica Humanitas* (signed 15 May 2026), official Vatican text: https://www.vatican.va/content/leo-xiv/en/encyclicals/documents/20260515-magnifica-humanitas.html
- Magisterium Explore (discovery only): https://www.magisterium.com/explore
- Versioned crosswalk: `data/normative-crosswalk.json`; Magisterium locator observations: `data/magisterium-locator-audit.json`
- CDCF Project Vetting Criteria v0.2 draft: https://catholicdigitalcommons.org/governance/project-governance/project-vetting-criteria
- CEC Research Charter: https://github.com/node-and-norm/control-evidence-corpus/blob/main/RESEARCH_CHARTER.md
- CEC Comparative Pilot Design: https://github.com/node-and-norm/control-evidence-corpus/blob/main/research/COMPARATIVE_PILOT_DESIGN.md
- Node & Norm homepage map and source limitations: https://nodeandnorm.org/

## 15. Change record

| Version | Date | Decision | Evidence status |
|---|---|---|---|
| 0.2.0 | 2026-11-06 | Added 18 source-located provisional mappings for *Antiqua et Nova* and *Magnifica Humanitas*; specified Magisterium MCP source-fidelity and original-text verification protocol; retained six exploratory locator checks | Sources inspected; no independent normative review or Catholic control evaluation |
| 0.1.0 | 2026-11-06 | Created an exploratory Catholic institutional extension to CEC with explicit comparison, normative review, risks and release gates | Planning only; no results |


## 15. Development amendment: source-verification pilot and synchronized publication

**Amendment date:** 6 November 2026. **Protocol edition:** 0.3.0, still unfrozen for the main comparative study. **Reading package:** 0.4.0-dev. This amendment preserves H1–H4, the two institutional settings, CEC's canonical schemas, and the existing independent-review gates.

### Scope and prospective plan

SV-20261106-001 is an exploratory source-verification run with two purposive targets: Antiqua et Nova paragraph 44 and Magnifica Humanitas paragraph 105. A local plan and SHA-256 were recorded before its new calls. This is not a registered confirmatory study. Prior locator anomalies were known. The plan allows two searches and one fetch per exact target, with no retries, identifier substitutions, or automatic repairs.

The unit is a selected search/fetch pair, distinct from the number of search results, tool calls, documents, incidents, and controls. Classify each pair as locator_match, locator_mismatch, fetch_not_found, target_not_returned, or tool_error. A separate official-source check assesses numbered paragraph identity; it does not establish an independent theological judgment.

### Capture and public evidence

The run preserves exact application requests and displayed response fields. Search envelopes are normalized to returned_items; decorative display labels duplicate title and URL and are omitted. Timestamps record local serialization after tool return, not provider arrival or execution time. Provider request IDs and model snapshots remain unavailable. This is application-level evidence, not a raw transport recording.

The full returned paragraph is excluded from public export pending redistribution review. The public projection retains document metadata, a SHA-256 of the returned text, text length, a short excerpt, and an omission explanation. An operator working copy is not an established long-term private archive; archival custody remains to be assigned. No secrets, private course transcript, sensitive pastoral data, or sealed holdout is published.

### Recorded outcome and inference boundary

The bounded run made four MCP calls: two searches and two fetches, without retries. One requested identifier returned found=false; the other fetch returned paragraph 90 instead of the search's paragraph 105. Neither selected pair supplied the requested verified passage through that pair. These are observed retrieval outcomes for two prior-informed targets, not a provider-wide reliability estimate, a causal diagnosis, or a Catholic institutional safeguard result.

The six earlier locator rows remain a legacy selected summary, separate from this prospective capture. They must not be described as all historical API calls. Zero independent Catholic risk/incident records are admitted to CEC; zero Catholic safeguard evaluations or independent normative reviews are completed by this run.

### Source-of-record and publication rule

The active protocol is generated from archived protocol 0.2 and this amendment. The study manifest and five reading files are built from the same release inputs. The scoping chapter and source-run results are included in the HTML, notebook, and protocol reading versions. The PDF expands all sections; the notebook executes offline using embedded, labeled snapshots. No research APIs run when a reader opens it.

Use a namespaced development tag for this extension, leaving the global CEC version unchanged. Keep the root README byte-identical; update the extension README and navigation only. Merge through a recorded pull request after repository and document checks. Preserve historical commits, make no force pushes, and remove only this workstream's branch after its changes are merged and recoverable. A development release is not an empirical release, ecclesial approval, or independent validation.

### Next gates

Resolve identifier/chunk semantics or conduct a separately planned replication. Obtain qualified review of a bounded subset of the 18 mappings. Reconcile an upstream source snapshot before selecting the first five institutional risk scenarios. Freeze the support rubric and comparison design before interpreting the main hypotheses. LangChain orchestration remains optional; one assistant using several tools is not a multi-agent study.
