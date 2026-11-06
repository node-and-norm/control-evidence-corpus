# From the course to the study

**Node & Norm | Course-alignment supplement 0.3.1 | 6 November 2026**

This supplement connects your *Deep Research From Scratch* materials to the Catholic Institutional AI Risk and Control Evidence Pilot. The evidence workbench remains version 0.3.0; the governing pilot protocol remains the unfrozen 0.2.0 draft. No hypothesis, normative mapping, empirical record, or research result is changed here.

## 01. What was reviewed

All six uploaded PDFs are byte-identical copies of one 14-page deck. Their shared SHA-256 is `687b815dc1e738c6d39ce9d978b826909f8d10b4a200c67358ee91fc228ad1d3`. They contribute one source, not six independent sources.

The full texts of the five linked Studio Python modules were read at course commit `93f35e5d2a51590f9542207a9ff66a01901da5bc`. All five notebook links are registered below. Notebook 1 was partially inspected; a complete cell/output review of all five notebooks was not obtained. The source-module review should not be described as a complete notebook execution audit. The earlier evidence workbench separately records its review of the supplied lesson transcripts.

The public PDF link could not be fetched by the web reader. The attached copy supplied the text and rendered diagrams; pages 8–13 were rendered locally. The optional videos, foundation courses, and their current interfaces were not reviewed in this pass. No course notebook, model request, MCP server, package installer, or live research graph was executed.

## 02. The structure worth borrowing

The diagram on slide 8 presents **Scope → Research → Write**. Slide 9 separates clarification from brief generation. Slide 10 shows the model–tool loop. Slide 11 adds a supervisor that assigns topics and receives findings. Slide 12 joins these into the full system, ending with one-shot report generation. Slide 13 identifies design decisions, research agents, multi-agent systems, and component evaluation as learning goals.

That organization gives readers a useful route through complex work. Our adaptation adds explicit evidence checks and qualified review before findings are released:

**Scope → Retrieve and preserve → Verify and interpret → Compare and review → Write and approve.**

This is Node & Norm's proposed adaptation, not a claim that the course teaches a complete Catholic research or empirical assurance protocol. The course explains a research-assistant architecture. CEC supplies a separate research method whose usefulness and reliability still need to be tested.

## 03. Five notebook chapters, each with an inspectable handoff

The names below are a proposed authoring sequence. They are not five newly implemented research agents or five completed experiments. The existing study guide and evidence notebook remain the current entry points.

| Course unit | Proposed Node & Norm chapter | Reader's question | Record that must survive the handoff |
|---|---|---|---|
| 1. Scoping | `01_scope_and_questions.ipynb` | What exactly are we investigating, and what is outside scope? | Brief, requirements checklist, assumptions, exclusions, protocol version, and explicit decisions |
| 2. Research Agent | `02_sources_and_evidence.ipynb` | Where did the evidence come from, and what was left out? | Queries, permitted full responses, source families, timestamps, rights decisions, failures, and selection reasons |
| 3. Research Agent MCP | `03_magisterium_source_checks.ipynb` | Does the returned passage match the cited document and paragraph? | Tool contract, search/fetch identifiers, returned locators, official-source check, mismatch and correction records |
| 4. Research Supervisor | `04_analysis_and_review.ipynb` | Who did what, and where did reviewers disagree? | Actual task/run IDs, context boundaries, preserved branch outputs, concise decisions, independent initial reviews and adjudication |
| 5. Full system | `05_findings_and_limits.ipynb` | Which conclusions are supported, and how can I challenge them? | Claim-to-evidence links, calculations, counterevidence, uncertainty, exclusions, review status and release decision |

Every chapter should begin with a plain-language question, show a small workflow, identify its inputs, explain the method, display actual available records, and end with limitations and the next decision. Technical cells can follow that narrative. A missing result should appear as “not yet run,” not as an empty success panel or invented example result.

For Catholic reviewers, every normative record must distinguish the original source proposition, our interpretation, its proposed institutional application, and any technical control hypothesis. Keep *Antiqua et Nova* and *Magnifica Humanitas* distinct. This pass adds no new theological interpretation and does not reverify their existing mappings.

## 04. What the linked implementations reveal

These are bounded static observations about the inspected course version. They are not runtime test results or general claims about LangChain products.

**Scoping.** `research_agent_scope.py` uses structured models for clarification and brief generation. Its routing uses the returned clarification field. Our inference: predictable output structure helps manage the workflow, but content still needs a requirements check. Preserve the original request alongside the brief so omitted constraints and added assumptions can be detected.

**Research.** `research_agent.py` retains compressed research and a string assembled from tool and AI message content. Our inference: the field named `raw_notes` is useful but is not, on its own, a lossless request/response archive. In our study, preserve complete permitted message envelopes and tool arguments before summarization, with identifiers and links from each summary to its inputs. Preserve contradictory evidence and unresolved states through compression.

**MCP.** `research_agent_mcp.py` configures a filesystem server through `npx`, discovers tools, and binds the returned tools to the model. Our adaptation: Magisterium source discovery should have an explicit approved read-tool list, a captured tool contract, and source-locator checks. Filesystem access should not confer permission to change canonical records. Package/model versions and unknown metadata must be recorded. Do not infer a general protocol requirement from this example's asynchronous Python implementation.

**Supervisor.** In `multi_agent_supervisor.py`, completion, missing tool calls, an iteration limit, and caught exceptions can all lead toward an end state. Its concurrency parameter is supplied to the prompt; the inspected execution path dispatches the selected research calls with `asyncio.gather` without an explicit local semaphore. Our adaptation: enforce budgets and concurrency in runtime code, and record why each branch ended. Distinguish `completed`, `budget_exhausted`, `tool_error`, `human_stop`, and `unresolved`. A stopped branch is not automatically a successful branch.

**Full system.** `research_agent_full.py` passes accumulated notes to the writer and connects the supervisor subgraph to final report generation. Our adaptation: place an evidence-status check before synthesis and an accountable release decision after it. Partial drafts may be useful, but incomplete research must remain visibly incomplete. Generation of fluent prose cannot upgrade a candidate finding to an approved result.

The example scripts are instructional implementations. The additional controls above arise from our evidence and research requirements; their absence from a small tutorial is not proof of a framework defect.

## 05. The evidence tests to prepare

These are proposed component acceptance questions, not completed evaluations or frozen statistical thresholds.

| Stage | Test to prepare | Failure that must remain visible |
|---|---|---|
| Scope | Check the brief against a human-reviewed list of required and excluded questions | Omitted requirement or invented objective |
| Retrieval | Check query/result/fetch identity, source origin and paragraph location | Wrong passage, unavailable fetch or lost provenance |
| Compression | Compare each summary with its preserved inputs | Deleted qualification, missing contradiction or unsupported addition |
| Delegation | Inspect task coverage, overlap, branch status and resource use | Duplicated work, dropped branch evidence or an exhausted budget labeled complete |
| Interpretation | Obtain qualified, attributable source and applicability reviews | Unresolved disagreement or an AI proposal counted as independent human judgment |
| Report | Trace each material finding to supporting and challenging evidence | Unsupported conclusion, absent denominator, or a missing limitation |

Evaluate these components before treating an end-to-end report as dependable. Use the same source packets and clearly separate development revisions from later held-out assessment. Report useful supported coverage as well as unsupported-claim rates so an answer of “unknown” to everything cannot appear successful.

The existing 17 software fixtures remain software checks. Neither those fixtures nor this source-alignment review completes the planned controlled safeguard experiments or validates the Catholic mappings.

## 06. Reader design and next action

Keep one canonical record behind multiple views: a concise HTML narrative for institutional leaders, passage-level review for theologians, and executable analysis for researchers. The claim, supporting evidence, contrary evidence, uncertainty, and reviewer status should be reachable from the same finding. Use consistent identifiers across all views.

Use a single declared source for production code and import it into notebooks. The course's notebook-first teaching pattern is helpful for learning, but a research reading notebook should not silently regenerate canonical records or overwrite evidence. Separate reading, replay from saved outputs, and explicit networked regeneration. Opening a notebook must not incur model costs or contact external services.

The next implementation should be the first scoping chapter plus a small source-capture run, not five empty notebooks or a new agent platform. The draft brief can be checked now; source collection can proceed in the existing upstream conversation. A later Magisterium run should preserve exact permitted requests and responses prospectively, then undergo original-source and qualified interpretation review.

No LangChain dependency is added by this supplement. No multi-agent study, human review, live source-verification run, institutional approval, or empirical finding is claimed. Repository source tracking improves inspectability; the research still has to earn its conclusions.

## Source register and review limits

The machine-readable `source-register.json` records the PDF identity, all five notebook links, the five inspected module paths and Git blob identifiers, review coverage, baseline CEC commit, and access limitations. References below use the pinned course commit rather than a moving branch.

- [Scoping module](https://github.com/langchain-ai/deep_research_from_scratch/blob/93f35e5d2a51590f9542207a9ff66a01901da5bc/src/deep_research_from_scratch/research_agent_scope.py)
- [Research agent module](https://github.com/langchain-ai/deep_research_from_scratch/blob/93f35e5d2a51590f9542207a9ff66a01901da5bc/src/deep_research_from_scratch/research_agent.py)
- [MCP research module](https://github.com/langchain-ai/deep_research_from_scratch/blob/93f35e5d2a51590f9542207a9ff66a01901da5bc/src/deep_research_from_scratch/research_agent_mcp.py)
- [Supervisor module](https://github.com/langchain-ai/deep_research_from_scratch/blob/93f35e5d2a51590f9542207a9ff66a01901da5bc/src/deep_research_from_scratch/multi_agent_supervisor.py)
- [Full-system module](https://github.com/langchain-ai/deep_research_from_scratch/blob/93f35e5d2a51590f9542207a9ff66a01901da5bc/src/deep_research_from_scratch/research_agent_full.py)

Course content remains attributed to its publishers. The uploaded slide deck and complete course code are not republished in this supplement. This is an assistant-prepared static review with no independent reviewer participation.
