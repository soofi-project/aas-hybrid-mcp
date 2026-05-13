# AAS → Graph mapping

How each AAS model class maps to graph node labels, properties, and
relationship types. Use this to understand where data lives and how to
traverse it.

## Common labels

Every node carries `:GraphNode`. Referable nodes add `:Referable` /
`:Referenceable`; identifiable nodes add `:Identifiable` on top.

Every SubmodelElement gets `:SubmodelElement` plus its concrete type
label (e.g. `:Property`, `:Entity`, `:Operation`).

## Top-level relationships

| AAS field | Relationship | Target |
|---|---|---|
| `assetInformation` | `MANAGES_ASSET` | `:Asset` |
| `submodels` | `HAS_SUBMODEL` | `:Submodel` |
| `derivedFrom` | `DERIVED_FROM` | `:AssetAdministrationShell` |
| `administration` | `HAS_ADMIN_INFO` | `:AdminInfo` |

## SubmodelElement containment

| AAS element | Field | Relationship | Notes |
|---|---|---|---|
| Submodel | `submodelElements` | `HAS_ELEMENT` | Direct children |
| SubmodelElementCollection | `value` | `HAS_ELEMENT` | Nested children |
| SubmodelElementList | `value` | `HAS_ELEMENT` | List items |
| SubmodelElementList | `semanticIdListElement` | `HAS_SEMANTIC_ID_LIST_ELEMENT` | Per-item ref |
| **Entity** | **`statements`** | **`HAS_ELEMENT`** | See Key insight below |
| Entity | `globalAssetId` | `REPRESENTS_ASSET` | → `:Asset` |
| Entity | `entityType` | `.entityType` (property) | Enum as string — only scalar on `:Entity` |
| Entity | `specificAssetIds` | `HAS_SPECIFIC_ASSET_ID` | → `:SpecificAssetId` |
| ReferenceElement | `value` | `HAS_VALUE` | Cross-reference to target node |

**Key insight — Entity.statements shares `HAS_ELEMENT`.** Nested Entity
trees descend via `[:HAS_ELEMENT*]` exactly like other containers.
There is no separate relationship for Entity containment.

**`Entity.globalAssetId` is never a node property on `:Entity`.**
Traverse `[:REPRESENTS_ASSET]->(:Asset)` to read `.globalAssetId`:

```cypher
MATCH (e:Entity)-[:REPRESENTS_ASSET]->(a:Asset)
RETURN e.idShort, a.globalAssetId
```

Matching on `e.globalAssetId` returns `null`.

## Element value access

Values live as either **node properties** (`.value`) or **relationships**.
When `.value` is `null` on an element that should carry content, the
value lives on a relationship — traverse the label that matches the
element type.

| Element type | Value access | What the target carries |
|---|---|---|
| `Property` | `.value` (string) | — |
| `MultiLanguageProperty` | `(el)-[:HAS_VALUE]->(:LangString)` | `.language`, `.text` |
| `File` | `.value` (string), `.contentType` | URL / path |
| `Blob` | `.value` (string), `.contentType` | Base64-encoded binary |
| `Range` | `.min`, `.max`, `.valueType` | — |
| `SubmodelElementCollection` | `(el)-[:HAS_ELEMENT]->(...)` | child elements |
| `SubmodelElementList` | `(el)-[:HAS_ELEMENT]->(...)` | list items; also `.orderRelevant` (bool) |
| `ReferenceElement` | `(el)-[:HAS_VALUE]->(target)` | referenced node |
| `RelationshipElement` | `(el)-[:HAS_FIRST]->...`<br>`(el)-[:HAS_SECOND]->...` | referenceable nodes |
| `AnnotatedRelationshipElement` | `HAS_FIRST`, `HAS_SECOND`, `HAS_ANNOTATION` | referenceable nodes |
| `Entity` | no scalar `.value`; only `.entityType` | traverse `REPRESENTS_ASSET`, `HAS_ELEMENT` (statements), `HAS_SPECIFIC_ASSET_ID` |
| `Operation` | no scalar value | `HAS_INPUT_VARIABLE`, `HAS_OUTPUT_VARIABLE`, `HAS_INOUTPUT_VARIABLE` → contained SMEs |
| `BasicEventElement` | no scalar value | `OBSERVES`, `USES_MESSAGE_BROKER` → referenceable nodes |

**Operation variables:** wrapped in `OperationVariable`; the `.value`
is extracted, so `HAS_*_VARIABLE` edges point directly to the contained
SubmodelElement (not to an intermediate wrapper).

## Shared metadata (every SubmodelElement)

Applied to all SubmodelElement subtypes:

| AAS field | Relationship |
|---|---|
| `semanticId` | `HAS_SEMANTIC_ID` |
| `supplementalSemanticIds` | `HAS_SUPPLEMENTAL_SEMANTIC_ID` |
| `qualifiers` | `HAS_QUALIFIER` |
| `description` | `HAS_DESCRIPTION` |
| `displayName` | `HAS_DISPLAY_NAME` |
| `extensions` | `HAS_EXTENSION` |
| `embeddedDataSpecifications` | `HAS_EMBEDDED_DATA_SPECIFICATION` |

## Auxiliary nodes

| AAS type | Field | Relationship |
|---|---|---|
| AssetInformation | `specificAssetIds` | `HAS_SPECIFIC_ASSET_ID` |
| AdministrativeInformation | `embeddedDataSpecifications` | `HAS_EMBEDDED_DATA_SPECIFICATION` |
| AdministrativeInformation | `creator` | `CREATED_BY` |
| SpecificAssetId | `externalSubjectId` | `HAS_EXTERNAL_SUBJECT_ID` |
| SpecificAssetId | `semanticId` | `HAS_SEMANTIC_ID` |
| SpecificAssetId | `supplementalSemanticIds` | `HAS_SUPPLEMENTAL_SEMANTIC_ID` |

**Next:** `get_manual_page("cypher")` for traversal patterns and
anti-patterns; `get_graph_schema()` for the complete catalogue.
