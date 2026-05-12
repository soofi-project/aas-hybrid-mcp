# AASX field → Neo4j graph mapping

How each AAS model class maps to Neo4j node labels, node properties, and
relationship types. Use this to understand where data lives and how to
traverse it.

## Common labels

Every node carries `:GraphNode`. Referable nodes add `:Referable`,
`:Referenceable`. Identifiable nodes add `:Identifiable` on top.

Every SubmodelElement gets `:SubmodelElement` plus its concrete type label
(e.g. `:Property`, `:Entity`, `:Operation`).

## Top-level nodes

| AAS Type | JSON/Java field | Neo4j relationship | Target |
|---|---|---|---|
| AssetAdministrationShell | `assetInformation` | `MANAGES_ASSET` | `:Asset` |
| | `submodels` | `HAS_SUBMODEL` | `:Submodel` |
| | `derivedFrom` | `DERIVED_FROM` | `:AssetAdministrationShell` |
| | `administration` | `HAS_ADMIN_INFO` | `:AdminInfo` |

## SubmodelElements — containment slots

These are the source of the most traversal bugs. Read the **Key insight**
below carefully.

| AAS Type | JSON/Java field | Neo4j relationship | Notes |
|---|---|---|---|
| Submodel | `submodelElements` | `HAS_ELEMENT` | Direct children only |
| SubmodelElementCollection | `value` | `HAS_ELEMENT` | Nested child elements |
| SubmodelElementList | `value` | `HAS_ELEMENT` | List items |
| SubmodelElementList | `semanticIdListElement` | `HAS_SEMANTIC_ID_LIST_ELEMENT` | Per-item semantic ref |
| **Entity** | **`statements`** | **`HAS_ELEMENT`** | **Child entities — see Key insight** |
| Entity | `globalAssetId` | `REPRESENTS_ASSET` | `:Asset` (from the ID string) |
| Entity | `entityType` | `.entityType` (property) | Enum as string — the **only** scalar value on `:Entity` |
| Entity | `specificAssetIds` | `HAS_SPECIFIC_ASSET_ID` | `:SpecificAssetId` |
| ReferenceElement | `value` | `HAS_VALUE` | Cross-reference to target node |

**`Entity.globalAssetId` is never a node property on `:Entity`.**
It is mapped purely as a `[:REPRESENTS_ASSET]` relationship to the
`:Asset` node.  The actual `globalAssetId` string lives on the `:Asset`
node as `.globalAssetId`.  To resolve an Entity to its asset ID, always
traverse:
 
 ```cypher
 MATCH (e:Entity)-[:REPRESENTS_ASSET]->(a:Asset)
 RETURN e.idShort, a.globalAssetId
 ```

Never match on `e.globalAssetId` — it will be `null`.

### Key insight — Entity.statements is HAS_ELEMENT

Entity.statements is mapped to the **same relationship label** as
SubmodelElementCollection children and SubmodelElementList items:
`HAS_ELEMENT`. This means that `[:HAS_ELEMENT*]` descends through
nested Entity trees seamlessly. There is no separate relationship for
Entity containment.

**Example — container AAS with an Entity tree (generic):**

Any container-style submodel that contains entities for contained assets.
First, discover which submodel template carries the containment structure
via `get_templates_index()` and `get_template(name)`, then determine the
Entity idShorts from `get_template(name)` — they vary by template:

```cypher
// Identify the container template semanticId via get_templates_index()
// Determine entity nesting from get_template(name)
MATCH (container:AssetAdministrationShell)-[:HAS_SUBMODEL]->(sm:Submodel)
      -[:HAS_SEMANTIC_ID]->(:SemanticConcept {id: $containerTemplateSemanticId})
MATCH (sm)-[:HAS_ELEMENT*]->(parent:Entity)
MATCH (parent)-[:HAS_ELEMENT]->(child:Entity)
MATCH (child)-[:REPRESENTS_ASSET]->(asset:Asset)
RETURN container.idShort, parent.idShort, child.idShort, asset.globalAssetId
```

If the submodel contains only top-level entities (no parent/child nesting),
skip the intermediate `parent:Entity` step:

```cypher
MATCH (sm:Submodel)-[:HAS_SEMANTIC_ID]->(:SemanticConcept {id: $containerTemplateSemanticId})
MATCH (sm)-[:HAS_ELEMENT*]->(e:Entity)
MATCH (e)-[:REPRESENTS_ASSET]->(a:Asset)
RETURN e.idShort, a.globalAssetId
```

## SubmodelElement value access

Each AAS SubmodelElement type maps its value-carrying fields to either
**Neo4j node properties** (`.value`) or **relationships**
(`[:HAS_VALUE]`, `[:HAS_ELEMENT]`, …). The table below is exhaustive —
derived from the connector's `*Node` mappers.

> **When you see `value: null` on a node that's supposed to carry content,
> the value lives on a relationship, not as a property.**
> Check which relationship label applies to the element's type and traverse it.

| AAS type (Neo4j label) | Value access | What the target carries |
|---|---|---|
| `Property` | `.value` (string) | — |
| `MultiLanguageProperty` | `(el)-[:HAS_VALUE]->(:LangString)` | `.language`, `.text` |
| `File` | `.value` (string), `.contentType` | URL/path |
| `Blob` | `.value` (string), `.contentType` | Base64-encoded binary |
| `Range` | `.min`, `.max`, `.valueType` | — |
| `SubmodelElementCollection` | `(el)-[:HAS_ELEMENT]->(...)` | child elements |
| `SubmodelElementList` | `(el)-[:HAS_ELEMENT]->(...)` | list items; also `.orderRelevant` (boolean) |
| `ReferenceElement` | `(el)-[:HAS_VALUE]->(targetNode)` | referenced node |
| `RelationshipElement` | `(el)-[:HAS_FIRST]->...`<br>`(el)-[:HAS_SECOND]->...` | referenceable nodes |
| `AnnotatedRelationshipElement` | `HAS_FIRST`, `HAS_SECOND`, `HAS_ANNOTATION` | referenceable nodes |
| `Entity` | no scalar `.value`; only `.entityType` | traverse `REPRESENTS_ASSET`, `HAS_ELEMENT` (statements), `HAS_SPECIFIC_ASSET_ID` |
| `Operation` | no scalar value | `HAS_INPUT_VARIABLE`, `HAS_OUTPUT_VARIABLE`, `HAS_INOUTPUT_VARIABLE` → contained SMEs |
| `BasicEventElement` | no scalar value | `OBSERVES`, `USES_MESSAGE_BROKER` → referenceable nodes |

**Operation variables:** wrapped in `OperationVariable` — the connector
extracts `.value` from each, so `HAS_*_VARIABLE` edges point directly
to the contained SubmodelElement.

## Shared metadata (every SubmodelElement)

Applied automatically by `AbstractSmeNode` — inherited by all SME types:

| JSON/Java field | Neo4j relationship |
|---|---|
| `semanticId` | `HAS_SEMANTIC_ID` |
| `supplementalSemanticIds` | `HAS_SUPPLEMENTAL_SEMANTIC_ID` |
| `qualifiers` | `HAS_QUALIFIER` |
| `description` | `HAS_DESCRIPTION` |
| `displayName` | `HAS_DISPLAY_NAME` |
| `extensions` | `HAS_EXTENSION` |
| `embeddedDataSpecifications` | `HAS_EMBEDDED_DATA_SPECIFICATION` |

## Auxiliary nodes

| AAS Type | JSON field | Neo4j relationship |
|---|---|---|
| AssetInformation | `specificAssetIds` | `HAS_SPECIFIC_ASSET_ID` |
| AdministrativeInformation | `embeddedDataSpecifications` | `HAS_EMBEDDED_DATA_SPECIFICATION` |
| AdministrativeInformation | `creator` | `CREATED_BY` |
| SpecificAssetId | `externalSubjectId` | `HAS_EXTERNAL_SUBJECT_ID` |
| SpecificAssetId | `semanticId` | `HAS_SEMANTIC_ID` |
| SpecificAssetId | `supplementalSemanticIds` | `HAS_SUPPLEMENTAL_SEMANTIC_ID` |

**Next:** `get_manual_page("cypher")` for traversal patterns and anti-patterns;
`get_graph_schema()` for the complete node/relationship catalogue.
