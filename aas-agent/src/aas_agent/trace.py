"""Markdown conversation logger for debugging agent traces."""

import logging
from datetime import datetime, timezone
from pathlib import Path

log = logging.getLogger(__name__)


class ConversationLogger:
    """Writes a single conversation to a Markdown file.

    Collects all tokens yielded by the agent (including tool-call blocks)
    and flushes to disk when the conversation ends. The file is only written
    if a log directory is configured; missing directory is created on first
    write.

    Usage:
        logger = ConversationLogger(log_dir, conversation_id)
        logger.write_header(messages, model)
        logger.append(token)     # once per yielded token
        logger.flush()           # in finally block
    """

    def __init__(self, log_dir: Path | None, conversation_id: str) -> None:
        self._path = log_dir / f"{_timestamp()}_{conversation_id}.md" if log_dir else None
        self._parts: list[str] = []

    def write_header(self, messages: list[dict], model: str) -> None:
        ts = datetime.now(timezone.utc).isoformat(timespec="seconds")
        self._parts.append(f"# Conversation {ts}\n\n**Model:** {model}\n\n")
        for msg in messages:
            role = msg.get("role", "")
            content = msg.get("content", "")
            if role == "system":
                continue
            self._parts.append(f"## {role.capitalize()}\n\n{content}\n\n")
        self._parts.append("## Assistant\n\n")

    def append(self, token: str) -> None:
        self._parts.append(token)

    def flush(self) -> None:
        if self._path is None or not self._parts:
            return
        try:
            self._path.parent.mkdir(parents=True, exist_ok=True)
            self._path.write_text("".join(self._parts), encoding="utf-8")
        except Exception:
            log.exception("Failed to write conversation log to %s", self._path)


def _timestamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
