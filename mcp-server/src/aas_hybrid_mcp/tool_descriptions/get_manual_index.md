Return the operator manual index — a routing page that lists every
sub-page (`cypher`, `templates`, `writing`, `troubleshooting`, `recipes`)
together with the four rules that catch the most failures.

Call this once per session to learn what the manual covers, then fetch
specific sub-pages with `get_manual_page(page=...)` on demand.
