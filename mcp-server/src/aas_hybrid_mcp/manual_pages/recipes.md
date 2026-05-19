# Worked recipes

Starting points for common patterns — adapt to your specific data model.
Each recipe assumes you have already called `get_templates_index()`.

## Recipe A — Container traversal (contained assets)

A container AAS has a submodel whose template describes an Entity
hierarchy, each linked to `:Asset` via `REPRESENTS_ASSET`. Custom
templates use project-specific URIs — the pattern is the same.

1. Find the container submodel via `get_templates_index()` or by
   listing semanticIds on the shell.
2. Traverse the Entity tree:

```cypher
MATCH (container:AssetAdministrationShell)-[:HAS_SUBMODEL]->(sm:Submodel)
      -[:HAS_SEMANTIC_ID]->(:SemanticConcept {id: $containerTemplateSemanticId})
MATCH (sm)-[:HAS_ELEMENT*]->(parent:Entity)
MATCH (parent)-[:HAS_ELEMENT]->(child:Entity)
MATCH (child)-[:REPRESENTS_ASSET]->(asset:Asset)
RETURN container.idShort, parent.idShort, child.idShort, asset.globalAssetId
```

If the nesting is flat (no parent/child), skip the intermediate
`parent:Entity` step:

```cypher
MATCH (sm)-[:HAS_ELEMENT*]->(e:Entity)
MATCH (e)-[:REPRESENTS_ASSET]->(a:Asset)
RETURN e.idShort, a.globalAssetId
```

## Recipe B — Instance → Type → Documentation

Product-level documentation often lives on the *type* AAS;
instance-specific data live on the *instance*.

```cypher
MATCH (instance:AssetAdministrationShell {id: $instanceId})
      -[:DERIVED_FROM]->(type:AssetAdministrationShell)
RETURN type.id, type.idShort
```

Then find the relevant submodel on the type shell via its template's
semanticId (discovered through `get_templates_index()`).

## Recipe C — Semantic property lookup (domain question → template → value)

Use this when the question implies a known data category (speed, weight,
payload, operating range, …). Identify the relevant template from
`get_templates_index()` **before** querying — then navigate directly to
the value. Never dump all shells first.

**Case 1 — Asset named explicitly** (e.g. "Wie schnell kann der MiR100 fahren?")

The user supplies a name, but idShorts are internal graph values — the user's
term is rarely the exact idShort. Always discover the exact idShort first:

```cypher
MATCH (aas:AssetAdministrationShell)
RETURN aas.idShort, aas.id
ORDER BY aas.idShort
```

Do this **once**. Pick the shell whose idShort matches the user's intent.
Then run the combined query with the discovered idShort:

```cypher
MATCH (aas:AssetAdministrationShell {idShort: $exactIdShort})
      -[:HAS_SUBMODEL]->(sm:Submodel)
      -[:HAS_SEMANTIC_ID]->(sc:SemanticConcept {id: $templateSemanticId})
MATCH (sm)-[:HAS_ELEMENT*]->(p:Property)
WHERE p.idShort IN $propertyIdShorts
RETURN aas.idShort, p.idShort, p.value, p.valueType
```

`$exactIdShort` → the idShort you found in the inventory above.
`$templateSemanticId` → from `get_templates_index()`.
`$propertyIdShorts` → from `get_template(name)`.

Do **not** add a separate submodel-listing step after the inventory —
go directly to the combined query.

**Case 2 — No asset named** (e.g. "Welcher Roboter ist der schnellste?")

Find all shells that carry the relevant submodel template, then read and rank:

```cypher
MATCH (aas:AssetAdministrationShell)
      -[:HAS_SUBMODEL]->(sm:Submodel)
      -[:HAS_SEMANTIC_ID]->(sc:SemanticConcept {id: $templateSemanticId})
MATCH (sm)-[:HAS_ELEMENT*]->(p:Property {idShort: $propertyIdShort})
RETURN aas.idShort, p.value
ORDER BY toFloat(p.value) DESC
```

**Do not use CONTAINS or =~ on idShort/id** — see cypher.md anti-patterns
#3 and #4. If the user gives you a name, it is the exact idShort; use `=`.

## Recipe D — Diagnostics: "What's on this shell?"

When you have an AAS ID but don't know what submodels it exposes:

```cypher
MATCH (aas:AssetAdministrationShell {id: $aasId})-[:HAS_SUBMODEL]->(sm:Submodel)
OPTIONAL MATCH (sm)-[:HAS_SEMANTIC_ID]->(sc:SemanticConcept)
RETURN sm.idShort, sm.id, sc.id AS templateSemanticId
```

Look up each semanticId in `get_templates_index()` to learn its purpose.

**Next:** `get_manual_page("troubleshooting")` if any step returned zero rows.
