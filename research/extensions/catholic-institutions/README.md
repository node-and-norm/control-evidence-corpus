# Catholic Institutional AI Risk and Control Evidence Pilot

**Status: exploratory research design, not an approved empirical release.**

This directory is a bounded research extension of the [Node & Norm Control Evidence Corpus (CEC)](https://github.com/node-and-norm/control-evidence-corpus). CEC's general-purpose empirical study, existing schemas and release gates remain unchanged. This extension develops a Catholic institutional risk and control-evidence pilot, initially focused on pastoral AI assistants and Catholic education.

## Read the study

1. [Visual HTML study report and roadmap](study-report.html) — the primary reading experience for institutional leaders, theologians and reviewers. Open locally in any browser or via GitHub's HTML download; GitHub's file viewer does not render HTML as a live page.
2. [Jupyter study guide](study-guide.ipynb) — an annotated companion with code-independent figures and optional Python verification cells.
3. [Research protocol v0.2.0](PROTOCOL.md) — governing working draft, hypothesis, sampling restrictions, comparison design and decision gates.
4. [Study manifest](study.json) — versioned status, phases, questions and links used to regenerate presentation artifacts.
5. [Pilot decision log](DECISIONS.md) — open choices and explicit amendments.
6. [Catholic normative crosswalk](data/normative-crosswalk.json) — 18 paragraph-located candidate source concepts, mapped to CEC evidence questions; qualified review pending.
7. [Magisterium connector locator audit](data/magisterium-locator-audit.json) — six exploratory search/fetch checks, including unresolved mismatches. Not a general reliability assessment.

## Maintenance and generation

Run `python scripts/build_study.py` from this directory to regenerate `study-report.html` and `study-guide.ipynb` from the versioned `study.json` and protocol. The builder uses Python's standard library only. Changes to methods require a reviewed update of `PROTOCOL.md`; regenerate the reader artifacts and record all substantive changes in `DECISIONS.md`.

The builder also reads the two versioned `data/` files for the Catholic-source and citation-integrity section. The report is static. It does **not** pull data from the Node & Norm homepage, infer completion, synchronize with GitHub, or claim a reviewed result. A future source adapter must require deliberate source/version selection, rights review, and explicit status transitions. A manually entered roadmap status is always labeled as such.

## Research boundary

The homepage map is discovery infrastructure. Risk records are possibilities; incident reports are documented accounts; controlled evaluations are laboratory evidence; CEC event-control annotations are separately gated empirical conclusions. Normative citations are subject to qualified Catholic review. These roles cannot be silently combined.

**No empirical Catholic risk or incident records were admitted into CEC as part of this extension.**

## Catholic source hierarchy

Use the official Vatican publications of *Antiqua et Nova* (2025) and *Magnifica Humanitas* (2026) as the authoritative textual references. Use Magisterium AI as a discovery and source-triage tool only when retrieved identifiers and paragraph locators can be checked. Preserve failed or inconsistent retrievals. Normative interpretation and proposed CEC evidence questions remain provisional until qualified independent review.
