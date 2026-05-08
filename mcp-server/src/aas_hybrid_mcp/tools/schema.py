"""MCP tool: AAS graph schema documentation."""

from fastmcp import FastMCP

from aas_hybrid_mcp.tool_descriptions import load as load_description

_GRAPH_SCHEMA = """\
# AAS Neo4j Graph Schema

Generated from the Kafka Connect plugin (aas-neo4j-kafka-connect-plugin).
All nodes also carry the label `GraphNode`. Use `get_aas_graph_schema` tool for live schema.

## Core Nodes

### AssetAdministrationShell
The top-level AAS entity.
- Labels: AssetAdministrationShell, Identifiable, Referable, Referenceable
- Properties: `id`, `idShort`, `category`
- Relationships:
  - `-[:MANAGES_ASSET]->(:Asset)`
  - `-[:HAS_SUBMODEL]->(:Submodel)`
  - `-[:DERIVED_FROM]->(:AssetAdministrationShell)` (type/instance derivation)
  - `-[:HAS_ADMIN_INFO]->(:AdminInfo)`
  - `-[:HAS_DISPLAY_NAME]->(:LangString)`
  - `-[:HAS_DESCRIPTION]->(:LangString)`
  - `-[:HAS_EXTENSION]->(:Extension)`
  - `-[:HAS_EMBEDDED_DATA_SPECIFICATION]->(:DataSpecification)`
  - `-[:DEPLOYED_IN]->(:Repository)`

### Asset
The physical or logical asset managed by an AAS.
- Labels: Asset, Referenceable
- Properties: `globalAssetId`, `assetKind` (Instance/Type), `assetType`
- Relationships:
  - `-[:HAS_SPECIFIC_ASSET_ID]->(:SpecificAssetId)`
  - `-[:DEPLOYED_IN]->(:Repository)`

### Submodel
Groups related SubmodelElements, belongs to an AAS.
- Labels: Submodel, Identifiable, Referable, Referenceable
- Properties: `id`, `idShort`, `category`, `kind`
- Relationships:
  - `-[:HAS_ELEMENT]->(:SubmodelElement)` (direct children)
  - `-[:HAS_SEMANTIC_ID]->(:SemanticConcept|ConceptDescription)`
  - `-[:HAS_SUPPLEMENTAL_SEMANTIC_ID]->(:SemanticConcept)`
  - `-[:HAS_ADMIN_INFO]->(:AdminInfo)`
  - `-[:HAS_DISPLAY_NAME]->(:LangString)`
  - `-[:HAS_DESCRIPTION]->(:LangString)`
  - `-[:HAS_QUALIFIER]->(:Qualifier)`
  - `-[:HAS_EMBEDDED_DATA_SPECIFICATION]->(:DataSpecification)`
  - `-[:DEPLOYED_IN]->(:Repository)`

## SubmodelElement Types

All SubmodelElements share:
- Labels: SubmodelElement, Referable, Referenceable, [ConcreteType]
- Common Properties: `idShort`, `smId`, `idShortPath`, `category`
- Common Relationships:
  - `-[:HAS_SEMANTIC_ID]->(:SemanticConcept)`
  - `-[:HAS_SUPPLEMENTAL_SEMANTIC_ID]->(:SemanticConcept)`
  - `-[:HAS_DESCRIPTION]->(:LangString)`
  - `-[:HAS_DISPLAY_NAME]->(:LangString)`
  - `-[:HAS_QUALIFIER]->(:Qualifier)`
  - `-[:HAS_EXTENSION]->(:Extension)`
  - `-[:HAS_EMBEDDED_DATA_SPECIFICATION]->(:DataSpecification)`

### Property
Key-value data point.
- Additional Properties: `value`, `valueType`
- Additional Relationships: `-[:HAS_VALUE_ID]->(reference)`

### File
Reference to a file (e.g. PDF document).
- Additional Properties: `value` (URL path), `contentType`

### Blob
Binary large object (base64 encoded).
- Additional Properties: `value`, `contentType`

### Range
Numeric range with min/max.
- Additional Properties: `valueType`, `min`, `max`

### MultiLanguageProperty
Multilingual text value.
- Additional Relationships:
  - `-[:HAS_VALUE]->(:LangString)`
  - `-[:HAS_VALUE_ID]->(reference)`

### SubmodelElementCollection
Nested container for SubmodelElements.
- Additional Relationships: `-[:HAS_ELEMENT]->(:SubmodelElement)`

### SubmodelElementList
Ordered list of SubmodelElements.
- Additional Properties: `orderRelevant`
- Additional Relationships:
  - `-[:HAS_ELEMENT]->(:SubmodelElement)`
  - `-[:HAS_SEMANTIC_ID_LIST_ELEMENT]->(reference)`

### ReferenceElement
Cross-reference to another AAS element.
- Additional Relationships: `-[:HAS_VALUE]->(target)`

### RelationshipElement
Directed relationship between two elements.
- Additional Relationships:
  - `-[:HAS_FIRST]->(reference)`
  - `-[:HAS_SECOND]->(reference)`

### AnnotatedRelationshipElement
RelationshipElement with additional annotations.
- Labels: ..., AnnotatedRelationshipElement, RelationshipElement
- Additional Relationships:
  - `-[:HAS_FIRST]->(reference)`
  - `-[:HAS_SECOND]->(reference)`
  - `-[:HAS_ANNOTATION]->(:SubmodelElement)`

### Entity
An entity with statements and optional asset representation. Statements
are exposed as standard `HAS_ELEMENT` children (same as SMC/SML contents),
so transitive `[:HAS_ELEMENT*]` traversal descends through Entity trees
without special-casing.
- Additional Properties: `entityType`
- Additional Relationships:
  - `-[:REPRESENTS_ASSET]->(:Asset)`
  - `-[:HAS_SPECIFIC_ASSET_ID]->(:SpecificAssetId)`

### Operation
An executable operation with input/output variables.
- Additional Relationships:
  - `-[:HAS_INPUT_VARIABLE]->(:SubmodelElement)`
  - `-[:HAS_OUTPUT_VARIABLE]->(:SubmodelElement)`
  - `-[:HAS_INOUTPUT_VARIABLE]->(:SubmodelElement)`

### BasicEventElement
Event source/sink for publish-subscribe.
- Additional Properties: `direction`, `state`, `messageTopic`, `lastUpdate`, `minInterval`, `maxInterval`
- Additional Relationships:
  - `-[:OBSERVES]->(reference)`
  - `-[:USES_MESSAGE_BROKER]->(reference)`

### Capability
Declares a capability (no additional properties or relationships).

## Auxiliary Nodes

### SemanticConcept
Semantic identifier referenced via HAS_SEMANTIC_ID.
- Labels: SemanticConcept, Referenceable
- Properties: `id`

### ConceptDescription
Formal semantic definition (also target of HAS_SEMANTIC_ID from Submodels).
- Labels: ConceptDescription, Identifiable, Referable, Referenceable
- Properties: `id`

### LangString
Multilingual text.
- Properties: `language`, `text`

### AdminInfo
Administrative/versioning metadata.
- Properties: `version`, `revision`, `templateId`
- Relationships:
  - `-[:HAS_EMBEDDED_DATA_SPECIFICATION]->(:DataSpecification)`
  - `-[:CREATED_BY]->(reference)`

### Repository
BaSyx server endpoint.
- Properties: `url`

### SpecificAssetId
Named asset identifier.
- Properties: `name`, `value`
- Relationships:
  - `-[:HAS_EXTERNAL_SUBJECT_ID]->(reference)`
  - `-[:HAS_SEMANTIC_ID]->(reference)`

### Qualifier
Constraint or qualifier on a SubmodelElement.
- Properties: `kind`, `type`, `valueType`, `value`
- Relationships:
  - `-[:HAS_VALUE_ID]->(reference)`
  - `-[:HAS_SEMANTIC_ID]->(reference)`

### Extension
Custom extension data.
- Properties: `name`, `value`, `valueType`
- Relationships:
  - `-[:HAS_SEMANTIC_ID]->(reference)`
  - `-[:REFERS_TO]->(reference)`

### DataSpecification
Embedded data specification (IEC 61360).
- Properties: `sourceOfDefinition`, `value`, `valueFormat`, `symbol`, `unit`, `dataType`, `levelMin`, `levelMax`, `levelNom`, `levelTyp`
- Relationships:
  - `-[:HAS_DATA_SPECIFICATION]->(reference)`
  - `-[:HAS_DEFINITION]->(:LangString)`
  - `-[:HAS_PREFERRED_NAME]->(:LangString)`
  - `-[:HAS_SHORT_NAME]->(:LangString)`
  - `-[:HAS_ALLOWED_VALUE]->(:AllowedValue)`

### AllowedValue
Allowed value in a DataSpecification.
- Properties: `value`
- Relationships: `-[:HAS_VALUE_ID]->(reference)`

## Complete Relationship List

Core traversal: `MANAGES_ASSET`, `HAS_SUBMODEL`, `HAS_ELEMENT`, `DERIVED_FROM`
Semantics: `HAS_SEMANTIC_ID`, `HAS_SUPPLEMENTAL_SEMANTIC_ID`, `HAS_SEMANTIC_ID_LIST_ELEMENT`
Metadata: `HAS_ADMIN_INFO`, `HAS_DESCRIPTION`, `HAS_DISPLAY_NAME`, `HAS_EXTENSION`, `HAS_QUALIFIER`
Values: `HAS_VALUE`, `HAS_VALUE_ID`
Assets: `HAS_SPECIFIC_ASSET_ID`, `REPRESENTS_ASSET`, `HAS_EXTERNAL_SUBJECT_ID`
Relationships: `HAS_FIRST`, `HAS_SECOND`, `HAS_ANNOTATION`
Operations: `HAS_INPUT_VARIABLE`, `HAS_OUTPUT_VARIABLE`, `HAS_INOUTPUT_VARIABLE`
Events: `OBSERVES`, `USES_MESSAGE_BROKER`
Data specs: `HAS_EMBEDDED_DATA_SPECIFICATION`, `HAS_DATA_SPECIFICATION`, `HAS_DEFINITION`, `HAS_PREFERRED_NAME`, `HAS_SHORT_NAME`, `HAS_ALLOWED_VALUE`
Other: `DEPLOYED_IN`, `CREATED_BY`, `REFERS_TO`

## Traversal Tips

`[:HAS_ELEMENT*]` covers all generic containment — Submodel contents,
SubmodelElementCollection / SubmodelElementList children, and Entity
statements. A single transitive walk descends through every nesting
pattern without slot-specific edge knowledge.

The following relations look like containment but use their own edge
labels because the slot carries semantic role information beyond plain
containment:

- `HAS_ANNOTATION` — AnnotatedRelationshipElement annotations
  (DataElement-only, not arbitrary SubmodelElements)
- `HAS_INPUT_VARIABLE` / `HAS_OUTPUT_VARIABLE` / `HAS_INOUTPUT_VARIABLE` —
  Operation parameter slots, direction-typed
- `HAS_FIRST` / `HAS_SECOND` — RelationshipElement endpoints (references,
  not containment)

## Common Anti-Patterns

The following Cypher mistakes look reasonable but silently return zero rows.
Read this section before writing queries.

**1. `Repository` is AAS-storage, not a physical location.**
The `(:Repository)-[:DEPLOYED_IN]` edge points to the *AAS environment* where
a shell is stored (e.g. a BaSyx server URL). It is not a hall, room, or
factory section. Never filter on `Repository.url` to find assets at a
physical location — that information lives in the shell's submodels (e.g.
in submodels conforming to IDTA `HierarchicalStructures` or other
location-bearing templates, surfaced via `HAS_SEMANTIC_ID`).

```cypher
// WRONG — Repository is not a location
MATCH (aas)-[:DEPLOYED_IN]->(:Repository {url: 'hall-4'}) ...

// RIGHT — query the location-bearing submodel by its IDTA semanticId
MATCH (sm:Submodel)-[:HAS_SEMANTIC_ID]->(:SemanticConcept {id: $semanticId})
MATCH (aas:AssetAdministrationShell)-[:HAS_SUBMODEL]->(sm) ...
```

**2. `semanticId` is a relation, not a property.**
Submodels and SubmodelElements do not carry a `semanticId` *property*.
The semantic-id is a relation `-[:HAS_SEMANTIC_ID]->(:SemanticConcept)`.

```cypher
// WRONG — silently returns 0 rows
MATCH (sm:Submodel {semanticId: 'https://...'}) ...

// RIGHT
MATCH (sm:Submodel)-[:HAS_SEMANTIC_ID]->(:SemanticConcept {id: 'https://...'}) ...
```

**3. Use IDTA semanticIds verbatim — do not enrich them.**
IDTA template URIs are published in a specific form (see the
`get_templates_index()` tool). Do not append `/Submodel` or other
suffixes. For example, `HierarchicalStructures` is
`https://admin-shell.io/idta/HierarchicalStructures/1/1` — *not*
`.../1/1/Submodel`.

**4. `assetType` and `assetKind` are optional and often null.**
They are not reliable filters. Type vs. instance is encoded structurally
via `(:AssetAdministrationShell)-[:DERIVED_FROM]->(:AssetAdministrationShell)`;
domain classification (transport robot, welding cell, …) lives in
submodels conforming to capability- or technical-data templates, not in
`assetType`.

**5. Never match by `idShort` — always reason via `semanticId`.**
`idShort` is a free-form local label chosen by the shell author; it is
not a stable semantic identifier and must not be used for domain
classification or capability matching. The semantic meaning of a shell,
submodel, or element is expressed exclusively through
`-[:HAS_SEMANTIC_ID]->(:SemanticConcept)` and
`-[:HAS_SUPPLEMENTAL_SEMANTIC_ID]->(:SemanticConcept)`.
To find what semanticIds exist in the graph, list them:
```cypher
MATCH (sm:Submodel)-[:HAS_SEMANTIC_ID]->(sc:SemanticConcept)
RETURN DISTINCT sc.id ORDER BY sc.id
```
Then match the correct id against the templates index (`get_templates_index()`)
to identify the template — never guess a semanticId from training memory.

For *property-level* semanticIds that are not template ids (e.g. ECLASS
IRDIs like `0173-1#02-ABL884#002`), call `lookup_semantic_id(id)` to
resolve the IEC 61360 ConceptDescription content (preferredName,
definition, dataType, unit). If the lookup returns `resolved=false`, the
IRDI is a standardised external reference whose dictionary content is
not available locally — report this transparently.

## Example Queries

List all AAS with their assets:
```cypher
MATCH (aas:AssetAdministrationShell)-[:MANAGES_ASSET]->(a:Asset)
RETURN aas.idShort, aas.id, a.globalAssetId, a.assetKind
```

Find submodels of an AAS:
```cypher
MATCH (aas:AssetAdministrationShell {idShort: $idShort})-[:HAS_SUBMODEL]->(sm:Submodel)
RETURN sm.idShort, sm.id
```

Find all PDF files linked to an AAS:
```cypher
MATCH (aas:AssetAdministrationShell {id: $aasId})-[:HAS_SUBMODEL]->(sm:Submodel)
      -[:HAS_ELEMENT*]->(f:File)
WHERE f.contentType = 'application/pdf'
RETURN sm.id AS submodelId, f.idShort, f.value
```

Get properties of a submodel:
```cypher
MATCH (sm:Submodel {idShort: $smIdShort})-[:HAS_ELEMENT*]->(p:Property)
RETURN p.idShort, p.value, p.valueType
```

Find elements by semantic concept:
```cypher
MATCH (el:SubmodelElement)-[:HAS_SEMANTIC_ID]->(sc:SemanticConcept {id: $semanticId})
RETURN el.idShort, el.smId, labels(el) AS types
```

Find all operations in an AAS:
```cypher
MATCH (aas:AssetAdministrationShell {id: $aasId})-[:HAS_SUBMODEL]->(sm:Submodel)
      -[:HAS_ELEMENT*]->(op:Operation)
RETURN sm.idShort, op.idShort, op.smId
```

Get entity with its asset representation:
```cypher
MATCH (e:Entity)-[:REPRESENTS_ASSET]->(a:Asset)
RETURN e.idShort, e.entityType, a.globalAssetId
```

Traverse relationships between elements:
```cypher
MATCH (rel:RelationshipElement)-[:HAS_FIRST]->(first)
MATCH (rel)-[:HAS_SECOND]->(second)
RETURN rel.idShort, labels(first), labels(second)
```

Walk from an instance shell to its type shell:
```cypher
MATCH (instance:AssetAdministrationShell {id: $instanceId})
      -[:DERIVED_FROM]->(type:AssetAdministrationShell)
RETURN type.id, type.idShort
```

Find all instance shells derived from a type (reverse of DERIVED_FROM):
```cypher
MATCH (instance:AssetAdministrationShell)-[:DERIVED_FROM]->
      (type:AssetAdministrationShell {idShort: $typeIdShort})
RETURN instance.idShort, instance.id
```

Traverse ReferenceElement containment — a container AAS owns the submodel,
contained assets appear as ReferenceElement values inside it:
```cypher
MATCH (container:AssetAdministrationShell)-[:HAS_SUBMODEL]->(sm:Submodel)
      -[:HAS_SEMANTIC_ID]->(:SemanticConcept {id: $containerTemplateSemanticId})
MATCH (sm)-[:HAS_ELEMENT*]->(ref:ReferenceElement)-[:HAS_VALUE]->(contained)
RETURN container.idShort, contained.idShort, labels(contained) AS containedType
```

Find all submodels conforming to a given IDTA template, across all shells:
```cypher
MATCH (sm:Submodel)-[:HAS_SEMANTIC_ID]->(:SemanticConcept {id: $templateSemanticId})
MATCH (aas:AssetAdministrationShell)-[:HAS_SUBMODEL]->(sm)
RETURN aas.idShort, aas.id, sm.idShort, sm.id
```

List the submodels of a shell with their template's semanticId
(useful to identify what kind of shell you're looking at):
```cypher
MATCH (aas:AssetAdministrationShell {id: $aasId})-[:HAS_SUBMODEL]->(sm:Submodel)
OPTIONAL MATCH (sm)-[:HAS_SEMANTIC_ID]->(sc:SemanticConcept)
RETURN sm.idShort, sm.id, sc.id AS templateSemanticId
```
"""


def register(mcp: FastMCP) -> None:
    """Register the AAS schema tool."""

    @mcp.tool(description=load_description("get_graph_schema"))
    def get_graph_schema() -> str:
        """AAS Neo4j graph schema: all node labels, relationships, properties, and example Cypher queries."""
        return _GRAPH_SCHEMA
