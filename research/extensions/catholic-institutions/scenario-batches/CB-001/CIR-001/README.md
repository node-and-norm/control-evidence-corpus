# CIR-001: citation identity, before meaning

**First engineering comparison executed. Independent and theological review remain open.**

Start with [results and limits](RESULTS.md), then inspect the [source packet](SOURCE_PACKET.md), [pre-execution freeze](FREEZE.md), [fixed design](plan.json), [tested engine](engine.py) and [first-run receipt](execution.json).

The simple checklist and structured gate agreed on all24 cases: eight valid constructed identities retained and sixteen invalid/unresolved cases held. The structured gate showed no admission advantage. Every output kept meaning unreviewed. Twenty-two packets were authored synthetic cases; two were known historical metadata replays. There were no new service calls, model inferences or human subjects.

## Reproduce without an API key

From this directory run:

```bash
python reproduce.py --output /tmp/cir001-new-replay
```

Choose a new output directory. [prepare_inputs.py](prepare_inputs.py) recreates the original fixture bytes from explicit constructions and the existing public source-run capture, then verifies their frozen hashes. The replay generates all72 procedure outputs, a case-by-case CSV and a provenance receipt. Its output hash must equal the captured first-run hash. It is labelled a replay copy, not a new observation.

The current study's HTML/PDF/notebook reading edition supplied in the conversation embeds this result and its AI-use qualification. The original flat execution packet is included in that download. The repository retains the readable recipe, frozen hashes, source references and replay path; it does not claim that the generated replica was separately archived at the original execution time.

The existing published study remains version0.4.1-dev while PR#37 is under development. No new release tag, main-site deployment, canonical CEC admission or institutional approval follows from this component run. The root README and inherited source mappings remain unchanged.
