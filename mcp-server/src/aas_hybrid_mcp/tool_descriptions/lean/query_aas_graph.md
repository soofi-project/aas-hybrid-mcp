Execute a read-only Cypher query against the AAS graph (Neo4j).
INPUT: `cypher` (str, `$name` placeholders), `params` (dict, optional).
OUTPUT: `rows` (list of dicts, capped at 1000), `total`, `truncated`. Write operations are rejected; a rejected or failed query returns `error`. `_warnings` (optional) flags unknown relationship types, labels or property keys (with the known ones) and other Neo4j notices; read it when a result is empty or unexpected.
