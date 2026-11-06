# Follow the evidence
## A guided review of the Catholic institutional AI study

**Node & Norm | Evidence workbench 0.3.0 | 6 November 2026**

**Research status:** development and source-retrieval observations only. The governing pilot protocol remains the unfrozen **0.2.0** draft. This companion adds evidence requirements and review instruments; it does not change the hypotheses, admit empirical cases, or complete an independent review.

## 01. Start here: what a reader should be able to establish

A Catholic leader should be able to read a finding, inspect its supporting record, see who interpreted it, and understand what would change the conclusion. A theologian should be able to separate a Church document from our interpretation of it. A researcher should be able to recover the inputs, transformations, exclusions, and calculations. None of those tasks should require trusting an AI-written summary.

The HTML report is the front door. The notebook walks through the method and runs local checks. The underlying records carry the evidence. We retain the existing visual study and its 18 provisional mappings involving *Antiqua et Nova* and *Magnifica Humanitas*. This companion explains what additional evidence is needed before those proposals become defensible findings.

**Choose your reading path.** Institutional leaders: sections 01, 03, 05, and 10. Theologians and canonical reviewers: sections 04, 05, 07, and 09. Technical researchers: sections 02, 06, 08, and 11. Every path reaches the same limitations and source records.

**Current evidence boundary.** The inspected v0.2 package contains 18 normative mapping candidates and six selected locator comparisons. It declares zero independently coded Catholic empirical cases and zero completed Catholic safeguard evaluations. It contains no executed multi-agent Catholic study. A role description, proposed workflow, or notebook cell is not evidence of execution.

## 02. What I reviewed, and what the course actually contributes

The supplied material includes the six lesson transcripts and the five-notebook outline for LangChain Academy's **Deep Research From Scratch** course. The shared ChatGPT page did not return its transcript during this review. The available course files, rather than a claim to have read every message of that conversation, support this comparison. The current official `research_agent.py` and `multi_agent_supervisor.py` were also inspected. Their blob identifiers are recorded in the evidence inventory. Current course code may differ from the version shown in the lessons.

| Course component | What transfers to this study | Evidence researchers must additionally retain |
|---|---|---|
| Overview: scope, research, write | An explicit sequence with clear handoffs | A protocol gate before research and a human release gate after writing |
| Notebook 1: clarification and brief | A short, versioned research question with scope and exclusions | User requirements, amendments, assumptions, and tests for omitted or invented requirements |
| Notebook 2: research agent | Bounded search, tool use, iteration, and separate raw notes and summaries | Exact queries, full permitted tool responses, retrieval failures, source families, stop reasons, and summary-to-source links |
| Notebook 3: MCP | A defined contract for source retrieval | Server/tool identity, request-response matching, access scope, schema version, and locator checks |
| Notebook 4: supervisor | Explicit delegation and context separation for separable questions | Parent-child run IDs, task briefs, model/configuration identity, conflicts, failed branches, and synthesis decisions |
| Notebook 5: integrated report | Synthesis from a retained research brief and accumulated findings | A claim-to-evidence register, correction history, independent review, and a release manifest |
| Component evaluations across lessons | Test the brief, search continuation, and delegation separately | Frozen test data, raw outputs, evaluator versions, independent reference judgments, uncertainty, and negative results |

The course explicitly retains both compressed findings and raw research notes. It also warns that multi-agent systems add cost and complexity, and favors one agent when tasks cannot be cleanly separated. These are directly relevant design lessons. Our study needs stronger evidence custody, source-rights controls, normative review, and independent measurement than an instructional research assistant demonstrates.

Two cautions matter. A structured output schema verifies shape, not truth. An LLM judge supplies another model judgment, not an independent theological determination or human reference standard. The course's model-generated reflections are observable outputs; they are not a complete record of a model's internal reasoning. This study will record concise decision rationales and observable actions, not claim access to hidden reasoning.

**Sources:** user-supplied course transcript, modules 1–6; [official course repository](https://github.com/langchain-ai/deep_research_from_scratch); [research agent](https://github.com/langchain-ai/deep_research_from_scratch/blob/main/src/deep_research_from_scratch/research_agent.py); [supervisor](https://github.com/langchain-ai/deep_research_from_scratch/blob/main/src/deep_research_from_scratch/multi_agent_supervisor.py); [LangSmith evaluation concepts](https://docs.langchain.com/langsmith/evaluation-concepts).

## 03. The audit: what exists and what is missing

The inspected baseline is CEC branch commit `05db933132a41f9ec15c9b85e52758960b06ad6f`. The local v0.2 package's six top-level text/data artifacts matched the Git blob identifiers returned by the live repository. This establishes correspondence for those bytes, not the validity of their scientific content.

| Area | Evidence in the inspected package | Remaining gap |
|---|---|---|
| Question and hypotheses | A working protocol with H1–H4 and a simpler-method rival | Independent review, endpoint definitions, and protocol freeze |
| Catholic sources | 18 paragraph-located proposals from two documents | Named, qualified review of interpretation and institutional applicability |
| Locator integrity | Six selected comparison rows, including mismatches | Complete original request/response archives, exact call times, query-to-row linkage, and a defined sampling frame |
| Decisions | Ten dated design entries | Structured alternatives, accountable acceptance, evidence references, and before/after-outcome flags |
| AI disclosure | General disclosure and a CEC policy | Run-level model, prompt, tool, handoff, error, and intervention records |
| Notebook | Three local structural-check cells in the original source notebook | Evidence walkthroughs and boundary tests; the earlier standalone reading copy repaired its file dependencies |
| Evaluation | Comparison and controlled-test plans | Executed study outputs, independent initial ratings, calibrated rubrics, and uncertainty estimates |
| Publication | HTML, notebook, protocol, and source JSON | Claim-level admission checks and a complete, reviewed release package |

**A necessary correction in wording:** the legacy audit contains six selected **locator comparisons**, not a complete count of API calls, independent queries, or all retrievals. The same underlying passage ID may occur in several results. Retain that dependency. Two matches, three mismatches, and one unsuccessful fetch describe these six rows only; they do not estimate Magisterium's reliability.

The complete original tool responses are absent from the inspected repository package. Earlier conversation records may retain them, but that does not make them preserved repository evidence. We will not reconstruct missing logs from memory, invent timestamps, or present newly written prompts as historical prompts. A later recovered export should be appended with its acquisition history and linked to the legacy rows.

## 04. The evidence path: keep each proposition separate

**Question → source → retrieved passage → interpretation → institutional relevance → control hypothesis → test or event record → reviewer judgment → finding → publication.**

Each transition requires a stable identifier and an explanation. The source's authority does not automatically transfer to our interpretation, and an interpretation does not establish a technical control's effectiveness.

| Record | Minimum information | Boundary |
|---|---|---|
| Source | Issuer, title, genre, date, language/edition, authoritative URL, locator, retrieval and rights state | A search result is discovery evidence |
| Passage | Returned ID and locator, source location, permitted text or access reference, hash where retained | A matching title does not establish a matching paragraph |
| Interpretation | Source proposition, explicit teaching versus inference, alternatives, reviewer qualifications and status | AI synthesis remains a proposal |
| Scenario | Workflow, affected people, failure mechanism, context, risk-source identifier | A plausible risk is not an observed incident |
| Event/control | Event ID, objective, opportunity, time window, actual evidence and missingness | One incident can contain several controls |
| Evaluation | Frozen inputs, configurations, baseline, benign controls, responses, exclusions and metric code | A test result is bounded by its conditions |
| Finding | Claim type, supporting and challenging evidence, limitations, reviewer decision and version | A citation count cannot substitute for support |

For *Antiqua et Nova* and *Magnifica Humanitas*, retain separate document identities, authorship, paragraph numbering, source dates, and editions. Record source genre and ecclesial context without inventing a universal numerical authority score. A canonical obligation, pastoral recommendation, doctrinal proposition, institutional policy, and engineering proposal require different qualifications and forms of review.

The existing crosswalk stays provisional. A qualified reviewer may accept a paragraph locator while rejecting our proposed interpretation or the inference that a specific software control follows. Preserve those distinct decisions and any dissent.

**Source anchors:** [Antiqua et Nova, official Vatican text](https://www.vatican.va/roman_curia/congregations/cfaith/documents/rc_ddf_doc_20250128_antiqua-et-nova_en.html); [Magnifica Humanitas, official Vatican text](https://www.vatican.va/content/leo-xiv/en/encyclicals/documents/20260515-magnifica-humanitas.html); existing `data/normative-crosswalk.json`. These anchors are retained from v0.2; this maintenance review is not a new theological verification of all 18 mappings.

## 05. A worked case that reveals the limit of our evidence

**Case LOC-04: the paragraph a search promised differs from the paragraph a fetch returned.** The legacy row reports a *Magnifica Humanitas* search URL ending in `para-95`. The fetch record in that row ends in `para-90`. The same passage ID was also reported under `para-99` in another search. The classification is `locator_mismatch`.

**Supported at the artifact level:** the retained row contains inconsistent locators. Its selected fields and the classification can be inspected and recomputed locally.

**Still unresolved:** complete original request/response capture, the mechanism causing the discrepancy, whether the identifier addresses a larger chunk, whether the service's behavior has changed, and the frequency of such discrepancies. This record does not establish a defect in the provider, an error in Church teaching, or the failure of an institutional safeguard.

**Research decision:** keep the disputed discovery pointer separate from any verified quotation. Locate the intended paragraph in the official publication. Record that as a new verification step with its own evidence and reviewer. Never overwrite the original mismatch or silently change the cited paragraph.

**For a theological reviewer:** inspect the intended paragraph, its surrounding argument, the fetched paragraph, and the proposed mapping. Decide source identity, contextual fidelity, interpretation, and institutional applicability separately. The technical locator check alone answers none of those doctrinal questions.

This small case explains why our reader-facing report must link to records underneath it. A polished summary can conceal a retrieval failure unless the evidence trail remains visible.

## 06. How to document an AI-assisted or multi-agent study

We will describe an AI team only when separate agents actually execute identifiable tasks and their outputs are retained. Several tools used by one assistant are not evidence of a multi-agent experiment. The maintenance review producing this companion used one assistant with retrieval and local programming tools. No independent AI team, human panel, or Catholic control experiment was executed for it.

A future run must preserve the following under appropriate access controls:

- **Identity and configuration:** study and run IDs; parent run and delegated-task IDs; provider and model ID; exposed snapshot/version; prompt template and resolved application inputs; tool definitions; model parameters; code revision; dependency lock; source snapshot; dataset split. Unknown metadata stays null with a reason.
- **Observable execution:** issued queries and tool arguments; returned content or permitted artifact references; request/response IDs; timestamps; latency and usage when exposed; validation results; all attempts, exceptions, cancellations, and timeouts; summaries linked to their original records.
- **Authority and decisions:** who may approve, abstain, revise, or stop; human interventions; proposed and accepted changes; reason for delegation; state before and after material changes; remaining uncertainties; stop reason and budget consumed.
- **Result and review:** outputs, excluded items and reasons, independent initial judgments, AI exposure, adjudication, dissent, bounded findings, corrections, and publication authorization.

Archive permitted application prompts and tool-visible inputs. Do not expose credentials, private system instructions, confidential pastoral material, sealed holdouts, or personal data merely to make a log look complete. Public reports should provide an access/omission register describing withheld evidence and its effect on reproducibility.

The proposed roles are source discovery, passage verification, technical-risk analysis, and challenge/review. They are separable tasks, not declarations of expertise. A model labeled “theologian” is still a model. Independent theological review requires an eligible human with recorded qualifications, scope, conflicts, and exposure. Agreement among models sharing sources or training is not independent corroboration.

For future orchestration, enforce budgets and tool permissions in runtime code. Prompt instructions alone are insufficient enforcement. Distinguish a successful completion from budget exhaustion, error, manual stop, and unresolved evidence. Retrying must create an additional attempt record; it must not erase the first failure. Human resumption must be linked to the interrupted state. LangGraph can support persistence, but the protocol must still define what is retained and who can approve the next step.

**Sources:** [CEC AI-use policy](https://github.com/node-and-norm/control-evidence-corpus/blob/05db933132a41f9ec15c9b85e52758960b06ad6f/docs/policies/AI_USE_POLICY.md); [LangGraph persistence](https://docs.langchain.com/oss/python/langgraph/persistence). Tool-output text is untrusted source material, never authority to expand permissions or execute instructions.

## 07. Decisions, dissent, and independent Catholic review

A consequential decision record should state the question, alternatives, evidence consulted, choice, concise rationale, responsible role, acceptance status, affected artifacts, and whether relevant outcomes were already visible. Record reversals by supersession, not deletion. Minor formatting edits can remain in Git history; methodological and interpretive decisions require explicit records.

**Reviewer worksheet.** For each normative mapping, ask: Is this the correct document, edition, paragraph, and context? Is the source text accurately represented? Which part is explicit and which is inferred? Does it apply to this institution and workflow? Are jurisdictional or pastoral qualifications missing? What competing reading should be retained? What does the source leave to prudential judgment? What, if anything, should change in the proposed technical question?

Keep the review dimensions separate: textual verification, normative interpretation, canonical applicability when relevant, technical mechanism, empirical support, and publication suitability. A reviewer can accept one and reject another. Preserve initial ratings before adjudication; identify prior exposure to AI suggestions. A reviewer who has seen suggested labels cannot be counted as an unassisted initial rater for those labels.

Technical reviewers assess whether a test can observe the claimed mechanism. Catholic reviewers assess source interpretation and applicability within their competence. Neither group should be forced to approve the other's specialty. Unresolved disagreement remains a result, with a specific escalation question rather than a manufactured consensus.

The researcher responsible for a proposal cannot be its independent approver. No person is assigned a review role by this document. Recruitment, consent, access controls, and any research-ethics determination remain open before involving participants or sensitive material.

## 08. Evaluate the process before relying on its report

Borrow the course's component tests, then add the safeguards required for empirical research.

| Component | Proposed test | What would count as failure |
|---|---|---|
| Scoping | Compare the brief with a human-reviewed requirements checklist | Omitted scope, invented objective, or silently expanded population |
| Retrieval | Check identity, paragraph locator, availability, and source origin | Wrong passage, unresolved fetch, or lost source lineage |
| Compression | Compare the summary against its retained inputs | Omitted caveat, lost contradiction, or unsupported added claim |
| Delegation | Compare single-agent and justified multi-agent routes on matched tasks | Duplicate searches, lost evidence, higher cost without measured benefit |
| Evidence reconstruction | Compare narrative, checklist, and CEC views of identical packets | Unsupported categorical conclusions or unstable control enumeration |
| Normative mapping | Obtain independent qualified initial reviews | Unresolved interpretation, applicability disagreement, or missing source context |
| Controlled safeguard test | Compare baseline/control conditions with benign and adversarial cases | Failure persistence, harmful false positives, or unsupported transfer claims |
| Report synthesis | Trace each material claim to admitted records and limitations | Missing support, contradicted claim, or an uncertainty silently upgraded to fact |

Do not optimize only for fewer unsupported claims: a system that answers “unknown” to everything can appear successful. Report supported-answer coverage and unresolved-state retention alongside unsupported claims, burden, and time. Preserve denominators at the question, case, control-opportunity, run, and valid-response levels. Repeated outputs from the same case or model are dependent observations; they do not create extra independent cases.

Keep development cases separate from held-out evaluation. Split by event/source family where shared evidence could leak. Freeze the sampling frame, rubric, primary outcome, statistical plan, and invalid-response policy before confirmatory interpretation. Record every exploratory revision. Compare methods using the same source content and retrieval cutoff; extra evidence must be evaluated as a separate enrichment effect.

An LLM-as-judge can assist screening, but it needs calibration against qualified judgments and its own error analysis. Do not treat model consensus or expert consensus as direct knowledge of an unobserved historical event. Negative findings, disagreement, unavailable evidence, and failed trials belong in the report.

This workbench's executable checks are **software and record-integrity tests only**. They do not satisfy the planned 3–5 safeguard experiments, validate the theological mappings, or establish CEC's scientific effectiveness.

## 09. What “all the evidence” should mean

Preserve all material observable research records that can lawfully and ethically be retained, together with a register of omissions. Do not promise complete access to external systems or model internals.

**Public layer:** protocol, original analysis, source metadata and permitted excerpts, redacted traces, candidate and exclusion registers, code, synthetic fixtures, bounded findings, reviewer-role disclosures, limitations, and corrections.

**Controlled layer:** protected source content, consented restricted records, private reviewer details, contractual material, sealed holdouts, and unredacted logs when authorized. Access requires a defined custodian, purpose, retention rule, and review. A public Git branch is not a private workspace.

**Excluded layer:** secrets, passwords, access tokens, unnecessary personal data, identifiable sacramental or pastoral-counseling material, and data whose retention lacks authorization. Neither API access nor public availability automatically grants republication rights.

A hash can establish whether two retained byte sequences match. It does not prove a source's truth, the accuracy of a quotation, the independence of a reviewer, or the time at which a document originally existed. A source URL alone does not preserve a mutable page. Record version, acquisition date, access conditions, and a rights-permitted snapshot or precise locator.

For summaries, preserve links to originals and document what was omitted. Do not replace raw evidence with compressed notes. For external tracing services, keep a portable export under the study's retention rules; a vendor dashboard should not be the only copy of research evidence.

## 10. The plan from here, with evidence gates

| Stage | Deliverable | Gate that must be met |
|---|---|---|
| A. Evidence readiness | Run, claim, review, decision, and omission contracts; this guided review | Maintainer review of the proposed contract; legacy gaps visible |
| B. Source verification pilot | A small, logged set of new Magisterium search/fetch/original-text checks | Requests and responses preserved; no silent locator substitutions; rights decisions recorded |
| C. Qualified mapping review | Initial human reviews of a bounded subset of the 18 candidates | Qualifications, conflicts, context, and disagreements recorded |
| D. First five risk scenarios | Frozen upstream source IDs, workflow definitions, and eligibility decisions | Both technical and normative support are separately reviewable |
| E. Comparative and safeguard work | Executed evaluations under approved, frozen procedures | Raw outputs, failures, independent judgments, denominators, uncertainty |
| F. Research release | Claim-linked HTML report, notebooks, data, code, and correction history | Review, rights, privacy, reproducibility, and accountable approval |

Stages A–C can be prepared while upstream ingestion continues. Full ingestion is not evidence readiness; neither is it necessary to wait for every record before designing or testing source-capture procedures. CEC's existing general empirical pilot stays separate. The Catholic pilot retains its provisional targets of 20–25 risks, 5–10 incidents, and 3–5 controlled evaluations.

**LangChain decision:** adopt the course's workflow discipline now. Keep LangGraph and LangSmith optional until a measured need justifies them. A prospective adoption comparison should use matched tasks, held-out cases, evidence fidelity, review burden, cost, failure recovery, and source-loss measures. The ability to produce a longer report is not an adoption criterion.

No institutional presentation, endorsement request, new paid service, model experiment, or automated ingestion is initiated by this companion.

## 11. How to inspect and reproduce this workbench

The existing protocol and source datasets remain unchanged. This companion adds an evidence standard, templates, a guarded admission-check function, synthetic boundary tests, a guided notebook, and a browser-readable report.

The notebook has a read-first narrative and optional local code. It embeds the selected legacy locator rows and an inventory snapshot so it can run without credentials, network access, or the original directory. When companion files are present, it compares their hashes before using them. An absent companion means “embedded snapshot used,” not “live repository verified.”

Run the local checks with `python scripts/check_evidence.py` from the workbench directory. The test suite intentionally feeds invalid records to the admission function. A passing suite means those software boundary examples behaved as expected; it does not certify real-world evidence or reviewer independence. The validation output identifies itself as a maintenance check.

A future release must support two different operations: **replay**, which recomputes results from preserved outputs; and **regeneration**, which reissues model/API requests. The latter may differ even with the same inputs. Keep these claims distinct. Networked research, with budgets and credentials, must be an explicit action rather than an automatic consequence of opening or running a reading notebook.

**Source-of-record hierarchy:** governing CEC documents → pilot protocol → evidence records and review decisions → notebook calculations → published findings. Reader artifacts must not silently become a second source of truth.

## 12. Open scrutiny, not a claim of completion

The strongest next step is a small prospective source-verification run with complete permitted capture, followed by qualified review of a few mappings. This would replace a general promise of traceability with an inspectable example.

A reviewer should be able to challenge the source, the interpretation, the method, the evidence sufficiency, or the conclusion independently. The study succeeds as research only if those challenges can change what we report.

**Remaining limitations:** the shared conversation itself was unavailable; user-supplied course excerpts were available. No independent reviewer participated in this maintenance audit. Complete historical traces are not in the inspected package. New templates are prospective, not recovered records. Normative validity, human reliability, comparative value, and safeguard effectiveness remain unestablished. No new Catholic empirical finding is claimed.
