"""Deterministic permission guards. Not an operating-system sandbox."""
from pathlib import Path

class TeamBlocked(ValueError):
    """A spec, capability, capture or review boundary was violated."""


def require_offline(mode: str, max_calls: int) -> None:
    if mode != 'offline_fixture':
        raise TeamBlocked('Live mode is disabled. Issue #41 and reviewed provider adapters are required.')
    if isinstance(max_calls, bool) or not isinstance(max_calls, int) or not 1 <= max_calls <= 5:
        raise TeamBlocked('Prototype permits one to five explicitly recorded role calls.')

def prepare_run_directory(run_dir: Path, protected_root: Path) -> Path:
    target=Path(run_dir).resolve(); protected=Path(protected_root).resolve()
    if target==protected or protected in target.parents:
        raise TeamBlocked('Use a temporary directory outside the repository; role execution cannot modify the corpus.')
    target.mkdir(parents=True,exist_ok=True)
    if any(target.iterdir()):
        raise TeamBlocked('A new run needs an empty directory; retained attempts must not be overwritten.')
    return target
