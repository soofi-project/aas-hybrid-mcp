# IDTA template workflow

User questions almost always map to a domain concept — location,
containment, capability, contact information, maintenance schedule,
certificates, technical data, … The answer lives in a submodel that
conforms to a specific IDTA template. Your job is to translate user
intent → template → semanticId → graph traversal. Don't invent ad-hoc
Cypher patterns and don't recall semanticIds from training memory.

## Three-step lookup

1. **Skim `get_templates_index()`** for templates whose description
   matches the user's concept. The index is the ground truth for which
   templates exist and what their `semanticId` is.
2. **Confirm against the graph.** Submodels are not labelled by their
   template — only the relation
   `-[:HAS_SEMANTIC_ID]->(:SemanticConcept {id: ...})` proves
   conformance. List the actual semanticIds with the discovery query in
   `get_manual_page("cypher")` if the index ID does not match anything.
3. **Read `get_template(name)`** when you need the field-level
   structure (which child idShorts to expect, their nesting) before
   composing the traversal into the submodel's elements.

## ZVEI vs IDTA — the graph may not use IDTA's IDs

Several legacy templates use ZVEI URIs even when IDTA has published an
equivalent template. The most common case is Nameplate: the IDTA
templates index lists
`https://admin-shell.io/idta/nameplate/3/0/Nameplate`, but a graph
populated from older AASX files may carry
`https://admin-shell.io/zvei/nameplate/2/0/Nameplate` instead. Filtering
on the IDTA-3.0 ID returns zero rows.

When this happens, do NOT conclude the data is absent. Run the
discovery query and use whatever semanticId the graph actually carries:
```cypher
MATCH (sm:Submodel)-[:HAS_SEMANTIC_ID]->(sc:SemanticConcept)
RETURN DISTINCT sc.id ORDER BY sc.id
```

## When no template matches

A custom `semanticId` in the data is the AAS ecosystem's escape hatch
for concepts not yet standardised — finding one confirms the data is
correctly modelled, not that data is missing. State the gap explicitly:
name which template domains *do* exist, name which template you looked
for, and offer the closest matches.

## IDTA vs custom templates

The `get_templates_index()` tool returns **IDTA** templates only. Your
graph may also contain **custom templates** with project-specific
semanticIds (e.g. `urn:custom:dfki:facility-information:1/0`).

To discover all templates (IDTA + custom) in your graph:

```cypher
MATCH (sm:Submodel)-[:HAS_SEMANTIC_ID]->(sc:SemanticConcept)
RETURN DISTINCT sc.id ORDER BY sc.id
```

Custom templates work exactly like IDTA templates — use their semanticId
to find AAS shells that expose them, then traverse their element tree.

**Next:** `get_manual_page("cypher")` for the actual traversal patterns;
`get_manual_page("recipes")` for end-to-end worked examples (including
Recipe A-alt for custom templates).
