"""Markdown conversation logger for debugging agent traces."""

import hashlib
import logging
from datetime import datetime, date, timezone
from pathlib import Path

log = logging.getLogger(__name__)


def _session_id(messages: list[dict]) -> str:
    """Derive a stable session ID from the conversation history.

    Open WebUI sends the full history on every turn, so the first user
    message is the same across all turns of one conversation.
    We combine today's date with an 8-char hash of that message so
    different conversations on the same day don't collide.
    """
    first_user = next(
        (m.get("content", "") for m in messages if m.get("role") == "user"),
        "",
    )
    h = hashlib.md5(first_user.encode(), usedforsecurity=False).hexdigest()[:8]
    return f"{date.today().strftime('%Y%m%d')}_{h}"


class ConversationLogger:
    """Writes agent turns to a Markdown file, one file per session.

    Session detection (priority order):
    1. ``chat_id`` from the request (if the client sends it).
    2. Fingerprint of the first user message in the history — Open WebUI
       sends the full conversation history on every turn, so this is
       stable across all turns of the same chat session.

    Both modes append to the same file so a conversation accumulates
    in one place. The turn number (= number of user messages seen so far)
    is written into the header so individual turns are distinguishable.
    """

    def __init__(
        self,
        log_dir: Path | None,
        completion_id: str,
        chat_id: str | None = None,
    ) -> None:
        self._completion_id = completion_id
        self._path: Path | None = None
        self._session: str = ""

        if log_dir is not None:
            self._session = chat_id if chat_id else ""
            # Path is set in write_header once we have messages for fingerprinting
            self._log_dir = log_dir
        else:
            self._log_dir = None
        self._parts: list[str] = []
        self._after_header = False  # True once write_header has run, False after first append

    def write_header(self, messages: list[dict], model: str, extra: dict | None = None) -> None:
        """Write a turn header with the latest user message and turn number."""
        ts = datetime.now(timezone.utc).isoformat(timespec="seconds")

        last_user = ""
        for msg in reversed(messages):
            if msg.get("role") == "user":
                last_user = msg.get("content", "")
                break

        turn_num = sum(1 for m in messages if m.get("role") == "user")

        if self._log_dir is not None and self._path is None:
            if not self._session:
                self._session = _session_id(messages)
            self._path = self._log_dir / f"{self._session}.md"

        meta = f"*{ts} — model: {model} — turn {turn_num} ({self._completion_id})"
        if extra:
            meta += f" — {extra}"
        meta += "*"

        self._parts.append(f"\n---\n{meta}\n\n")
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
            with self._path.open("a", encoding="utf-8") as f:
                f.write("".join(self._parts))
        except Exception:
            log.exception("Failed to write conversation log to %s", self._path)
