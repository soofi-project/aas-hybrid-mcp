Semantic vector search over PDF documents ingested from AAS Submodel File elements.
INPUT: `query` (str), `submodel_id` (required str, the id of the submodel that holds the File element), `limit` (1-50, default 10), `asset_name` (optional str), `doc_language` (optional str).
OUTPUT: `results` (chunk text, `submodel_id`, source filename, page, score, optional `source_md_link`), `total`, `query_rewritten`, `rewritten_query`. An empty result carries a reason (`not_indexed` or `no_match`).
