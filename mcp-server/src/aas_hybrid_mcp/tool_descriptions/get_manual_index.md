Return the operator manual index — a routing page that lists every
sub-page (`cypher`, `templates`, `writing`, `troubleshooting`, `recipes`, `mapping`)
together with the four rules that catch the most failures.

Call once per session before your first graph query or write to learn what
the manual covers, then fetch specific sub-pages with
`get_manual_page(page=...)` on demand. Key sub-pages:
- `cypher` — **before any `query_aas_graph` call**
- `writing` — **before any `put_*` / `delete_*` call**
- `templates` — **before looking up or writing a template-conformant submodel**
