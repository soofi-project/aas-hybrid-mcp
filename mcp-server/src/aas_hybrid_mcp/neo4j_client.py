"""Async Neo4j driver wrapper (read-only transactions)."""

import logging
import os

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


async def _run_query(tx, cypher: str, params: dict):
    result = await tx.run(cypher, params)
    records = []
    async for record in result:
        records.append(record.data())
    return records


async def read_query(cypher: str, params: dict | None = None) -> list[dict]:
    """Execute a read-only Cypher query and return results as list of dicts."""
    driver = await _get_driver()
    async with driver.session(database=NEO4J_DATABASE) as session:
        return await session.execute_read(_run_query, cypher, params or {})


async def close():
    """Close the driver connection."""
    global _driver
    if _driver is not None:
        await _driver.close()
        _driver = None
        log.info("Neo4j driver closed")
