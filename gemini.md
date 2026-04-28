Project: Semantic-Guided RAG for Industrial Incident Management
1. Core Architecture (The Stack)
AAS (BaSyx): Der "Single Source of Truth" für Asset-Strukturen (V3.0, JSON).
Neo4j (Knowledge Graph): Speichert Relationen (Asset ↔ Standort ↔ Capability ↔ SubmodelID).
Weaviate (Vector DB):
Collection 1 (Chunks): Handbuch-Texte aus MinIO (Metadaten: page, source_file, image_link, submodelId).
Collection 2 (AAS-Semantics): idShorts, Descriptions und MultiLanguageProperties der AAS für semantische Suche.
MinIO: S3-Speicher für die Original-PDFs und Bilder.
MCP (Model Context Protocol): Schnittstelle zwischen LLM und Infrastruktur.
Tools: Generisches AAS-Update-Tool (JSON-Patch).
Resources: AAS-Templates für Incident-Reports (JSON).
2. Entry Points (Discovery)
Deterministic: QR-Code Scan liefert direkt die AAS-ID (High-Speed/Robust).
Semantic Reasoning: Anfrage wie „Transportroboter in Halle 4“ wird via Neo4j-Cypher-Query auf die exakte AAS-ID aufgelöst (Capability + Location).
3. The "Closed-Loop" Workflow
Identify: Agent ermittelt Asset und relevante submodelIds via Neo4j.
Retrieve: Gezieltes RAG in Weaviate mit Pre-Filtering auf die submodelId (verhindert Halluzinationen/falsche Handbücher).
Analyze: Agent nutzt Text-Chunks und referenziert Bilder/Seiten via MinIO-Links.
Report: Agent befüllt ein Incident-Report-Template (MCP Resource) und pusht es via MCP-Tool zurück in die BaSyx-AAS.
4. Key Features for the Paper
V3.0 Compliance: Wegfall der category, stattdessen Nutzung von supplementalSemanticIds für DFKI-spezifische URIs (Hybrid-Semantik).
VDI 2860 Integration: Fachlich fundierte ConceptDescriptions für Capabilities (Handling, Assembly, Transport).
Explainable AI (XAI): Quellenangaben und Bild-Referenzen direkt aus den Vektor-Metadaten.
Asynchronous Pipeline: Kafka-Connect für automatisches Embedding bei AAS-Registrierung.
5. Future Work
Multimodality: Direkte Identifikation von Assets via Foto (CLIP-Embedding in Weaviate).
Automated Enrichment: Agent findet fehlende technische Daten im Handbuch und schlägt AAS-Updates vor.



Ergänzung vielleicht auch einfach future work:

RAG-Integration von MLPs: In der Weaviate-Collection AAS-Semantics werden nicht nur die Descriptions der ConceptDescriptions indiziert, sondern auch die Inhalte der MultiLanguageProperties aus den Submodels (z.B. dein Kommentar zur Nutzlast des MiR100).
Vorteil: Der Agent hat Zugriff auf "Short-Facts". Wenn der Werker fragt: "Wie viel kann der Roboter tragen?", muss der Agent nicht das 200-seitige PDF durchsuchen, sondern findet den Vektor der MLP direkt im Submodel – das ist schneller, präziser und spart Tokens.
Metadaten-Link: Jeder MLP-Chunk in Weaviate erhält einen Link zurück zur exakten submodelElementPath, damit der Agent weiß, aus welchem Feld die Info stammt.
