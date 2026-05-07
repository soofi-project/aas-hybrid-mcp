"""Tool description loader.

Each MCP tool's description lives in its own ``<tool>.md`` file in this
directory so that they can be edited independently of the Python source.
The descriptions are read once at import time of the module that
registers the tool — they ship in the wheel via the ``package-data``
entry in ``pyproject.toml`` and can be bind-mounted into the running
container for live edits.
"""

from pathlib import Path

_DIR = Path(__file__).parent


def load(name: str) -> str:
    """Return the description for the given tool name."""
    return (_DIR / f"{name}.md").read_text(encoding="utf-8")
