# Evidence workbench 0.3.0

**Start with [Follow the evidence](EVIDENCE_REVIEW.md).** The [repository notebook](repository-review.ipynb) is an executable reading index with saved outputs. The generator produces an expanded, self-contained `evidence-review.ipynb` and an accessible `evidence-review.html` from the same review text and inventory. Generated reading editions are also supplied as conversation attachments; they are not hosted as a live website by this branch.

This companion does not replace or freeze [pilot protocol 0.2.0](../PROTOCOL.md). The [original visual study](../study-report.html), 18 provisional Catholic mappings, canonical CEC design, and upstream ingestion remain unchanged.

## Inspect the records

- [Evidence inventory](evidence-inventory.json): legacy artifact hashes, inspected sources and capture limits.
- [Prospective templates](templates/evidence-records.json): run, step, artifact, normative review, decision, finding and publication records. Null fields are unfilled, not executed research.
- [Decisions](decisions.json) and [AI-use disclosure](AI_USE_DISCLOSURE.md).
- [Boundary checks](scripts/check_evidence.py): 17 invented software fixtures, no scientific-validation claim.
- [Local validation record](validation/local-checks.json).

From this directory, run `python scripts/check_evidence.py`. Install the review dependencies in a separate environment, then run `python scripts/build_review.py` to regenerate HTML and the expanded notebook. The builder uses `mistune`; the checks and notebook code use the standard library. Jupyter execution itself requires a Python kernel. Open the generated HTML in a browser. The compact repository notebook requires the checked-out companion files; the expanded generated notebook embeds its inventory and checker and runs offline without those files.

No full raw historical tool archive is supplied. This absence is recorded rather than repaired with invented evidence. New raw capture, qualified review and empirical work remain evidence gates. The public branch contains no secrets, private course transcript, sensitive institutional data, or sealed holdout.
