Fuzzy semantic search over IDTA submodel template specifications.
Returns chunks ranked by relevance with template name and source page.

**Use when the template name is unknown** — search by intent
("is there a standardised submodel for service requests?").
For the complete catalogue, prefer `get_templates_index()`.

COMPLEMENTS the deterministic tools:
- `get_templates_index()` — all templates with name/version/semanticId
- `get_template(name)` — one template's element structure
- This tool — fuzzy retrieval when you don't know the name

Use the exact name from search results for `get_template(name)` —
spaces and capitalisation matter.

INPUT: `query` (str), `template_name` (optional str), `limit` (1–50,
default 5).
OUTPUT: `results` list with chunk text and template metadata; `total`
count.
