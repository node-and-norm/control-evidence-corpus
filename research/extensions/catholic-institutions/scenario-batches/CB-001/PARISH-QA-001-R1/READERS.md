# Reader generation and recovery

The five current **0.4.4-draft** reader files are delivered with this study continuation as attachments and in a ZIP. They combine the earlier 0.4.2 study, recovered OA-001 material, and this live observation run. They do not overwrite published 0.4.1 release assets and are not a website deployment.

The previous handoff failed after the OA-001 source commit. The source files were recovered from GitHub Actions artifact 13552590033 for commit 180fcdc42b2d997277d9bf5af0ff194f7184ae4a. Its downloaded ZIP matched the recorded SHA-256 2a311d75a23c628e35f9775bb019b3d2c9ab2d553fbeb4b23b21ec61df556a90. The recovered builder and six-question draft also matched the Git blob identifiers returned by the connector.

The attached package includes the four exact 0.4.2 portable base files and recovered obligations sources. Run the obligations build_readers.py with that base to reconstruct 0.4.3, then run this directory's build_readers.py with --base pointing at the reconstructed 0.4.3 directory and --out pointing at a new output directory. --execute runs only offline notebook checks; --pdf renders the study reading copy. Requires mistune, nbformat, nbclient, a Jupyter Python kernel, Playwright and Chromium. The existing requirements-reading.txt in the extension records the reading environment.

The repository stores the evidence, readable guide, replay checks, compact notebook and builder. The larger generated readers and local plan/capture envelopes are supplied in the downloadable package. Rebuilding the expanded readers requires those specified portable base inputs; no claim is made that every historical reading dependency is present in the repository checkout alone.

The current study HTML and portable notebook expose all six exact responses and returned source metadata. The PDF gives the full study narrative and the observation summary; its raw-response panels are deliberately excluded from printing and remain in the companion JSON/notebook. The main protocol remains 0.3.0 and unfrozen. All conclusions requiring qualified review remain pending.
