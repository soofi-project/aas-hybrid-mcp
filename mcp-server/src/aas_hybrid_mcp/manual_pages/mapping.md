# AAS → Graph mapping

How each AAS model class maps to graph node labels, properties, and
relationship types. Use this to understand where data lives and how to
traverse it.

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
| Entity | `globalAssetId` | `REPRESENTS_ASSET` | → :Asset |
| ReferenceElement | `value` | `HAS_VALUE` | Cross-reference |

**Key insight — Entity.statements shares `HAS_ELEMENT`.** Nested Entity
trees descend via `[:HAS_ELEMENT*]` just like other containers. There
is no separate relationship for Entity containment.

**`Entity.globalAssetId` is never a node property on `:Entity`.**
Traverse `[:REPRESENTS_ASSET]->(:Asset)` to read `.globalAssetId`.

## Element value access

Values live as either **node properties** (`.value`) or **relationships**.
When `.value` is `null`, check the relationship for the element type.

| Element type | Value access |
|---|---|
| `Property` | `.value` (string) |
| `MultiLanguageProperty` | `(el)-[:HAS_VALUE]->(:LangString)` — `.language`, `.text` |
| `File` / `Blob` | `.value`, `.contentType` |
| `SubmodelElementCollection` / `SubmodelElementList` | `(el)-[:HAS_ELEMENT]->(...)` |
| `ReferenceElement` | `(el)-[:HAS_VALUE]->(target)` |
| `RelationshipElement` | `HAS_FIRST`, `HAS_SECOND` |
| `Entity` | no `.value`; traverse `REPRESENTS_ASSET`, `HAS_ELEMENT`, `HAS_SPECIFIC_ASSET_ID` |
| `Operation` | `HAS_INPUT_VARIABLE`, `HAS_OUTPUT_VARIABLE`, `HAS_INOUTPUT_VARIABLE` |

Every SubmodelElement carries metadata via its own relationships:
`HAS_SEMANTIC_ID`, `HAS_SUPPLEMENTAL_SEMANTIC_ID`, `HAS_QUALIFIER`,
`HAS_DESCRIPTION`, `HAS_DISPLAY_NAME`, `HAS_EXTENSION`,
`HAS_EMBEDDED_DATA_SPECIFICATION`.

**Next:** `get_manual_page("cypher")` for traversal patterns;
`get_graph_schema()` for the complete node/relationship catalogue.
