"""Tool description loader.

Each MCP tool's description lives in its own ``<tool>.md`` file in this
directory so that they can be edited independently of the Python source.
The descriptions are read once at import time of the module that
registers the tool — they ship in the wheel via the ``package-data``
entry in ``pyproject.toml`` and can be bind-mounted into the running
container for live edits.

``DOCS_MODE`` selects how much documentation the server ships:

* ``full`` (default): the long descriptions in this directory plus the
  ``get_manual_*`` tools.
* ``lean``: the short descriptions in ``lean/`` (signature, input, output)
  and no manual tools. Guidance is then expected to come from outside the
  server, e.g. from a skill.
"""

import os
from pathlib import Path

_DIR = Path(__file__).parent
_MODES = ("full", "lean")


def docs_mode() -> str:
    """Return the configured documentation mode (``full`` or ``lean``)."""
    mode = os.environ.get("DOCS_MODE", "full").strip().lower() or "full"
    if mode not in _MODES:
        raise ValueError(f"DOCS_MODE must be one of {_MODES}, got {mode!r}")
    return mode


def lean_mode() -> bool:
    return docs_mode() == "lean"


def load(name: str) -> str:
    """Return the description for the given tool name."""
    base = _DIR / "lean" if lean_mode() else _DIR
    return (base / f"{name}.md").read_text(encoding="utf-8")
