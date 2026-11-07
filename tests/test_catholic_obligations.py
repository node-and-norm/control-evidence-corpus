"""Expose the bounded obligations-record integrity checks to repository CI."""
from pathlib import Path
import runpy
_MODULE = Path(__file__).resolve().parents[1] / 'research/extensions/catholic-institutions/scenario-batches/CB-001/obligations/validate.py'
Integrity = runpy.run_path(str(_MODULE))['Integrity']
