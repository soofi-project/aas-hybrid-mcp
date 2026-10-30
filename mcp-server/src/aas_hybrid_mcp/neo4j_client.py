"""Async Neo4j driver wrapper (read-only transactions)."""

import logging
import os
import re

from neo4j import AsyncGraphDatabase

log = logging.getLogger(__name__)

NEO4J_URI = os.environ.get("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER = os.environ.get("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.environ.get("NEO4J_PASSWORD", "")
NEO4J_DATABASE = os.environ.get("NEO4J_DATABASE", "neo4j")

_driver = None


async def _get_driver():
    global _driver
    if _driver is None:
        auth = (NEO4J_USER, NEO4J_PASSWORD) if NEO4J_PASSWORD else None
        _driver = AsyncGraphDatabase.driver(NEO4J_URI, auth=auth)
        log.info("Neo4j driver created for %s", NEO4J_URI)
    return _driver


# GQL statuses Neo4j attaches to a query that names a relationship type,
# label or property key which has never been created in the database. The
# name is in backticks in the description.
_UNKNOWN_NAME_STATUSES = {
    "01N51": (
        "relationship_types",
        re.compile(r"The relationship type `(.+?)` does not exist"),
    ),
    "01N50": ("labels", re.compile(r"The label `(.+?)` does not exist")),
    "01N52": ("property_keys", re.compile(r"The property `(.+?)` does not exist")),
}


def unknown_names(summary) -> dict[str, list[str]]:
    """Relationship types, labels and property keys the DB does not know, by kind."""
    found: dict[str, list[str]] = {}
    for status in summary.gql_status_objects:
        kind_re = _UNKNOWN_NAME_STATUSES.get(status.gql_status)
        if kind_re is None:
            continue
        kind, regex = kind_re
        m = regex.search(status.status_description)
        # Keep the warning visible even if Neo4j rewords the description.
        name = m.group(1) if m else "<unparsed>"
        names = found.setdefault(kind, [])
        if name not in names:
            names.append(name)
    return found


def other_notifications(summary) -> list[dict]:
    """Neo4j notifications that have no dedicated warning (e.g. cartesian product).

    The completion statuses 00000 / 02000 are not notifications and are left
    out: ``total`` already says whether the result was empty.
    """
    out = []
    for status in summary.gql_status_objects:
        if not status.is_notification or status.gql_status in _UNKNOWN_NAME_STATUSES:
            continue
        entry = {
            "code": status.gql_status,
            "message": status.status_description,
            "severity": status.raw_severity,
        }
        pos = getattr(status, "position", None)
        if pos is not None:
            entry["position"] = {"line": pos.line, "column": pos.column}
        out.append(entry)
    return out


async def _run_query(tx, cypher: str, params: dict):
    result = await tx.run(cypher, params)
    records = []
    async for record in result:
        records.append(record.data())
    summary = await result.consume()
    notices = {
        "unknown_names": unknown_names(summary),
        "notifications": other_notifications(summary),
    }
    return records, notices


async def read_query_with_notices(
    cypher: str, params: dict | None = None
) -> tuple[list[dict], dict]:
    """Run a read-only query; also return what Neo4j said about it.

    The second value has ``unknown_names`` (by kind, see ``unknown_names``) and
    ``notifications`` (everything else worth passing on).
    """
    driver = await _get_driver()
    async with driver.session(database=NEO4J_DATABASE) as session:
        return await session.execute_read(_run_query, cypher, params or {})


async def read_query(cypher: str, params: dict | None = None) -> list[dict]:
    """Execute a read-only Cypher query and return results as list of dicts."""
    rows, _ = await read_query_with_notices(cypher, params)
    return rows


async def relationship_types() -> list[str]:
    """All relationship types present in the database, sorted."""
    rows = await read_query(
        "CALL db.relationshipTypes() YIELD relationshipType "
        "RETURN relationshipType ORDER BY relationshipType"
    )
    return [r["relationshipType"] for r in rows]


async def labels() -> list[str]:
    """All node labels present in the database, sorted."""
    rows = await read_query("CALL db.labels() YIELD label RETURN label ORDER BY label")
    return [r["label"] for r in rows]


async def close():
    """Close the driver connection."""
    global _driver
    if _driver is not None:
        await _driver.close()
        _driver = None
        log.info("Neo4j driver closed")
