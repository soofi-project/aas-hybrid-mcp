"""Markdown conversation logger for debugging agent traces."""

import hashlib
import logging
from datetime import datetime, timezone
from pathlib import Path

log = logging.getLogger(__name__)


def _session_id(messages: list[dict]) -> str:
    """Stable per-session fingerprint from the first user message.

    Open WebUI sends the full conversation history on every turn, so the
    first user message is identical across all turns of the same chat —
    a 12-char hash is enough to disambiguate different chats.
    """
    first_user = next(
        (m.get("content", "") for m in messages if m.get("role") == "user"),
        "",
    )
    return hashlib.md5(first_user.encode(), usedforsecurity=False).hexdigest()[:12]


def _filename_ts(dt: datetime) -> str:
    """ISO-style UTC timestamp safe for filenames (no colons)."""
    return dt.strftime("%Y-%m-%dT%H-%M-%SZ")


class ConversationLogger:
    """Writes one Markdown file per turn into a per-session folder.

    Layout::

        {log_dir}/{first-turn-ts}__{session-id}/turn-{NN}__{turn-ts}.md

    The folder is created on the first turn; subsequent turns of the same
    session land in the same folder (located via ``glob('*__{sid}')``).

    Session ID priority:
    1. ``chat_id`` passed in by the API layer (Open WebUI Pipelines /
       custom header — see ``api._extract_client_id``).
    2. Hash of the first user message in the history.
    """

    def __init__(
        self,
        log_dir: Path | None,
        completion_id: str,
        chat_id: str | None = None,
    ) -> None:
        self._log_dir = log_dir
        self._completion_id = completion_id
        self._chat_id = chat_id
        self._path: Path | None = None
        self._parts: list[str] = []
        self._after_header = False

    def _resolve_path(self, messages: list[dict], turn_num: int, now: datetime) -> Path | None:
        if self._log_dir is None:
            return None
        sid = self._chat_id or _session_id(messages)
        existing = sorted(self._log_dir.glob(f"*__{sid}"))
        folder = existing[0] if existing else self._log_dir / f"{_filename_ts(now)}__{sid}"
        return folder / f"turn-{turn_num:02d}__{_filename_ts(now)}.md"

    def write_header(self, messages: list[dict], model: str, extra: dict | None = None) -> None:
        now = datetime.now(timezone.utc)
        ts = now.isoformat(timespec="seconds")

        last_user = ""
        for msg in reversed(messages):
            if msg.get("role") == "user":
                last_user = msg.get("content", "")
                break

        turn_num = sum(1 for m in messages if m.get("role") == "user")
        self._path = self._resolve_path(messages, turn_num, now)

        meta = f"*{ts} — model: {model} — {self._completion_id}"
        if extra:
            meta += f" — {extra}"
        meta += "*"

        self._parts.append(f"# Turn {turn_num}\n{meta}\n\n")
        self._parts.append(f"## User\n\n{last_user}\n\n")
        self._parts.append("## Assistant\n\n")
        self._after_header = True

    def append(self, token: str, strip_leading_newlines: bool = False) -> None:
        if strip_leading_newlines and self._after_header:
            token = token.lstrip("\n")
            self._after_header = False
        self._parts.append(token)

    def flush(self) -> None:
        if self._path is None or not self._parts:
            return
        try:
            self._path.parent.mkdir(parents=True, exist_ok=True)
            target = self._path
            i = 2
            while target.exists():
                target = self._path.with_name(
                    f"{self._path.stem}_{i}{self._path.suffix}"
                )
                i += 1
            with target.open("w", encoding="utf-8") as f:
                f.write("".join(self._parts))
        except Exception:
            log.exception("Failed to write conversation log to %s", self._path)
