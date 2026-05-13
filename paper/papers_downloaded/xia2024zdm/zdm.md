# Journal of Manufacturing Systems 77 (2024) 678–696 **==> picture [61 x 67] intentionally omitted ...

Source: xia2024zdm.pdf


---

### Page 679

> _D. Shi et al.                                                                                                                                                                                                                                      Journal of Manufacturing Systems 77 (2024) 678–696_ 

an object, containing three sets of attributes, namely static, process, and resource attribute set. This information model was implemented in an XML nodeset file as a part of the OPC UA server. Sousa et al. [14] integrated measuring devices into an IoT system using OPC UA to receive and send information related to quality control activities. Aminabadi et al. [15] employed OPC UA for in-line process quality control of injection molding machines, collecting heterogeneous data from machines and additional sensors. These information models above are typically proprietary and designed by the authors for specific applications without considering existing standards. Bogedale et al. [16] adopted OPC UA CS compliant with the EUROMAP 63 standard for injection molding machines to ensure interoperability. However, quality measurement data had to be manually added to the information model and linked with machine process data. 

This situation highlights a common issue in industry practices, where quality data, especially those involving human inspections or laboratory tests, are not always seamlessly integrated into information models like those provided by OPC UA. Given OPC UA’s design for machine-tomachine communication, it is not ideally suited to handle data generated from human-involved activities. A more general approach to information modeling is ontology [8]. Ontology provides a structured framework that organizes information by defining concepts and categories within a subject domain, along with their attributes and relationships. This structure can facilitate semantic interoperability, enabling effective communication and collaboration across various stakeholders in a complex domain [17]. Ontologies are typically implemented in web ontology language (OWL) and resource description framework (RDF) and use query languages, such as SPARQL, for information querying. In the ZDM domain, Psarommatis et al. [18] utilized three classes—‘Resource’, ‘Operation’, and ‘Entity’—from Manufacturing Semantic Ontology, based on OWL to structure and enrich input data within the proposed decision support system for defect detection and decision-making in repair activities. Historical data on defect types and severity, along with associated repair decisions, were stored in an RDF database. Once a new defect was identified, past decisions related to defects of similar severity and type were retrieved by SPARQL queries for current decision-making support. Roh et al. [19] developed a sensor ontology based on OWL to describe sensing data in the aspects of sensing data in additive manufacturing, linking sensor data from the production process to product quality. Xu et al. [20] established an ontology-based database for quality problem-solving in the automotive industry, where relationships of faults, immediate measures, causes, and measures were extracted from the original quality-related documents to construct the OWL-based ontology. Rheman and Kifor [21] constructed an OWL-based ontology for preserving, reusing, and sharing valuable knowledge generated during failure mode and effects analysis (FMEA). However, semantic web technologies such as OWL and SPARQL have not been widely adopted in the established software landscape of the production industry, which includes systems such as Enterprise Resource Planning (ERP), Product Lifecycle Management (PLM), and Manufacturing Execution Systems (MES). The widespread acceptance of ontology remains limited in the production industry. Apart from semantic web technologies, researchers have also developed ontologies in proprietary formats within specific software applications. For instance, Chen et al. [22] utilized an ontology graph to represent their proposed information model, which included process parameters, design parameters, process signatures, structured properties, and mechanical properties. A Bayesian network, built upon this ontology graph, was used for quality prediction, allowing the explicit consideration of constraints and causal relationships between variables during inference. Yang et al. [23] expressed knowledge in the form of an ontology that was extracted from the raw part verification reports during the pre-assembly process for quality improvement. This ontology, expressed in a format similar to RDF, indicated relationships among problems, causes, solutions, parts, and locations. Liu et al. [24] designed an information model for a DT framework aimed at quality traceability 

and dynamic control. The model was implemented in an XML format as part of a software application, taking inputs from associated systems such as MES, ERP, PLM, etc. 

However, information models in the form of ontology and OPC UA inherently possess certain limitations that can impact their interoperability. One of the primary limitations is that these models are designed with machine understanding in mind. As a result, the properties and data structures within these models often contain limited contextual information necessary for human interpretation. This focus on machine readability can make it challenging for human users, who are not familiar with the models developed by others and require more context for the reuse. Furthermore, the properties within these models are typically defined and named by developers based on the specific requirements of the application or software for which they are designed. This approach can lead to inconsistency in terminology and definitions across different systems and applications. The lack of a mechanism to reference external, generalized explanations for these properties exacerbates the issue, potentially hindering interoperability between different systems. 

Recently, AAS has emerged as a new standard for information modeling in manufacturing use cases, effectively integrating the concepts of DTs and ontologies while complementing the functionalities of the OPC UA information model [25]. AAS’s design promotes compatibility and convertibility with RDF [26] and OPC UA [27]. IEC 63278–2 [11] specifies and standardizes the AAS metamodel, which ensures uniformity across AAS applications. AAS mainly carries information through its submodels (SM), each representing a specific aspect of an asset tailored to a common use case in the practice. In academic research, the potential applications of AAS are being explored. Rahal et al. [28] conducted a general survey on AAS applications. In the area of ZDM, Cavalieri et al. [29] developed SMs for condition monitoring and maintenance to implement predictive maintenance. The SM Condition Monitoring contained information related to data acquisition, data manipulation, configuration, and aggregation, while the SM Maintenance encapsulated maintenance schedules and machine statuses. However, the structure of these SMs within the AAS framework was not detailed by the authors. Kim et al. [30] implemented ISO 15926 using AAS modeling to enhance the exchange of maintenance data in process plants. Monitoring data was modeled as the submodel element (SME) Property” in SM Operational Data. To provide standard definitions and semantics for properties, the ISO 15926 Reference Data Library (RDL) was introduced as an external dictionary. This integration of external dictionaries is a distinctive feature of AAS, ensuring the semantic interoperability of each SME. Sapel et al. [31] developed information models for production planning and control in the area of injection molding. The models were implemented in both ontology and AAS. The relevant industrial standards were referenced to provide standardized vocabularies and definitions. 

However, the process of referencing existing vocabularies has been manually performed by the model developers [30,31]. This is often labor-intensive and susceptible to inaccuracies. The automation of this process remains a significant hurdle. Despite the critical importance of addressing this challenge to improve efficiency and reduce errors, it has been relatively underexplored in research. Given that property attributes within information models can be interpreted as textual data, NLP techniques present a promising solution. For instance, Xu et al. [20] conducted text mining based on a document frequency algorithm, a statistical NLP technique, to extract feature words from the original quality-related documents for the definitions of properties. Similarly, Rheman and Kifor [21] and Yang et al. [23] also employed NLP techniques to extract knowledge for the creation of ontologies. 

In NLP, this problem is essentially about semantic matching or semantic search that matches two pieces of text, structured or unstructured. It is crucial in various NLP tasks such as machine reading comprehension, text classification, sentiment analysis, etc. [32]. In our problem setting, “two pieces of text” refer to the query property and the

### Page 680

_Journal of Manufacturing Systems 77 (2024) 678–696_ 

_D. Shi et al.                                                                                                                                                                                                                                      Journal_ 

existing property in a standardized vocabulary repository. The SOTA approaches for semantic matching and search involve encoding textual inputs into vectors by fine-tuning pre-trained language models (PLMs) such as BERT-like transformers and then comparing these vectors for similarity. The latest advancement in NLP is the emergence of LLMs, which are large-scale PLMs. [33]. A notable example is ChatGPT, which has demonstrated exceptional capabilities in text understanding. It is drawing more and more attention to exploring the potential of LLMs for solving industrial challenges. 

## _1.3. Research gaps and our contributions_ 

As highlighted in the literature review, data interoperability issues have been relatively underexplored in the area of ZDM. Most related studies have focused on formulating information models within specific frameworks. However, they often overlook the broader implications of the reusability of the developed information models and the systematic methodologies for information modeling. Moreover, the challenge of automatically processing data within models, e.g., for semantic reference, has not received much attention. 

In response to these gaps, we propose the utilization of AAS for information modeling coupled with an LLM for semantic reference. This combination aims to significantly enhance data interoperability in the quality control process and reduce manual intervention at the development stage. The primary contributions of our work are as follows: 

- 1) **Development of a systematic use-case-driven methodology for AAS-based information modeling.** This methodology is designed to be adaptable and scalable to a wide array of manufacturing use cases. 

- 2) **Implementation of AAS submodel templates as reusable information models for quality control** . We provide a clear exposition of how these models enhance data interoperability and how the models are deployed in the production environment. 

- 3) **Introduction of an LLM-based approach for semantic search** . This approach aims to automatically search and match query properties with standardized properties within the existing repository. It can also be applied to query the information and data from the AAS instances for process automation. 

## **2. Preliminaries** 

## _2.1. Asset administration shell_ 

An AAS serves as a centralized representation for all relevant information about an asset, functioning as the single source of truth in the Industry 4.0 framework. As Fig. 2 shows, an AAS and its represented asset are considered an Industry 4.0 component. Employing an objectoriented modeling approach, both the AAS and its components are expressed as classes, facilitating seamless integration into modern software architectures. Each AAS is linked to a specific asset and is uniquely identified by a distinctive identifier for that asset and the AAS itself respectively. The asset’s information is encapsulated within the AAS through its SMs, which are the primary carriers of information in the AAS, describing specific asset aspects relevant to particular use cases. For instance, the submodel _Digital Nameplate_ , as shown in Fig. 2, is the digital representation of regulatory-required physical nameplates on machines. Similarly, the SM _Generic Frame for Technical Data_ and _Provision of Simulation Models_ provide structured technical datasheets and metainformation of a simulation model, respectively. 

SMs are composed of hierarchically arranged SMEs, which are the fundamental building blocks for AAS information modeling. The AAS metamodel specifies various types of SMEs, such as Submodel Element Collection (SMC), Property, File, Multi-Language Property (MLP), Reference Element (RE), and Entity, each serving distinct asset description and differentiation functions. For example, an SMC represents a logical grouping of SMEs, while File allows for the attachment of data files, Property defines a characteristic for asset description and distinction, and RE allows the reference of another SME, SM, or AAS. The syntactic constraint and richness of SMEs are detailed in the standard [11]. 

Interoperability is primarily achieved by the standardized AAS metamodel as the rules for modeling, the standardized submodel templates (SMTs), and the concept description for semantic referencing. An SMT mainly determines the data structure and its compositions, i.e., SMEs, within this structure. An essential idea in Industry 4.0 is establishing standardized SMTs for every relevant aspect of an asset. Users can utilize the standardized SMTs and populate them with values to create specific SM instances in their applications, ensuring consistency. 

**==> picture [433 x 242] intentionally omitted <==**

**Fig. 2.** Illustration of Asset Administration Shell.

### Page 681

> _D. Shi et al.                                                                                                                                                                                                                                      Journal of Manufacturing Systems 77 (2024) 678–696_ 

The development and standardization of SMTs is an ongoing effort within the AAS community, primarily promoted by the Industrial Digital Twin Association (IDTA) [34]. Proposals for new SMTs or developed SMTs can be submitted to IDTA for review and standardization, with approved SMTs being published as open-source resources. For instance, the aforementioned three SMs in Fig. 2 have been published as the standardized SMTs by IDTA. While SMTs unify the data structure for specific use cases, semantic referencing through _Concept Description_ facilitates the universal understanding of individual SMEs. _Concept Description_ implemented as a class associated with SMEs, allows SMEs to reference external data specifications, which contain the existing standardized vocabularies and ontologies such as IEC 61360 Common Data Dictionary (CDD) [35], ECLASS [36], and ISO 15926 RDL [37]. This ensures consistent and accurate data interpretation across different systems and contexts, significantly enhancing interoperability. 

## _2.2. Semantic search_ 

Semantic referencing involves the comparison of semantic similarities of two data elements. In this process, one element is typically a query word or concept from the information model being developed, and the other is a target vocabulary term predefined in external data specifications such as IEC CDD, ECLASS, and ISO RDL. These data specifications are often structured as databases, where each vocabulary is represented as a property with several attributes within a formal ontological structure. Table 1 showcases an exemplary ECLASS property in the XML format. The attributes are shown in blue. The key attributes that express semantic meaning are _preferred_name_ and _definition_ . By referencing these standardized vocabularies in the AAS information model, developers can ensure that the data and concepts used in their models are consistent with established industry standards. 

The search engine implemented in the existing database [34–36] relies on literal matches between query words and vocabulary names, such as _’preferred_name’_ in ECLASS, without comprehending the broader meaning of both the query and the standardized vocabulary. Semantic search seeks to enhance search accuracy by understanding the intent 

behind the searcher’s query and the contextual meaning of the search terms. The semantic search problem we aim to address can be formulated as follows. 

Let _Xs_ = { _es_ } _[n] i_ =1[be a set of the query words identified by developers ] as data elements in an AAS information model, for which they seek semantic references. _Xs_ may not possess a formalized structure like an ontology. In real-world scenarios, _Xs_ could simply be a list of properties with or without textual descriptions. Each data element _es_ is characterized by its name and, potentially, an additional textual description. Let _Yt_ = { _et_ } _[m] j_ =1[represent a data specification database containing a ] large number m of pre-defined vocabularies with m≫n. Each vocabulary is structured, including attributes such as semantic identity, name, definition, unit, and value type. 

Given _Xs_ and _Yt_ , our task is to develop an effective search function _f_ ( _Xs, Yt_ ) that finds a matched subset _X_[ʹ] _t_[within ] _[Y][t ]_[based on property ] name, definition, and contextual information. 

Upon identifying the corresponding vocabularies within _X_[ʹ] _t_[, their ] semantic identifiers are referenced in the _Concept Description_ of the properties. This automated semantic search function aims to enhance search accuracy and minimize human intervention during the development stage of SMTs. 

## **3. Information modelling for quality control** 

This section presents our approach for information modeling, as depicted in Fig. 1, aimed at constructing the information models in the form of AAS SMTs. SMTs serve as the reusable template, allowing users to input values into pre-defined properties to facilitate interoperable information exchange. To ensure the interoperability and wide acceptance of the developed information models, we follow the relevant international and German standards as the modeling guidelines and propose a three-step modeling approach accordingly: use case description, derivation of AAS SMT from the use case, and semantic searching to link standardized vocabulary. 

**Table 1** 

Exemplary ECLASS property in the XML format. 

|LASS property in the XML format.||
|---|---|
|<ontoml:property<br>xsi:type="ontoml:NON_DEPENDENT_P_DET_Type"|id="0173-1#02-|
|AAM548#004" guid="e6de1ca0e4854c8fb77d095e72aec9d9">||
|<name_scope class_ref="0173-1#01-RAA001#001"/>||
|<date_of_original_definition>2011-02-11Z</date_of_original_definition>||
|<date_of_current_version>2019-06-11Z</date_of_current_version>||
|<date_of_current_revision>2019-06-11Z</date_of_current_revision>||
|<revision>1</revision>||
|<status>66</status>||
|<source_language language_code="en" country_code="US"/>||
|<preferred_name>||
|<label language_code="en" country_code="US">delivery time of supplier</label>||
|</preferred_name>||
|<definition>||
|<text language_code="en" country_code="US">duration per working|days needed by the|
|supplier to deliver the product beginning with the receipt of the order</text>||
|</definition>||
|<domain xsi:type="ontoml:REAL_MEASURE_TYPE_Type">||
|<unit unit_ref="0173-1#05-AAA495#003"/>||
|<quantity quantity_ref="0173-1#Z4-BAJ217#003"/>||
|</domain>||
|<is_multivalent>true</is_multivalent>||
|</ontoml:property>||

### Page 682

> _D. Shi et al.                                                                                                                                                                                                                                      Journal of Manufacturing Systems 77 (2024) 678–696_ 

## _3.1. Standard roadmap_ 

Standards typically summarize the best industry practice in a subject domain and provide the commonly accepted terminology. As depicted in Fig. 3, we adhere to a top-down approach, aligning with the standards related to AAS-based information modeling of quality control, which from a broad guidance level down to the system level of manufacturing operations management, further to the detailed execution level of quality control. 

At the guidance level, VDI 4499 Part 3 guides data management and software architecture for the digital factory [38], outlining standard procedures for deriving and implementing information models. Its recommendations for application field analysis and model design have been adopted in our work. Specifically, we utilize use case descriptions for application field analysis, employ Unified Modeling Language (UML) class diagrams for model design, and implement these models using AAS. This workflow is by the AAS standard IEC 63278 Part 1 [39] and Part 4 [40]. Notably, the methodology for use case description in IEC 63278–4 stems from IEC TR 63283–2 [41], and the semantic definition of data elements in information models as per IEC 63278–1 refers to the standard IEC 61360 [42]. These two standards are also essential within the overall modeling process. 

Quality control, as a part of quality management within an enterprise, must align with the overall enterprise-control system. IEC 62264 (also well-known as ISA 95) provides a comprehensive overview and detailed information models and terminology, describing the interaction between the business systems of an enterprise and its manufacturing operations and control systems. In particular, quality control and assurance are recognized as functions of quality operations management, modeled in standards [42–44]. To ensure the developed information models for quality control are consistent with other system components, we strive to maintain alignment with the IEC 62264 information models. 

Furthermore, the execution of quality control is governed by specific domain standards, often involving visual inspection and geometrical measurement. For demonstration purposes, we adhere to geometrical product specifications standards (GPS) to define quality criteria. 

## _3.2. Use case description_ 

In the context of Industry 4.0, interoperability is conceptualized as the ability of two or more objects from the same or different vendors to exchange information and utilize that information for accurate collaboration [39]. To realize interoperability through information models, it is imperative to identify the ’what’, ’when’, and ’who’ of the exchange process to specify the information model’s requirements. This is the purpose of the use case description. 

[41] to abstractly describe the process of today’s quality control. This methodology is well suited to describe the interaction of technical roles with a technical system, where information exchange often occurs during the interaction. Fig. 4 shows the use case of quality control. The use-case description language employs triplets to describe the interaction between two objects. The process starts from the specification of quality requirements, which may originate from the customer or a process engineer overseeing the production process and adhering to relevant quality standards. These quality requirements typically define the quality features for inspection. Depending on the inspection type, the inspector may need to configure the inspection machine beforehand for in-line inspections or conduct manual inspections for off-line cases. The inspection results could be structured or unstructured, such as manually recorded protocols in paper form or digital protocols from the inspection machine. In the case of laboratory tests, specimens are analyzed, and the results are often presented in the form of certificates or test reports. This results in heterogeneous forms of quality data. Simultaneously, the production machine generates process data, encompassing both static configurations and dynamic monitoring data. Different machine vendors may structure process data in different ways. In practice, quality data are generally associated with a production lot or a shift rather than directly linked to the corresponding process data of the individual (intermediate) products. 

The dotted box in Fig. 4 depicts the desired quality prediction within the ZDM strategy. To implement this, linking these two data types is crucial, but often manually executed or automated through tailored solutions in practice, making the process time-consuming, costly, and prone to errors. This linkage not only facilitates product traceability but also provides the necessary dataset for training AI models for future quality prediction. 

Based on the use case description for quality control, the following requirements for information modeling are identified. 

- Quality feature representation: The information model should enumerate the list of quality features as the measurable quality requirements. 

- Administrative information for quality control: The model must incorporate the administrative details of the execution of quality control, such as the date and contact information of the individual responsible for quality control. 

- Inspection/Test method or device specification: Detailed information about the inspection or test methods and devices used should be included in the model. 

- Metrology results: The model should provide the metrology results for each quality feature. This includes measurements, observations, and any deviations from standard values. 

We follow the methodology outlined in the standard IEC TR 63283–2 

**==> picture [505 x 151] intentionally omitted <==**

**Fig. 3.** Standard roadmap of information modeling for quality control.

### Page 683

_Journal of Manufacturing Systems 77 (2024) 678–696_ 

**==> picture [325 x 286] intentionally omitted <==**

**Fig. 4.** Use case of quality control. 

- Linkage to corresponding (intermediate) products: This linkage enables stakeholders to track the quality data back to specific product items. 

- Linkage to corresponding machine process data: This linkage enables stakeholders to track the quality data back to a specific job cycle and bridges the quality data with the process data, such as configuration settings and operational data of the production machine. 

## _3.3. Submodel templates for quality control_ 

Building on the requirements derived from the use case analysis, we developed a comprehensive suite of information models that fit within the framework of quality operations management as outlined in IEC 62264. This standard divides the entire manufacturing system into four key categories: production operations management, maintenance operations management, quality operations management, and inventory operations management. An overarching generic information model is defined to ensure the equivalent model structure of each operations management category. This generic model is designed to represent different stages of operations and is composed of a definition information model, a capability information model, a schedule information model, and a performance information model. They indicate the definition of work, available capabilities for performing work, scheduled requests to perform work, and outcomes of work performed, respectively. Each model incorporates several common object models, including personnel, role-based equipment, physical assets, materials, and process segments [43]. 

However, while IEC 62264 offers a general framework for operations models, it does not delve into the unique characteristics of quality operations management. Our approach aims to utilize the overarching structure provided by IEC 62264 but with a concentrated focus on the distinctive aspects of quality control. In the context of quality control, the four-stage information models refer to quality test definition model, quality test schedule model, quality test capability model, and quality test performance model. The quality test definition model defines the 

work associated with quality control that is pre-determined at the production design stage. When a production order is initiated, the work should be scheduled and requested for execution described in the quality test schedule model. Scheduling should consider the up-to-date information on available production resources necessary for quality control, which is provided by the quality test capability model. As a response to the request, the work performed is documented in the quality test performance model. 

Fig. 5 presents four UML class diagrams and their corresponding AAS implementations as part of the proposed SM _Quality Control._ The complete information model’s UML diagrams can be found in Fig. 8 in Annex I. Each class diagram specifies the class name (in cursive), such as _QualityTestPerformance_ , and the type of superclass (in bold), such as _Submodel Collection_ – a predefined class in the AAS metamodel. The list of SMEs follows, formatted as “name: SME type [cardinality]”, indicating optional or mandatory attributes. For instance, the cardinality of “[0.1]” indicates that the underlying SME is optional, whereas the cardinality of “[1]” means mandatory. Adjacent to the UML diagrams are their implementations in the AASX Package Explorer, an editor for AASX files [44], demonstrating the hierarchical structure of the SM _Quality Control._ Each SME is listed with its name and type, such as SM, SMC and Property. 

The first class of the SM _Quality Control_ in Fig. 5 illustrates the aforementioned four-stage models as the SMCs: _QualityTestDefinition, QualityTestCapability, QualityTestSchedule,_ and _QualityTestPerformance_ Depending on the application scenario, the user decides which SMC is relevant and should be populated. A detailed description of the main composition within _QualityTestPerformance_ is provided below. 

The SMC _QualityTestPerformance_ offers the information to document the executed quality control activities. It includes the reference to the corresponding _QualityTestDefinition_ and _QualityTestSchedule_ via the RE _DefinitionRef_ and _ScheduleRef,_ respectively. The administrative information is described by the SMEs _ID, Description, OperationsType, State, HierarchyScope, ActualStartTime,_ and _ActualEndTime,_ which are defined in IEC 62264–2 [45]. The quality-control-specific attributes are modeled

### Page 684

_Journal of Manufacturing Systems 77 (2024) 678–696_ 

**==> picture [505 x 304] intentionally omitted <==**

**Fig. 5.** UML diagram of AAS SMT _Quality Control_ , alongside its second-level SMC _QualityTestPerformance,_ the third-level SMC _QualityFeatureActual_ , and the fourthlevel SMC _FeatureDefinition._ 

in the following SMCs, as shown in the second class in Fig. 5: 

- _ActualProductionDependency:_ This SMC connects the quality control activity to the corresponding production process and job order to link quality data with machine process data. In IEC 62264-3 [46], the performance model of a production process segment is termed “job response”, which provides machine process data. When this model is implemented as an AAS submodel, it can be referenced by RE _JobResponseRef._ 

- _ActualProductDependency:_ It links to the related (intermediate) product, which can be modeled as a product AAS, encapsulating information such as bill of material and CAD model. This contextual information can be referenced by RE _ProductRef._ 

- _ResponsibilityActual._ It provides the contact information of the organization or person who performed the quality control activities. The contact information is modeled in SMC ContactInformation, containing the attributes provided by an existing SMT _Contact Information_ [47]. 

- _EquipmentActual._ Details about the equipment used for quality control are captured here. The equipment refers to the model of rolebased equipment defined in IEC 62264-1 [43]. It represents a production facility at a hierarchy level, such as a work center, production line, production unit, work cell, etc., rather than a physical asset. For instance, a testing laboratory is typically modeled as a work center, including all equipment in the lab. At the same time, a standalone test device could be a work unit, which is at the same equipment hierarchy level as a production machine. Role-based equipment can be modeled as an AAS and is referenced by RE _EquipmentRef._ 

- _PhysicalAssetActual._ Details about the physical assets used for quality control are captured here. IEC 62264 differentiates between the role of an asset in production and its physical characteristics. The physical asset model contains information about the physical piece of 

equipment, while an object in the equipment model defines the equipment’s role during production. As mentioned, the role of a test device could be a work unit, while this device itself is a physical asset and has a unique serial number from its manufacturer. The physical asset can be replaced (e.g. because it is broken); in that case, the role will not change, but a new physical asset with a unique serial number will take the place of the old physical asset. In the SMC _PhysicalAssetActual_ , the AAS of the physical asset is referenced by RE _AssetRef_ . 

- _MaterialActual,_ If relevant, this attribute includes information about materials consumed during the quality control process. This SMC is more relevant to operations like production and maintenance. 

- _QualityFeatureActual._ This SMC documents the specifications of tested quality features and the test results. Its main components are further detailed in the third and fourth class diagrams. The notation “ _QualityFeature{00}: SMC [1.* ]_ “ indicates the possibility of multiple quality features, each described by its own SMC. Each _QualityFeature_ and the 

- documents the feature definition in SMC _FeatureDefinition_ test results in several properties. In SMC _FeatureDefinition,_ several types of geometric features are predefined according to a series of GPS-related standards. Depending on the feature type, the user decides which SMC is relevant and should be populated. The measurement value of the quality feature is represented by Property _ValueActual_ . Property _QualityinRange_ indicates whether the measured value is within the allowed range. 

## _3.4. Semantic search_ 

Each property presented in the UML is assigned a name and a description, defined by developers to align with the requirements of the specific use case and the relevant standards. At this stage, properties are defined in a proprietary approach. Semantic search aims to identify the potential reference of each property to the existing professional

### Page 685

> _D. Shi et al.                                                                                                                                                                                                                                      Journal of Manufacturing Systems 77 (2024) 678–696_ 

vocabulary in the standardized vocabulary repositories. The process of semantic search involves mapping the name and description of each proprietary property to its counterparts in repositories, such as ECLASS. This mapping ensures that the properties used in a particular AAS model align with industry-accepted terms and definitions, minimizing ambiguities and inconsistencies. 

The proposed search function _f_ ( _Xs, Yt_ ) comprises three key components: an embedding model ℇ _θ_ ℇ for similarity calculation, an approximate nearest neighbor (ANN)-based top-K retriever **R** _θ_ **R** and a generative classification model ℘ _θ_ ℘ for reranking. The algorithm, outlined in Table 2, executes as follows. In the first step, each property in _Xs_ and _Yt_ is reformulated by concatenating its semantically meaningful attributes (like property name, short name, definition, etc.) into a coherent sentence. This prepares the properties for subsequent encoding. Next, the properties in _Xs_ and _Yt_ are encoded into a common vector space using the embedding model ℇ _θ_ ℇ to create query embeddings and target embeddings, respectively. The vector length _l_ is predetermined during the training of the embedding model. To manage the potentially large size of the target embeddings, the retriever **R** _θ_ **R** is used to partition these embeddings into smaller indexed fractions and output the index path _І_ (ℇ _θ_ ℇ ( _Yt_ )). Based on this, the retriever **R** _θ_ **R** rapidly identifies the top-K candidates with the highest similarity scores for each query, which are the most similar to the query property. Finally, the candidates in textual format are iteratively input into the generative model ℘ _θ_ ℘ along with the query property. The model ℘ _θ_ ℘ evaluates each pair to determine whether they are matched, updating the scores accordingly. After iterating through the K pairs, the candidates are reranked based on the updated scores, ensuring the most relevant matches are prioritized. 

The simplified structures of the models ℇ _θ_ ℇ and ℘ _θ_ ℘ are presented in Fig. 6. The foundation language model refers to a pre-trained LLM. It is important to note that the foundation models for embedding and generative classification are distinct. To fine-tune an embedding model, the query, the positive candidate, and _K_ − 1 negative candidates are separately input into the foundation model. The last hidden layer is used to obtain the embeddings through the pooling layer. Depending on the pre-trained foundation model, the pooling layer may refer to special token pooling, mean pooling, last token pooling, etc. For each query embedding ℇ _θ_ ℇ ( _es,i_ ), we compute the cosine similarity scores with each candidate embedding ℇ _θ_ ℇ ( _e[K] t,ij_ ) and scaled them by a factor _s_ : 

**==> picture [254 x 16] intentionally omitted <==**

**==> picture [255 x 61] intentionally omitted <==**

**==> picture [255 x 43] intentionally omitted <==**

During the inference stage, the embedding model outputs embeddings to serve as the input for the retriever **R** _θ_ **R** . This work utilizes the existing Faiss library [48] to implement the retriever. The retrieved top-K candidates are then concatenated with the prompt and the query, forming the input for the generative classification model. For each pair of _es,i_ and _e[K] t,_ ij[, this generative model ][℘] _θ_ ℘[(] _[e] t[K][,][ e][s]_[)][predicts a binary label ] _yC,ij_ ∈ _YC_ , where the label set is _YC_ = { _yes, no_ } _._ The prediction is driven by a prompt _pi,j_ through a causal language modeling head, which predicts the probability of the next token from the dictionary. The implementation of the generative model is based on the default class “LlamaForCausalLM” or “MistralForCausalLM” in the HuggingFace transformers library [49]. 

There are two approaches to obtaining the generative model for our application: prompt engineering and fine-tuning. Prompt engineering primarily leverages the design of prompts to exploit the powerful generalization capabilities of the pre-trained LLM. This method requires minimal computational resources. Table 3 presents the designed chainof-thought (CoT) prompt, which is the SOTA in-context learning (ICL) approach for prompting. The first part specifies the systematic instructions, clarifying the task and constraints. The second part emulates the human reasoning process by decomposing the complex task into several smaller steps. The third part provides examples of inputs and correct outputs. The final part consists of the actual inputs for prediction in a structured way. 

Fine-tuning, on the other hand, adapts the pre-trained LLM to our application by adjusting its parameters based on the training dataset. This process is computationally intensive and requires substantial re- 

**Table 2** 

Algorithm of semantic search function. 

**==> picture [433 x 199] intentionally omitted <==**

**----- Start of picture text -----**<br>
Algorithm: semantic search function<br>Input : a list of query properties  , a list of target standardized properties<br>Input : encoder ℇ ℇ [, retriever ][ℛ] ℛ [, proposal ][℘] ℘<br>Output : matched<br>Restructuring  and  by concatenating all the attributes of a property as a sentence<br>Encoding all the properties in  and  to a common vector space: ℇ ℇ [(] ) ∈ℝ and ℇ ℇ [(] ) ∈ℝ ,<br>denotes the given length of the embedding vector.<br>Partitioning and indexing the embeddings of ℇ ℇ [(] ) to get the index path  ℇ ℇ [(] )<br>for  each query vector ℇ ℇ [(] ) in ℇ ℇ [(] )  do<br>Retrieving and ranking the top-K candidates in terms of similarity  = ℛ ℛ [(ℇ] ℇ [(] ), ℇ ℇ [(] ) )<br>for  each candidate  do<br>Binary generative classification ℘ ℘ [(] , ) and update the score<br>end<br>reranking the candidates and let human decide the final target property<br>end<br>Consolidating by aggregating<br>**----- End of picture text -----**<br>

### Page 686

> _D. Shi et al.                                                                                                                                                                                                                                      Journal of Manufacturing Systems 77 (2024) 678–696_ 

**==> picture [433 x 290] intentionally omitted <==**

**Fig. 6.** Structure of the LLM-based embedding model and generative model. The dark blue blocks indicate a model component, while the light blue blocks indicate inputs, intermedia outputs or final outputs. 

**Table 3** 

Design of CoT prompt. 

|**Prompt part**|**Prompts**|
|---|---|
|**Instruction**|You will read two sentence-like query property and candidate|
||property to be matched. Each property has the attributes like|
||name and description. Your task is to decide whether the two<br>properties are matched (they refer to the same property). Only|
||answer ‘yes’or ‘no’.|
|**Reasoning**<br>**process**|Think step by step. First, properties may be professional<br>terminologies in specifc domains, you should consider the|
||domain knowledge.<br>Second, the property names and descriptions or defnitions are|
||most important. Should consider synonyms.<br>Third, query property may be defned for a specifc use case or<br>domain, while candidate property may be defned in more<br>general terms. If the scope of the query belongs to that of the<br>candidate, they should be considered matching. However, if the|
||scope of the candidate belongs to that of the query, they should|
||be considered not matching.|
|**Examples**|Below are several examples._<_input_> <_query_>_name:<br>SERIAL_CODE. description: Serial number_<_/query<br>_> <_candidate_>_name: ID. defnition: referenceable identifer<br>_<_/candidate_> <_/input_> <_response_>_no_<_/response_>_|
|**Input**|_……_<br>_<_input_>_<br>_<_query_>_name:…description:…_<_/query_>_<br>_<_candidate_>_name:…defnition:…_<_/candidate_>_<br>_<_/input_>_<br>_<_response_> <_/response_>_.|



sources. However, fine-tuning alleviates the need for extensive prompt engineering and results in shorter prompts, which can reduce the usage cost per query. Only the instruction and input parts of the prompt shown in Table 3 are input into the model. This prompt is often referred to as zero-shot learning (ZSL) in prompt engineering. To address the challenges associated with fine-tuning LLMs, we employ a technique called low-rank adaptation (LoRA) [50]. In adapter-based fine-tuning, the 

original weights of the LLM remain frozen, and new trainable parameters are introduced as adapter modules. During fine-tuning, only the weights of these modules are updated. A LoRA module decomposes a weight matrix _W_ ∈ R _[d]_[×] _[d ]_ into two lower-rank matrices _BA_ , where _B_ ∈ R _[d]_[×] _[r]_ , _A_ ∈ R _[r]_[×] _[d]_ , and _r_ **≪** _d_ . Here, _r_ denotes the rank of the decomposition matrices. The quantity of training parameters for a single attention matrix is substantially reduced from _d_[2 ] to 2 _rd_ , making the fine-tuning process far more feasible for practical implementation. 

## **4. Case study** 

The proposed methodology for AAS-based information modeling has been effectively applied in various domains to develop diverse SMTs for different use cases [34]. This case study aims to demonstrate the application of AAS to address interoperability issues in data integration within the quality control process. Currently, data integration in ZDM is often achieved through ad-hoc solutions. For instance, process data— — such as machine status, control parameters, and sensor data along with quality test results, are accessed via different software systems and stored in various databases and formats. Variable names, definitions, and relationships are manually documented by process engineers in unstructured formats such as Word or Excel files. These documents are then delivered to data scientists for developing AI models for quality prediction. This manual data exchange and integration process often leads to inconsistencies and difficulties in data sharing across different systems and departments. 

The AAS provides a standardized framework for data representation in a hierarchical structure, serving as a single source of truth. This framework ensures seamless interoperability across different systems and scalable data integration by populating standardized SMTs with relevant data for new assets. For the user, AAS offers a unified interface to query information and data carried by the AAS using the proposed LLM-based semantic search. 

In the following subsections, we describe the application scenario to

### Page 687

> _D. Shi et al.                                                                                                                                                                                                                                      Journal of Manufacturing Systems 77 (2024) 678–696_ 

provide context and understanding and then focus on the implementation of AAS in the operational environment. While the development of quality prediction models as the data consumer is beyond the scope of this paper, we demonstrate the use of the LLM-based semantic search function to query the information and data within the AAS. In Section 5, we evaluate the search function for semantic referencing during the SMT development stage, which maps the proprietary properties to the standardized ECLASS properties to improve interoperability. 

## _4.1. Application scenario_ 

Our approach was implemented and evaluated for a real-world scenario of injection molding, a process widely used for mass-producing plastic products. Injection molding involves melting polymer granules and injecting them into mold cavities, where they solidify into the final product upon cooling. The equipment typically used in this process includes an injection molding machine, a mold, and peripheral devices like temperature control units and hot runners. 

The production process begins with the design and verification of the mold during the new-product-introduction stage. However, the parameters set at this stage are not directly transferable to mass production. The commissioning of the equipment parameters is necessary to adapt to the conditions of mass production. The transition from commissioning to mass production requires continuous monitoring of production processes and product quality. Over time, changes within the mold can lead to quality abnormalities. Issues are reported to the process engineer, who analyzes the problem, identifies the root cause, and implements corrective measures, often involving re-adjustment of parameters. 

Since this iterative commissioning process is time-consuming and often delays production, the manufacturer desired to implement the ZDM strategy using the collected process data, incl. sensor data, equipment setting parameters, and status parameters to predict the quality data. To ensure the scalability and adaptability of the solution across different production lines and factories with varied equipment and management software, a focus on interoperability is essential. To this end, we introduced the solution of AAS-based information modeling to create common SMTs as interoperable information carriers across different departments and software systems within the company. This approach facilitates subsequent data consumption, such as using AI models for quality control and LLMs for semantic search and reasoning. 

## _4.2. System implementation_ 

The SM _Quality Control_ , as designed in Section 3, is initially implemented in a passive AASX file format using the AASX Package Explorer. The properties defined in the class diagrams in Fig. 5 are then matched with standardized ECLASS properties for semantic reference. A detailed demonstration and evaluation of the proposed semantic search are provided in Section 5. Once the SMTs are established, AASs can be effectively implemented and integrated into the operational environment, as illustrated in Fig. 7. 

The green section of Fig. 7 depicts the relevant processes and activities on the shop floor. The quality test is conducted according to ISO 2859–1 [51] for manual visual inspection, aided by a metrology measurement device for geometrical measurement and an electronic scale for weighing. During each production cycle, a handling robot moves the produced part from the injection molding machine to the measurement device. The quality test activities and results are programmatically populated into the SMT _Quality Control_ , which is deserialized as a Java object via the Basyx Java SDK in the IT backend [52]. Similarly, the collected process data are populated into the SMT _JobResponse_ of the AAS _InjectionMoldingMachine_ , referenced via the RE _JobResponseRef_ within the SMT _Quality Control_ . Once populated with values, these templates become specific AAS/SM instances. These instances are transmitted via edge gateways from the shop floor operational system to the cloud, where they are hosted on the AAS server and become accessible for querying, supported by the AAS registry. The registry maintains records of identifiers and endpoints for all AASs and SMs, facilitating property lookup. Properties and their values within hosted SMs are queryable via REST-API. The yellow section shows how the combination of the AAS server and registry forms the basic IT infrastructure, supporting the operational framework of AAS in the production environment. 

In the example provided in Fig. 7, a quality feature named “DistanceC_TopViewis” is predefined as 81 mm in the CAD, with a tolerance norm following DIN 16749, equating to a tolerance range of ± 0.44 mm. The actual measured value and associated contextual information are populated into the SMT _QualityControl_ in the AAS server backend. This generates an AAS instance specific to that production cycle. The dynamic value generated can be visualized on the server front end at the bottom left side. External applications like quality prediction models and LLMs access this value and other relevant information within the AAS through REST APIs. These APIs can be queried in the domain 

**==> picture [505 x 215] intentionally omitted <==**

**Fig. 7.** Process flow of quality control for injection molding in the case study scenario.

### Page 688

> _D. Shi et al.                                                                                                                                                                                                                                      Journal of Manufacturing Systems 77 (2024) 678–696_ 

“/swagger” of the corresponding port. The returned data is presented in XML/JSON format, encompassing all the information of the queried SME. 

These deserialized data form the knowledge base for the LLM search function. Given a query, the search function can retrieve properties within the AAS that are most similar to the query, allowing users to efficiently locate desired information from a single AAS instance rather than sifting through various unstructured source documents. Extending the search function with an LLM-Chat model enables users to query information seamlessly. Table 4 presents the use of the LLM-based semantic search function to query the information and data within the AAS instance, which are necessary for implementing the ZDM strategy. Fig. 9 in Annex II includes a screenshot of the web user interface for semantic search. In this demonstration, we illustrate how a data scientist can utilize the combination of AAS and LLM to access quality predictionrelated information and data. The embedding models and generative models used are described in more detail in Section 5. The LLM-Chat model is “gpt-4–1106-preview” provided by Azure OpenAI Service. 

This demonstration highlights the significant advantages of combining AAS and LLM. First, since all relevant information is collected within the AAS in a structured manner with detailed metadata in the form of properties and attributes, information and data are highly 

compact and structured, resulting in more efficient and accurate responses compared to querying multiple raw, unstructured data sources. For instance, as presented in the first conversation in Table 4, the SMC QualityFeatureList not only includes the measured value of the quality feature, which is typically found in the test protocol but also its definition and norm requirements, which would otherwise need to be sourced from relevant standards or technical documents. Second, the detailed information in the AAS provides the application-specific facts to the LLM, while the pre-trained LLM contains a certain amount of common sense and domain knowledge, which enhances the responses. For instance, in the second conversation, machine state variables are accessible via the communication protocol provided by the machine, where the variables are typically presented as abbreviations. Understanding these abbreviations and their contextual meaning is crucial for data scientists developing AI models. This information usually needs to be found in relevant documents or manually documented by process engineers. The LLM can explain variable abbreviations based on AAS properties and its embedded knowledge, providing users with a better understanding of the context. Third, the AAS server provides REST APIs for external software services to access its data. The REST API endpoint for the queried property can be automatically generated by the LLM with knowledge of the AAS model structure, enabling the automation of the 

**Table 4** Use of the LLM-based semantic search function to query the information and data within the AAS instance for quality control. 

||**Queries**<br>**Semantic search results**<br>**Conversation 1: query the measured quality feature**|
|---|---|
||Which properties contain the measured quality features?<br>idShort<br>description<br>Score<br>QualityFeatureList<br>List of<br>quality<br>criteria of<br>the item<br>and their<br>properties<br>0.88<br>What are the measured quality features within the SMC QualityFeatureList and which<br>attributes does one quality feature have?<br>Quality Features:<br>Properties:<br>DistanceC_TopView<br>LinearFeatureName, DimensionDescription,<br>InspectionRelevant, ToleranceNorm, UpperTolerance,<br>LowerTolerance, OneSided<br>What is the measured value of this feature?<br>The measured value of this feature is specifed in the ValueActual property. The value is<br>80.87.<br>**Conversation 2: query the machine state variable**<br>Which properties contain the states of the production machine?<br>idShort<br>description<br>Score<br>MachineState<br>containing<br>up-to-date<br>machine<br>state<br>parameters<br>for a<br>certain job<br>at a certain<br>cycle time<br>0.83<br>Which variables are recorded in the SMC MachineState?<br>The SMC MachineState records the following variables: spcTime, EL_CYC_TIME,<br>EL_NZL_MEAN, EL_CLAMP_PRESS, EL_MOP, EL_PLST_END_ERR, EL_INJ_START_STR…<br>Can you explain these variables based on their descriptions and your knowledge to me?<br>spcTime: This variable captures the exact time when a machine cycle is completed. It is<br>essential for tracking production timing and effciency within the MES.<br>EL_CYC_TIME: This represents the total time taken to complete one cycle of operation.<br>Cycle time is a critical measure of productivity and effciency, indicating how quickly a<br>machine can produce a part.<br>EL_NZL_MEAN: This is the average temperature recorded during the cycle, likely related to<br>the nozzle temperature in injection molding or similar processes. Maintaining the correct<br>temperature is crucial for product quality and consistency….<br>Which variables may be signifcantly related to the quality feature DistanceC_TopView<br>of the product?<br>EL_CLAMP_PRESS (Mold clamping pressure): Adequate clamping pressure is essential to<br>ensure the mold halves remain closed without any gap during the injection process,<br>preventing fash and ensuring consistent dimensions.EL_MAX_INJ_PRESS<br>(MaximumInjectionPressure): The maximum injection pressure ensures that the material is<br>properly forced into all areas of the mold, impacting the fnal dimensional accuracy.…<br>Can you generate REST API for the property EL_CLAMP_PRESS? For example, The API is<br>in such a pattern:http://localhost:5001/submodels/aHR0cHM6Ly9leGFtcGxlLmNvbS<br>9pZHMvc20vMDM4MF84MDQwXzkwMzJfNjc1MQ= =/submodel-elements/Qualit<br>yTestPerformance.QualityFeatureActual.QualityFeature00<br>aHR0cHM6Ly9leGFtcGxlLmNvbS9pZHMvc20vMzE5NV8zMTYwXzIwNDJfNTEwNw is<br>the encoded submodel id for JobResponse in Base64 format. The REST API endpoint for the<br>property EL_CLAMP_PRESS is:<br>http://localhost:5001/submodels/<br>aHR0cHM6Ly9leGFtcGxlLmNvbS9pZHMvc20vMzE5NV8zMTYwXzIwNDJfNTEwNw= =/<br>submodel-elements/MachineState.EL_CLAMP_PRESS|

### Page 689

_Journal of Manufacturing Systems 77 (2024) 678–696_ 

_D. Shi et al.                                                                                                                                                                                                                                      Journal_ 

data integration process. 

## **5. Evaluation of semantic search** 

## _5.1. Objectives_ 

In current practices, searching the reference of _Concept Description_ for property has to be manually conducted through the search engine provided by data specification repositories, being notably time-consuming and inefficient. For instance, when attempting to find a reference for Property ToleranceNorm in the ECLASS repository, a search of the term “Tolerance Norm” yields 394 results, as shown in Fig. 10 in Annex II, making it difficult to pinpoint the exact referencable property. This requires a manual review of preferred names and definitions to identify the correct target ECLASS property, which is an exceedingly laborious and error-prone process. The proposed algorithm for semantic search transcends the limitations of literal match searches. It allows for the inclusion of contextual descriptions alongside the property name, e.g. „referenced norm or standard defining the applicable tolerance of the tested quality feature“, enhancing the precision of the search. Fig. 10 in Annex II shows the search results on the implemented user interface. 

To evaluate the effectiveness of the proposed semantic search algorithm, statistical experiments are conducted on the customized AASECLASS dataset, where the AAS properties are queried in the ECLASS repository for semantic reference. These experiments aim to address the following research questions (RQs): 

- RQ1: What is the optimal setup for the embedding model and the retrieval process, including the type of pre-trained embedding models and the optimal top-K number for the retriever? 

- RQ2: Is fine-tuning (or transfer learning) the LLM-based embedding model on the small customized dataset effective and worthwhile? 

- RQ3: What is the optimal strategy for the reranker: fine-tuning or prompt engineering? Additionally, is fine-tuning the LLM-based generative classification model on the small customized dataset effective and worthwhile? 

the embedding model ℇ _θ_ ℇ combined with the retriever **R** _θ_ **R** , aiming to answer RQ1 and RQ2. All the queries and ECLASS properties are encoded by the embedding model ℇ _θ_ ℇ . For each query, the retriever **R** _θ_ **R** retrieves the top-K candidates from a pool of 27,423 ECLASS properties. Among the K candidates, only one may correspond to the true positive match. The fine-tuning and evaluation dataset consists of samples, each comprising a query property, one positive candidate, and K − 1 negative candidates. 

The models are fine-tuned over ten epochs on the GPU cluster of 8xA100 GPUs. For evaluation, we use the following evaluation metrics: mean reciprocal rank at rank K (MRR@K), mean hit rate at rank K (MHR@K). MRR@K is a standard measure for assessing retrieval system effectiveness. For the query set _Xs_ , the MRR is calculated as: 

**==> picture [254 x 19] intentionally omitted <==**

Where _ranki_ denotes the position of the true positive ECLASS property. If the true positive does not appear within the top-K candidates, _ranki_ = 0. 

MHR@K indicates whether the true positive one appears within the returned K candidates, regardless of their rank. It’s a binary measure per query. MHR metrics at different K values (20, 15, 10, 5) help determine the optimal top-K value. 

In Exp.2, the focus shifts to the generative classification model ℘ _θ_ ℘ used for reranking, aiming to answer RQ3. Each input sample is restructure as a matching pair consisting of a query property, a candidate match, and a match label. For each query pair, the generative model fine-tuning, we balance the training dataset by ensuring the number of ℘ _θ_ ℘ predicts a binary label to determine if the pair matches. For negative pairs equals the number of positive pairs. The models are finetuned across ten epochs and evaluated on the test set. In the test set, negative samples are much more prevalent than positive ones since only one true positive sample appears in the K candidates. Due to this imbalance, the F1 score is primarily used as the evaluation measure, which is the standard measure in the entity matching task [53]. Other metrics such as accuracy, recall and precision are also presented. 

## _5.2. Datasets_ 

## _5.4. Evaluated models_ 

The AAS-ECLASS dataset established in this work contains the query set _Xs_ and the target set _Yt_ . The query set _Xs_ comprises AAS properties from all the SMTs published on the IDTA website [34], including SMT _Quality Control._ After deduplication, this results in 376 unique properties, each characterized by the attribute of “idShort” and “description”. The target set _Yt_ includes all unique properties from the ECLASS repository, version 12 Advanced. Following the removal of properties with different versions, the dataset includes 27,423 unique properties, each with the attribute of “preferred name” and “definition”. Out of the total 2376 AAS properties, only 491 have referenced the corresponding ECLASS properties, identifying them as positive pairs. This ground truth is established through _Concept Description_ of each query property in the existing SMTs, which is manually populated using the ECLASS search engine. Since the labor-intensive nature of manual annotation may include false results due to human errors, the final search results produced by the algorithms were also evaluated manually. A significant portion of AAS properties ack referencable ECLASS properties. This is mainly due to the limitations of the current ECLASS repository, which does not comprehensively cover all properties relevant to the production industry and is subject to annual updates. The 491 positive samples undergo a train-valid-test split in a 6–2-2 ratio, resulting in 295–98-98 train-valid-test samples. 

## _5.3. Experiment settings and evaluation metrics_ 

There are two experiments designed to evaluate different aspects of the semantic search algorithm. In Exp.1, we assess the performance of 

In Exp.1, the retriever remains consistent throughout, utilizing the well-accepted Faiss library [48]. The primary focus is comparing different embedding models and evaluating the impact of varying the top-K value. The embedding models under evaluation include the SOTA commercial model "text-embedding-3-large" from OpenAI [54], the representative open-source LLM-based embedding model “SFR-Embedding-Mistral” [55], and the representative sentence-transformer-based embedding model “all-mpnet-base-v2″ [56]. 

In Exp.2, the evaluated models include the representative opensource LLM Llama2 [57] and, with various model versions and prompting strategies. Additionally, we re-implemented two representative SOTA approaches for entity matching on our dataset: a fine-tuning transformer-based approach [60] and a GPT-4 with ICL approach [61]. 

## _5.5. Exp.1 results and discussions_ 

RQ1: What is the optimal setup for the embedding model and the retrieval process, including the type of pre-trained embedding models and the optimal top-K number for the retriever? Table 5 shows the evaluation results, demonstrating that the pre-trained SFR-EmbeddingMistral model achieved the best performance, outperforming even the latest commercial model "text-embedding-3-large" from OpenAI. The conventional sentence-transformer-based model "all-mpnet-base-v2" did not perform as well as the LLM-based models. The advantage of using all-mpnet-base-v2 is its lower computational resource requirement, allowing it to perform inference efficiently even on a CPU. For users who do not have access to GPU resources needed to run LLM-based

### Page 690

> _D. Shi et al.                                                                                                                                                                                                                                      Journal of Manufacturing Systems 77 (2024) 678–696_ 

## **Table 5** 

Exp.1 results. The first three models are the pre-trained models, while the last one is the SFR-Embedding-Mistral fine-tuned on our dataset. The metrics are presented in percentile. 

|<br>percentile.||||||
|---|---|---|---|---|---|
|**Model**|**MHR@ 20**|**MHR@ 15**|**MHR@ 10**|**MHR@ 5**|**MRR@ 10**|
|SFR-Embedding-Mistral|**92.9**|**89.8**|**88.8**|**80.6**|**68.6**|
|text-embedding−3-large|90.8|87.8|87.8|78.6|64.6|
|all-mpnet-base-v2<br>fne-tuned SFR-Embedding-Mistral|75.5<br>88.4|70.4<br>84.8|64.3<br>83.6|59.2<br>79.2|45.5<br>62.4|



embedding models like SFR-Embedding-Mistral, or those who cannot access LLM web services like GPT-4, all-mpnet-base-v2 serves as a viable alternative. 

The SFR-Embedding-Mistral model attained a 92.9 % MHR@ 20 and an 88.8 % MHR@ 10 with a 4.1 % drop rate for searching a query among 27,423 ECLASS properties. When K = 5, the MHR drops from 88.8 % to 80.6 %, resulting in an 8.2 % drop rate. Considering that when K = 10, the drop in MHR is not substantial and it saves time in the subsequent pairwise reranking inference, we decided to use a top-10 setting in the current implementation of the semantic search algorithm. This setting sends the top 10 candidates to the subsequent pairwise matching step. 

RQ2: Is fine-tuning (or transfer learning) the LLM-based embedding model on the small customized dataset effective and worthwhile? We fine-tuned this model on the AAS-ECLASS dataset, following the model structure depicted in Fig. 6, with the pre-trained SFR-Embedding-Mistral serving as the foundation model. The implementation primarily utilized the HuggingFace transformers library [58] for the pipeline and modeling, along with the PEFT library [59] for LoRa-based fine-tuning. The LoRa rank is set to 64. Other hyperparameters are set as suggested in the LoRa paper [50]. The result was a "fine-tuned SFR-Embedding-Mistral" model. Surprisingly, the fine-tuned model performed worse than the pre-trained model. This decline in performance could be attributed to the complexity of training embedding models and the small size of our dataset. As indicated in [55], the original SFR-Embedding-Mistral was fine-tuned on the baseline e5-mistral-7b-instruct model using transfer learning with a large batch size of 2048 across diverse tasks on tens of different datasets. In contrast, our computing resources only allow a batch size of 32, and our dataset is too small compared to these public datasets. In this sense, it is better to directly use the pre-trained embedding model, rather than fine-tuning it on a domain-specific but small-scale dataset. 

## _5.6. Exp.2 results and discussions_ 

RQ3: What is the optimal strategy for the reranker: fine-tuning or prompt engineering? Additionally, is fine-tuning the LLM-based generative classification model on the small customized dataset effective and worthwhile? Table 6 presents the experiment results. The fine-tuned Llama2-Chat-13B model and GPT4-CoT represent the fine-tuning and prompt engineering approaches, respectively. The base model of Llama2-Chat-13B is fine-tuned on our dataset with a LoRa rank of 32. 

## **Table 6** 

Exp.2 results. The first two models are the proposed two generative classification approach. The next four models are comparative models for ablation study. The last two models are the competitive SOTA approaches implemented on our dataset. The metrics are presented in percentile. 

|Model|F1|Recall|Precision|Accuracy|
|---|---|---|---|---|
|Fine-tuned Llama2-Chat−13B|**76.5**|**79.6**|**73.6**|**93.0**|
|GPT4-CoT<br>Pre-trained Llama2-Chat−13B-ZSL|75.5<br>25.4|72.3<br>63.3|78.6<br>15.9|92.7<br>47.0|
|Pre-trained Llama2−70B-ZSL|29.0|94.9|16.8|32.0|
|Pre-trained Llama2−70B-CoT<br>GPT4-ZSL<br>GPT4-ICL[61]<br>Fine-tuned RoBERTa-large[60]|46.5<br>55.5<br>71.9<br>65.2|40.8<br>40.8<br>70.4<br>90.8|54.1<br>87.0<br>73.45<br>50.9|86.7<br>90.7<br>92.2<br>86.2|



The prompt follows the ZSL method in prompt engineering, containing only the instruction and the input data. GPT4-CoT employs the CoT prompt presented in Table 3, with two positive and two negative matching examples provided as demonstrations. As a result, the finetuned Llama2-Chat-13B achieved slightly better performance than GPT4-CoT. A higher recall rate of 79.6 % suggests that the fine-tuned model more effectively avoids missing the correct ECLASS property when it appears among the retriever’s candidates. However, a relatively lower precision of 73.6 % indicates a tendency for false matching with incorrect properties. 

For the ablation study, we compare “fine-tuned Llama2-Chat-13B” with “pre-trained Llama2-Chat-13B-ZSL” to demonstrate the effectiveness of fine-tuning. Without fine-tuning, the pre-trained Llama2-Chat13B model with the ZSL prompt is not adequate for our use case. Even using the larger Llama2-Chat-70B model with ZSL does not change the result. In comparison, GPT4-ZSL performs much better than the pretrained Llama2–70B-ZSL, indicating that GPT4 outperforms the opensource LLM in our case, but still does not achieve meaningful results. – Comparing the pre-trained Llama2 70B-ZSL with the pre-trained Llama2– 70B-CoT, and GPT4-ZSL with GPT4-CoT, we observe significant improvements. This demonstrates the effectiveness of the designed CoT prompts. 

Finally, we compare our approach with two representative SOTA approaches implemented on our dataset. GPT4-ICL [61] is similar to GPT4-ZSL but uses an ICL prompt, which excludes the reasoning process in Table 3 . The fine-tuned RoBERTa-large refers to fine-tuning a small-scale transformer-based model, which is the best model in the entity matching task [53]. Our approaches outperform both SOTA approaches. 

We also assess the inference time for different models: Llama2-Chat13B (0.75 s/query), GPT-4-CoT (1.19 s/query), and RoBERTa-large (0.15 s/query). The inference time for GPT-4-CoT depends on the latency of the internet connection to the LLM server. Although RoBERTalarge is five times quicker than Llama2-Chat-13B, its inference speed cannot compensate for this speed advantage. More incorrect predictions can lead to much more increased human intervention, ultimately consuming more time. 

## **6. Conclusions** 

In this study, we have presented a systematic methodology for information modeling that utilizes the AAS and LLM to tackle interoperability challenges toward ZDM. Our focus is on integrating data from various sources, presented in different formats and accessed through different interfaces, a common occurrence during the development stage of quality prediction models. In comparison to conventional information models in the form of ontology and OPC UA, AAS emerges as a novel enhancement, offering semantic interoperability that facilitates machine-to-machine communication and ensures the models are comprehensible to human users. This methodology outlines the process of developing AAS models and guiding future developers. 

Furthermore, we have developed a specific SMT _Quality Control_ to achieve interoperable data integration within the quality control process. This model allows for the integration of heterogeneous source data into AAS SMs, enhancing the data with links and contextual information. Such enriched information models enable data consumers to easily

### Page 691

> _D. Shi et al.                                                                                                                                                                                                                                      Journal of Manufacturing Systems 77 (2024) 678–696_ 

understand the data, thereby facilitating the implementation of datadriven ZDM strategies. 

An essential aspect of AAS models is their capability to reference external standardized definitions of properties, promoting a unified understanding of properties across different systems and contexts. To minimize manual effort in the development phase, we proposed a novel semantic search algorithm based on LLMs. This algorithm automates the identification of query properties within a standardized vocabulary repository. Its effectiveness has been validated and demonstrated by evaluating a specially constructed dataset comprising query properties from published SMTs and standardized ECLASS properties. The comprehensive experiments also answer three RQs related to the algorithm, from which we can derive several insights that are generally meaningful for the usage of LLM in the manufacturing industry. 

The effectiveness and value of fine-tuning LLMs on small customized datasets are highly task-dependent. For complex tasks like text embedding, successful implementation often requires transfer learning across diverse tasks using large-scale datasets. Fine-tuning on a specific small dataset can sometimes reduce the model’s overall capability. Conversely, for simpler generative tasks, fine-tuning can yield impressive results even with small datasets. For instance, a relatively small open-source LLM with 13 billion parameters can be fine-tuned to outperform GPT-4, which has trillions of parameters. When a specific task needs to be performed repeatedly, fine-tuning an LLM for that task is advisable. However, fine-tuning LLMs requires substantial resources and expertise. Techniques like LoRa can assist in fine-tuning, but they still demand significant computational power, such as at least an 80 GB VRAM GPU or several 32 GB or 40 GB GPUs for efficient fine-tuning. In scenarios where fine-tuning LLMs is impractical due to resource limitations, using GPT-4 with CoT prompting, is a viable alternative. Without such prompt engineering, GPT-4 alone with ZSL is not effective for domain-specific tasks. 

In future work, the developed SMTs will be submitted for further review and standardization, making them readily available for use in quality control applications. 

Declaration of Generative AI and AI-assisted technologies in the writing process. 

During the preparation of this work, the author(s) used Grammarly and ChatGPT in order to improve language and readability. After using this tool/service, the author(s) reviewed and edited the content as needed and take(s) full responsibility for the content of the publication. 

## **CRediT authorship contribution statement** 

**Philipp Liedl:** Writing – review & editing, Project administration, Methodology, Investigation, Data curation, Conceptualization. **Thomas Bauernhansl:** Writing – review & editing, Supervision, Funding acquisition. **Dachuan Shi:** Writing – review & editing, Writing – original draft, Visualization, Validation, Software, Resources, Methodology, Investigation, Formal analysis, Data curation, Conceptualization. 

## **Declaration of Competing Interest** 

The authors declare that they have no known competing financial interests or personal relationships that could have appeared to influence the work reported in this paper. 

## **Acknowledgments** 

This work was supported in part by the “SDM4FZI” project (13IK001ZF) and in part by the “InterOpera” project (13I40V006C). Both projects are funded by the German Federal Ministry for Economic Affairs and Climate Action. 

## **Annex I**

### Page 692

> _D. Shi et al.                                                                                                                                                                                                                                      Journal of Manufacturing Systems 77 (2024) 678–696_ 

**==> picture [505 x 574] intentionally omitted <==**

**Fig. 8.** UML diagram of AAS SMT _Quality Control_ . a. top-level SMCs of _Quality Control_ ; b. lower-level SMCs of _QualityTestPerformance_ . 

.

### Page 693

_Journal of Manufacturing Systems 77 (2024) 678–696_ 

_D. Shi et al.                                                                                                                                                                                                                                      Journal_ 

## **Annex II** 

**==> picture [505 x 331] intentionally omitted <==**

**Fig. 9.** Screenshot of the web user interface for semantic search based on LLM and AAS. 

.

### Page 694

> _D. Shi et al.                                                                                                                                                                                                                                      Journal of Manufacturing Systems 77 (2024) 678–696_ 

**==> picture [505 x 620] intentionally omitted <==**

**Fig. 10.** Exemplary search results for Property _ToleranceNorm_ . Top: search result returned by the search engine of ECLASS; Bottom: search result returned by our algorithm for semantic search. 

.

### Page 695

> _D. Shi et al.                                                                                                                                                                                                                                      Journal of Manufacturing Systems 77 (2024) 678–696_ 

## **References** 

- [1] Mitra A., Fundamentals of quality control and improvement. Chichester, West Sussex: Wiley Blackwell; 2016. 

- [2] Judi H.M., Genasan D., Jenal R. Quality control implementation in manufacturing companies: motivating factors and challenges. INTECH Open Access Publisher 2011. 

- [3] Powell D, Magnanini MC, Colledani M, Myklebust O. Advancing zero defect manufacturing: A state-of-the-art perspective and future research directions. Comput Ind 2022;136:103596. https://doi.org/10.1016/j.compind.2021.103596. 

- [4] Tariq U, Joy R, Wu S-H, Mahmood MA, Malik AW, Liou F. A state-of-the-art digital factory integrating digital twin for laser additive and subtractive manufacturing processes. RPJ 2023;29(10):2061–97. https://doi.org/10.1108/RPJ-03-20230113. 

- [5] Psarommatis F, Sousa J, Mendonça JP, Kiritsis D. Zero-defect manufacturing the approach for higher manufacturing sustainability in the era of industry 4.0: a position paper. Int J Prod Res 2022;60(1):73–91. 

- [6] Psarommatis F, May G, Dreyfus P-A, Kiritsis D. Zero defect manufacturing: state-ofthe-art review, shortcomings and future directions in research. Int J Prod Res 2020; 58(1):1–17. https://doi.org/10.1080/00207543.2019.1605228. 

- [7] Fragapane G, Eleftheriadis R, Powell D, Antony J. A global survey on the current state of practice in Zero Defect Manufacturing and its impact on production performance. Comput Ind 2023;148:103879. https://doi.org/10.1016/j. compind.2023.103879. 

- [8] Psarommatis F, May G. A literature review and design methodology for digital twins in the era of zero defect manufacturing. Int J Prod Res 2023;61(16):5723–43. https://doi.org/10.1080/00207543.2022.2101960. 

- [9] Leberruyer N, Bruch J, Ahlskog M, Afshar S. Toward Zero Defect Manufacturing with the support of Artificial Intelligence—Insights from an industrial application. Comput Ind 2023;147:103877. https://doi.org/10.1016/j.compind.2023.103877. 

- [10] Boss B. et al., “Digital Twin and Asset Administration Shell Concepts and Application in the Industrial Internet and Industrie 4.0: An Industrial Internet Consortium and Plattform Industrie 4.0 Joint Whitepaper”- 2020. 

- [11] IEC, PREN IEC 63278–2:2022: Asset Administration Shell for Industrial Applications – Part 2: Information meta model, 2022. 

- [12] OPC Foundation, Unified Architecture, 2023, online available: 〈https://opcfoun dation.org/about/opc-technologies/opc-ua/〉〈〉. 

- [13] Han Y, Hu Y, Wang Y, Jia G, Ge C, Zhang C, et al. Research and Application of Information Model of a Lithium Ion Battery Intelligent Manufacturing Workshop Based on OPC UA. Batteries 2020;6(4):52. https://doi.org/10.3390/ batteries6040052. 

- [14] Sousa J, Mendonça JP, Machado J. A generic interface and a framework designed for industrial metrology integration for the Internet of Things. Comput Ind 2022; 138:103632. https://doi.org/10.1016/j.compind.2022.103632. 

- [15] Aminabadi SS, Tabatabai P, Steiner A, Gruber DP, Friesenbichler W, Habersohn C, et al. Industry 4.0 in-line Ai quality control of plastic injection molded parts. Polym (Basel) 2022;14(17). https://doi.org/10.3390/polym14173551. 

- [16] Bogedale L, Doerfel S, Schrodt A, Heim H-P. Online prediction of molded part quality in the injection molding process using high-resolution time series. Polym (Basel) 2023;15(4). https://doi.org/10.3390/polym15040978. 

- [17] Fraga AL, Vegetti M, Leone HP. Ontology-based solutions for interoperability among product lifecycle management systems: A systematic literature review. J Ind Inf Integr 2020;20:100176. https://doi.org/10.1016/j.jii.2020.100176. 

- [18] Psarommatis F, Kiritsis D. A hybrid Decision Support System for automating decision making in the event of defects in the era of Zero Defect Manufacturing. J Ind Inf Integr 2022;26:100263. https://doi.org/10.1016/j.jii.2021.100263. 

- [19] Roh B-M, Kumara SRT, Yang H, Simpson TW, Witherell P, Jones AT, et al. Ontology Network-Based In-Situ Sensor Selection for Quality Management in Metal Additive Manufacturing. J Comput Inf Sci Eng 2022;22(6). https://doi.org/10.1115/ 1.4055853. 

- [20] Xu Z, Dang Y, Munro P. Knowledge-driven intelligent quality problem-solving system in the automotive industry. Adv Eng Inform 2018;38:441–57. https://doi. org/10.1016/j.aei.2018.08.013. 

- [21] Zobia Rehman S.K. A Conceptual Architecture of Ontology Based KM System for Failure Mode and Effects Analysis. INTERNATIONAL JOURNAL OF COMPUTERS COMMUNICATIONS & CONTROL ISSN 1841–9836, 9(4):463–470, August, 2014. 

- [22] Chen R, Lu Y, Witherell P, Simpson TW, Kumara S, Yang H. Ontology-Driven Learning of Bayesian Network for Causal Inference and Quality Assurance in Additive Manufacturing. IEEE Robot Autom Lett 2021;6(3):6032–8. https://doi. org/10.1109/LRA.2021.3090020. 

- [23] Yang J, Kim E, Hur M, Cho S, Han M, Seo I. Knowledge extraction and visualization of digital design process. Expert Syst Appl 2018;92:206–15. https://doi.org/ 10.1016/j.eswa.2017.09.002. 

- [24] Liu J, Cao X, Zhou H, Li L, Liu X, Zhao P, et al. A digital twin-driven approach towards traceability and dynamic control for processing quality. Adv Eng Inform 2021;50:101395. https://doi.org/10.1016/j.aei.2021.101395. 

- [25] Miny T, Thies M, Lukic L, Kabisch S, Oladipupo K, Diedrich C, et al. Overview and ¨ Comparison of Asset Information Model Standards. IEEE Access 2023;11: 99189–221. https://doi.org/10.1109/ACCESS.2023.3312286. 

- [26] Rongen S, Nikolova N, van der Pas M. Modelling with AAS and RDF in Industry 4.0. Comput Ind 2023;148:103910. https://doi.org/10.1016/j.compind.2023.103910. 

- ¨ 

- [27] Drath R., et al. (2023): Diskussionspapier – Interoperabilitat mit der Verwaltungsschale, OPC UA und AutomationML. In: Plattform Industrie 4.0. Online accessible: 〈https://opcfoundation.org/wp-content/uploads/2023/04/Di skussionspapier-Zielbild-und-Handlungsempfehlungen-fur-industrielle-Intero perabilitat-5.3-protected.pdf〉. 

- [28] Rahal JR, Schwarz A, Sahelices B, Weis R, Anton SD. The asset administration shell ´ as enabler for predictive maintenance: a review. J Intell Manuf 2023. https://doi. org/10.1007/s10845-023-02236-8. 

- [29] Cavalieri S, Salafia MG. A Model for Predictive Maintenance Based on Asset Administration Shell. Sens (Basel) 2020;20(21). https://doi.org/10.3390/ s20216028. 

- [30] Kim B, Kim S, Teijgeler H, Lee J, Lee JY, Lim D, et al. Use of Asset Administration Shell Coupled with ISO 15926 to Facilitate the Exchange of Equipment Condition and Health Status Data of a Process Plant. Processes 2022;10(10):2155. https:// doi.org/10.3390/pr10102155. 

- [31] Sapel P, Hopmann C. Towards an ontology-based dictionary for production planning and control in the domain of injection molding as a basis for standardized asset administration shells. J Ind Inf Integr 2023;35:100488. https://doi.org/ 10.1016/j.jii.2023.100488. 

- [32] Liu Q, Mao R, Geng X, Cambria E. Semantic matching in machine reading comprehension: An empirical study. Inf Process Manag 2023;60:103145. https:// doi.org/10.1016/j.ipm.2022.103145. 

- [33] W.X. Zhao, et al., A Survey of Large Language Models, (2023). https://doi.org/10. 48550/arXiv.2303.18223. 

- [34] IDTA, Registered AAS Submodel Templates, 2024, Available online: https:// industrialdigitaltwin.org/en/content-hub/submodels. 

- [35] IEC, IEC 61987 - IEC/SC 65E - Common Data Dictionary (CDD - V2.0015.0004)”. 2023. Available online:: 〈https://cdd.iec.ch/cdd/iec61987/iec61987.nsf〉〈〉. 

- [36] ECLASS, An introduction to the standard, 2023. Available online: 〈https://eclass. eu/en/eclass-standard/introduction〉〈〉. 

- [37] 15926browser. RDL Stands for Reference Data Library (search screen). 2023. Available online: http://data.15926.org/rdl#. 

- [38] VDI 4499 Part 3:2016–04, Digital Factory - Data Management and System Architectures, Guideline, Beuth Verlag GmbH, Berlin, 2016. 

- [39] IEC, IEC EN 63278–1:2023: Asset Administration Shell for industrial applications - Part 1: Asset Administration Shell structure, 2023. 

- [40] IEC. IEC ED1 63278–4:2023 Asset Administration Shell for Industrial Applications Part 4: Use Cases And Modelling Examples 2023. 

- [41] IEC. IEC TR 63283–2:2022 Industrial-process measurement, control and automation - Smart manufacturing - Part 2: Use cases. 

- [42] IEC. EN IEC 61360–1:2018–07, Standard Data Element Types with Associated Classification Scheme - Part 1: Definitions - Principles and Methods, Standard, Beuth Verlag GmbH, Berlin, 2018. 

- [43] IEC. EN IEC 62264–1:2014–07, Enterprise-Control System Integration - Part 1: Models and Terminology, Standard, Beuth Verlag GmbH, Berlin, 2014. 

- [44] IDTA, A.A.S.X. Package Explorer, Github repository, 2023, Available online: 

   - 〈https://github.com/admin-shell-io/aasx-package-explorer〉. 

- [45] IEC. EN IEC 62264–2:2014–06, Enterprise-Control System Integration - Part 2: Objects and Attributes for Enterprise-Control System Integration, Standard, Beuth Verlag GmbH, Berlin, 2014. 

- [46] IEC. EN IEC 62264–3:2017–12, Enterprise-Control System Integration - Part 3: Activity Models of Manufacturing Operations Management, Standard, Beuth Verlag GmbH, Berlin, 2017. 

- [47] IDTA, I.D.T.A. 02002–1-0 Submodel for Contact Information, Available online: 〈htt ps://industrialdigitaltwin.org/en/wp-content/uploads/sites/2/2022/10/IDTA-02 002–1-0_Submodel_ContactInformation.pdf〉. 

- [48] M. Douze et al., The Faiss library (2024) [Online]. Available: https://doi.org/10. 48550/arXiv.2401.08281. 

- [49] HuggingFace, Transformers (2024), [Online]. Available: 〈https://huggingface. co/docs/transformers/index〉. 

- [50] E.J. Hu et al., LoRA: Low-Rank Adaptation of Large Language Models, (2021) [Online]. Available: 〈http://arxiv.org/pdf/2106.09685v2〉. 

- [51] DIN, DIN ISO 2859–1:2014–08, Annahmestichprobenprüfung anhand der Anzahl fehlerhafter Einheiten oder Fehler (Attributprüfung) - Teil 1: Nach der annehmbaren Qualitatsgrenzlage (AQL) geordnete Stichprobenpl¨ ane für die ¨ Prüfung einer Serie von Losen - (ISO 2859–1:1999 + Cor. 1:2001 + Amd.1:2011). 

- [52] BaSyxEclipse Ba.Syx Java V2 SDK (2024), [Online]. Available: 〈https://github.co m/eclipse-basyx/basyx-java-server-sdk〉〈〉. 

- [53] Barlaug N, Gulla JA. Neural networks for entity matching: a survey. ACM Trans. Knowl. Discov. Data 2021;15:1–37. 

- [54] OpenAI, Embeddings (2024) [Online]. Available: 〈https://platform.openai.com/do cs/guides/embeddings/embedding-models〉. 

- [55] R. Meng et al., SFR-Embedding-Mistral:Enhance Text Retrieval with Transfer Learnin (2024), Salesforce AI Research Blog, [Online]. Available: 〈https://blog. salesforceairesearch.com/sfr-embedded-mistral〉. 

- [56] huggingface, Model card: sentence-transformers/all-mpnet-base-v2. Available online: 〈https://huggingface.co/sentence-transformers/all-mpnet-base-v2〉. 

- [57] H. Touvron et al., Llama 2: Open Foundation and Fine-Tuned Chat Models (2023) [Online]. Available: 〈https://ai.meta.com/research/publications/llama-2-openfoundation-and-fine-tuned-chat-models〉. 

- [58] HuggingFace, Transformers (2024), [Online]. Available: 〈https://huggingface. co/docs/transformers/index〉. 

- [59] S. Mangrulkar, S. Gugger, L. Debut, Y. Belkada, S. Paul and B. Bossan, PEFT: Stateof-the-art Parameter-Efficient Fine-Tuning methods (2022) [Online]. Available: 〈https://github.com/huggingface/peft〉. 

- [60] Li Y, Li J, Suhara Y, Doan A, Tan W-C. Deep entity matching with pre-trained language models. Proc VLDB Endow 2020;14:50–60. https://doi.org/10.14778/ 3421424.3421431. 

- [61] R. Peeters and C. Bizer, Entity Matching using Large Language Models (2023) [Online]. Available: 〈http://arxiv.org/pdf/2310.11244v2〉.

### Page 696

