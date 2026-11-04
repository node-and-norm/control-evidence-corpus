# Review the Control Evidence Corpus

CEC's current evidence supports inspection of development infrastructure. An empirical study still needs independent ratings, adjudication, acceptance criteria and source-rights review. [Research decision gates](../research/README.md#decision-gates), [comparative pilot](../research/COMPARATIVE_PILOT_DESIGN.md).

## Evidence to read

| Review question | Read | Boundary |
| :--- | :--- | :--- |
| What does a control observation contain? | [Codebook](methods/CODEBOOK.md), [schemas](../schemas/README.md), [synthetic examples](../examples/README.md) | Examples demonstrate the structure with invented records. |
| What is the proposed contribution? | [Research brief](../research/README.md), [novelty review](../research/NOVELTY_REVIEW.md) | Existing work overlaps with CEC; added value remains to be tested. |
| How will usefulness be tested? | [Comparative design](../research/COMPARATIVE_PILOT_DESIGN.md), [pilot workbench](../research/pilot/README.md) | Study roles and acceptance thresholds remain unfilled. |
| What happened in development? | [Model experiment index](../experiments/jev-cec/README.md), [sandbox run index](../experiments/us-control-sandbox/RUN-INDEX.md) | Synthetic runs and model outputs remain distinct from human empirical labels. |
| What source work exists? | [Tempe reconnaissance](../research/reconnaissance/tempe.md) | The source map is AI-assisted and awaits independent review. |
| What may be redistributed? | [Rights ledger](policies/RIGHTS_LEDGER.md), [source policy](policies/SOURCE_POLICY.md) | Rights require source-specific decisions. The blanket corpus license is unselected. |

## Keep development results separate

The repository contains three synthetic demonstrations and sixteen scripted sandbox conditions. Neither collection supplies independently coded empirical events. [Examples](../examples/README.md), [data statement](policies/DATA_STATEMENT.md).

The model experiments have their own questions, packets and authored reference answers. The four-question run differs from the earlier three-question run, so their counts do not form a direct improvement comparison. The instruction comparison retains 24 unavailable pairs and no net paired advantage for shorter instructions. [First run](../experiments/jev-cec/execution-v1/LIVE-RESULTS.md), [four-question run](../experiments/jev-cec/execution-v2/LIVE-RESULTS.md), [instruction comparison](../experiments/jev-cec/instruction-comparison-001/LIVE-RESULTS.md).

The missingness-boundary design has eight proposed packets and a 32-response mock rehearsal. Its live study remains unrun. [Missingness design](../experiments/jev-cec/missingness-boundary-001/RUNNER.md).

## Versions, citation and rights

The citation record identifies 0.3.0-dev, released October 3, 2026. Cite the exact development commit used and its unvalidated infrastructure status. [CITATION.cff](../CITATION.cff), [release record](../docs/releases/README.md).

The data statement retains a link to the earlier 0.2.0-dev distribution. The release index and citation record identify the newer development release. Neither record supplies an approved empirical dataset or a dataset DOI. [Historical distribution statement](policies/DATA_STATEMENT.md#distribution-and-citation), [release index](releases/README.md).

The maintainer has not selected a blanket corpus license. Upstream source restrictions remain attached to each source, and unknown rights block redistribution. [Rights ledger](policies/RIGHTS_LEDGER.md).

## Known limits

Public evidence can be incomplete, dependent or selected for reasons unrelated to control operation. The planned study therefore separates source assertions, reviewer judgments and missingness. [Source policy](policies/SOURCE_POLICY.md), [sampling plan](methods/SAMPLING_PLAN.md), [codebook](methods/CODEBOOK.md).

Software checks test declared data and presentation conditions. They cannot establish independent human judgment, construct validity or source-rights approval. [Reproducibility limits](reference/REPRODUCIBILITY.md#what-a-successful-run-cannot-establish).
