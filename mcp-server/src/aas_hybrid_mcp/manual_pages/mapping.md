# AASX field → Neo4j graph mapping

Shows how the Kafka Connect plugin (aas-repository-neo4j-kafka-plugin)
maps each AAS4J type's fields to Neo4j node labels and relationship types.
Derived from the `*Node` mapping classes in the plugin's source code.

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
| Entity | `specificAssetIds` | `HAS_SPECIFIC_ASSET_ID` | `:SpecificAssetId` |
| ReferenceElement | `value` | `HAS_VALUE` | Cross-reference to target node |

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

## Value-bearing elements

| AAS Type | JSON/Java field | Neo4j | Details |
|---|---|---|---|
| Property | `value` | `.value` (property) | Scalar string on the node |
| Property | `valueType` | `.valueType` (property) | |
| Property | `valueId` | `HAS_VALUE_ID` | Reference target |
| MultiLanguageProperty | `value` (LangString[]) | `HAS_VALUE` | `:LangString` (.language, .text) |
| MultiLanguageProperty | `valueId` | `HAS_VALUE_ID` | Reference target |
| File | `value` | `.value` (property) | URL path |
| File | `contentType` | `.contentType` (property) | MIME type |
| Blob | `value` | `.value` (property) | Base64-encoded |
| Range | `min`, `max` | `.min`, `.max` (property) | |

## Relationship-bearing elements

| AAS Type | JSON/Java field | Neo4j relationship |
|---|---|---|
| RelationshipElement | `first`, `second` | `HAS_FIRST`, `HAS_SECOND` |
| AnnotatedRelationshipElement | `first`, `second` | `HAS_FIRST`, `HAS_SECOND` |
| AnnotatedRelationshipElement | `annotations` | `HAS_ANNOTATION` |
| Operation | `inputVariables` | `HAS_INPUT_VARIABLE` |
| Operation | `outputVariables` | `HAS_OUTPUT_VARIABLE` |
| Operation | `inoutputVariables` | `HAS_INOUTPUT_VARIABLE` |
| BasicEventElement | `observed` | `OBSERVES` |
| BasicEventElement | `messageBroker` | `USES_MESSAGE_BROKER` |

**Note:** Operation variables are wrapped in `OperationVariable` — the
plugin extracts `.value` from each, so the `HAS_*_VARIABLE` edges point
directly to the contained SubmodelElement.

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
