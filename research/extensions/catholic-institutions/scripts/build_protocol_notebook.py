#!/usr/bin/env python3
"""Create a narrative Jupyter reader without changing the archived protocol.

Only standard-library modules are required. No model, network or research calls.
Source cells reassemble to the original UTF-8 bytes; presentation cells are marked.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / 'reading/editions/0.4.4-draft/NodeNorm_Protocol_v0_4_4.md'
OUTPUT = ROOT / 'reading/notebooks/NodeNorm_Protocol_v0_4_4.ipynb'
MANIFEST = ROOT / 'reading/notebooks/protocol-notebook.json'
EXPECTED_SHA256 = 'ee9ef5f8a7ea6e1e0eca53e2279f1268f7dad9f1829012031848ae51182baca7'
BASE_COMMIT = 'adbaf96070c0d26d87091aef58c5b1f9d47cfb44'
REPO = 'https://github.com/node-and-norm/control-evidence-corpus'
SOURCE_PATH = 'research/extensions/catholic-institutions/reading/editions/0.4.4-draft/NodeNorm_Protocol_v0_4_4.md'
SOURCE_URL = f'{REPO}/blob/{BASE_COMMIT}/{SOURCE_PATH}'
STUDY_URL = f'{REPO}/blob/{BASE_COMMIT}/research/extensions/catholic-institutions/reading/editions/0.4.4-draft/NodeNorm_Notebook_v0_4_4.ipynb'
INTRO = f'''# Node & Norm | Research protocol

**Jupyter reading edition of the 0.4.4-draft protocol and dated annexes.**

The governing comparative protocol remains **0.3.0 and unfrozen**. This notebook changes the reading format only. It adds no experiment, approval, source interpretation, or new finding.

[Open the complete study notebook]({STUDY_URL}) · [Inspect the archived source text]({SOURCE_URL})

## How to read this notebook

You can read the entire protocol without running code. Each section is a separate notebook text cell, with the source's headings, tables, terminology, disclosures, and citations retained. This is a real `.ipynb` file with narrative cells; it contains no code cells or invented execution results.

| Your question | Where to start |
| :--- | :--- |
| What are we investigating? | Original protocol sections 1–5: problem, question, contribution, hypotheses and boundaries. |
| How are sources and evidence handled? | Sections 6–9 and the source-verification amendment. |
| What did AI contribute, and who has reviewed it? | Section 10 and the AI-assistance disclosure. |
| What did the engineering comparison establish? | The CITATION-GATE-001-R1 engineering addendum. |
| Where do canon law and institutional responsibility enter? | Applicability supplement OA-001. |
| What did Magisterium actually return? | PARISH-QA-001-R1 observation annex; complete responses are in the study notebook. |

The source is a cumulative historical document. Its core protocol comes first, followed by dated amendments and annexes. Earlier status statements and repeated section numbers remain as recorded; this conversion does not silently reconcile them. Read the later annexes for subsequent observations. Qualified review and institutional applicability remain separate, open questions.

---

**Preservation note.** The cells below are the complete archived source, divided at its existing headings. Joining only cells marked `archived_source` reproduces the original file exactly. Presentation notes above and below are separately marked. The original Markdown, HTML and earlier notebooks remain in the repository for comparison.
'''
END = f'''---

## Provenance and limits of this reading edition

Source commit: `{BASE_COMMIT}`  
Source SHA-256: `{EXPECTED_SHA256}`

The local and repository checks compare text and notebook structure. They do not establish legal accuracy, theological approval, independent scientific validity or a completed human review. This assistant-prepared presentation change creates no new review attestation. The source's existing AI disclosure and study limitations remain in force.

GitHub renders Jupyter notebooks as static reading pages. Executing code or using arbitrary interactive JavaScript requires a suitable notebook environment; neither is needed to read this protocol. A repository HTML file is a source file, whereas a hosted webpage is a separate publication.

[GitHub notebook-rendering documentation](https://docs.github.com/en/repositories/working-with-files/using-files/working-with-non-code-files) · [GitHub Pages documentation](https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages)

Rebuild with `python research/extensions/catholic-institutions/scripts/build_protocol_notebook.py`. Add `--check` to verify the generated notebook and manifest without writing files. No network, model or service requests occur.
'''


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def cell(text: str, cell_id: str, role: str, **details: object) -> dict:
    return {'cell_type': 'markdown', 'id': cell_id,
            'metadata': {'node_norm': {'role': role, **details}},
            'source': text.splitlines(keepends=True)}


def source_chunks(text: str) -> list[str]:
    # This frozen source contains no fenced code. Do not split future code blocks.
    if '```' in text or '~~~' in text:
        raise ValueError('Source contains a fence; review the partition rule explicitly.')
    starts = [m.start() for m in re.finditer(r'^#{1,3} ', text, re.MULTILINE)]
    cuts = sorted({0, len(text), *starts})
    return [text[a:b] for a, b in zip(cuts, cuts[1:]) if a != b]


def generate(source_bytes: bytes) -> dict:
    if sha(source_bytes) != EXPECTED_SHA256:
        raise ValueError('Archived protocol differs from the fixed source digest.')
    text = source_bytes.decode('utf-8')
    chunks = source_chunks(text)
    cells = [cell(INTRO, 'protocol-reading-guide', 'presentation')]
    offset = 0
    for i, chunk in enumerate(chunks, 1):
        cells.append(cell(chunk, f'protocol-source-{i:03}', 'archived_source',
                          section_index=i, character_start=offset,
                          source_chunk_sha256=sha(chunk.encode('utf-8'))))
        offset += len(chunk)
    cells.append(cell(END, 'protocol-reader-provenance', 'presentation'))
    result = {'cells': cells, 'metadata': {
        'node_norm': {'format_version': '1.0.0', 'reading_content_edition': '0.4.4-draft',
                      'core_protocol': '0.3.0; unfrozen', 'source_commit': BASE_COMMIT,
                      'source_url': SOURCE_URL, 'source_sha256': EXPECTED_SHA256,
                      'conversion': 'verbatim heading-partitioned narrative cells',
                      'new_research_results': False, 'code_cells': 0,
                      'network_required': False, 'qualified_review': 'pending'}},
        'nbformat': 4, 'nbformat_minor': 5}
    if reassemble(result) != source_bytes:
        raise ValueError('Notebook source cells do not reproduce the archived source.')
    return result


def reassemble(notebook: dict) -> bytes:
    return ''.join(''.join(c['source']) for c in notebook['cells']
                   if c['metadata']['node_norm']['role'] == 'archived_source').encode('utf-8')


def serialize(value: dict) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=1) + '\n').encode('utf-8')


def build(check: bool = False) -> dict:
    source_bytes = SOURCE.read_bytes()
    notebook = generate(source_bytes)
    payload = serialize(notebook)
    manifest = {'kind': 'protocol_notebook_presentation', 'source_commit': BASE_COMMIT,
                'source_path': SOURCE_PATH, 'source_sha256': EXPECTED_SHA256,
                'source_bytes': len(source_bytes), 'notebook_path': 'reading/notebooks/' + OUTPUT.name,
                'notebook_sha256': sha(payload), 'notebook_bytes': len(payload),
                'source_cells': sum(c['metadata']['node_norm']['role'] == 'archived_source' for c in notebook['cells']),
                'presentation_cells': 2, 'code_cells': 0,
                'source_reassembly_identical': True, 'new_research_results': False,
                'archived_files_modified': False, 'qualified_review': 'pending'}
    for path, data in [(OUTPUT, payload), (MANIFEST, serialize(manifest))]:
        if check:
            if not path.is_file() or path.read_bytes() != data:
                raise ValueError(f'Missing or inconsistent generated file: {path.name}')
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
    return manifest


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    print(json.dumps(build(args.check), indent=2))
