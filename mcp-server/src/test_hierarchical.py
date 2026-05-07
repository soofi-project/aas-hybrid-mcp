"""Test script for HierarchicalStructures traversal."""

import sys
sys.path.insert(0, '.')

import asyncio
import json

from aas_hybrid_mcp.neo4j_client import read_query, close


async def main():
    # Original query
    query1 = """
    MATCH (sm:Submodel)-[:HAS_SEMANTIC_ID]->(:SemanticConcept {id: $hsSemId})
    MATCH (aas:AssetAdministrationShell)-[:HAS_SUBMODEL]->(sm)
    MATCH (sm)-[:HAS_ELEMENT*]->(hall:ReferenceElement)-[:HAS_VALUE]->(hallNode)
    WHERE hallNode.idShort IN $hallNames
    MATCH (hallNode)-[:HAS_ELEMENT*]->(ref:ReferenceElement)-[:HAS_VALUE]->(asset)
    RETURN DISTINCT aas.id AS aasId,
                    aas.idShort AS aasIdShort,
                    hallNode.idShort AS hall,
                    asset.id AS assetId,
                    asset.idShort AS assetIdShort,
                    labels(asset) AS assetLabels
    ORDER BY hall, aasIdShort, assetIdShort
    """

    params = {
        "hsSemId": "https://admin-shell.io/idta/HierarchicalStructures/1/1/Submodel",
        "hallNames": ["Hall3", "Hall4"]
    }

    print("=" * 80)
    print("Running original query...")
    print("=" * 80)
    
    results = await read_query(query1, params)
    
    print(f"\nRows returned: {len(results)}")
    
    if len(results) > 0:
        print("\nFirst 5 rows as JSON:")
        for row in results[:5]:
            print(json.dumps(row, indent=2))
    else:
        print("\nNo results. Trying alternative query...")
        print("\nStep 1: Find submodels with HierarchicalStructures semanticId")
        
        query2 = """
        MATCH (sm:Submodel)-[:HAS_SEMANTIC_ID]->(sc:SemanticConcept)
        WHERE sc.id = $hsSemId
        RETURN sm.id AS submodelId, sm.idShort AS submodelIdShort, sc.id AS semanticId
        """
        
        submodels = await read_query(query2, params)
        print(f"Found {len(submodels)} submodels with HierarchicalStructures")
        for sm in submodels:
            print(f"  - {sm['submodelId']} (idShort: {sm['submodelIdShort']})")
        
        if len(submodels) > 0:
            print("\nStep 2: Examine structure of first submodel")
            
            # Get the submodel structure
            query3 = """
            MATCH (sm:Submodel {id: $smId})-[:HAS_ELEMENT]->(elem)
            RETURN elem.idShort AS elementIdShort, 
                   labels(elem) AS elementLabels,
                   elem.modelType AS modelType
            """
            
            submodel_params = {"smId": submodels[0]['submodelId']}
            elements = await read_query(query3, submodel_params)
            
            print(f"\nTop-level elements of submodel {submodels[0]['submodelId']}:")
            for elem in elements:
                print(f"  - {elem['elementIdShort']} ({elem['elementLabels']}, {elem.get('modelType', 'N/A')})")
                
                # If it's a ReferenceElement, trace the path further
                if 'ReferenceElement' in elem['elementLabels']:
                    query4 = """
                    MATCH (sm:Submodel {id: $smId})-[:HAS_ELEMENT]->(:ReferenceElement {idShort: $elemId})-[:HAS_VALUE]->(node)
                    RETURN node.idShort AS nodeIdShort, labels(node) AS nodeLabels, node.modelType AS nodeModelType
                    """
                    node_params = {"smId": submodels[0]['submodelId'], "elemId": elem['elementIdShort']}
                    nodes = await read_query(query4, node_params)
                    
                    for node in nodes:
                        print(f"    -> {node['nodeIdShort']} ({node['nodeLabels']}, {node.get('nodeModelType', 'N/A')})")
                        
                        # Try to go one level deeper
                        if 'Entity' in node['nodeLabels'] or 'Asset' in node['nodeLabels']:
                            query5 = """
                            MATCH (sm:Submodel {id: $smId})-[:HAS_ELEMENT]->(:ReferenceElement {idShort: $elemId})-[:HAS_VALUE]->(:Entity {idShort: $nodeId})-[:HAS_ELEMENT]->(child)
                            RETURN child.idShort AS childIdShort, labels(child) AS childLabels
                            """
                            child_params = {"smId": submodels[0]['submodelId'], "elemId": elem['elementIdShort'], "nodeId": node['nodeIdShort']}
                            children = await read_query(query5, child_params)
                            
                            print(f"      Children of {node['nodeIdShort']}:")
                            for child in children:
                                print(f"        - {child['childIdShort']} ({child['childLabels']})")


if __name__ == "__main__":
    asyncio.run(main())
