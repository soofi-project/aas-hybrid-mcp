**Before calling: obtain the exact template name from `get_templates_index()` or `search_idta_templates()`** — names must match verbatim (spaces, mixed case). Example: `"Template Name"`, not `"TemplateName"`.

Return the element structure of a specific IDTA submodel template:
modelType, idShort, semanticId, and nesting of child elements.

Call this before writing a submodel that should conform to a published
template, or to learn which child idShorts to traverse in a graph query.
