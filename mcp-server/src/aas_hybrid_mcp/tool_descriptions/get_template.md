Return the element structure of a specific IDTA submodel template:
modelType, idShort, semanticId, and nesting of child elements.

Call this before writing a submodel that should conform to a published
template, or to learn which child idShorts to traverse in a graph query.

Pass the template name as returned by `get_templates_index()`
(e.g. `Nameplate`, `HandoverDocumentation`, `ServiceRequestNotification`).
