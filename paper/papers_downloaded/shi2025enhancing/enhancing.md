# Computers in Industry 171 (2025) 104330 **==> picture [61 x 67] intentionally omitted <==**

Source: shi2025enhancing.pdf


---

### Page 2

_Computers in Industry 171 (2025) 104330_ 

_D. Shi et al.                                                                                                                                                                                                                                      in_ 

and employ the enhanced RAG for knowledge inference. 

The main contributions of this paper are summarized as follows: 

- A novel solution to achieve CDTs is proposed by enhancing RAG systems for the manufacturing industry through the integration of AAS and fine-tuned LLMs. AAS replaces conventional KGs to enable interoperable knowledge representation, while an LLM fine-tuned with CSL enhances retrieval accuracy, ultimately improving the quality of RAG-generated responses. 

- A method to encode entities within an AAS instance, including their semantic and positional information, for use with LLMs. Since the AAS framework lacks a native inference mechanism, this work proposes a novel approach to represent AAS entities in a format suitable for LLMs, effectively enabling LLMs to serve as the inference engine for AAS-based knowledge. 

- A CSL is proposed to fine-tune open-source LLMs, transforming a decoder-only generative LLM into an encoding-based selection model. This CSL-based fine-tuning enhances the model’s sensitivity to similar distractors, thereby refining initial retrieval results that previously relied solely on semantic similarities. 

- The enhanced RAG system is first demonstrated in the practical use case of a machine integrator, focusing on integrating components’ kinematic models in a robotic work cell. Additionally, a novel human evaluation protocol is introduced to systematically assess the correctness of RAG responses. Furthermore, extensive statistical experiments are conducted to evaluate the fine-tuned LLM, benchmarking it against SOTA entity matching approaches. 

The remainder of this paper is organized as follows: Section 2 reviews related work. Section 3 presents the enhanced RAG system. Section 4 demonstrates its application in robotic work cell integration and evaluates the RAG system’s responses within this use case. Section 5 provides a statistical evaluation of the retrieval quality achieved through the proposed CSL-based fine-tuning approach. 

## **2. Related work** 

## _2.1. CDT and RAG in the manufacturing industry_ 

Either for CDTs or RAG systems, the primary goal is to develop their capability of accurate responses to user queries. These users could be humans or intelligent systems. In manufacturing, a CDT represents the virtual representation of production resources that can operate as a query response. While most previous works on DTs have concentrated on modeling their physical behaviors for simulation and health monitoring purposes (Li, 2024), CDTs extend this focus to encompass the knowledge aspect of DTs, thereby endowing them with cognitive capabilities. This concept aligns closely with the goals of RAG systems, which are more widely recognized outside of the manufacturing sector and are designed to enhance knowledge retrieval and response generation in general applications of NLP. 

CDTs and RAG systems share two critical components: knowledge representation and retrieval (Zheng et al., 2022; Gao et al., 2023). Table 1 summarizes related work and their solutions concerning these two aspects. It is evident that all the CDTs developed in previous work employ ontologies and KGs for knowledge representation. Ontology provides the information modeling framework under which concepts within a subject domain can be semantically defined as entities with attributes and their relationships. The Web Ontology Language (OWL) is the most commonly used expression language to implement ontologies. The OWL files stored in a database tool can then be directly queried by the query language SPARQL for retrieval. As a database query language, SPARQL is driven by designed logical rules, meaning the system can only respond to predetermined queries following these rules. A more common approach is to convert ontologies to KGs, where the ontology serves as the blueprint or schema, providing the structured framework and 

## **Table 1** 

Previous work related to CDT and RAG applications in the manufacturing domain. 

||Reference|Application|Knowledge|Knowledge|
|---|---|---|---|---|
||CDT (D’Amico<br>et al., 2022)|Malfunction<br>detection|representation<br>Ontology|retrieval<br>SPARQL|
||CDT (Lu et al.,|System|Ontology&KG|SPARQL|
||2022)|development|||
||CDT (Roˇzanec<br>et al., 2021)|Production<br>planning|Ontology&KG|Neo4j-API|
||CDT (Mortlock|Product design|KG|GNN|
||et al., 2022)||||
||RAG (Bahr et al.,<br>2024)<br>RAG (|FMEA<br>Contextual|Ontology&KG<br>Unstructured|Sentence<br>transformer<br>Sentence|
||Chandrasekhar<br>et al., 2024)|querying in<br>additive|Doc.|transformer|
||RAG (Tinnes<br>et al., 2024)<br>RAG (Freire et al.,|manufacturing<br>Product<br>descriptions<br>Knowledge|AAS<br>Unstructured|Sentence<br>transformer<br>OpenAI embedding|
||2024)<br>RAG (Alvaroa and|sharing for factory<br>operators<br>FMEA|Doc.<br>Unstructured|OpenAI embedding|
||Barredaa, 2024)||Doc.|&reranker using<br>sentence|
|||||transformer|
||RAG (Xia et al.,<br>2024)<br>RAG (Liu et al.,|Product<br>descriptions<br>FMEA|AAS<br>KG|OpenAI embedding<br>fne-tuned BiLSTM|
||2024)|||embeddings|
||RAG (Zhou et al.,|FMEA|KG|Graph embeddings|
||2024)||||
||**Proposed**|System integration|AAS|Open-source LLM-|
||**Enhanced RAG**|and development||embeddings&<br>reranker based on|
|||||fne-tuned LLM|



vocabularies, and the KG then incorporates this blueprint for instantiation and inference (Lu et al., 2022; Roˇzanec et al., 2021). In this case, Neo4j is a popular open-source graph database tool that provides a query language and APIs for data integration. 

Alternatively, knowledge can be directly structured as KGs’ entities, their attributes, and interrelationships. For instance, Liu et al. (2024), Zhou et al. (2024), and Bahr et al. (2024) constructed KGs for failure mode and effects analysis (FMEA), where entities represent textual descriptions of failure modes, causes, and effects. However, KGs face several limitations. KG entities are typically defined by individual developers based on domain knowledge, without a unified schema governing attributes, relationships, or metadata. This leads to inconsistencies in entity structure, limiting reuse across different applications. Additionally, failure-related terms and descriptions vary among experts, causing semantic ambiguities that complicate knowledge integration. Traditional KGs rely primarily on textual descriptions, lacking embedded metadata such as versioning, timestamps, and lifecycle information, making them unsuitable for long-term knowledge management in industrial applications. Beyond manually constructed KGs, Mortlock et al. (2022) introduced graph learning to extract entities from raw unstructured data to automatically build KGs and then trained a GNN to predict the query results. While this approach enables adaptive responses, it sacrifices interoperability, as the constructed graph is trained in an ad-hoc manner for a specific application, limiting its generalizability. 

In comparison to logical rules in CDTs, RAG systems rely on machine learning models for knowledge inference. It typically employs at least two models, as shown in Fig. 1: an embedding model for encoding the inputs and an LLM chat model for response generation. The inputs for the embedding model could be structured in KGs (Bahr et al., 2024) or remain as unstructured documents (Chandrasekhar et al., 2024; Freire et al., 2024; Alvaroa and Barredaa, 2024). Structured input can provide

### Page 3

> _D. Shi et al.                                                                                                                                                                                                                                      Computers in Industry 171 (2025) 104330_ 

more precise information by removing noisy texts and adding relationships between KG entities. For instance, Bahr et al. (2024) introduced a KG-enhanced RAG system utilizing OpenAI’s commercial chat and embedding models for FMEA in the production of high-voltage systems for electric vehicles. The system was evaluated against traditional FMEA Excel spreadsheets and the RAG system based on unstructured input data, using metrics such as correctness, usability, relevance, completeness, and time efficiency. The results demonstrated that the RAG system outperformed conventional methods across all metrics, particularly in usability. Recently, Tinnes et al. (2024) and Xia et al. (2024) have attempted to employ AAS for the knowledge representation of product-related information. 

As observed in the aforementioned related works, previous research has primarily focused on implementing and evaluating standard RAG solutions for manufacturing-related applications, which merely rely on embedding models such as OpenAI’s embedding models and opensource sentence transformers for information retrieval. These standard RAG systems have demonstrated promising results when compared to conventional tools such as Excel spreadsheets. Since LLMs possess exceptional generalization capabilities, users are not required to understand their underlying mechanisms or structure their tasks according to specific model constraints. Instead, they can interact with LLMs through accessible interfaces (e.g., OpenAI API). In this regard, the primary costs associated with adopting RAG systems primarily involve model usage fees and the integration of RAG into existing software toolchains. For instance, vector databases must be established to store and retrieve embeddings efficiently, and user interfaces need to be integrated into existing software, either as query functions or chatbot interfaces. 

However, even the most advanced embedding models struggle to consistently rank the true positive candidate at the top, particularly when multiple semantically similar distractors exist within the retrieved candidate set (Shi et al., 2025). As a result, the retrieved knowledge, which serves as the input for the chat model, may lack critical information, potentially leading the chat model to generate incomplete or misleading responses. Most prior works have not thoroughly explored how retrieval mechanisms can be further optimized to enhance overall system performance. Notably, only Liu et al. (2024) and Zhou et al. (2024) attempted to encode KGs using BiLSTM and GNN, respectively, for improved knowledge retrieval. After retrieving candidate results, Alvaro and Barredaa (2024) was the only study to introduce a pre-trained reranker to refine retrieval outcomes. The refinement of entity retrieval results has been studied in the field of entity matching, which is reviewed in the following subsection.c 

## _2.2. Entity retrieval and matching in NLP_ 

— When knowledge is structured whether in the form of an ontology, KG, or AAS—it essentially becomes a collection of individual entities with attributes. Searching for a query within a series of entities involves tasks broadly categorized under entity matching within the field of NLP. This task encompasses the retrieval of initial candidates, known as blocking (Barlaug and Gulla, 2021), and their subsequent pairwise matching. Once the query entities and the entities in the knowledge base are encoded into dense vectors, an ANN algorithm identifies the vectors in the knowledge base that are closest to the query vector and designates them as candidates. The core challenge in EM lies in accurately comparing the similarity between the query entity and the retrieved candidates. 

The standard task formulation in entity matching has long been pairwise matching (Barlaug and Gulla, 2021), where a query entity is independently compared to each candidate to determine whether they match. This operates under the principles of binary classification, requiring repeated classification for all retrieved candidates. Fine-tuning pre-trained language models (PLMs) has become the SOTA approach for pairwise entity matching. Models such as RoBERTa are appended with a 

dense classification layer and fine-tuned to predict binary match labels (Li et al., 2023). Recent advancements in this field have seen the rise of LLMs with prompt engineering (Peeters and Bizer, 2023). Powerful LLMs like GPT-4, leveraging in-context learning (ICL), have demonstrated performance comparable to fine-tuned PLMs. Beyond prompt-based approaches, recent studies have fine-tuned LLMs as generative models to produce binary outputs (e.g., yes/no) for given entity pairs. With optimized hyperparameters, medium-sized LLMs, such as LLaMA2–13B, have demonstrated the ability to outperform both PLMs and LLMs with prompt techniques (Shi et al., 2025). 

While these approaches follow the standard pairwise matching paradigm, they face challenges in distinguishing true matches from semantically similar distractors. Modern blocking methods retrieve highly similar candidates, but pairwise matching lacks a global perspective on the entire candidate set, making it difficult to differentiate between correct matches and similar distractors. This often leads to false positive classifications. Additionally, the pairwise comparison requires repetitive computations for all the candidates, significantly increasing computational overhead and response latency in large-scale applications. 

This issue has also been noticed in a recent study (Wang et al., 2024), where the authors explored the feasibility of prompting LLMs to directly select the true positive candidate from the top-K candidates or to compare the query with multiple candidates simultaneously. However, their experiments utilized only medium-sized open-source LLMs (3–11B parameters) with zero-shot prompting (ZSP). The proposed method failed to achieve SOTA results delivered. 

## _2.3. Research gaps_ 

The literature review identifies several key research gaps. We explicitly explain how our approach addresses these gaps, aligning with our main contributions summarized in Section 1. 

- Existing CDTs lack true cognitive capabilities as their retrieval systems rely on predefined logical rules. By introducing RAG into CDTs, we aim to incorporate LLMs for retrieval and response generation. Also, our objective is not only to apply RAG to manufacturing, as most previous studies did, but also to enhance RAG in two key aspects: knowledge representation and entity retrieval. 

- While ontology and KGs are standard solutions for knowledge representation in existing CDTs and RAG systems, we propose to replace them with the AAS, a framework specifically designed for the manufacturing industry to enhance interoperability. Unlike KGs, AAS defines hierarchically structured information models, adhering to the standardized metamodel specified in IEC 63278–2 (2022) at a high level, while supporting individual standardized SMTs (IDTA, 2024 ) for domain-specific applications. Additionally, AAS entities 

- conform to the data schema of IEC 61360 (2017) and enable semantic reference to established industrial terminology dictionaries, such as ECLASS (2024). These features collectively ensure data consistency, reusability, and seamless cross-enterprise knowledge representation. Furthermore, the AAS can also be automatically converted into ontologies and further constructed as KGs (Rongen et al., 2023). 

- There is growing interest in adopting powerful LLMs, such as GPT variants, in manufacturing. However, most studies focus solely on prompt engineering and have not explored the feasibility of finetuning LLMs to incorporate domain-specific knowledge. Our approach fills this gap by fine-tuning LLMs to enhance the retrieval capabilities of the RAG system. 

- In the entity matching domain, existing work remains confined to the standard pairwise matching setting, where entity pairs are evaluated independently. This approach naturally struggles to handle semantically similar distractors among the retrieved candidates. To overcome this, we propose using CSL to reshape the training setting of

### Page 4

_Computers in Industry 171 (2025) 104330_ 

_D. Shi et al.                                                                                                                                                                                                                                      in_ 

entity matching and fine-tune the LLM as a contrastive selection model. 

## **3. Enhanced retrieval-augmented generation system** 

The proposed enhancement to the RAG system, as depicted in Fig. 1, demonstrates a synergistic advantage by integrating AAS-based knowledge representation with a fine-tuned LLM as the entity selection model. Section 3.1 Section 3.2 describes the presents the overall workflow. encoding of AAS for LLMs, while Section 3.3 details the fine-tuning of an LLM with CSL to improve initial retrieval performance. 

## _3.1. Overall workflow_ 

As illustrated in Fig. 2, the enhanced RAG system involves three distinct LLMs: _LLMc_ , _LLMe_ , and _LLMr_ . _LLMc_ is a pre-trained LLM chat model responsible for extracting query entities in Step 1 and generating responses in Step 6, _LLMe_ denotes the LLM-based embedding model used to encode query and AAS entities in Step 3, and _LLMr_ is the proposed fine-tuned selection model designed for refining the retrieval results in Step 5. The key process begins by using _LLMc_ to extract the query entity _eq_ from the input query sentence. Simultaneously, AAS entities _eaas,n_ along with their semantic and positional information are extraced from AAS models by the developed AAS parser. Next, _LLMe_ encodes the query and AAS entities into dense vector representations for the subsequent similarity search. The search is performed using an ANN algorithm based on cosine similarity. This work utilizes the existing Faiss library to index the AAS knowledge base and conduct the search (Douze et al., 2024). The similarity search retrieves the top-K candidate entities _e[k] aas_[as ] the inputs for _LLMr_ . The selection model _LLMr_ identifies the most likely positive candidate _e_[ʹ] _aas_[and ranks it at the top position. Finally, the ] top-ranked candidates alongside the query and the instruction prompts are fed into the chat model _LLMc_ to generate the final response _y_ . 

## _3.2. Encoding AAS-based knowledge representation_ 

Table 6 in Annex I. An AAS is typically composed of SMEs and Submodel Element Collections (SMCs). SMCs are containers that contain multiple SMEs, forming a hierarchical structure. SMEs such as “Property” can be generally viewed as an entity with several attributes, such as _idShort_ , _description_ , and _semanticID_ . Special SMEs, such as Relationship Elements and Reference Elements, can directly link to other SMEs, enabling the creation of more complex, nested, and interconnected model structures. The types of various SMEs and attributes of SMEs are standardized in the – AAS metamodel and explained in IEC 63278 2 (2022). For clarity and readability, the AAS-related terminologies used in this work are defined and explained in Table 7 in Annex I. 

Fig. 3 abstracts an exemplary portion of AAS-based knowledge representation for the integration of components’ kinematic models within a robotic work cell. Its visualization in the AASX editor is provided in Fig. 6. In this example, the robotic cell and its main components ( _e.g._ , the gripper) are represented by their respective AAS. Their logical relationships are established through the Relationship Element “hasPart” within the SM _BillofMaterial_ of _RobotCell_ . Both AAS instances contain an SM _KinematicModel_ , which stores information related to the kinematic models. At the component level, this SM includes details for each link and joint through corresponding SMCs and contains information such as names, payload, and calibration data. At the system level, the components’ links are jointed through the SMC _KinematicChain_ , where the corresponding links are referenced via Reference Elements. In addition to the structural information, the content information is primarily carried by individual entities and their attributes. Several exemplary attributes are highlighted in the text box in Fig. 3. For instance, “idShort” refers to the name of a Property, “qualifier” restricts the value statement by defining conditions, and “semanticID” provides a reference to an entity in an external concept repository. Additionally, a property may include a concept description that adheres to a standardized schema for semantic description, such as IEC 61360 (2017). 

Encoding knowledge within the AAS requires capturing both the structural and semantic information of individual entities. An entity _eaas_ within the AAS can be represented as: 

**==> picture [254 x 9] intentionally omitted <==**

Encode AAS entities _eaas_ requires converting AAS into string representations while preserving their structural and semantic information. To achieve this, we first introduce the AAS structure before detailing the encoding process. 

where: 

**==> picture [254 x 9] intentionally omitted <==**

AAS represents assets and knowledge as structured information models, which can be expressed in XML format, as exemplified in 

**==> picture [505 x 215] intentionally omitted <==**

**Fig. 2.** Workflow of the enhanced RAG system. Steps 2 and 5 represent the core contributions of this work and are elaborated in Sections 3.1 and 3.2, respectively.

### Page 5

> _D. Shi et al.                                                                                                                                                                                                                                      Computers in Industry 171 (2025) 104330_ 

**==> picture [361 x 378] intentionally omitted <==**

**Fig. 3.** An exemplary part of the AAS model for integrating components’ kinematic models in a robotic work cell. The diagram uses grey to represent AAS, yellow for SM, blue for SMC, green for Relationship Elements or Reference Elements, and orange for Property Elements (Each contains several Attributes listed inside the right box). Solid arrows indicate containment relationships, while dashed arrows denote “routes to” connections. (For interpretation of the references to color in this figure legend, the reader is referred to the web version of this article.) 

## _s_ = ʹʹ _/shells/_ { _AAS_  ID_ } _/submodels/_ { _SM_  ID_ } _/submodelelements/_ { _SME_  Path_ }ʹʹ# 

(3) 

The attribute string _a_ is the concatenation of the selected entity’s attributes, which contains the relevant information for query matching. The position string _s_ is defined as an HTTP/REST path in accordance with the API specifications of the AAS (IDTA, 2023). _AAS_  ID_ denotes the idShort of the AAS instance, _SM_  ID_ denotes the idShort of the SM, and _SME_  Path_ traces the path through the SMEs. For instance, the path of Property _Yaw_ in Fig. 3 is expressed as “ _KinematicChain.ConnectedJoint00. OriginTransfered.Yaw_ ”. This path provides the contextual information of an entity and is utilized as part of the input for the chat model. The implementation details on how to extract the attribute string and position string of an AAS entity are provided in Section 4.2. 

## _3.3. Fine-tuning large language models with the contrastive selection loss_ 

In the conventional entity matching process, Step 5 in Fig. 2 involves taking the query and one candidate entity at a time for pairwise matching. This step is formulated as a binary classification task, aiming to determine whether the two entities are a match or not (Barlaug and 

Gulla, 2021). However, this pairwise matching process must be repeated for each candidate within the top-K retrieved list. In contrast, the proposed selection model _LLMr_ , fine-tuned with CSL, simultaneously compares the query entity with multiple candidates retrieved by the embedding model _LLMe_ in a single forward pass. During the fine-tuning stage, one of the candidates is labeled as the positive match for calculating the loss, while the others serve as hard negative samples. In the inference stage, _LLMr_ predicts the index of the positive candidate, which is then reranked to the top position and used as input for the chat model _LLMc_ for response generation. 

Fig. 4 depicts the model structure for fine-tuning open-source LLMs with the CSL. The selection model _LLMr_ designed using a Siamese network architecture, where the backbone consists of two instances of the Mistral-7B model, which is a decoder-only Transformer. We adopt the Huggingface implementation of the Mistral model (Huggingface, 2024b). Notably, the pre-trained weights are initialized from the open-source SFR-Embedding-Mistral model (Meng et al., 2024), which also serves as our embedding model _LLMe_ in the RAG system. The choice

### Page 6

> _D. Shi et al.                                                                                                                                                                                                                                      Computers in Industry 171 (2025) 104330_ 

**==> picture [247 x 289] intentionally omitted <==**

**Fig. 4.** Model structure for fine-tuning open-source LLMs with the CSL as the selection model _**LLMr**_ . The yellow blocks represent the query and its embeddings, while the blue blocks represent the top-K candidates and their embeddings. (For interpretation of the references to color in this figure legend, the reader is referred to the web version of this article.) 

Section 5.4. of this model is based on the empirical findings presented in Within the Siamese network, the two instances of Mistral-7B share the same weights. To enable efficient fine-tuning, we apply the LowRank Adapter (LoRa) technique (Hu et al., 2021). The LoRa preserves an original weight matrix _W_ ∈ R _[d]_[×] _[d ]_ by keeping it frozen, while introducing two lower-rank matrices _B_ and _A_ , where _B_ ∈ R _[d]_[×] _[r]_ , _A_ ∈ R _[r]_[×] _[d]_ , and _r_ **≪** _d_ . Here, _r_ denotes the rank of the decomposition matrices. This significantly reduces the number of trainable parameters for a trainable matrix from _d_[2 ] to 2 _rd_ , making the fine-tuning process more computationally efficient and feasible for practical implementation. Fine-tuning updates only the adapter’s weights while keeping the pre-loaded weights from SFR-Embedding-Mistral unchanged. The rank _r_ is a critical hyperparameter that significantly impacts model performance. Its optimal value is determined through empirical experiments and provided along with other hyperparameters in Section 5.3. This approach ensures that the entire retrieval process operates with a single set of LLM weights. During initial retrieval, only the SFR-Embedding-Mistral weights are loaded into _LLMe_ . For reranking, the _LLMe_ weights and the fine-tuned LoRa weights are merged in memory and loaded as _LLMr_ . 

The attribute strings of the query entity and the candidate entities are separately processed through the two Mistral-7B models within the Siamese network. Since Mistral-7B is a decoder-only Transformer, the last hidden state of the final token is extracted as the embedding representation for each input: 

**==> picture [254 x 11] intentionally omitted <==**

To ensure scale invariance, these embeddings undergo L₂ normalization: 

**==> picture [254 x 21] intentionally omitted <==**

**==> picture [255 x 39] intentionally omitted <==**

where _S_ ∈ R[1][×] _[N ]_ is the similarity matrix. 

**==> picture [255 x 48] intentionally omitted <==**

The CSL is formulated using cross-entropy loss, which maximizes the similarity of the true positive candidate while minimizing it for the negative candidates. Given the true labels _lj_ , which indicate the index of the positive candidate in a one-hot encoded format, the CSL is computed as: 

**==> picture [254 x 23] intentionally omitted <==**

During the inference stage, the fine-tuned model predicts the similarity scores _sj_ for each query with its _N_ candidates. When _N_ = _K_ , the inference needs to be performed only once to cover the entire retrieved top-K candidates. The predicted positive candidate is reranked at the top position and selected for response generation. When _N < K_ , the inference process is repeated ⌊ _K/N_ ⌋ +1 times, resulting in ⌊ _K/N_ ⌋ +1 selected candidates. The influence of hyperparameter _N_ is investigated in Section 5.4 and discussed in Section 5.5. 

## _4. Case Study_ 

This section presents a practical application of the enhanced RAG system, integrating AAS-based knowledge representation and the finetuned LLM within the context of a robotic work cell’s mechanical design during the engineering phase. Section 4.1 introduces the use case, Section 4.2 details the implemented AAS SMs and the RAG system, and Section 4.3 evaluates the system’s responses within this use case. 

## _4.1. Application scenario_ 

Fig. 5 illustrates the workflow for developing a robotic work cell in the ROS framework, focusing on the mechanical engineer’s perspective. The process begins with creating a comprehensive CAD model of the work cell, which includes key components such as a collaborative sixaxis robot, an EGP-64 gripper, a structural base, and a pneumatic disassembly unit. During this phase, all moving parts, which will later be defined as links or joints in the kinematic models, are labeled with detailed information. The CAD models of each component are converted into the URDF using a plug-in in the CAD software. This URDF provides ROS with the necessary kinematic simulation and visualization data. Each URDF file includes details on the properties of joints and links, such as inertial, collision, and visual properties, along with joint types and their respective limits. These URDF files, the associated mesh files for visual and collision geometries, and configuration files for controllers are organized into a structured ROS package, forming a standardized component library. 

However, integrating these components into a single, cohesive kinematic model for the work cell typically involves several manual processes. This includes identifying and incorporating critical information that is often missing from the individual URDF files, such as calibration data, metadata from the CAD models, and the connections between joints and links across different components. This is where AAS comes into play. AAS serves as the single point of truth, encapsulating all

### Page 7

> _D. Shi et al.                                                                                                                                                                                                                                      Computers in Industry 171 (2025) 104330_ 

**==> picture [505 x 182] intentionally omitted <==**

**Fig. 5.** Workflow for the integration of components’ kinematic models in a robotic work cell. 

**==> picture [505 x 257] intentionally omitted <==**

**Fig. 6.** Left: Demonstrator of the integrated robotic cell for disassembling. Right: AAS implementation of the robotic cell and the components, focusing on their kinematic models. 

relevant information and metadata within a pre-defined and unified SMT _KinematicModel_ . Based on this knowledge base, the integration engineer can query the required information through the proposed RAG system. 

## _4.2. Implementation_ 

Fig. 6 illustrates the demonstrator of the integrated robotic cell designed for disassembly tasks. This setup includes a simulation and visualization model, which, together with the implemented RAG system based on AAS and LLM, constitutes the CDT of the robotic cell. In the following, we will primarily focus on explaining the enhanced RAG system, as depicted in Fig. 7. 

The web application of the enhanced RAG is built upon an existing open-source project tailored for RAG applications (Schiesser, 2024). The left section of the user interface is dedicated to configuration settings. 

The chat model _LLMc_ is configured to use GPT-4o, which is accessed via REST-API provided by Azure OpenAI. The embedding model _LLMe_ utilizes the open-source SFR-Embedding-Mistral model (Meng et al., 2024), while the reranking model _LLMr_ employs our proposed model fine-tuned with the proposed CSL. These two open-source models are deployed locally using the Ollama framework (Yang et al.,2024). A detailed evaluation of the reranking model is provided in Section 5.4. 

The knowledge base configuration is restricted to utilizing the uploaded AASX file, which is the AAS file format. The AASX file is essentially a package file with the “.aasx” extension, similar to a.zip archive. This package primarily contains the AAS information model in XML or JSON format, along with attached files such as images, models, PDFs, and other supporting documents. A part of an exemplary XML file is provided in Table 6 in Annex I. To process the AAS data, a custom AASX parser has been developed to extract SMEs as entities from the XML file. These extracted entities are then formatted according to Eqs.

### Page 8

> _D. Shi et al.                                                                                                                                                                                                                                      Computers in Industry 171 (2025) 104330_ 

**==> picture [505 x 270] intentionally omitted <==**

**Fig. 7.** Web application of the enhanced RAG. 

(2) and (3) for subsequent processing. As presented in Table 6, a Property (SME type) contains attributes such as “idShort”, “description”, and “value”. The extracted and concatenated attribute string for this Property is formatted as: “ _idShort: TypeName, description: defined equipment type within the equipment hierarchy according to IEC 622641_ – _1, value: work cell_ ”. Additionally, the position string within the AAS hierarchy is: _“Position: /shells/CobottaCell/submodels/KinematicModel/submodelelements/Identifier.TypeName_ ”. Each AAS entity is ultimately represented by its attribute string and position string for the subsequent encoding step. In the current implementation, attached files within the AASX package have not been extracted as inputs for LLMs, meaning that the current RAG system does not fully leverage the rich representation capabilities of AAS. This is a limitation of the current work. 

The implemented AAS models are depicted in Fig. 6. The robotic cell, referred to as CobottaCell, consists of four main components, whose interrelationships are modeled within the SM _BillofMaterial_ . The kinematic information is encapsulated in the SM _KinematicModel_ . This model not only includes basic metadata related to identification, files, and coordination systems of the CAD models but also represents the kinematic relationships through the SMC _KinematicChain_ . Within the _KinematicChain_ , the base link, denoted as Link00, defines the reference link termed “world”, followed by a sequence of joints that connect the various components. Each _ConnectedJoint_ is detailed in a dedicated SMC 

that includes entities such as _JointName_ , _OriginTransferred_ (indicating the relative position between the parent link and child link), _ParentLinkRef_ , _ChildLinkRef_ , and _Type_ of the joint. The _ParentLinkRef_ and _ChildLinkRef_ provide references to the respective links defined in the SM _KinematicModel_ of the corresponding components, enabling precise modeling of the kinematic connections within the robotic cell. 

The right section of the web interface shown in Fig. 7 facilitates interaction with the chat model _LLMc_ . The key processes of the enhanced RAG system are presented in Fig. 2. Initially, the input query is processed using the prompt for entity extraction, denoted as _pq_ . This step converts the user query into an entity-like format suitable for subsequent retrieval and reranking. The prompt _pq_ is outlined in Table 2. For example, when being asked, “Can you explain each component?”, the query is transformed into “component explanation. overview of each subsystem or hardware module in a manufacturing environment, detailing their function and operational roles.” The AAS entities, along with the transformed query entity, are encoded by the embedding model. The most relevant entities are identified through an initial retrieval process followed by reranking, ensuring that the most contextually appropriate information is selected. This contextual knowledge is then integrated into the prompt for response generation _pr_ , as presented in Table 2. 

## **Table 2** 

Prompt template for entity extraction _**pq**_ and response generation _**pr**_ . 

Prompt for entity extraction _**pq** Given a question, generate one or several keywords related to the question, and generate a short description containing these keywords in context of manufacturing industry. Example:_ **Q:** _What is the name of the robotic cell?_ **Your answer:** _name of robotic cell. name or abbreviation of robotic work cell or station for production._ **Q:** _Which physical components does it have?_ **Your answer:** physical components. Bill of Materials or hardware subsystems in a manufacturing environment _._ **Q:** _{Query_str}?_ **Your answer: Prompt for response generation** _**pr** I want to build a robot cell by integrating its kinematic components and will ask related questions. Please answer the questions based on your knowledge of the manufacturing domain and the retrieved entities in the Asset Administration Shell model. The entity’s location provides the additional context information and indicates which objects the entity information belongs to. "——————————————————————" "{AAS_entities_str}" "——————————————————————" Given this information, please answer the question: {query_str}. Formulate the answer briefly and concisely_

### Page 9

> _D. Shi et al.                                                                                                                                                                                                                                      Computers in Industry 171 (2025) 104330_ 

## _4.3. Evaluation of the RAG responses_ 

structured checklist. Three independent human evaluators assess each response against these sub-claims. If a response accurately matches a sub-claim but lacks completeness, it is assigned a Factuality score of 1 and a Completeness score of 0. If the response addresses the relevant sub-claim but contains inaccuracies, it is assigned a Factuality score of 0 and a Completeness score of 1. If the response satisfies both accuracy and completeness, both scores are set to 1; otherwise, both scores remain 0. The final scores for Factuality and Completeness are averaged across all sub-claims for each response. An example of a question, response, ground-truth answer, and evaluation is presented in Table 3. For “ _1. KiWiCell’_ instance, in the first sub-claim, _s base link is fixed to the system reference ‘world’_ ”, the response correctly reflects this information in the first and second points, leading to a Factuality score of 1. However, a crucial detail— “base link” of KiWiCell —is missing from the response, leading to a Completeness score of 0 for this sub-claim. For the last sub-claim, the correct information states that the gripper should be connected to the robot. However, the response incorrectly states that the gripper is connected to the system, and does not specify the link information, leading to both Factuality and Completeness scores of 0. The final Factuality score, averaged across four sub-claims, is 0.75, while the Completeness score is 0. 

This subsection evaluates the RAG system’s response within the use case, where the primary knowledge base consists of the implemented AAS SMs: KinematicModel (parent) and BillofMaterial for the robotic cell, as well as KinematicModel (child) for its subsystems. For the evaluation, we design 30 relevant questions that a mechanical engineer might typically ask during the conventional manual process of information acquisition. A comprehensive statistical evaluation of the retrieval component within the RAG system is presented in Section 5, which relies on the extended AAS entity matching dataset. 

The designed evaluation questions align with industrial practices and naturally encompass various formats, including long-form open-ended _“ ”_ questions such as _How are the components connected in the work cell?_ , single-hop reasoning questions like _“Which robotic arm is used? Provide the type and identifier”_ , multi-hop reasoning questions like _“How are the robot’s joints and links named?”_ and binary yes/no questions such as _“Is there calibration data for properly aligning each robot’s joint?”_ Assessing Gao responses to such complex queries presents significant challenges ( et al., 2023). In related works (Liu et al., 2024; Zhou et al., 2024), evaluations of industrial RAG applications are conducted through subjective human assessment, while only a few studies employ automated metrics such as F1 score, semantic similarity, or ROUGE (Alvaroa and Barredaa, 2024). These automated metrics are more suitable for evaluating short-form answers that follow a fixed format but may not capture the correctness and quality of long-form questions. Although human evaluation provides a more holistic assessment, typically rating re– sponses on a scale (e.g., 0 5), it lacks transparency and reproducibility. 

To measure the reliability of human evaluation, we calculate Fleiss’ Kappa ( _κ_ ), which is commonly used for measuring the inter-annotator agreement (IAA), for Factuality and Completeness scores of the enhanced RAG system _,_ respectively, using the following formula: 

**==> picture [254 x 19] intentionally omitted <==**

Inspired by Self-RAG (Asai et al., 2023), we design a hybrid evaluation protocol that integrates human evaluation with clearly defined logical rules to ensure objective assessment of response correctness while minimizing subjectivity. We focus on the correctness of the RAG responses. Correctness is quantified using two key metrics: (1) Factuality, which assesses whether the response accurately reflects the information in the AAS without introducing hallucinations, and (2) Completeness, which measures whether the response fully addresses the question without omitting critical details from the AAS context. 

where _P_ denotes the average observed agreement, and _Pe_ denotes the expected agreement by chance. _Pi_ is calculated at the sub-claim level to ensure that the expected agreement _Pe_ is always 0.5. For the _i_ -th subclaim, _Pi_ is computed as: 

**==> picture [254 x 24] intentionally omitted <==**

where _nij_ represents the number of annotators who assign label _j_ , _N_ is the total number of annotators (here _N_ = 3), and _k_ is number of possible labels ( _k_ = 2). 

To implement this evaluation, we invite a mechanical engineer responsible for robot kinematic modeling to manually define and answer the questions. The answers are formulated in multiple sub-claims as a 

Afterward, _P_ is obtained by averaging _Pi_ across all sub-claims of 30 questions. In this study, one of the evaluators is a mechanical engineer responsible for defining the ground-truth labels, while the other two are AAS experts without specific expertise in robotic kinematic simulation. Despite this difference in domain expertise, we achieve very high IAA scores, with Factuality reaching 90.4 % and Completeness 96.8 %. This demonstrates that this evaluation framework ensures a relatively deterministic and transparent scoring mechanism for assessing response correctness. 

## **Table 3** 

Exemplary question, response, ground-truth answer, and evaluation results. The underlined parts in ground-truth answers represent essential information that should be addressed in the RAG response. 

|**Table 3**<br>Exemplary question, response, ground-truth answer, and evaluation results. The<br>underlined parts in ground-truth answers represent essential information that<br>should be addressed in the RAG response.|<br>AAS experts without specifc expertise in robotic kinematic simulation.<br>Despite this difference in domain expertise, we achieve very high IAA<br>scores, with Factuality reaching 90.4 % and Completeness 96.8 %. This<br>demonstrates that this evaluation framework ensures a relatively|
|---|---|
|Exemplary Questions<br>_How are the components connected in the work cell?_<br>**Response**<br>_The components of the CobottaCell are connected as follows:_<br>1._KiWiCell (structural base) starts from Link00 (system reference“world”)._<br>2._ConnectedJoint00 (c_211_kiwi_cell_joint): Fixes the KiWiCell to the“world”, _<br>_establishing the base position._<br>3._ConnectedJoint01 (c_210_cobotta_pro_joint): Attaches the CobottaPro robot to the_<br>_KiWiCell, positioning the robot securely._<br>4._ConnectedJoint02 (c_212_pneumatic_disassembly_unit_with_2_cylinders_joint): Connects_<br>_the pneumatic disassembly unit to the KiWiCell._<br>5._ConnectedJoint03 (c_213_schunk_egp64_gripper_joint): Links the EGP_−_64 gripper to the_<br>_system, fnalizing the setup with the end-effector._<br>**Ground-truth answer**<br>1. KiWiCell’s base link is fxed to the system reference “world”<br>2. CobottaPro’s base link (link00) is fxed to KiwiCell’s robot base plate link (link01)<br>3. Pneumatic disassembly unit’s base link (link00) is fxed to KiwiCell’s robot base<br>plate link (link01)<br>4. Gripper’s base link (link00) is fxed to CobottaPro’s J6 link (link06)<br>**Evaluation**<br>Factuality: 0.75<br>Completeness: 0|<br>deterministic and transparent scoring mechanism for assessing response<br>correctness.<br>Under this evaluation framework, we assessed the enhanced RAG<br>system, comparing its performance to human performance and a base-<br>line RAG system. The results presented inTable 4 include metrics for<br>Factuality and Completeness, as well as the average inference time per<br>query (ITQ) in seconds. For cases where evaluator scores are inconsis-<br>tent for a sub-claim, a majority vote is used to determine the fnal scores.<br>**Table 4**<br>Evaluation results for enhanced RAG system, baseline RAG, and human per-<br>formance. ITQ refers to inference time per query in seconds. Baseline RAG relies<br>solely on initial retrieval without reranking. The proposed enhanced RAG<br>additionally reranks the retrieval results by the fne-tuned entity selection<br>model.|
||Approach<br>Factuality<br>Completeness<br>ITQ (s)|
||Human performance<br>95.1 %<br>97.6 %<br>38.7<br>Baseline RAG<br>81.7 %<br>70.7 %<br>1.3<br>Enhanced RAG<br>89.0 %<br>81.7 %<br>2.8|



Under this evaluation framework, we assessed the enhanced RAG system, comparing its performance to human performance and a baseline RAG system. The results presented in Table 4 include metrics for Factuality and Completeness, as well as the average inference time per query (ITQ) in seconds. For cases where evaluator scores are inconsistent for a sub-claim, a majority vote is used to determine the final scores. 

Evaluation results for enhanced RAG system, baseline RAG, and human performance. ITQ refers to inference time per query in seconds. Baseline RAG relies solely on initial retrieval without reranking. The proposed enhanced RAG additionally reranks the retrieval results by the fine-tuned entity selection model.

### Page 10

> _D. Shi et al.                                                                                                                                                                                                                                      Computers in Industry 171 (2025) 104330_ 

In the traditional manual process, a robotics engineer has to retrieve information from various documents, such as Excel and Word files, within the project folder. This method is notably time-intensive, even though the expert is allowed to provide very brief answers without composing full sentences. Interestingly, human experts tend to make more errors on fact-checking questions. For instance, when asked, _“Provide me the calibration offset of all the gripper’s joints”_ , careless mistakes and typos are observed. 

Also, Completeness scores are relatively higher than Factuality scores in human performance. In contrast, RAG systems often struggle to deliver complete answers. Continuing with the previous example, both RAG systems provide the value for only one joint instead of both. This shortfall is primarily due to the retrieval component fetching excessive irrelevant information or failing to identify all positive candidates accurately. Such noise can also introduce hallucinations. For example, when queried about which joint of the pneumatic disassembly unit is connected to the work cell, the system responded, _“Pull Cylinder Joint (Prismatic) is connected to the base structure (KiWiCell).”_ However, “Pull Cylinder Joint” is not mentioned among the kinematic joints of the pneumatic disassembly unit. Keywords like “joint” and “pneumatic disassembly unit” semantically match multiple properties within the AAS, such as those in the SM Technical Data, leading to the retrieval of unrelated information. Incorporating a reranking step, the enhanced RAG system demonstrates improved performance over the baseline. When the correct information is retrieved and ranked higher, the factual accuracy of responses generally meets expectations. However, challenges persist in ensuring that the system retrieves all necessary information while avoiding the misranking of irrelevant or noisy information at high positions. 

In addition to improvements in factuality and completeness, we also evaluated the computational efficiency of the proposed enhanced RAG system using ITQ. As shown in Table 4, the ITQ for the enhanced RAG system is 2.8 s, approximately twice that of the baseline RAG (1.3 s). This increase is attributed to the added reranking step, which involves a fine-tuned LLM-based entity selection model. However, the additional computation is justified by the substantial gains in performance, with factuality improving by + 7.3 % and completeness by + 11.0 %. 

These observations underscore the critical role that retrieval quality plays in determining the overall performance of RAG systems. To further assess the effectiveness of our proposed entity selection model for retrieval improvements, we conduct a more detailed statistical evaluation on a larger dataset in Section 5. 

For practical deployment, the LLMs in the enhanced RAG pipeline are hosted on an NVIDIA DGX A100 system using the vLLM inference framework (Kwon et al., 2023), which enables efficient multi-model serving. vLLM supports horizontal scaling, with each model deployed at a dedicated endpoint, allowing for modular and independent scaling of high-demand components such as the chat model. 

Regarding memory footprint, the entity selection model and embedding model are both based on the shared LLM backbone “SFREmbedding-Mistral-7B”, each requiring approximately 9 GB of GPU memory. For response generation, we utilize GPT-4 due to its superior performance. In scenarios where a local model is preferred, a large-scale alternative such as LLaMA2-70B can be used, which requires approximately 70 GB of GPU memory for streaming inference in our implemented pipeline. 

## **5. Statistical evaluation of retrieval quality** 

## _5.1. Objectives_ 

This section conducts a statistical evaluation of the retrieval quality achieved through the proposed CSL-based fine-tuning approach using the extended AAS entity matching dataset. The LLM fine-tuned with CSL acts as the entity selection model for reranking. It aims to refine the initial retrieval results and ultimately enhance the overall RAG perfor- 

mance. The experiments in this section are designed to address the following specific research questions (RQs): 

- RQ1: Does the proposed fine-tuning strategy with CSL effectively improve the initial retrieval results? 

- RQ2: What is the optimal setting for _N_ , the number of in-batch candidates, in terms of balancing accuracy and efficiency during inference? 

- RQ3: Can the proposed fine-tuning strategy with CSL outperform SOTA pairwise entity matching and pre-trained LLMs with prompt engineering? 

Previous studies related to RAG primarily rely on initial similaritybased retrieval to identify relevant information within the knowledge base, but did not explicitly evaluate the performance of this retrieval process. RQ1 seeks to fill this gap by assessing whether the proposed CSL-based fine-tuning can enhance the quality of initial retrieval results. 

The setting of _N_ plays a crucial role in the fine-tuning process with CSL. This parameter determines how many candidates are processed simultaneously during a single inference. The Top-K parameter is empirically set to 10, which has been found to be optimal for initial retrieval (Shi et al., 2024). If _N_ = _K_ , the model achieves maximum efficiency, as it only requires one inference to process all top-K candidates. However, increasing _N_ may potentially degrade performance, as selecting the correct candidate becomes more challenging when the model must choose from a larger set. RQ2 investigates the trade-off _N_ . between accuracy and efficiency by exploring the optimal value for 

RQ3 compares the proposed CSL-based fine-tuning strategy against SOTA approaches: fine-tuning a pairwise entity matcher and using pretrained LLMs with prompt engineering. This comparison will determine whether CSL offers a significant advantage. 

## _5.2. Datasets_ 

To conduct the experiments, we compiled an entity retrieval dataset consisting of query entities and entities from the standardized vocabulary repository ECLASS (2024). ECLASS is a standardized dictionary of professional terminologies across various industrial sectors. It follows the standardized schema defined in IEC 61360 to describe terminology in the form of an ontology, representing each entity with several standardized attributes. ECLASS commonly serves as the semantic reference for AAS entities. The dataset is based on ECLASS version 12 Advanced, which contains 27,423 unique entities, forming the knowledge base. The query entities used for the search comprise 2522 AAS entities extracted from the _KinematicModel_ SM proposed in this work and 57 standardized SMTs, which were defined and published by the Industrial Digital Twin Association (IDTA). Fig. 8 illustrates an exemplary AAS entity “Representation” within _KinematicModel_ , which is part of the metadata for the CAD model. In the dataset, we primarily use the attributes “IdShort” and “Description” for retrieval purposes. 

Ground-truth labels were established using two approaches. First, the SMT developers have already mapped ECLASS entities to the concept descriptions of the corresponding 491 AAS entities in the SMTs published on the IDTA website. For these query entities, a true positive match was predefined. For instance, as illustrated in Fig. 8, the AAS entity “Representation” includes a SemanticID that links to an ECLASS entity. In this case, the query entity becomes “ _Representation.Geometric representation of the model. ValueList: SolidBody, WireFrame, Surface, Mesh, PointCloud_ ”, with the true positive match being “ _Representation. Graphical appearance_ ”. Negative samples are generated by using a similarity search to identify _K_ − 1 negative candidates from the ECLASS repository. For other AAS entities without predefined ECLASS references, we developed a labeling tool to manually identify the true positive match from the retrieved top-K candidates. As shown in Fig. 9, the tool’s user interface displays the top-10 candidates returned by the initial retrieval, ranked by similarity score. Annotators then select the

### Page 11

> _D. Shi et al.                                                                                                                                                                                                                                      Computers in Industry 171 (2025) 104330_ 

**==> picture [457 x 355] intentionally omitted <==**

**Fig. 8.** Exemplary property “representation” within the SM _KinematicModel_ . The upper-left figure shows its position within the SM. The lower-left figure shows its attributes. The right figure shows its concept description and the referenced ECLASS entity through the semanticID. 

true positive match based on their domain knowledge and the context provided by the SM. The result is recorded as an array containing the query entity, the positive match, nine negative candidates, and the corresponding one-hot encoded label. This ultimately results in 800 data samples, further divided into 480 training samples, 160 validation samples, and 160 test samples. 

## _5.3. Experiment settings_ 

The experiments were conducted on an NVIDIA DGX A100 system, equipped with eight A100 GPUs. The network modeling and the pipeline for training and inference of the selection model _LLMr_ are primarily implemented using the HuggingFace Transformers library. The _LLMr_ is fine-tuned based on SFR-Embedding-Mistral using LoRa over 10 epochs. The LoRa rank _r_ is a critical hyperparameter that significantly impacts model performance. In our experiments, _r_ is empirically set to 128 for all LLMs. The learning rate is set to 2 _e_[−][4] , and the batch size is set to 32. Other training hyperparameters are aligned with the original LoRa paper (Hu et al., 2021). 

For the chat model _LLMc_ , we utilize the latest GPT-4o model available at the time of writing ( _i.e._ , gpt-4o-2024–05-13), which is accessed via the Azure OpenAI REST API. For the embedding model _LLMe_ , we empirically evaluate several commonly used embedding models from related works and ultimately select the SFR-Embedding-Mistral model. The comparative embedding models and the evaluation results are presented below. 

To evaluate the model performance, we employ F1 score, a standard metric in entity matching tasks, and mean reciprocal rank at rank K 

(MRR@K), a standard metric in information retrieval tasks. The F1 score assesses the model’s ability to correctly identify matches, while MRR@K evaluates how well the model ranks the true positive candidate within the retrieved set. MRR is calculated as: 

**==> picture [254 x 18] intentionally omitted <==**

where _ranki_ denotes the position of the true positive match within the top-K candidates. Should no true positive appears in the candidates, _ranki_ = 0. K is set to 10. 

Three groups of comparative retrieval systems are considered in the experiments. The first group consists of methods that execute only the initial retrieval step: the well-known _BM25 model_ (Robertson and Zaragoza, 2009), a probabilistic retrieval algorithm that ranks candidates based on statistical features, the SOTA commercial model “text-embedding-3-large” from OpenAI (2024), the representative sentence-transformer-based embedding model “all-mpnet-base-v2” (Huggingface, 2024a), the representative Llama-based embedding model “RepLLaMA” (Ma et al., 2023), and the representative Mistral-based embedding model “SFR-Embedding-Mistral”. The second group incorporates SOTA fine-tuned pairwise entity matchers for reranking: a transformer-based model _RoBERTa_ (Li et al., 2023) and a fine-tuned LLM termed _Llama4EM_ (Shi et al., 2025). The third group includes two approaches utilizing prompt engineering without fine-tuning: GPT-4 with ICL for pairwise entity matching, termed _GPT4EM_ (Peeters and Bizer, 2023), and GPT-4 with ICL for entity selection, termed _GPT4SEM_ (Wang et al., 2024). For a fair comparison, all

### Page 12

> _D. Shi et al.                                                                                                                                                                                                                                      Computers in Industry 171 (2025) 104330_ 

**==> picture [481 x 307] intentionally omitted <==**

**Fig. 9.** User interface of the developed labelling tool to manually identify the true positive match for the given query entity. 

## **Table 5** 

Experiment results. Our approach is SFR-Embedding-Mistral fine-tuned with CSL. The comparative approaches are summarized in the three groups. The evaluation metrics are MRR@10 (in percentage), F1 score (in percentage), and inference time per query (ITQ). 

|Group<br>G1: inital retrieval|Model<br>BM25<br>text-embedding−3-<br>large|MRR@10<br>27.8<br>54.2|F1<br>23.1<br>45.4|ITQ<br>(s)<br>0.1<br>0.3|
|---|---|---|---|---|
||all-mpnet-base-v2|38.1|29.9|0.1|
||RepLLaMA|44.1|21.3|1.2|
|G2: fne-tuned pairwise<br>entity matcher|SFR-Embedding-<br>Mistral<br>RoBERTa<br>Llama4EM|57.5<br>59.7<br>61.3|48.1<br>32.4<br>46.6|0.2<br>0.4<br>1.3|
|G3: LLM with prompt|GPT4EM|59.7|37.9|7.9|
|engineering<br>G4: Our approach<br>with different_N_|GPT4SEM<br>**_N_** =**_10_**<br>_N_ =8<br>_N_ =6<br>_N_ =4<br>_N_ =2|67.9<br>72.0<br>**72.4**<br>71.7<br>71.0<br>71.4|54.4<br>**63.8**<br>63.8<br>63.8<br>62.5<br>62.5|0.7<br>**1.2**<br>2.6<br>3.9<br>4.2<br>5.4|



approaches were implemented within the same experimental framework. 

## _5.4. Experiment results_ 

Table 5 summarizes the experiment results. Our approach, SFREmbedding-Mistral fine-tuned with CSL, is compared against three groups of retrieval systems to evaluate its effectiveness. Additionally, we empirically investigate the impact of the number of negative candidates _N_ in an input sample. 

the lowest ITQ (0.1 s). While efficient in speed, this model falls significantly short in retrieval effectiveness compared to more modern approaches. Among the embedding models commonly used in prior works, the sentence-transformer-based model “all-mpnet-base-v2” improves MRR@10–38.1 %, but still underperforms compared to LLM-based embeddings. The OpenAI commercial model “text-embedding-3large”, which benefits from proprietary optimizations, achieves a substantially higher MRR@10 (54.2 %) and F1 score (45.4 %). The opensource Llama2-based model “RepLLaMA” shows moderate retrieval performance with an MRR@10 of 44.1 % but suffers from the highest ITQ (1.2 s). Finally, the SFR-Embedding-Mistral model, used as our baseline for initial retrieval, outperforms all other models with an MRR@10 of 57.5 % and an F1 score of 48.1 %, while maintaining a competitive ITQ of 0.2 s. However, while it shows improvement, it still leaves room for further enhancements, particularly when reranking mechanisms are introduced. 

In the entity matching domain, the most common approach is finetuning a pairwise entity matcher for reranking. Prior to the rise of LLMs, fine-tuned transformer models were predominant. For example, the fine-tuned RoBERTa model increases the MRR@10–59.7 %, with a moderate ITQ of 0.4 s. When fine-tuning a Llama2 model, the performance improves further, achieving an MRR@10 of 61.3 %, though at the cost of a higher ITQ (1.3 s). However, an important observation is that pairwise matchers are validated based on MRR rather than F1 score. The selected model checkpoints prioritize achieving the highest MRR, which leads to better retrieval performance but may result in a lower F1 score. If we instead select model checkpoints that optimize for F1, we observe a noticeable drop in MRR. This trade-off suggests that pairwise fine-tuning may not fully capture the complexities of distinguishing true positives from similar distractors. 

The same observation applies to GPT4EM and GPT4SEM. GPT4EM follows a pairwise matching approach using LLM with prompt engineering, while GPT4SEM adopts a listwise selection strategy. The results 

The traditional BM25 model yields a poor MRR@10 of 27.8 % with

### Page 13

> _D. Shi et al.                                                                                                                                                                                                                                      Computers in Industry 171 (2025) 104330_ 

demonstrate that GPT4EM achieves an MRR@10 of 59.7 %, but at the cost of a significantly higher ITQ (7.9 s) and a drop in F1 score (37.9 %). In contrast, GPT4SEM surpasses all pairwise entity matching methods, achieving an MRR@10 of 67.9 %, while also drastically reducing ITQ to 0.7 s and improving F1 score to 54.4 %. These findings suggest that listwise selection approaches can not only enhance retrieval effectiveness (higher MRR and F1) but also significantly improve computational efficiency compared to pairwise approaches. 

By significantly improving MRR@10 to over 71 % and F1 score to over 62 %, our approach surpasses all the comparative methods. When _N_ = 10, all the initially retrieved top-10 candidates are directly fed into the model for selection, maintaining a relatively low ITQ despite the complex Siamese network architecture. Interestingly, varying _N_ does not significantly impact the performance as initially expected. When _N_ = 8, the best MRR@10 of 72.4 % is achieved but with more than double the ITQ compared to when _N_ = 10. Further reducing _N_ leads to a slight drop in performance. 

## _5.5. Discussions_ 

RQ1: Does the proposed fine-tuning strategy with CSL effectively improve the initial retrieval results? The experimental results demonstrate a significant performance improvement in terms of MRR@10 and F1 score when applying our fine-tuning strategy with CSL compared to the baseline SFR-Embedding-Mistral model. This enhancement validates the effectiveness of our approach. 

RQ3: Can the proposed fine-tuning strategy with CSL outperform SOTA pairwise entity matching and pre-trained LLMs with prompt engineering? To evaluate this, we perform a one-sample _t_ -test comparing our approach against the grouped results from G2 and G3 in terms of MRR@10 and F1 score. The analysis yields _p_ -values of 0.0075 for MRR@10 and 0.011 for F1, indicating statistically significant evidence that our method outperforms the SOTA group. 

Additionally, we observed that even without fine-tuning, the GPT4SEM model outperforms fine-tuned pairwise entity matching approaches. This highlights the importance of the listwise selection approach, which exposes the model to all candidates in a single data sample, allowing for better differentiation between semantically similar distractors. 

Furthermore, a deeper comparison between pairwise matching approaches (such as RoBERTa and Llama4EM in Group 2, and GPT4EM in Group 3) and listwise selection approaches (such as GPT4SEM and our proposed method) reveals critical insights. By design, pairwise matching methods evaluate candidate pairs independently, optimizing the model for binary classification accuracy rather than the overall ranking of candidates. This often results in better F1 scores, but the optimization objective does not align with MRR, which measures ranking effectiveness. As a result, models fine-tuned to maximize F1 score may not necessarily achieve the best MRR, and vice versa. Moreover, pairwise matchers are susceptible to false positives because they assess each candidate without considering the broader context of all retrieved candidates. For instance, given a query entity “ConformityToSafetyStandards”, the only true positive candidate should be “compliance to standard(s) or specification”. However, the best pairwise matcher Llama4EM incorrectly predicts multiple positives, including “reference standard for functional safety”, which, while semantically related, is not the correct match. This issue arises because pairwise models focus on binary classification rather than relative ranking among all the candidates. In contrast, listwise selection methods naturally optimize the ranking objective by directly comparing all candidates and identifying the most likely match against distractors. This makes them more effective in refining retrieval results. 

Despite significantly improving the retrieval performance, our approach does not yet achieve very high MRR or F1 scores, indicating that false positives and false negatives still occur. This may be caused by the RAG system’s difficulty in providing fully complete responses. In our 

training and evaluation dataset, each query is associated with only a single true positive candidate. Consequently, we employ cross-entropy loss to optimize the model’s ability to identify this positive match. However, in real-world RAG applications, multiple true positives may exist. In such cases, our approach may lead to missed detections, potentially resulting in incomplete responses. 

RQ2: What is the optimal setting for _N_ , the number of in-batch candidates, in terms of balancing accuracy and efficiency during inference? Through experimentation, we determined that setting _N_ = 10 offers an optimal balance between accuracy and computational efficiency during inference. 

_N_ At first glance, this result may seem counterintuitive, as a larger could theoretically increase the difficulty of correctly selecting the true positive among more candidates. However, our findings suggest that the impact of _N_ is not as significant as expected, and usage of a smaller value even leads to worse performance. Upon closer examination of sample predictions, we identify two key reasons behind this observation. 

First, the retrieved negative samples are already ranked by the initial retrieval step, meaning that the hardest negative samples typically appear at the top of the candidate list. However, in many cases, the knowledge base itself contains only a limited number of highly similar distractors. As a result, not all _K_ candidates ( _K_ = 10 in our case) are equally difficult for the model to distinguish from the true positive. This means that increasing _N_ does not necessarily introduce significantly more confusion or difficulty in the model’s learning process. 

Second, when _N_ is too small, the inference process must be repeated multiple times, increasing the risk of false detection. Since each iteration must correctly identify the true positive from a subset of candidates, any single incorrect prediction leads to an overall failure in reranking. This cumulative error effect makes smaller _N_ values less reliable, as more inference cycles introduce additional opportunities for misclassification. 

## **6. Conclusions** 

This paper introduces an enhanced RAG system, integrating AAS for interoperable knowledge representation and LLM for knowledge inference. The proposed approach enhances the cognitive capabilities of conventional DTs toward integrated CDTs. 

A key focus of this work is the formulation of knowledge in the form of AAS and its encoding as a knowledge base of the RAG system. We proposed concatenating the attributes of AAS entities into attribute strings to convey semantic information and using relative paths of entities within the AAS as position strings to express structural relationships. The demonstration validates that the RAG system can effectively understand the interrelationships between components of the robotic cell and their kinematic connections. However, this study did not address the encoding of documents attached within the AAS, such as PDFs, drawings, and CAD models. 

The second major focus is enhancing retrieval capabilities using a CSL-based fine-tuning strategy. This approach fine-tunes a generative LLM as an encoding-based selection model, enabling it to directly identify the correct candidate from the top-K results generated by the initial retrieval. Experimental results demonstrated that the fine-tuned model effectively improved overall retrieval performance when used as a reranker. Notably, the experiments highlight the importance of contrastive comparisons between candidates; even without fine-tuning, GPT-4 with ICL-based prompt engineering outperformed the bestperforming pairwise entity matchers that only process query-candidate pairs. However, the current implementation is restricted to predicting a single true positive candidate during inference, aligning with the structure of our training dataset. This limitation reduces its applicability in scenarios where multiple true positives exist. In such cases, the model may miss additional correct matches, leading to incomplete retrieval results and providing less information to the chat model for response generation. 

Future work will focus on expanding the RAG system’s capabilities to

### Page 14

_Computers in Industry 171 (2025) 104330_ 

_D. Shi et al.                                                                                                                                                                                                                                      in_ 

process not only the structured entities within the AAS but also the attached files, such as technical documents and CAD models. This will leverage one of AAS’s significant advantages over knowledge graphs in industrial applications, offering a more comprehensive and flexible representation of information and knowledge. Furthermore, the reranking approach should be further improved, particularly in handling multiple correct matches. 

## **CRediT authorship contribution statement** 

D’Amico, R.D., Erkoyuncu, J.A., Addepalli, S., Penver, S., 2022. Cognitive digital twin: an approach to improve the maintenance management. CIRP J. Manuf. Sci. Technol. 38, 613–630. 

Douze M. et al., 2024. The Faiss Library. (Online). https://doi.org/10.48550/arXiv.2401. 08281. 

ECLASS, An introduction to the standard. 2024. (Online). 〈https://eclass.eu/en/ecla ss-standard/introduction〉. 

- Freire, S.K., Wang, C., Foosherian, M., Wellsandt, S., Ruiz-Arenas, S., Niforatos, E., 2024. Knowledge Sharing in Manufacturing using Large Language Models: User Evaluation and Model Benchmarking. 〈http://arxiv.org/pdf/2401.05200v2〉. 

- Gao, Y., Xiong, Y., Gao, X., Jia, K., Pan, J., Bi, Y., Dai, Y., Sun, J., Wang, M., Wang, H., 2023. Retrieval-Augmented Generation for Large Language Models: A Survey. 

〈http://arxiv.org/pdf/2312.10997v5〉. 

**Dachuan Shi:** Writing – review & editing, Writing – original draft, Visualization, Validation, Software, Resources, Methodology, Investigation, Formal analysis, Data curation, Conceptualization. **Olga Meyer:** Visualization, Project administration, Methodology, Data curation. **Jianzhang Li:** Writing – review & editing, Writing – original draft, Visualization, Software, Methodology, Investigation, Data curation. **Thomas Bauernhansl:** Writing – review & editing, Supervision, Resources, Funding acquisition. 

## **Declaration of Generative AI and AI-assisted technologies in the writing process** 

During the preparation of this work, the author(s) used Grammarly and ChatGPT in order to improve language and readability. After using this tool/service, the author(s) reviewed and edited the content as needed and take(s) full responsibility for the content of the publication. 

## **Declaration of Competing Interest** 

The authors declare that they have no known competing financial interests or personal relationships that could have appeared to influence the work reported in this paper. 

## **Acknowledgements** 

This work was supported in part by the Kopernikus Project “Synergie” (03SFK3A3-3; 03SFK3T2-3) and in part by the project H2GigaFRHY (3HY112C). Both projects are funded by the German Federal Ministry of Education and Research. 

## **Appendix A. Supporting information** 

Supplementary data associated with this article can be found in the online version at doi:10.1016/j.compind.2025.104330. 

## **Data availability** 

The data that has been used is confidential. 

## **References** 

Alvaroa, J., Barredaa, J., An advanced retrieval-augmented generation system for manufacturing quality control. Preprint Submitted to Advanced Engineering Informatics 2024. 

Asai, A., Wu, Z., Wang, Y., Sil, A., Hajishirzi, H., 2023. Self-RAG: Learning to Retrieve, Generate, and Critique through Self-Reflection. 〈http://arxiv.org/pdf/2310. 11511v1〉. 

- Bahr, L., Wehner, C., Wewerka, J., Bittencourt, J., Schmid, U., Daub, R., 2024. Knowledge Graph Enhanced Retrieval-Augmented Generation for Failure Mode and Effects Analysis. 〈http://arxiv.org/pdf/2406.18114v2〉. 

- Barlaug, N., Gulla, J.A., 2021. Neural networks for entity matching: a survey. ACM Trans. Knowl. Discov. Data 15 (3), 1–37. 

- Boss, B. Digital Twin and Asset Administration Shell Concepts and Application in the Industrial Internet and Industrie 4.0. An Industrial Internet Consortium and Plattform Industrie 4.0 Joint Whitepaper. 2020. (Online). 〈https://www.plattform-i 40.de/IP/Redaktion/DE/Downloads/Publikation/Digital-Twin-and-Asset-Administ ration-Shell-Concepts.pdf?__blob=publicationFile&v=1〉. 

- Chandrasekhar, A., Chan, J., Ogoke, F., Ajenifujah, O., Farimani, A.B., 2024. AMGPT: a Large Language Model for Contextual Querying in Additive Manufacturing. 〈http:// arxiv.org/pdf/2406.00031v1〉. 

Hu, E. et al., 2021. LoRA: Low-Rank Adaptation of Large Language Models. (Online). 〈http://arxiv.org/pdf/2106.09685v2〉. 

Huggingface, 2024a. ModeL Card: Sentence-transformers/all-mpnet-base-v2. (Online). 〈https://huggingface.co/sentence-transformers/all-mpnet-base-v2〉. 

Huggingface, 2024b. modeling_mistral.py,. (Online). 〈https://github.com/huggin 

gface/transformers/blob/main/src/transformers/models/mistral/modeling_mistral. py#L456〉. 

- IDTA, 2023. Specification of the Asset Administration Shell – Part 2: Application Programming Interfaces, 2023, (Online). 〈https://industrialdigitaltwin.org/wp-cont ent/uploads/2023/04/IDTA-01002-3-0_SpecificationAssetAdministrationShell_Part 2_API.pdf〉. 

IDTA, 2024. Registered AAS Submodel Templates. (Online). 〈https://industrialdigitalt win.org/en/content-hub/submodels〉. 

- IEC, IEC 61360-1:2017, Standard Data Element Types with Associated Classification Scheme - Part 1: Definitions - Principles and Methods. 

IEC, IEC 63278-2:2022: Asset Administration Shell for Industrial Applications – Part 2: Information meta Model. (Online). 〈https://webstore.iec.ch/publication/65093〉. 

- Kwon W., et al., 2023, Efficient Memory Management for Large Language Model Serving with PagedAttention. In: Proceedings of the ACM SIGOPS Twenty Ninth Symposium on Operating Systems Principles, 〈https://docs.vllm.ai/en/latest/〉. 

Li, Y., Li, J., Suhara, Y., Doan, A., Tan, W., 2023. Effective entity matching with transformers. VLDB J. 32, 1215–1235. 

Li, Y., Wang, Q., Pan, X., Zuo, J., Xu, J., Han, Y., 2024. Digital twins for engineering asset management: synthesis, analytical framework, and future directions. Engineering. Liu, P., Qian, L., Zhao, X., Tao, B., 2024. Joint knowledge graph and large language model for fault diagnosis and its application in aviation assembly. IEEE Trans. Ind. Inf. 1–10. 

Lu, J., Yang, Zheng, X., Wang, J., Dimitris, K., 2022. Exploring the concept of Cognitive Digital Twin from model-based systems engineering perspective. Int J. Adv. Manuf. Technol. 121 (9-10), 5835–5854. 

Ma, X., Wang, L., Yang, N., Wei, F., Lin, J., 2023. Fine-Tuning LLaMA for Multi-Stage Text Retrieval. (Online). 〈https://arxiv.org/abs/2310.08319〉. 

Meng R. et al., 2024. SFR-Embedding-Mistral:Enhance Text Retrieval with Transfer Learnin. Salesforce AI Research Blog. (Online). 〈https://huggingface.co/Salesforce/ SFR-Embedding-Mistral〉. 

Miny, T., Thies, M., Lukic, L., K¨abisch, S., Oladipupo, K., Diedrich, C., Kleinert, T., 2023. Overview and comparison of asset information model standards. IEEE Access 11, 99189–99221. 

Mortlock, T., Muthirayan, D., Yu, S.-Y., Khargonekar, P.P., Abdullah Al Faruque, M., 2022. Graph learning for cognitive digital twins in manufacturing systems. IEEE Trans. Emerg. Top. Comput. 10 (1), 34–45. 

OpenAI, 2024. Embeddings. (Online). 〈https://platform.openai.com/docs/guides/embe ddings/embedding-models〉. 

Oztemel, E., Gursev, S., 2020. Literature review of Industry 4.0 and related technologies. J. Intell. Manuf. 31 (1), 127–182. 

Peeters, R., Bizer, C., 2023. Entity Matching using Large Language Models. 〈http://arxiv. org/pdf/2310.11244v2〉. 

Robertson, S. and Zaragoza, H., 2009. The Probabilistic Relevance Framework: BM25 and Beyond. doi: 10.1561/1500000019. 

Rongen, S., Nikolova, N., van der Pas, M., 2023. Modelling with AAS and RDF in Industry 4.0. Comput. Ind. 148, 103910. 

ROSIndustrial, Description, 2024, (Online). 〈https://rosindustrial.org/about/descript ion/〉〈〉. 

Roˇzanec, J.M., Lu, J., Rupnik, J., Skrjanc, M., Mladeni[ˇ] ´c, D., Fortuna, B., Zheng, X., Kiritsis, D., 2021. Actionable Cognitive Twins for Decision Making in Manufacturing. 〈http://arxiv.org/pdf/2103.12854v1〉. 

Schiesser, M., 2024. RAGapp. (Online). 〈https://github.com/ragapp/ragapp〉. 

Shi, D., Liedl, P., Bauernhansl, T., 2024. Interoperable information modelling leveraging asset administration shell and large language model for quality control toward zero defect manufacturing. J. Manuf. Syst. 77, 678–696. 

- Shi, D., Meyer, O., Oberle, M., Bauernhansl, T., 2025. Dual data mapping with fine-tuned large language models and asset administration shells toward interoperable knowledge representation. Robot. Comput. Integr. Manuf. 91, 102837. 

- Simonic, M., Pahic, R., Gaspar, T., Abdolshah, S., Haddadin, S., Catalano, M.G., Worgotter, F., Ude, A., 2021. Modular ROS-based software architecture for reconfigurable, Industry 4.0 compatible robotic workcells, In: Proceedings of the Twentieth International Conference on Advanced Robotics (ICAR). 2021 20th International Conference on Advanced Robotics (ICAR), Ljubljana, Slovenia. 06.12.2021 - 10.12.2021. IEEE, pp. 44–51. 

Tinnes, Christof, Ristin, Marko, Hohenstein, Uwe, Fathi, Kiavash, 2024. From unstructured product descriptions to structured data for industry 4.0 with ChatGPT. Int. Conf. Ind. CyberPhys. Syst. (ICPS).

### Page 15

Tola, D., Corke, P., 2024. Understanding URDF: A dataset and analysis. IEEE Robot. Autom. Lett. 9 (5), 4479–4486. 

Wang, T., Lin, H., Chen, X., Han, X., Wang, H., Zeng, Z., Sun, L., 2024. Match, Compare, or Select? An Investigation of Large Language Models for Entity Matching. (Online). 〈https://arxiv.org/abs/2405.16884v1〉. 

- Xia, Y., Xiao, Z., Jazdi, N., Weyrich, M., 2024. Generation of asset administration shell with large language model agents: toward semantic interoperability in digital twins in the context of industry 4.0. IEEE Access 12, 84863–84877. 

_Computers in Industry 171 (2025) 104330_ 

- Yang, M., et al., 2024. Ollama. (Online). 〈https://github.com/ollama/ollama〉. Zheng, X., Lu, J., Kiritsis, D., 2022. The emergence of cognitive digital twin: vision, challenges and opportunities. Int. J. Prod. Res. 60 (24), 7610–7632. 

- Zhou, B., Li, X., Liu, T., Xu, K., Liu, W., Bao, J., 2024. CausalKGPT: Industrial Structure Causal Knowledge-enhanced Large Language Model for Cause Analysis of Quality Problems in Aerospace Product Manufacturing.

### Page 16

