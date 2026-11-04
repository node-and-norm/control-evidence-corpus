# Verify CEC development artifacts

CEC's continuous integration workflow uses Python 3.11 and `jsonschema` 4.25.1. The builders regenerate tracked schemas and examples, so run them in a disposable clone. [Requirements](../requirements.txt), [CI workflow](../.github/workflows/validate.yml), [existing guide](reference/REPRODUCIBILITY.md).

## Run the demonstration and checks

Run this POSIX shell block from a directory where a new `cec-verification` folder may be created. The subshell stops at the first failure. Record the printed commit and select the branch or commit under review before testing.

```sh
(
  set -eu
  git clone https://github.com/node-and-norm/node-norm-control-evidence.git cec-verification
  cd cec-verification
  git rev-parse HEAD
  python3.11 -m venv .venv
  . .venv/bin/activate
  python -m pip install --requirement requirements.txt
  python scripts/build_schemas.py
  git diff --exit-code -- schemas
  python scripts/build_examples.py
  git diff --exit-code -- examples
  python scripts/check_docs.py
  python scripts/validate.py examples/synthetic.json
  python -m unittest discover -s tests -v
  python scripts/render_dossier.py examples/synthetic.json --view review --output build/review.md
  python scripts/export.py examples/synthetic.json --output build/synthetic-export.json
  (
    cd experiments/us-control-sandbox
    python -B -m unittest discover -s tests -v
    python -B verify_archive.py
    python -B build_evidence_appendices.py --check --output evidence-appendices/v0.1
  )
)
```

The supplied demonstration needs no model credentials or live inference requests. The builders operate on retained local data. [Reproducibility scope](reference/REPRODUCIBILITY.md), [sandbox instructions](../experiments/us-control-sandbox/README.md).

## Expected outcomes and write effects

| Step | Expected result | Write effect |
| :--- | :--- | :--- |
| Schema and example builders | Successful exit; Git reports no difference in `schemas/` or `examples/`. [Builders](../scripts/) | Regenerates those tracked directories in the disposable clone. |
| Documentation check | `Local Markdown links, fragments, and details sections pass.` [Checker](../scripts/check_docs.py) | Reads Markdown navigation. |
| Example validation | Exit 0 for the declared synthetic example. [Validator](../scripts/validate.py) | Reads the example and contracts. |
| Integrity tests | Tests finish with `OK`. [Test suite](../tests/) | May create temporary test artifacts. |
| Dossier rendering | `build/review.md` contains an explicitly synthetic review view. [Renderer](../scripts/render_dossier.py) | Creates the requested Markdown file. |
| Synthetic export | `build/synthetic-export.json` contains a labeled package and its recorded hashes. [Exporter](../scripts/export.py) | Creates the requested JSON file. |
| Sandbox tests and archive checks | Successful exits with the retained archive and appendices matching their declared checks. [Sandbox verifier](../experiments/us-control-sandbox/verify_archive.py) | Uses the separate development sandbox; empirical corpus records remain outside this workflow. |

Successful execution confirms the tested infrastructure behavior. Independent human reliability, empirical control effectiveness and redistribution rights retain separate review requirements. [Verification boundaries](reference/REPRODUCIBILITY.md#what-a-successful-run-cannot-establish).
