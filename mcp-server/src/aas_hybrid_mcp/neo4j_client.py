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


# GQL status Neo4j attaches to a query that names a relationship type which
# has never been created in the database; the type name is in backticks.
_UNKNOWN_REL_TYPE_STATUS = "01N51"
_UNKNOWN_REL_TYPE_RE = re.compile(r"The relationship type `(.+?)` does not exist")


def unknown_relationship_types(summary) -> list[str]:
    """Names of relationship types in the query that do not exist in the DB."""
    names: list[str] = []
    for status in summary.gql_status_objects:
        if status.gql_status != _UNKNOWN_REL_TYPE_STATUS:
            continue
        m = _UNKNOWN_REL_TYPE_RE.search(status.status_description)
        # Keep the warning visible even if Neo4j rewords the description.
        name = m.group(1) if m else "<unparsed>"
        if name not in names:
            names.append(name)
    return names


async def _run_query(tx, cypher: str, params: dict):
    result = await tx.run(cypher, params)
    records = []
    async for record in result:
        records.append(record.data())
    summary = await result.consume()
    return records, unknown_relationship_types(summary)


async def read_query_with_unknown_types(
    cypher: str, params: dict | None = None
) -> tuple[list[dict], list[str]]:
    """Run a read-only query; also return relationship types Neo4j does not know."""
    driver = await _get_driver()
    async with driver.session(database=NEO4J_DATABASE) as session:
        return await session.execute_read(_run_query, cypher, params or {})


async def read_query(cypher: str, params: dict | None = None) -> list[dict]:
    """Execute a read-only Cypher query and return results as list of dicts."""
    rows, _ = await read_query_with_unknown_types(cypher, params)
    return rows


async def relationship_types() -> list[str]:
    """All relationship types present in the database, sorted."""
    rows = await read_query(
        "CALL db.relationshipTypes() YIELD relationshipType "
        "RETURN relationshipType ORDER BY relationshipType"
    )
    return [r["relationshipType"] for r in rows]


async def close():
    """Close the driver connection."""
    global _driver
    if _driver is not None:
        await _driver.close()
        _driver = None
        log.info("Neo4j driver closed")
