"""MCP resource: AAS graph schema documentation."""

from mcp.server.fastmcp import FastMCP

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
An entity with statements and optional asset representation.
- Additional Properties: `entityType`
- Additional Relationships:
  - `-[:HAS_STATEMENT]->(:SubmodelElement)`
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
Entities: `HAS_STATEMENT`
Data specs: `HAS_EMBEDDED_DATA_SPECIFICATION`, `HAS_DATA_SPECIFICATION`, `HAS_DEFINITION`, `HAS_PREFERRED_NAME`, `HAS_SHORT_NAME`, `HAS_ALLOWED_VALUE`
Other: `DEPLOYED_IN`, `CREATED_BY`, `REFERS_TO`

## Traversal Tips

Use `[:HAS_ELEMENT*]` for transitive traversal of nested SubmodelElement hierarchies.

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
"""


def register(mcp: FastMCP) -> None:
    """Register AAS schema resource."""

    @mcp.resource("aas://schema/graph")
    def get_graph_schema() -> str:
        """AAS Neo4j graph schema: all node labels, relationships, properties, and example Cypher queries."""
        return _GRAPH_SCHEMA
