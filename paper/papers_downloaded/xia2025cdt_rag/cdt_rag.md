# Robotics and Computer–Integrated Manufacturing 97 (2026) 103105 **==> picture [61 x 67] intention...

Source: xia2025cdt_rag.pdf


---

### Page 2

> _D. Shi et al.                                                                                                                                                                                                                                      Robotics and Computer-Integrated Manufacturing 97 (2026) 103105_ 

prompting introduces intermediate reasoning steps that help decompose complex matching tasks into smaller, more tractable sub-tasks [20]. To further enhance the reliability and scalability of the matching process, we integrate the RAG technique. In real-world production environments, a facility hosts plenty of machines, each represented by a distinct AAS instance. Each AAS instance includes an SM Equipment Capability, containing dozens of capability entities. Given the size of the resulting search space, exhaustive pairwise comparisons between process requirements and capability entities would be impractical. The RAG system addresses this problem by first vectorizing all equipment capability entities in the knowledge base using an embedding model. These embeddings are stored in a vector database. When a requirement entity from an SM Process Segment is provided, the system conducts a similarity-based retrieval to efficiently identify relevant capability entities and thus the suitable equipment type. Afterward, the requirement entities are passed together with the CoT prompt into the LLM-based chat model to derive the required capabilities, which are further matched with equipment capability entities. The key contributions of this paper are as follows: 

- A systematic methodology is proposed to develop and standardize reusable AAS SMTs, drawing upon industry best practices from the AAS community. They form the foundation for interoperable knowledge representation within CDT. 

- PPR-related SMTs are designed to decouple process steps from production resources and to separate the functional roles of production resources from their corresponding physical assets. This separation in the information flow addresses a key requirement of RM. 

- A capability matching mechanism based on CoT-prompting is presented, enabling LLMs to automatically match production processes with suitable production resources. This facilitates intelligent knowledge inference within the CDT framework. 

- An IT architecture is designed and implemented to facilitate process configuration and the dynamic generation of AAS instances. It also hosts the AAS repository as a knowledge base and integrates an RAG system for knowledge retrieval from AAS and response generation for capability matching. 

The remainder of this paper is organized as follows: Section 2 reviews the related work. Section 3 outlines the methodology for developing AAS SMTs and the design of process- and resource-related SMTs. Section 4 introduces the capability matching mechanism and the RAG system. Section 5 presents the case study and evaluation. 

## **2. Related work** 

## _2.1. Knowledge representation and inference for capability matching_ 

CDTs aim to enhance the dynamic, context-aware responsiveness of DTs by incorporating formal knowledge representation and intelligent inference mechanisms, thereby enabling true cognitive capabilities [11–16]. This concept has also been widely used for capability matching in the context of RM [2]. Accordingly, ontologies and KGs, as the core techniques of knowledge representation and inference, are reviewed in this section. 

Ontology, as a Semantic Web technology, provides a framework for modeling domain knowledge through entities, their attributes, and relationships. To represent and store this knowledge, the Resource Description Framework (RDF) is commonly used to express data as – – subject predicate object triples. Building on RDF, the Web Ontology Language (OWL) adds richer semantics for defining classes, entities, and logical constraints [21]. For capability matching, Jarvenp¨ ¨aa et al. [¨ 22] defined ontologies of PPR and equipment capabilities using OWL. These OWL-based ontologies were queried using the SPARQL query language for knowledge inference. The matching process was performed at two levels: the capability name level and the parameter level. For example, 

when a product requires a screwing operation, the term "screwing" is queried within the capability ontology to identify relevant resources. Subsequently, technical parameters such as torque and screw size are evaluated through predefined query rules to verify compatibility and assert suitable matches. Silva et al. [23] utilized OWL-based ontologies to model the structure, capabilities, and skills of robots, with the ontological definitions derived from relevant technical standards. Similarly, capability matching was also conducted at the capability name level and the parameter level. Grimm et al. [24] employed OWL-based ontologies to represent capabilities, skills, and services in an automotive production planning scenario. Their capability matching approach relied on class expression satisfiability checking using an OWL reasoner. Specifically, a required capability, expressed with constraints, was compared against an offered capability. A match was identified if the conjunction of the two OWL class expressions was satisfiable. 

Ontologies can be limited in practice by their lack of large-scale instance data. A more common approach is to convert ontologies into KGs, where the ontology serves as schema and the KG then instantiates this schema, enabling reasoning and inference over both structure and content [25]. For instance, Mo et al. [26] extended existing PPR and capability ontologies by incorporating additional concepts such as task, capacity, and reconfiguration. These OWL-based ontologies serve as the schema layer, defining the classes, entities, relationships, and semantic rules, such as subclass hierarchies and constraints. These ontologies were then instantiated into KGs by adding an entity layer composed of actual instances and dynamic data from manufacturing sources. The reasoning process for capability matching integrates OWL-based logical inference with Cypher queries for KGs. Specifically, Cypher is used to identify which processes are associated with a given task and to retrieve the required capabilities and their specification values. OWL reasoning is then applied to decompose combined capabilities and check subclass capabilities from their parent. Finally, Cypher queries are used to identify assets that offer the required capabilities and to verify whether they meet the specified constraints. 

Apart from traditional query-based methods, Mo et al. [27] and Tang et al. [28] introduced a fuzzy evaluation matrix for capability matching, where the capability features of each resource were extracted from a KG and evaluated based on their weighted importance for each production requirement. 

## _2.2. Asset administration shell_ 

In comparison to ontology and KG, the AAS, promoted by Plattform Industrie 4.0 as the standardized DTs within the framework of Reference Architecture Model for Industry 4.0 [29], is specifically designed to address interoperability issues across different manufacturing subsystems and stakeholders through its standardized metamodel [17] and SMTs [18]. Additionally, the AAS can directly incorporate a variety of file types, such as PDF documents, CAD models, images, time series data, and other structured or unstructured data. This level of data integration is not typically achievable with ontologies and KGs. Furthermore, the AAS adopts an object-oriented modeling approach, where each AAS is expressed as well-defined classes. This approach integrates smoothly into modern software architectures, making the AAS a backend component rather than an isolated system [30]. Despite these differences, the AAS models can also be converted into RDF ontologies [31], allowing integration with existing ontologies and KGs when needed. 

For capability modeling, Nguyen et al. [32] introduced a set of SMs, including Service, Capabilities, and Skills to evaluate the feasibility of a work cell. SM Service specifies the required capabilities for a given task, while each resource’s SM Capabilities describes its available capabilities using descriptive entities. Matching between requirements and resources was achieved through name-based comparisons. Once a match was found, SM Skills provided detailed instructions on how capabilities would be executed. However, the inference process was implemented through external engineering logics, as AAS does not inherently support

### Page 3

> _D. Shi et al.                                                                                                                                                                                                                                      Robotics and Computer-Integrated Manufacturing 97 (2026) 103105_ 

reasoning mechanisms like those available in ontology or KG frameworks. 

For production planning and scheduling, Sapel and Hopmann [33] defined a series of information models tailored to the injection molding domain, based on relevant industrial standards. These models were implemented using both ontologies and AAS SMs. Kosse et al. [34] defined several AAS SMs related to the production process, specifically for dynamic scheduling in the production of precast concrete elements. These submodels were converted into RDF-based ontologies to facilitate storage and semantic reasoning. By using SPARQL, query rules were designed for retrieving data and information from the models, enabling the dynamic scheduling of production tasks. Similarly, Park et al. [35] designed AAS SMs to describe products, processes, plans, plants, and resources, providing necessary information for advanced planning and scheduling. Rehman et al. [36] proposed a skill-related SM, representing a specific step in the control and testing operation. It not only included the metadata and parameters of a skill but also utilized an AAS submodel element (SME) called Operation, which allowed for actual skill execution via an API call. This implementation was developed using the widely adopted AAS SDK BaSyx [37], which provides comprehensive software libraries for developing and deploying AAS-based solutions in backend systems. The testing results were populated into the SM Results and further processed by machine learning (ML) models for analysis. Shin et al. [38] also combined AAS with ML models, where the AAS provided structured information and dynamically populated values as inputs for the ML models for energy prediction. 

## _2.3. Large language models for knowledge inference_ 

Recently, LLM has been introduced for knowledge inference in the manufacturing domain [41–49]. LLMs exhibit exceptional generalization capacities and are transforming how humans conceive and implement AI algorithms. Users do not need to comprehend the workings of LLMs or structure their tasks to suit LLMs. Instead, they can access the LLM’s interface (e.g., GPT-4 API) [39]. In this regard, prompt engineering, such as in-context learning (ICL) [40] and CoT [20], has emerged as a new approach. 

Li et al. [41] constructed a manufacturing service KG for knowledge representation and employed LLMs as reasoning engines to support question answering and manufacturing service discovery. User queries were first transformed into graph structures, and graph embedding techniques were applied to encode query entities into embedding vectors. These embeddings were then used to perform a similarity search within the manufacturing service KG, with the retrieved relevant entities serving as the knowledge base for response generation. Similarly, Liu et al. [42] and Zhou et al. [43] built KGs for failure mode and effects analysis (FMEA), in which entities represented textual descriptions of failure modes, causes, and effects. These KGs were encoded using graph neural networks GNNs to enable knowledge retrieval, allowing maintenance-related questions to be addressed based on the structured failure knowledge. 

This concept aligns closely with the principles of RAG. For instance, Bahr et al. [44] built a KG to store maintenance-related knowledge, where KG entities were encoded as text chunks into vector embeddings. These embeddings were stored as literal values linked to their corresponding nodes within the KG. For retrieval, user queries were processed by performing a depth-first search across the KG, starting from each failure mode node. This RAG system offered a more efficient alternative to traditional Excel spreadsheets for FMEA. Wan et al. [45] constructed a KG that captured metadata from technical documents related to design for additive manufacturing. The knowledge source consisted of both the structured KG for indexing and the original unstructured documents. Knowledge inference was performed in two stages. In the first stage, user queries were aligned with KG entities using predefined query rules. If deeper contextual understanding was required, a second stage employed vector-based retrieval, where both the text from KG entities and the 

original documents were embedded into vectors for semantic search. Alvaro and Barreda [´ 46] developed a RAG system without KGs for quality control in ceramic tile manufacturing. They curated a dataset from defect handbooks and academic articles, structuring it into samples with fields such as defect type, causes, solutions, and origin. Apart from initial similarity-based retrieval, a cross-encoder reranker was introduced to enhance the retrieval results. 

Xia et al. [47] and Tinnes et al. [48] proposed an RAG system that employed LLMs with ICL to retrieve information from both structured and unstructured data sources related to product descriptions. This RAG system was employed to automatically generate product AAS instances. Shi et al. [49] introduced the combination of AAS and LLMs for quality control, where LLMs were fine-tuned for semantic matching in the development pipeline of SMTs. However, in these studies, LLMs were primarily used to support the generation of AAS content rather than to serve as reasoning engines for knowledge inference based on AAS models. 

## _2.4. Research gaps_ 

The literature review identifies several key research gaps. We explicitly explain how our approach addresses these gaps, aligning with our main contributions summarized in Section 1. 

- In terms of knowledge representation, previous work has primarily utilized ontologies and KGs in CDTs and capability matching for RM. Although many studies define similar concepts related to PPR and capabilities, the defined entities, relationships, and semantic rules in these ontologies and KGs vary significantly across implementations. This underscores a fundamental challenge of interoperability and reusability. On the other hand, while the AAS has been applied for information modeling in various domains, many SMs were developed in an ad-hoc manner, lacking a systematic methodology. There is no clear guidance on how an SM can be designed and standardized as an SMT. The proposed AAS-based modeling methodology addresses this issue. 

- In terms of knowledge inference, existing capability matching mechanisms rely on rule-based reasoning, typically through matching capability names and comparing numerical values of technical properties. This approach is limited to simple use cases where requirements and capabilities can be represented with a name and several technical properties. However, in practice, requirements and capabilities often require richer representations, including detailed textual descriptions, diagrams, or other contextual data. The reasoning process in such cases may go beyond simple logical comparisons. Moreover, rule-based systems are inherently limited in scalability, as they depend on manually defined rules tailored to specific applications. Our approach leverages LLMs for interpreting both structured data (e.g. numerical technical properties) and unstructured semantic information (e.g. textual descriptions). This enables more flexible and scalable capability matching. 

- Although LLMs have been introduced in manufacturing applications in conjunction with KGs and AAS, there has been little focus on how LLMs can be practically deployed with these information models in production environments. Especially for AAS, its metamodel does not specify a reasoning mechanism. Although the BaSyx framework provides REST API access to individual AAS entities, the reasoning process must be designed and developed by users. Our work addresses this gap by introducing the RAG system for the integration of AAS as the knowledge base and LLMs as data consumers to execute the capability matching mechanism. Accordingly, the IT architecture is designed and implemented, providing a technical reference for the AAS community.

### Page 4

> _D. Shi et al.                                                                                                                                                                                                                                      Robotics and Computer-Integrated Manufacturing 97 (2026) 103105_ 

## **3. Developing asset administration shells for knowledge representation in cognitive digital twins** 

## _3.1. Fundamentals_ 

As Fig. 2 shows, one AAS represents one asset, which could be either a physical asset, such as a production machine, or a virtual asset, like a machine model library. The AAS encapsulates the information about this asset through various SMs, each representing a specific aspect of the asset. For example, the SM Digital Nameplate describes asset identification, traceability, and regulatory declarations. Each SM is an information model with a hierarchical structure composed of SMEs and SME Collections (SMCs). An SME is equivalent to an entity within a KG, with the key difference being that in AAS, the types and attributes of SMEs are standardized according to the AAS metamodel [17]. This metamodel ensures the consistency of the AAS building units across different systems. For instance, SMCs serve as containers that group multiple SMEs, enabling hierarchical structuring within SMs. The SME Property is the most commonly used and allows for any data type to be assigned to its value. Multilanguage Property (MLP) allows for textual descriptions in multiple languages. File supports the attachment of multimedia files such as PDFs, images, or CAD models. Reference Element (Ref) and Relationship Element (Rel) facilitate references and relationships between SMEs, SMs, or AASs, enabling complex and nested structures. Each SME carries semantic information through its attributes, such as “idShort” for the short name, “description” for a textual explanation, “value” for the actual data, “semanticId” for a reference to an external vocabulary, “qualifier” for additional statements like cardinality or allowable range, etc. 

An empty SM is referred to as an SMT, which serves as a blueprint for instantiating the SM in specific applications. To ensure interoperability, SMs intended for the same modeling purpose should be unified and standardized as Standardized SMTs. Once an SMT is developed and standardized, users can populate it with values relevant to their specific applications. For example, every machine must have a physical nameplate as per regulations (e.g., EU Machine Directive 2006/42/EC). The SMT Digital Nameplate extends this concept digitally, allowing manufacturers to populate the standardized fields with asset-specific data for their machines. In the AAS community, Standardization efforts, including the development, review, publication, and update of SMTs, are led by the organization Industry Digital Twin Association (IDTA) [18]. 

In addition to the standardized metamodel and SMT, AAS also allows 

for the reference to external standardized professional vocabularies such as ECLASS [50], to provide consistent semantic references for each SME. This is primarily achieved through the attributes semanticId and Concept Description (CD), which link SMEs to external vocabularies, ensuring semantic consistency of SMEs’ definitions across systems and avoiding ambiguity. Further details on semantic referencing and automated semantic matching algorithms can be found in our previous work [51]. 

## _3.2. Methodology_ 

Developing an SMT involves defining individual entities and organizing them into a logical structure with the AAS SMEs and SMCs. Fig. 3 depicts the proposed use-case-driven AAS-expert-centric methodology in five phases. The green blocks represent the development processes, the blue blocks denote information resources, and the orange blocks indicate the generated artifacts. The ultimate objective is to create an SMT that allows users to populate the necessary values, ensuring interoperable knowledge representation across systems. 

The process begins with Phase 1: Use Case Description, typically initiated by domain experts who propose a practical industrial scenario involving information exchange, data consumption, and the need for interoperability. The development requires the collaboration of a working group consisting of both AAS experts and domain experts, led by an AAS specialist with experience in AAS-based information modeling. This phase focuses on describing the use case, outlining how technical roles interact within a specific system, and specifying the context and high-level requirements. Importantly, the use case description is independent of AAS at this stage. We follow a use case description method standardized in IEC TR 63,283–2:2022 [52], which provides a lightweight template compatible with the Industrial Internet – Reference Architecture template and the IEC62559 2 template. The description uses predicates to define interactions between technical roles, which helps clarify the processes, actors, and data flows in the use case. At this stage, it is crucial to identify which information is consumed or exchanged by which entities in the process. 

Following the use case description, the second phase is to derive the class diagram for the information models. Data, information, and knowledge are extracted from various sources, including expert interviews, applicable industry standards, and enterprise-specific conventions. The goal is to identify and define individual entities relevant to the use case. AAS experts must consider how to represent these entities and their relationships using AAS SMEs and SMCs, following the rules 

**==> picture [410 x 201] intentionally omitted <==**

**Fig. 2.** Simplified illustration of asset administration shell.

### Page 5

> _D. Shi et al.                                                                                                                                                                                                                                      Robotics and Computer-Integrated Manufacturing 97 (2026) 103105_ 

**==> picture [446 x 238] intentionally omitted <==**

**Fig. 3.** Methodology for developing AAS SMTs. 

specified in the AAS metamodel. The output of this phase is a Unified Modeling Language (UML) class diagram that visualizes the entities, their attributes, and their relationships. 

Based on the UML class diagram, the AAS SMT can be implemented using a modeling tool such as Eclipse AASX Package Explorer [53]. In this process, the entity name and definition identified in the class diagram map to the IdShort and description attributes of the respective SMEs. Additionally, a qualifier attribute can be used to specify whether an entity is mandatory or optional within the SMT. To further enhance interoperability, a semantic search implemented in our previous work [51] can be performed to identify whether a standardized vocabulary from an external repository, such as ECLASS or existing standardized SMTs, matches the defined entity. The matched vocabulary can be referenced via semanticId and linked to the CD of the corresponding SME. Once the AAS SMT is fully developed, it is saved in the ".aasx" file format. An accompanying specification document should also be prepared to guide users in understanding and correctly populating the SMT. Both the SMT and the specification document can be submitted to the IDTA for quality testing and review. If the SMT is intended as an enterprise-specific resource and does not require formal standardization, it does not need to be submitted for publication. However, even in 

this case, it should still undergo internal review and testing to ensure its compliance. 

These outcomes will undergo review by other working groups and the broader AAS community. The compliance of the SMT is tested using AAS SDK Basyx [37] for deserialization, ensuring seamless integration into software applications. Additionally, the content will be subject to continuous maintenance and updating. This iterative and collaborative process is key to ensuring the quality, adaptability, and relevance of the developed SMTs for Industry 4.0 applications. 

## _3.3. Use case and submodel templates for flexible production planning_ 

Under the guidance of the proposed methodology, the PPR-related SMTs for flexible production planning are developed. Fig. 4 abstractly depicts the use case for flexible production planning based on capability matching in a discrete RM system. In this scenario, the product is customized based on individual customer requirements, leading to dynamic changes in production processes. 

Manufacturers typically provide a configuration tool, enabling customers to tailor products based on existing types. Upon receiving a purchase order, the Enterprise-Resource-Planning (ERP) system relays it 

**==> picture [410 x 171] intentionally omitted <==**

**Fig. 4.** Use case for flexible production planning based on capability matching.

### Page 6

> _D. Shi et al.                                                                                                                                                                                                                                      Robotics and Computer-Integrated Manufacturing 97 (2026) 103105_ 

to the Product-Lifecycle-Management (PLM) system for adaptation. Here, process data and work instructions are integrated and returned to the ERP. Conventionally, physical production resources are directly linked to the process steps, forming a rigid sequence of steps, resources, and corresponding parameters. Afterward, the ERP initiates a production order for this product instance and assigns it to the Manufacturing Execution System (MES) at a production site. This chain frequently requires manual intervention and information provision, which extends decision-making loops, potentially compromising manufacturing flexibility and customization capabilities. 

The proposed SMTs intend to decouple production processes from resources and decouple functional roles of production resources from their physical assets, which leaves more flexibility at the planning and execution stage. Firstly, the information is structurally modeled and encapsulated into reusable AAS SMTs, enabling seamless information exchange across diverse applications like ERP, PLM, and MES. Secondly, process-related SMTs are designed to segregate production processes into modular and reusable segments. Each segment details production requirements, eliminating the need to directly associate with specific physical resources in the process engineering stage. Thirdly, functional roles are abstracted from physical assets by introducing an SMT RoleCapability that describes the functional capability and temporal capacity. This abstraction facilitates the effortless replacement of assets with others possessing similar functionalities. The task of auto-matching production requirements with resource capabilities will be entrusted to the RAG system. 

Fig. 5 presents the UML diagrams of the proposed AAS models. The 

product AAS, instantiated from a product order, carries lifecyclespanning information via SMs. Among others, the SM BillOfProcess describes the sequence of individual process steps, each of which is termed “process segment” in alignment with IEC 62,264–2 [19]. As Fig. 5 shows, the routing of processes is represented by a series of the SMCs Process in numerical order, e.g. Process00, Process01, etc. Each SMC Process contains metadata like ProcessId, ProcessName, ProcessDescription, and ProcessPlannedStartDate. Among others, ProcessRef, defined as an RE, refers to the SM ProcessSegment. Notably, an SMC can only host SMEs, not another SM, necessitating the RE’s role for inter-submodel connections. In the SM ProcessSegment, requirements are specified via SMCs RequiredEquipment, RequiredMaterial and RequiredPersonnel. Taking the SMC RequiredEquipment as an example, requirements are mainly expressed using descriptive language and technical specifications. Supplementary documents and engineering resources like drawings and CAD models can be annexed via the Attachments. This information will be primed for the LLM for capability matching. 

The capability of production equipment is represented by the SM RoleCapability. Previous work often represents capabilities solely through a combination of named technical properties and corresponding value constraints [22–28]. However, this oversimplifies the complexities in real-world scenarios. For example, consider the capability comparison between a 4-axis and a 5-axis machining center. While both machines may exhibit similar technical specifications, such as spindle speed, tool diameter, and maximum torque, their actual functional capabilities differ substantially. A 5-axis machining center can operate on more 

**==> picture [410 x 359] intentionally omitted <==**

**Fig. 5.** UML diagrams of process-related and resource-related AAS models. Each model is denoted by its idShort (e.g., "Product"), model type (e.g., "Asset Administration Shell"), and associated components. For instance, “+ SequenceID: Property [1]” in the SM BillOfProcess denotes that the SM BillOfProcess model contains a public Property called SequenceID, which has a cardinality of 1.

### Page 7

> _D. Shi et al.                                                                                                                                                                                                                                      Robotics and Computer-Integrated Manufacturing 97 (2026) 103105_ 

complex geometries of a workpiece without the need for repositioning, offering greater flexibility and precision. These distinctions belong to domain knowledge and may be conveyed through descriptive language and LLM-learned knowledge. Taking this into account, we describe the capability in SM RoleCapability with five facets. Firstly, the SME type Capability, as defined in the AAS metamodel, is utilized, referring to ontologies pre-established in standardized data specifications like ECLASS. Also, capability can be described in natural language by the ’s MLP. The primary technical specifications detailing the equipment capabilities and limitations are included in the SMC RoleSpecifications. Furthermore, historical records of matched process segments are aggregated under the SMC ReferenceWorkpiece, which provides the demonstration candidates for the LLM. In addition to functional capabilities, the equipment’s availability is captured through an RE RefRoleCapacity directing to the SM RoleCapacity. In line with IEC 62,264–2, capacity is chiefly characterized by three statuses—available, committed, and unattainable capacities—each contextualized with its duration, while supplementary details can be provided in the MLP Reason. 

RoleCapability is nested within the AAS RoleEquipment, representing the equipment’s functional role within the production. It aims to decouple the equipment role from its physical assets. Upon the stage of system integration, the AAS RoleEquipment should be created and associated with its asset. It contains operation-related information. On the other hand, the AAS PhysicalEquipment includes intrinsic characteristics via SMs such as DigitalNameplate and TechnicalData. They are typically furnished by the asset’s supplier. 

## **4. Leveraging large language models for knowledge inference in cognitive digital twins** 

## _4.1. Mechanism of capability matching_ 

The greatest challenge in capability matching lies in the semantic disconnect between product requirements and equipment capability descriptions. As illustrated in Fig. 6, requirements are defined from the product perspective and may include properties like PartDimensions, SurfaceFinishRa, and SpecialFeatures. However, these are rarely described in the same form within equipment capability models, which are defined from the machine’s perspective. For example, the requirement PartDimensions is related to machine attributes such as MaxWorkpieceLength, MaxWorkpieceWidth, and MaxWorkpieceHeight. The requirement SpecialFeatures is often not explicitly stated in the machine data but is instead embedded in high-level descriptors like machine type. For instance, both 3-axis and 5-axis machining centers might be capable of producing a feature, but only the latter can do so without repositioning, which significantly affects machining tolerances. 

This type of matching requires reasoning based on domain knowledge, not just straightforward name or value comparisons. In previous work, the translation from product requirements to required machine 

capability entities has relied on manually defined rule logic by domain experts. In contrast, our solution introduces LLM with CoT to automate this reasoning and translation process. Moreover, considering the large number and variety of machines deployed in a production environment and the extensive range of associated capability entities, scalability becomes a critical requirement that our approach effectively addresses through a RAG-based architecture. The main steps of the matching mechanism are presented below. The detailed RAG operations are introduced in Section 4.2. 

The first step aims to identify the relevant equipment type and generate the capability template based on its capability-related entities. The output of this step is an empty capability template as the input for the CoT prompting. Requirement-related entities are first extracted from the SM ProcessSegment, serving as the query entities. These queries are searched within the knowledge base, which consists of all AAS instances representing the available role-based equipment in the machine pool. This search is conducted via the RAG system. Due to the semantic disconnection between product requirements and equipment capabilities, a one-to-one match between requirement entities and capability attributes is not expected. Instead, equipment AAS instances containing the highest number of relevant retrieved capability entities are considered as the target equipment type. This step is essential for ensuring scalability. The machine pool consists of various types and variants of equipment, each described by a distinct set of capability entities. Without this automated identification process, the capability template would need to be manually defined for each equipment type. 

In the second step, the retrieved process requirements are combined with a CoT prompting template designed to guide the LLM in populating the required capability template. This step completes the translation from the product requirements to the required capabilities. The populated template provides the inputs for the subsequent comparison of the required capabilities and the equipment’s capabilities. The designed CoT template consists of four parts, as shown in Table 1. The first part defines the systematic instructions. The second part teaches step-by-step decision-making processes based on human experience, which breaks the complex task into several small steps and forces the agent to give a reason for each step. The third part provides a positive example with rationales. The last part is the actual input and output. The input corresponds to the entities of process requirements retrieved in the first step, while the output corresponds to the empty template of capability entities. 

In the last step, the values of the recommended capability attributes are employed as selection criteria to pinpoint the most suitable production machine. For a small-scale machine pool, this selection can be straightforwardly conducted by providing the capability entities of all machines to the LLM. To ensure scalability, we implement an iterative comparison query. For simplicity, the selection algorithm does not take device availability into account, as machines that are currently unavailable can be picked out directly by referring to their scheduling calendars. The principal criteria for selection are grounded in technical 

**==> picture [422 x 129] intentionally omitted <==**

**Fig. 6.** Mechanism for capability matching.

### Page 8

> _D. Shi et al.                                                                                                                                                                                                                                      Robotics and Computer-Integrated Manufacturing 97 (2026) 103105_ 

## **Table 1** 

Design of the CoT prompt. 

|Prompt part|Prompts|
|---|---|
|**Instruction**|You are a production planner. Based on the provided|
||production requirements, recommend the required machine<br>capability, fll in the capability template, and provide the|
||rationales without any additional explanations.|
|**Reasoning process**|First, decide on the machining type…The main<br>considerations are the machining features and the<br>tolerances…. Then consider the economics….|
|**Examples**|Below is a demo example. \nProcessName: machining an<br>aluminum frt ftting part \nPartDescription:…|
||Rationales: 1. The part has complex geometries and|
||requirements on consistent uniform surfaces. Indexed 4-axis|
||milling eliminates the need for multiple setups and ensures|
||better precision…2…|
||Output. \nMachineType: Indexed 4-axis milling machine…|
|**Input and output**|"————Input———-"|
|**template**|"_{requirement_entities}_"|
||"———–Output———"<br>"_{capability_entities}_"|



capability-related entities and the hourly rate. 

During each iteration, the same capability entities retrieved from all the machines are compared against the corresponding required capability entity. In cases where several candidates are viable after assessing all capability entities, the machine with the most economical hourly rate is chosen. 

## _4.2. Retrieval-augmented generation for capability matching_ 

The RAG system concerns the integration of the AAS as a knowledge base and LLMs as data consumers to execute the capability matching mechanism described above. Fig. 7 illustrates the RAG system in action with an example query and response. In this RAG system, three distinct types of LLMs are utilized: a chat model, an embedding model, and an entity matcher. The chat model is responsible for extracting query entities and generating responses. The embedding model encodes the extracted query entities and the entities within the AAS knowledge base into dense vector representations for similarity-based retrieval. Subsequently, the top-10 retrieved candidate entities are passed to the entity – matcher, which determines whether each query candidate pair constitutes a valid match. The entity search and match rely on the vector similarities of the concatenated idShort and description of individual AAS entities. The implementation and the evaluation are detailed in our previous work [51]. 

The RAG process begins by extracting query entities from the SM ProcessSegment. These query entities are then matched against 

capability-related entities within the AAS knowledge base through a two-stage process: initial similarity-based retrieval using embedding vectors, followed by pairwise entity matching. For each equipment AAS, the number of successfully matched capability entities is counted. The equipment AAS with the highest number of relevant matches is identified as the most suitable equipment type. Based on its capability candidates, an empty capability template is derived. Afterward, the complete set of requirement entities, along with their values and the derived empty capability template, are passed into the chat model, together with the CoT prompt template shown in Table 1. The chat model then populates the capability template, generating the required equipment capabilities to fulfill the process requirements. 

## **5. Case study and evaluation** 

## _5.1. Case study scenario_ 

The proposed CDT for capability matching toward RM was validated at a small-scale machining center. The center primarily undertakes internal machining tasks, equipped with 2 turning lathes and 4 milling machines, dedicated to the production of prototypes. The machines with their RoleID and machining types are shown in Table 2. Typically, production orders are submitted to the center in the form of drawings, 3D CAD models, and explanatory documents. For production planning, experienced mechanical engineers undertake the manual analysis of these orders to designate the most appropriate machine for execution, considering the machine’s technical capabilities, hourly rates, and availability. The scheduled production plan is documented and managed manually using Excel spreadsheets. The introduction of the CDT targets the digitization and automation of this existing production planning workflow. 

For validation, a test dataset is compiled, encompassing 106 historical production orders spanning from 2021 to 2023. Six orders, which were assigned to the six machines respectively, are used as the candidates of the demonstrative example. For each data sample, the example in the CoT prompt is randomly selected from these six candidates. The remaining orders are fed into the RAG system as inputs. The outputs predicted by the LLM are compared to the historically recorded machine allocations for the evaluation. In the following, we first delve into a detailed system implementation and the evaluation of the capability matching mechanism on the test dataset. The empirical findings are discussed. 

## _5.2. Implementation_ 

The proposed CDT is a software system that focuses on addressing 

**==> picture [458 x 177] intentionally omitted <==**

**Fig. 7.** Illustration of retrieval-augmented generation system for capability matching.

### Page 9

_Robotics and Computer-Integrated Manufacturing 97 (2026) 103105_ 

## **Table 2** 

Exemplary equipment in the machining center. 

**==> picture [446 x 297] intentionally omitted <==**

knowledge management and information flow within an RM environment without incorporating 3D visualization of the shop floor in its current implementation. Fig. 8 provides an overview of the system architecture and workflow, which revolves around three core components: the configuration tool for production planning, Basyx Java components, and the RAG system. 

The implemented configuration tool aims at dynamically creating the relevant AAS and SM instances of PPR elements for each customized product. First, the AAS models designed according to the proposed methodology are implemented as static AASX files using AASX Package Explorer [53], which acts as a ZIP-like archive, containing the AAS model in either XML or JSON format, along with any attached files such 

**==> picture [458 x 233] intentionally omitted <==**

**Fig. 8.** Implemented CDT software system, which is composed of three core components: configuration tool for production planning (green), Basyx Java components (blue) and the RAG system (yellow).

### Page 10

> _D. Shi et al.                                                                                                                                                                                                                                      Robotics and Computer-Integrated Manufacturing 97 (2026) 103105_ 

as images, PDFs, and CAD models. Fig. 9 shows the screenshots of the implemented AASX files for an exemplary product instance and a 5-axis CNC milling-turning center. Inherent attributes of this equipment are characterized via its AAS PhysicalEquipment designated as “DMGMoriDMU65FD”, typically furnished by the machine’s manufacturer. The machine’s functional role within the machining center is represented by its AAS RoleEquipment designated as “MillingCenter” with the RoleID “G01M001”. The product AAS contains essential production metadata, with a particular focus on the SM BillOfProcess, which is dynamically generated by concatenating the required process segments. This configuration step is performed through the developed frontend interface, as shown in the top-right screenshot of Fig. 8. 

To instantiate AAS instances in the runtime environment, the static AASX template files are deserialized into objects via Basyx Python SDK in the backend. The backend is developed using the FAST-API framework, which provides REST APIs for AAS management tasks such as creation, deletion, and manipulation of AAS instances. These APIs are consumed by the frontend, which is built using the Vue3 framework. The frontend allows users to interact with predefined SMs such as CNCMachining, Forming, and Coating, displayed as selectable options. The process engineer selects the appropriate process steps based on input documents like 2D/3D CAD models, technical drawings, and process specifications. The system then generates the corresponding BillOfProcess for the assigned product AAS, referencing the selected ProcessSegments. The selected product AAS and its related SM ProcessSegments are displayed in the "Selected Items" block within the frontend interface, enabling users to click on any item to navigate directly to the AAS repository, where they can populate the AAS with input values if needed. Additionally, more detailed information about the AAS and its SMs is displayed. 

The AAS repository is built using the off-the-shelf BaSyx Java Components [37], which provide the essential AAS infrastructure, including an AAS server, registry, and a MongoDB database for storing AAS instances. The AAS server and registry form the core IT infrastructure that supports the operational framework for AAS in a production environment. The registry maintains records of all registered AAS and SMs, including identifiers and endpoints, enabling efficient lookup and query of entities within the SMTs via REST-APIs. Additionally, a frontend interface, as shown in the bottom-right screenshot of Fig. 8, allows users to explore and populate the registered AAS. 

ProcessSegment and the equipment’s RoleCapability via the "GET" REST API. We extended the backend of an open-source RAG project [54] by incorporating a custom AAS parser to read the AAS models, enabling the RAG to utilize serialized AAS files as its knowledge base. For retrieval, the system employs the embedding model "text-embedding-3-large", while the "gpt-4-turbo-preview" model is used as the chat model and the entity matcher. Both models are accessible through the OpenAI APIs [55]. For chat completions, the temperature parameter is set to 0.2 to ensure more deterministic outputs. The chat interface is shown in the bottom-left screenshot of Fig. 8, where users can search and query any information within the AAS models. In this use case, we query the required capabilities through the designed CoT-prompt shown in Table 1. The values of these required capability entities are then compared with the corresponding data in the equipment’s RoleCapability. A detailed evaluation of the system’s performance is presented in the next section. 

## _5.3. Evaluation_ 

The effectiveness of the proposed capability matching mechanism is evaluated on the test dataset. Due to the limited availability of data samples and the complexity of the causality involved in the matching task, fine-tuning the LLM’s weights, as done in the previous work for entity matching [51], is not feasible. Therefore, the experiments in this study focus primarily on tuning the CoT prompts to optimize the performance of capability matching. Additionally, the proposed CoT-based matching mechanism is compared against conventional rule-based knowledge inference methods, which are widely used in previous studies [22–28]. The comparative methods are defined and explained as follows: 

- 1) Proposed CoT: the LLM is guided by the proposed CoT prompt as presented in Table 1 

- 2) Baseline: This is a rule-based knowledge inference method that relies on keyword searches. Machine capabilities and production processes are described using keywords and numerical specifications. For instance, the term “drilling” might be accompanied by specific technical descriptions such as “requiredPayload”. A series of mapping rules are implemented for our case study, such as “freeform” for 5-axis milling, “multi-sided” for 4-axis, and “cylindrical” for lathe. 

The RAG system receives the serialized SMs of the selected product’s 

**==> picture [446 x 217] intentionally omitted <==**

**Fig. 9.** Implemented AASX static model files of the designed AAS and SMs. Left: AAS PhysicalEquipment and RoleEquipment for a 5-axis CNC milling-turning center. Right: Product AAS of a customized part to be machined.

### Page 11

> _D. Shi et al.                                                                                                                                                                                                                                      Robotics and Computer-Integrated Manufacturing 97 (2026) 103105_ 

- 3) VariationA: the LLM is guided solely by the instruction prompt, without any further reasoning or example. 

- 4) VariationB: the LLM is guided by the prompt of the instruction and the reasoning process, but without the example. 

- 5) VariationC: the LLM is guided by the prompt of the instruction and a demonstrative example, but without the reasoning process. 

- 6) VariationD: the LLM is guided by a reverse-ordered CoT prompt, where the demonstrative example is presented before the reasoning process. 

Fig. 10 presents the evaluation results. The accuracies are calculated by contrasting the model’s predictions to the historically recorded allocations on the six machines, yielding a random accuracy threshold of 16.67 %. The baseline managed an accuracy of 29 %. In comparison, the proposed CoT exhibits outstanding performance, achieving an accuracy of 79 %. Table 3 presents the LLM responses for matching a machining part with a candidate machine. CoT prompting is applied to Step 2. The LLM enhanced with the CoT prompt demonstrates an ability to derive necessary machine capabilities not only from the part’s numerical specifications, such as PartDimensions, but also from a combination of textual descriptions like PartDescription and SpecialFeatures, as well as specific numerical values like Tolerance. It offers insights into related performance attributes such as positioning accuracy and repeatability, even though these details are not explicitly mentioned in the input. After identifying the necessary capabilities, the optimal machine is selected through the proposed iterative comparison query in Step 3. In this step, a straightforward instruction prompt is sufficient for guiding the LLM. Importantly, throughout both steps, the LLM is required to output structured responses according to a predefined template. In our tests, GPT-4 consistently adheres to this structured format, which ensures reliable and error-free processing of the results. However, we also tested – open-source models like Llama2 70B, which frequently failed to consistently output the responses in the required template format, regardless of how the prompt is formulated. This inconsistency led to difficulties and errors in post-processing the responses. We also examine the distribution of error cases and observe that 67 % of its errors stem from its inclination to recommend a 5-axis machine for tasks feasibly accomplished by a 3-axis machine with multiple setups, reflecting its bias towards the "accurate machining" criterion. This can be caused by inherited knowledge embedded in the model. 

’s variants In comparison, the significant accuracy drops of CoT reveal the effectiveness of the proposed CoT prompt. The performance of VariationA is the same as the baseline. 54 % of its errors incorrectly recommend a 3-axis milling-turning machine. The accompanying rationales hint at the possibility that the LLM, guided solely by instruction 

prompts, appears to match the workpieces having cylindrical features with a lathe. VariationC, an enhancement of VariationA with an added demonstrative example, doesn’t manifest any significant improvement. However, VariationC’s majority errors, unlike VariationA, prefer to recommend a 5-axis machine instead of a 3/4-axis. VariationB, an enhancement of VariationA with human reasoning processes, exhibits an improvement with an accuracy rate of 48 %. Being different from other variations, VariationB showcases a penchant for the 3-axis machine. It argues that most features can be machined by the 3-axis machine. Among others, the low performance of Variation D is unexpected. It reveals that the order of prompts also plays in determining prediction outcomes. Placing the reasoning prompt after the example seems to weaken the effectiveness of CoT reasoning inherent in the step-by-step human reasoning processes. 

These evaluation experiments provide valuable insights into how different components of CoT prompting impact the performance of the LLM. The superiority of VariationB over VariationA is evidence that general descriptions of step-by-step reasoning as additional instruction can significantly enhance the agent’s capability in the given task. The fact that VariationC’s performance aligns with VariationA, while their error patterns diverge, suggests that merely adding an example, without the context of sequential reasoning, might sway the LLM to overly rely on the example. Just having an example doesn’t necessarily equip the LLM with the right reasoning approach. The comparison between the proposed CoT and VariationD is particularly instructive. It highlights the importance of the sequence in which reasoning and an example are presented. The optimal combination appears to involve presenting reasoning followed by the example. A plausible explanation for this is that the LLM may give precedence to tokens presented earlier, allowing it to first grasp the structured reasoning from the human reasoning process and then reinforce this understanding with the subsequent example. This sequence seems to be the key to maximizing the effectiveness of both components. 

However, it’s important to note some limitations. Upon reviewing the 3D CAD models of error cases, we observed that textual descriptions don’t always capture the full essence of a workpiece. This can lead the LLM to base decisions on incomplete information. This limitation points to one constraint of the proposed matching mechanism. It can solely take the textual inputs in the AAS SMs, even though the AAS framework supports the inclusion of multi-modal data sources. This requires a multi-modal LLM in the future. 

## **6. Conclusions** 

In this work, we introduced a CDT system and its comprehensive 

**==> picture [302 x 181] intentionally omitted <==**

**Fig. 10.** Evaluation results.

### Page 12

> _D. Shi et al.                                                                                                                                                                                                                                      Robotics and Computer-Integrated Manufacturing 97 (2026) 103105_ 

## **Table 3** 

Exemplary LLM responses of the proposed CoT prompting for capability matching. 

|**Table 3**<br>Exemplary LLM responses of the proposed CoT prompting for capability matching.|**Table 3**<br>Exemplary LLM responses of the proposed CoT prompting for capability matching.|
|---|---|
|Capability matching Step 2: input of process requirements||
||PartDescription<br>The part has an irregular shape with a central cavity, an external contour that surrounds the main cavity, axial|
||holes, and axial slots. It includes a large circular feature, sharp internal corners, and several other geometrical|
||details. The part has threaded M4 and grooves along the side elevation.|
||SpecialFeatures<br>Sharp internal corners, deep cavity, M4 threads, grooves along the side elevation, non-standard radius, irregular|
||slot, and features requiring multiple setups and repositioning.|
|Material|Aluminum 6060<br>PartDimensions<br>70×45× 20mm|
|BlankType|Plate<br>Tolerance<br>±0.125mm|
|SurfaceFinish|as machined Ra3.2μm<br>ProcessName:<br>Machining an adapter|
|**Capability matching Step 2: LLM-CoT response**||
|MachineType|4-axis CNC milling|
|MaxXStroke|100mm|
|MaxYStroke|60mm|
|MaxZStroke|50mm|
|MaxWorkPieceDiameter|Not applicable|
|MaxWorkPieceLength|70mm|
|MaxWorkPieceWidth|45mm|
|MaxWorkPieceHeight|20mm|
|MaxWorkPieceWeight|2kg|
|PositioningAccuracy|±0.05mm|
|Repeatability|±0.05mm|
|AllowedMaterial|Aluminum 6060|
|rationales|1. The part has complex features such as grooves, M4 threaded holes, deep cavities, sharp internal corners, and non-standard radii, which|
||require precise machining and multiple repositioning. A 3-axis machine would require several setups and repositioning. Using a 4-axis|
||machine will reduce setup times, increase precision, and provide access to side features like the grooves.|
||2. The tolerance requirement of±0.125 mm is achievable on a 4-axis CNC milling machine without needing a more expensive 5-axis|
||machine, which is generally used for even more complex geometries requiring simultaneous multi-axis motion.|
||3. The part is relatively small and made from aluminum, which is easy to machine and does not require excessive spindle power or heavy-<br>duty machinery. The 4-axis machine provides enough fexibility in terms of strokes for this size and weight.|
||4. Although the part has sharp internal corners and grooves, these can be machined using specialized tools on a 4-axis machine without the|
||need for simultaneous 5-axis motion.|
||5. The positioning accuracy of±0.05 mm is suffcient for the tolerances required (±0.125 mm) and ensures precision for features like the|
||M4 threads and sharp corners.|
|**Capability matching Step 3: input of machine capabilities**||
|Prompt|You are a production planner. Based on the provided capability requirements, select the most suitable machine. First, check if the required<br>MachineType is compatible. Then check the individual technical specifcations Iteratively. If requirements are met, choose the machine|
||with the lowest HourlyRate.|
||Following the template to output the MachineID of the selected machine and give the rationales in json format, without additional texts.|
||Template: {“MachineID”:“”,“rationales:“”}|
||Required machine capabilities: {…}|
||Capabilities of the machine candidates: {…}|
|**Capability matching Step 3: LLM response**||
|Selected MachineID|G01M003|
|rationales|"MachineType": "Compatible, 4-axis machine with a dividing head matches the required 4-axis CNC milling."|
||"MaxXStroke": "Meets requirement, 800 mm_>_ 100 mm"|
||"MaxYStroke": "Meets requirement, 400 mm_>_60 mm"|
||"MaxZStroke": "Meets requirement, 400 mm_>_50 mm"<br>"MaxWorkPieceDiameter": "Not applicable, no confict"|
||"MaxWorkPieceLength": "Meets requirement, 1400 mm_>_70 mm",|
||"MaxWorkPieceWidth": "Meets requirement, 480 mm_>_45 mm",|
||"MaxWorkPieceHeight": "Meets requirement, 300 mm_>_ 20 mm",|
||"MaxWorkPieceWeight": "Unknown, but likely meets requirement as it’s a large machine"|
||"PositioningAccuracy": "Unknown, but likely acceptable for general milling tasks"|
||"Repeatability": "Not provided, but machine type and specs suggest suitability"|
||"AllowedMaterial": "Compatible with Aluminum 6060"|
||"HourlyRate": "Lowest among compatible machines at 120 euro/hour"|



development workflow for capability matching within the context of RM. The CDT framework leverages the AAS for interoperable knowledge representation and LLMs for intelligent knowledge inference. By automatically matching the capabilities of production resources with the requirements of production processes, our approach enables greater flexibility in responding to external changes driven by product customization during the production planning phase. 

We derived a scalable methodology for the development of reusable AAS SMTs based on practical experience. This methodology has gained widespread acceptance within the AAS community for standardizing SMTs and vocabularies as reusable resources, thereby enhancing interoperability across different systems and applications. 

Following this methodology, we developed process- and resourcerelated SMTs that decouple physical assets from their functional roles

### Page 13

_D. Shi et al.                                                                                                                                                                                                                                      Robotics and Computer-Integrated Manufacturing 97 (2026) 103105_ 

and from production processes at the information layer. This decoupling significantly enhances the flexibility of production planning. Process engineers are only responsible for defining process segments and their requirements, while production sites are tasked with selecting the appropriate resources based on real-time equipment capabilities and availability. 

Instead of manual resource allocation, we employed an RAG system to match production processes with the appropriate resources automatically via the proposed CoT prompting. The case study in a machining center validated this concept and the effectiveness of CoT prompting. The experimental results highlight the limitations of conventional rule-based methods in handling complex knowledge inference tasks. Capability matching does not merely depend on recognizing machining features represented by keywords or numeric specifications. It also involves understanding the positions of these features, the required tolerances, and the geometry of the workpieces. The LLM with the CoT prompt exhibits its superior performance in this scenario by efficiently processing both textual descriptions and numerical specifications of production requirements and machine capabilities. 

This case study underscored the potential of AAS in knowledge representation and the strength of LLMs in performing advanced knowledge inference. In future work, we aim to explore multimodal LLMs capable of processing diverse data types, including technical drawings and 3D models, further enhancing the CDT’s applicability in complex manufacturing environments. 

## **Declaration of generative AI and AI-assisted technologies in the writing process** 

During the preparation of this work, the author(s) used Grammarly and ChatGPT in order to improve language and readability. After using this tool/service, the author(s) reviewed and edited the content as needed and take(s) full responsibility for the content of the publication. 

## **CRediT authorship contribution statement** 

**Dachuan Shi:** Methodology, Writing – review & editing, Writing – original draft, Visualization, Validation, Software, Formal analysis, Data curation, Conceptualization, Investigation. **Olga Meyer:** Writing – review & editing, Project administration, Methodology, Formal analysis, Data curation. **Zhi Fan:** Investigation, Writing – original draft, Visualization. **Hao Wang:** Supervision, Resources. **Thomas Bauernhansl:** Supervision, Resources, Funding acquisition. 

## **Declaration of competing interest** 

The authors declare that they have no known competing financial interests or personal relationships that could have appeared to influence the work reported in this paper. 

## **Acknowledgments** 

This work was supported in part by the Kopernikus project “Synergie” (03SFK3A3-3; 03SFK3T2-3) and in part by the project H2GigaFRHY (3HY112C). Both projects are funded by the German Federal Ministry of Education and Research. 

## **Data availability** 

The data that has been used is confidential. 

## **References** 

- [2] A. Napoleone, E. Negri, M. Macchi, A. Pozzetti, How the technologies underlying cyber-physical systems support the reconfigurability capability in manufacturing: a literature review, Int. J. Prod. Res. 61 (2023) 3122–3144. 

- [3] R. Andersen, A. Napoleone, A.-L. Andersen, T.D. Brunoe, K. Nielsen, A systematic methodology for changeable and reconfigurable manufacturing systems development, J. Manuf. Syst. 74 (2024) 449–462. 

- [4] H. Arnarson, H. Mahdi, B. Solvang, B.A. Bremdal, Towards automatic configuration and programming of a manufacturing cell, J. Manuf. Syst. 64 (2022) 225–235. 

- [5] J.K. Touckia, Integrating the digital twin concept into the evaluation of reconfigurable manufacturing systems (RMS): literature review and research trend, Int. J. Adv. Manuf. Technol. 126 (2023) 875–889. 

- [6] Y. Fan, J. Yang, J. Chen, P. Hu, X. Wang, J. Xu, B. Zhou, A digital-twin visualized architecture for flexible manufacturing system, J. Manuf. Syst. 60 (2021) 176–201. 

- [7] B. Leng, S. Gao, T. Xia, E. Pan, J. Seidelmann, H. Wang, L. Xi, Digital twin monitoring and simulation integrated platform for reconfigurable manufacturing systems, Adv. Eng. Inform. 58 (2023) 102141. 

- [8] M.A. Ali, A. Alarjani, M.A. Mumtaz, A NSGA-II based approach for multi-objective optimization of a reconfigurable manufacturing transfer line digital twin: a case study, Adv. Prod. Eng. Manag. 18 (2023) 116–129. 

- [9] K.T. Park, J. Lee, H.-J. Kim, S.D. Noh, Digital twin-based cyber physical production system architectural framework for personalized production, Int. J. Adv. Manuf. Technol. 106 (2020) 1787–1810. 

[10] J. Leng, Q. Liu, S. Ye, J. Jing, Y. Wang, C. Zhang, D. Zhang, X. Chen, Digital twindriven rapid reconfiguration of the automated manufacturing system via an open architecture model, Robot. Comput.-Integr. Manuf. 63 (2020) 101895. 

- [11] X. Zheng, J. Lu, D. Kiritsis, The emergence of cognitive digital twin: vision, challenges and opportunities, Int. J. Prod. Res. 60 (2022) 7610–7632. 

- [12] J. Lu, Z. Yang, X. Zheng, J. Wang, K. Dimitris, Exploring the concept of cognitive digital twin from model-based systems engineering perspective, Int. J. Adv. Manuf. Technol. 121 (2022) 5835–5854. 

- [13] Z. Yao, H. Wu, Y. Song, Y. Cheng, H. Pan, M. Wu, M. Li, G. Qin, Q. Wang, X. Zhang, Surrogate model-based cognitive digital twin for smart remote maintenance of fusion reactor: modeling and implementation, Nucl. Fusion 64 (2024) 126007. 

- [14] R.D. D’Amico, A. Sarkar, M.H. Karray, S. Addepalli, J.A. Erkoyuncu, Knowledge transfer in digital twins: the methodology to develop cognitive digital twins, CIRP J. Manuf. Sci. Technol. 52 (2024) 366–385. 

- [15] C. Su, X. Tang, Y. Han, T. Wang, D. Jiang, Cognitive digital twin in manufacturing process: integrating the knowledge graph for enhanced human-centric industry 5.0, Int. J. Prod. Res. (2024) 1–22. 

[16] T. Mortlock, D. Muthirayan, S.-Y. Yu, P.P. Khargonekar, M. Abdullah Al Faruque, Graph learning for cognitive digital twins in manufacturing systems, IEEE Trans. Emerg. Top. Comput. 10 (2022) 34–45. 

- [17] IEC, IEC 63278-2:2022: asset administration shell for industrial applications – part 2: information meta model (2022). 

- [18] IDTA, Registered AAS submodel templates [Online]. Available: https://industrialdi gitaltwin.org/en/content-hub/submodels, 2023. 

- [19] IEC, IEC 62264-2: 2013 enterprise-control system integration – part 2: objects and attributes for enterprise-control system integration (2013). 

- [20] J. Wei, et al., Chain-of-thought prompting elicits reasoning in large language models [Online]. Available: http://arxiv.org/pdf/2201.11903v6, 2022. 

- [21] C. Hildebrandt, A. Kocher, C. Kustner, C.-M. Lopez-Enriquez, A.W. Muller, 

   - B. Caesar, C.S. Gundlach, A. Fay, Ontology building for cyber–physical systems: application in the manufacturing domain, IEEE Trans. Autom. Sci. Eng. 17 (2020) 1266–1282. 

[22] E. J¨arvenpa¨¨a, N. Siltala, O. Hylli, H. Nylund, M. Lanz, Semantic rules for capability matchmaking in the context of manufacturing system design and reconfiguration, Int. J. Comput. Integr. Manuf. 36 (2023) 128–154. 

[23] L.M. Da Vieira Silva, A. Kocher, A. Fay, A capability and skill model for ¨ heterogeneous autonomous robots, at - Automatisierungstechnik 71 (2023) 140–150. 

- [24] S. Grimm, A. Haselbock, J. Neidig, K. Perry, J. Peschke, O. Scharm, J. Schnittger, ¨ Capabilities and skills for manufacturing planning in an automotive use case scenario, at - Automatisierungstechnik 71 (2023) 151–163. 

- [25] J. Lu, Z. Yang, X. Zheng, J. Wang, K. Dimitris, Exploring the concept of cognitive digital twin from model-based systems engineering perspective, Int. J. Adv. Manuf. Technol. 121 (2022) 5835–5854. 

[26] F. Mo, J.C. Chaplin, D. Sanderson, G. Martínez-Arellano, S. Ratchev, Semantic models and knowledge graphs as manufacturing system reconfiguration enablers, Robot. Comput.-Integr. Manuf. 86 (2024) 102625. 

   - [27] F. Mo, H.U. Rehman, F.M. Monetti, J.C. Chaplin, D. Sanderson, A. Popov, A. Maffei, S. Ratchev, A framework for manufacturing system reconfiguration and optimisation utilising digital twins and modular artificial intelligence, Robot. Comput.-Integr. Manuf. 82 (2023) 102524. 

   - [28] Q. Tang, R. Shu, B. Wu, A Multi-Objective Site Selection Model Considering Service Utility and Capability Matching in Outsourcing Collaboration Mode. IEEE Access 12, 2024, pp. 43173–43190. 

   - [29] B. Boss et al., Digital twin and asset administration shell concepts and application in the industrial internet and industrie 4.0: an industrial internet consortium and plattform industrie 4.0 Joint Whitepaper (2020). 

   - [30] M. Jacoby, M. Baumann, T. Bischoff, H. Mees, J. Müller, L. Stojanovic, et al., Opensource implementations of the reactive asset administration shell: a survey, Sens. (Basel) 23 (11) (2023). 

   - [31] S. Rongen, N. Nikolova, M. van der Pas, Modelling with AAS and RDF in Industry 

      - 4.0, Comput. Ind. 148 (2023) 103910. 

- [1] M. Bortolini, F.G. Galizia, C. Mora, Reconfigurable manufacturing systems: literature review and research trend, J. Manuf. Syst. 49 (2018) 93–106.

### Page 14

> _D. Shi et al.                                                                                                                                                                                                                                      Robotics and Computer-Integrated Manufacturing 97 (2026) 103105_ 

- [32] Q.-D. Nguyen, Y. Huang, F. Keith, C. Leroy, M.-T. Thi, S. Dhouib, Manufacturing 4.0: checking the feasibility of a work cell using asset administration shell and physics-based three-dimensional digital twins, Machines 12 (2024) 95. 

- [33] P. Sapel, C. Hopmann, Towards an ontology-based dictionary for production planning and control in the domain of injection molding as a basis for standardized asset administration shells, J. Ind. Inf. Integr. 35 (2023) 100488. 

- [34] S. Kosse, V. Betker, P. Hagedorn, M. Konig, T. Schmidt, A semantic digital twin for ¨ the dynamic scheduling of Industry 4.0-based production of precast concrete elements, Adv. Eng. Inform. 62 (2024) 102677. 

- [35] K.-T. Park, J.-Y. Lee, M.-W. Park, Y.H. Park, J.-Y. Lee, Y.-H. Choi, Models and P4R asset description for digital twin-based advanced planning and scheduling using cyber-physical integration for resilient production operation, J. Manuf. Syst. 77 (2024) 127–153. 

- [36] H.U. Rehman, F. Mo, J.C. Chaplin, L. Zarzycki, M. Jones, S. Ratchev, A modular artificial intelligence and asset administration shell approach to streamline testing processes in manufacturing services, J. Manuf. Syst. 72 (2024) 424–436. 

- [37] BaSyx, Eclipse BaSyx Java V2 SDK, Online available, https://github.com/eclips e-basyx/basyx-java-server-sdk, 2022. 

- [38] S.-J. Shin, J. Um, Deploying data analytics models in asset administration shells: energy prediction in manufacturing, Eng. Appl. Artif. Intell. 138 (2024). 

- [39] T.B. Brown, et al., Language models are few-shot learners, 2020. 

- [40] Q. Dong, L. Li, D. Dai, C. Zheng, Z. Wu, B. Chang, X. Sun, J. Xu, Z. Sui, A survey on in-context learning, 2022. 

- [41] Y. Li, B. Starly, Building a knowledge graph to enrich ChatGPT responses in manufacturing service discovery, J. Ind. Inf. Integr. 40 (2024) 100612, https://doi. org/10.1016/j.jii.2024.100612. 

- [42] P. Liu, L. Qian, X. Zhao, B. Tao, Joint knowledge graph and large language model for fault diagnosis and its application in aviation assembly, IEEE Trans. Ind. Inf. 20 (2024) 8160–8169, https://doi.org/10.1109/TII.2024.3366977. 

- [43] B. Zhou, X. Li, T. Liu, K. Xu, W. Liu, J. Bao, CausalKGPT: industrial structure causal knowledge-enhanced large language model for cause analysis of quality problems in aerospace product manufacturing, Adv. Eng. Inform. 59 (2024) 102333, https:// doi.org/10.1016/j.aei.2023.102333. 

- [44] L. Bahr, C. Wehner, J. Wewerka, J. Bittencourt, U. Schmid, R. Daub, Knowledge graph enhanced retrieval-augmented generation for failure mode and effects analysis, J. Ind. Inf. Integr. 45 (2025) 100807. 

- [45] Y. Wan, Z. Chen, Y. Liu, C. Chen, M. Packianather, Empowering LLMs by hybrid retrieval-augmented generation for domain-centric Q&A in smart manufacturing, Adv. Eng. Inform. 65 (2025) 103212, https://doi.org/10.1016/j.aei.2025.103212. 

- [46] J.A. Heredia Alvaro, J.G. Barreda, An advanced retrieval-augmented generation[´] system for manufacturing quality control, Adv. Eng. Inform. 64 (2025) 103007. 

- [47] Y. Xia, Z. Xiao, N. Jazdi, M. Weyrich, Generation of asset administration shell with large language model agents: toward semantic interoperability in digital twins in the context of Industry 4.0, IEEE Access 12 (2024) 84863–84877. 

- [48] C. Tinnes, M. Ristin, U. Hohenstein, K. Fathi, H.W. van de Venn, in: From Unstructured Product Descriptions to Structured Data for Industry 4.0 with ChatGPT, in: 2024 IEEE 7th International Conference on Industrial Cyber-Physical Systems (ICPS), IEEE, St. Louis, MO, USA, 2024, pp. 1–8. 

- [49] D. Shi, P. Liedl, T. Bauernhansl, Interoperable information modelling leveraging asset administration shell and large language model for quality control toward zero defect manufacturing, J. Manuf. Syst. 77 (2024) 678–696. 

- [50] ECLASS, An introduction to the standard [Online]. Available: https://eclass.eu/en 

   - /eclass-standard/introduction, 2024. 

- [51] D. Shi, O. Meyer, M. Oberle, T. Bauernhansl, Dual data mapping with fine-tuned large language models and asset administration shells toward interoperable knowledge representation, Robot. Comput.-Integr. Manuf. 91 (2025) 102837. 

- [52] IEC, IEC TR 63283-2:2022 Industrial-process measurement, control and automation – smart manufacturing – part 2: use cases (2022). 

- [53] IDTA, Aasx-package-explorer, GitHub repository. 2024. [Online]. Available: https ://github.com/eclipse-aaspe/package-explorer. 

- [54] M. Schiesser, RAGapp [Online]. Available: https://github.com/ragapp/ragapp, 2024. 

- [55] OpenAI, Models [Online]. Available: https://platform.openai.com/docs/models, 2024.

### Page 15

