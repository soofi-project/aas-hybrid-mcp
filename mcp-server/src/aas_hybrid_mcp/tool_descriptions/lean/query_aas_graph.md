Execute a read-only Cypher query against the AAS graph (Neo4j).
INPUT: `cypher` (str, `$name` placeholders), `params` (dict, optional).
OUTPUT: `rows` (list of dicts, capped at 1000), `total`, `truncated`. Write operations are rejected; a rejected or failed query returns `error`.
