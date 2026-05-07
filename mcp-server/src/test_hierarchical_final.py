"""Test script for HierarchicalStructures traversal."""

import sys
sys.path.insert(0, '.')

import asyncio
import json

from aas_hybrid_mcp.neo4j_client import read_query, close


async def main():
    # Corrected query - uses Entity nodes and REPRESENTS_ASSET relationship
    query = """
    MATCH (sm:Submodel)-[:HAS_SEMANTIC_ID]->(:SemanticConcept {id: $hsSemId})
    MATCH (aas:AssetAdministrationShell)-[:HAS_SUBMODEL]->(sm)
    MATCH (sm)-[:HAS_ELEMENT]->(entry:Entity {idShort: 'EntryNode'})
    MATCH (entry)-[:HAS_ELEMENT]->(child:Entity)-[:REPRESENTS_ASSET]->(asset:Asset)
    WHERE child.idShort IN $hallNames OR aas.idShort IN $hallNames
    RETURN DISTINCT aas.id AS aasId,
                    aas.idShort AS aasIdShort,
                    aas.idShort AS hall,
                    asset.globalAssetId AS assetId,
                    asset.idShort AS assetIdShort,
                    labels(asset) AS assetLabels
    ORDER BY hall, aasIdShort, assetIdShort
    """

    params = {
        "hsSemId": "https://admin-shell.io/idta/HierarchicalStructures/1/1",
        "hallNames": ["Hall3", "Hall4"]
    }

    print("=" * 80)
    print("Running corrected query for HierarchicalStructures traversal")
    print("=" * 80)
    
    results = await read_query(query, params)
    
    print(f"\n1. Rows returned: {len(results)}")
    
    if len(results) > 0:
        print("\n2. First 5 rows as JSON:")
        for row in results[:5]:
            print(json.dumps(row, indent=2))
    else:
        print("\n3. No results returned")
    
    await close()


if __name__ == "__main__":
    asyncio.run(main())
