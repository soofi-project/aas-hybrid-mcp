# Semantic Aas

Source: semantic_aas_2019_semantic_asset_admin_shell.pdf


---
### Page 1

The Semantic Asset Administration Shell
B
Sebastian R. Bader1( ) and Maria Maleshkova2
1 Fraunhofer Institute for Intelligent Analysis and Information Systems IAIS,
Schloss Birlinghoven, 53757 Sankt Augustin, Germany
sebastian.bader@iais.fraunhofer.de
2 University of Bonn, Endenicher Allee 19a, 53115 Bonn, Germany
maleshkova@cs.uni-bonn.de
Abstract. Thedisruptivepotentialoftheupcomingdigitaltransforma-
tions for the industrial manufacturing domain have led to several refer-
enceframeworksandnumerousstandardizationapproaches.Ontheother
hand, the Semantic Web community has made significant contributions
in the field, for instance on data and service description, integration of
heterogeneoussourcesanddevices,andAItechniquesindistributedsys-
tems.Thesetwostreamsofworkare,however,mostlyunrelatedandonly
briefly regard the each others requirements, practices and terminology.
We contribute to this gap by providing the Semantic Asset Adminis-
tration Shell, an RDF-based representation of the Industrie 4.0 Com-
ponent. We provide an ontology for the latest data model specification,
created a RML mapping, supply resources to validate the RDF entities
and introduce basic reasoning on the Asset Administration Shell data
model. Furthermore, we discuss the different assumptions and presenta-
tionpatterns,andanalyzetheimplicationsofasemanticrepresentation
on the original data. We evaluate the thereby created overheads, and
conclude that the semantic lifting is manageable, also for restricted or
embedded devices, and therefore meets the conditions of Industrie 4.0
scenarios.
· ·
Keywords: Industrie 4.0 Data lifting Asset Administration Shell
1 Introduction
Even though the various digital developments and internet-based technologies
have attracted great attention in the manufacturing industry, a common under-
standing of the resulting requirements and implications has not been reached.
Thenumberofdifferentterms,whicharebeingusedinthiscontext,reflectsthis
challenge – Internet of Things (IoT), Industrial Internet, Cyber-physical Sys-
tems, Digital Twins and many more have slightly overlapping scopes but still
depict different applications and features. Still, the primary target is always the
effective integration and interoperability of industrial devices, services and data
sources.Therefore,theactualimplementationsrequireclearspecificationsofthe
used data formats, interfaces, and semantic meaning of the referenced objects
and attributes.
(cid:2)c TheAuthor(s)2019
M.Acostaetal.(Eds.):SEMANTiCS2019,LNCS11702,pp.159–174,2019.
https://doi.org/10.1007/978-3-030-33220-4_12

---
### Page 2

160 S. R. Bader and M. Maleshkova
IoTdataiscurrentlymainlyexchangedineitherJSONorXML.Thesecom-
monly used data formats ease the serialization and parsing by providing specifi-
cationsforthesyntacticstructureofthedataobjects.Additionalinformationon
the meaning of keys/values is usually specified in customized data models and
schemata. The latest specification of the Plattform Industrie 4.0 Asset Admin-
istration Shell (AAS) also follows this convention [1]. The AAS is promoted as
the digital twin for the German Plattform Industrie 4.0 and encompasses the
interpretation of the digital representation of any production-related asset. As
such,materialsandproducts,devicesandmachinesbutalsosoftwareanddigital
services have a respective digital version.
While the predefined structure and the usage of specific keys reduce the
heterogeneity inherent in the data exchange processes of current industrial sce-
narios, all real-world scenarios still require a thorough understanding of the
specific terms and values. Therefore they are dependent on extensive manual
work and understanding of the extended AAS model, followed by a time con-
sumingdatamapping.Asemanticformalizationofentitiesanddataobjectshas
several advantages in this context. The mature Semantic Web technology stack
around RDF enables clear references to classes, properties and instances in the
form of URIs, beyond the scope of single AAS objects but also across appli-
cations, domains, and organizations. The defined meaning of the used entities
further allows its combination with predefined logical axioms, which allow the
automatic derivation of new knowledge.
Wecontributetothestateoftheartbypresentingamappingfromthelatest
AASdatamodeltoRDF.Thusweprovideadatamodelasanopenlyaccessible
ontology and create SHACL shapes for all classes to enable schema validation.
We outline the various pitfalls, especially the different patterns to identify, and
refer to encoded entities and to links to remote resources. Based on the inher-
ent Web nature of RDF, we show how the transformation to the semantic data
model decreases the amount of required storage space. Furthermore, we present
patternstodirectlyinserttheRDFtranslationintotheoriginalXMLandJSON
files and discuss their implications. Relying on the RDF/XML and JSON-LD
serializations,weareabletomergethepredefineddatastructurewiththeseman-
tically defined data. We show that the provided extension points in the form of
submodel elements are suitable for this task and that the output AAS files are
still processablebyexisting software, therefore theriskof compatibility issuesis
manageable.
The applicability of the presented approach is evaluated by determining the
necessary overhead in terms of both storage and computation effort, and by a
detailed discussion of the restrictions of the RDF version. We show that some
semanticconstructsaremoreefficientthantheoriginallyspecifiedones,whereas
othersarenotdirectlycompatiblewiththedatastructureofRDFandsomeare
even not expressible at all.
In this context the paper makes the following contributions: (1) an RDF
data model of the Semantic Asset Administration Shell SAAS, (2) a mapping
from XML Asset Administration Shell representations to SAAS, (3) a set of

---
### Page 3

The Semantic Asset Administration Shell 161
preliminary reasoning axioms in order to explicitly derive implicitly encoded
informationfromthedatamodel,and(4)avalidationmodelforthisdatamodel,
encoded through SHACL shapes.
The remainder of this paper is organized as follows. Section2 contains an
overview on similar efforts in the field. Section3 introduces a formalization of
the regarded domain followed by the presentation of the RAMI ontology and an
RMLmappinginSect.5.Section6brieflyexaminesseveralaxiomsforautomated
reasoning on top of the SAAS, while Sect.7 illustrates the provided SHACL
Shapes for schema validation. We use several use cases (Sect.8) to evaluate our
approach(Sect.9).Finally,weconcludewithadiscussiononthepotentialofthe
SAAS and outline further research gaps.
2 Related Work
In this section, we discuss three areas of related work – the data model of the
AssetAdministration Shell, the existing mappings towards a semantic represen-
tation and related mappings of Industrie 4.0 data models to RDF.
Barnstedt et al. define the data model of the Asset Administration Shell [1],
the form of identifiers, access rights and roles, as well as XML and JSON serial-
izationsandtheirtransport.Thetextualdocumentationofthemodelisenhanced
withXMLandJSONschemata.Themodeldefinesabasicsetofkeysandprop-
erties, and outlines defined points for custom vocabularies and terminologies.
Part 2 of specification will further determine the APIs and interaction functions
of the Asset Administration Shell, and how operations can be provided and
described for the Industrie 4.0 (Fig.1).
Fig.1. Sections of the Asset Administration Shell Data Model according to [1] (page
44).
Grangel-Gonza ́lez provide a first RDF data model for the Administration
Asset Shell and the respective technical standards as published by ISO, IECC,
and DIN [6]. They further extended the work in [5] with a formalized model of
the Reference Architecture for Industrie 4.0 (RAMI4.0) and entities for units of

---
### Page 4

162 S. R. Bader and M. Maleshkova
measurementsandprovenance,andshowaprototypicalmappingusingR2RML.
However, the mapping itself was not generally applicable to other Asset Shells
as a common data model was not specified at this time.
Tantik and Anderl [11] present an analysis how recommendations of the
WorldWideWebConsortium(W3C)fittotheguidelinesofthePlattformIndus-
trie4.0.TheyoutlinevarioussuggestionshowstandardizedWebtechnologiescan
be integrated into Asset Shells. The authors present best practices and integra-
tion methods through a sample implementation scenario but do not discuss the
implications on the data model itself.
Mappings of relational or otherwise formatted data to RDF are possible
withtheRDBtoRDFMappingLanguageR2RML[2]orthebroaderapplicable
RDF Mapping Language RML [4], which also enables mappings from JSON,
XML or CSV to RDF. The desired transformations are also formulated in RDF
by defining the output graph structure by so-called Maps and URI templates.
While R2RML strictly relies on tables, and uses column names as resource and
attribute identifiers of row-based data objects, RML also transforms JSON and
XML data by identifying objects according to their keys. Even though some
tools have been introduced in order to support the creation of mappings for
both approaches, the possibility to collaboratively work on mappings was not
part of the design requirements and is still missing.
Katie et al. [8] show by integrating the machine-to-machine communication
protocolOPC-UAforserversandclientshowsemanticdescriptions,inparticular
SAWSDL annotations, bridge the gap between the heterogeneous devices of the
shop floor. The use of uniquely identified semantic descriptions supports the
automaticorchestrationofdecoupledCyber-physicalSystems.However,onlythe
specific input and output requirements of the OPC-UA methods are described.
NeitherthedataobjectsnortheOPC-UAgeneralinformationmodelisreflected.
Dietrich et al. examine the semantic characteristics of the Asset Adminis-
tration Shell in [3]. They outline the identification of attributes and properties
through cross-industry standards, mainly IEC 61360 and eCl@ss. In addition,
they discuss mappings to AutomationML and OPC-UA. However, Dietrich et
al.donotrecognizetheconceptsoftheSemanticWebandthereforedonotshow
how to integrate the Administration Shell with its technology stack.
Currently, to the best of our knowledge, there is no RDF representation
of the officially released data model of the Asset Administration Shell. This
is necessary in order to build a bridge between the latest approaches of data
provisioning models inthemanufacturing domain andtherichandmaturedata
integrationandformalizationcapabilitiesoftheSemanticWeb.Assuch,anRDF
datamodelhasthepotentialtoeasetheinformationexchangebutalsoprovides
thecapabilitiestointroducelogicalreasoningtotheAssetAdministrationShell.
3 Methodology
ThedatamodelfortheIndustrie4.0componentaimstoprovidehighcoverageof
the different modeling variants. RDF on the other hand has specific conditions

---
### Page 5

The Semantic Asset Administration Shell 163
how data is presented (triple-based structure, URI as identifier). In order to
structure the contribution of this paper, the parts of the respective data models
are defined as follows:
AAS captures the information about the Administration Asset Shell itself.
In this regard, AAS is the digital representation or Digital Twin of the Asset.
Information from AAS, therefore, refers to the information object or document
and only indirectly to the original asset. Examples are the creation date of the
digital representation, manuals, or how the AAS was generated or modified. It
is important to note that the same reference is used to denote both the Admin-
istration Asset Shell itself and the set of information contained by it.
Acapturestheinformationabouttheactualasset.Theassetcanbeanything
of interest in the context of a digital production setting. Even though assets are
usually embedded devices or internet-capable components, any physical object,
such as materials, production goods or machines, can be seen as an asset too.
In addition, assets also include software components and any digital service or
intangible thing, which is necessary to model a manufacturing use case.
S denotes the submodel of the asset shell. Submodels partition the provided
informationandcategorizefactsaccordingtotheirusage,forinstanceaspartof
adocumentationsubmodelorasubmodelforqualitytesting.Submodelsarefur-
therseparatedintoSubmodelElements,whichareeitherthemselvescollectionsof
SubmodelElementsorthefinalbearerofkey-value-encodedfacts.Asanycombi-
nationofdifferentsubmodelscanbeincludedintheAssetAdministrationShell,
the set Sk represents the superset, including all possible submodels.
I is the set of identifiers for data objects. Specifically I = I ∪I where
glob loc
I contains all globally valid identifiers, while the elements of I are only
glob loc
valid in their context, in particular inside the AAS, which uses them.
The concept descriptions denoted with CD may provide further defini-
tions about the used concepts, mainly attributes and data types. While con-
cept descriptions are optional components of an AAS, they give the ability to
place necessary explanations especially for entities with local identifiers close to
the data. Similarly to submodels, concept descriptions are not limited in their
appearance, therefore the superset CDl is used.
An instance aas of an AAS is, therefore, defined by the union of the men-
tioned sets:
aas∈AAS∪A∪Sk∪CDl (1)
The identifiers appear in all sets and are therefore not mentioned separately.
They connect the objects of the different sets with each other. However, the
nature of identifiers in the AAS data model is mostly the one of foreign keys,
whichdonotlinkdirectlytotheintendedobject.Wedefinetwotypesoffunctions
on the administration shell. First, a serialization ser transforms each adminis-
trationshelltoarepresentationinadataformat,inparticularJSONandXML:
ser :AAS →D ={XML,JSON,...}
Second, a mapping is a transformation m from the data model AAS to the
Semantic Asset Administration Shell SAAS. SAAS is defined as
SAAS =AAS ∪A ∪Sk ∪CDl (2)
RDF RDF RDF RDF

---
### Page 6

164 S. R. Bader and M. Maleshkova
Usingthesedefinitions,anAASinXMLundergoesseveralsteps(seeFig.2).
A created SAAS object using the provided mapping (Sect.5) can be sent to
a reasoning engine (Sect.6) to enrich it with additional facts. Both the native
SAAS andtheenrichedSAAS+ canbeforwardedtoavalidationmodule
RDF RDF
(Sect.7).Thevalidationmodulecreatesavalidationreport,containingtheerrors
and inconsistencies against the SAAS schema. Of course, also otherwise created
SAASobjectscanbesenttothereasoningorvalidationmodules(bottomlane).
Fig.2. Process steps through the provided modules.
4 The SAAS Data Model
In the following we present the SAAS data model as an RDF ontology1. As
mentioned, the ontology is an advanced version of the RAMI ontology [6] and,
therefore, the namespace rami is used. For each class from [1] a corresponding
OWL Class has been created and every attribute has been mirrored with either
an ObjectProperty or a DataProperty, except for the ‘semanticId’. The reason
for the later is that ’semanticId’ links to the unique identifier for the entity. In
RDF, this is the entity URI itself and therefore does not need to be repeated
(Fig.3).
All RDF entities are supplied with (sub)class assertions, labels and com-
ments. The SAAS classes reflect the original ones in most cases and form a sub-
class hierarchy based on the inheritance specification of the AAS data model.
However,neitherRDFnorOWLknowabstractclasses.AASusesabstractclass
constructs to partition certain attribute requirements and characteristics. For
instance, the ‘Has Kind’ class covers all realizations, which contain a ‘kind’
attribute.Thisattributeencodeswhetheracertainentityiseitherreferringtoa
concreteinstance(theexplicitmachineinstalledinashopfloor)orisrelatedtoa
wholetype(machinetypeAcanbeinstalledinacertainsetting).Thedatamodel
reflects the abstract nature through :class skos:note “abstract” statements.
WhiletheexistingschemesforXMLandJSONarebasedonatree-structure,
the RDF data model supports a more generic graph structure. While this might
lead to the conclusion that for every model from AAS or AAS a corre-
xml json
sponding RDF serialization must be possible, therefore AAS ⊆ SAAS, we will
show that some limitations exist and actually AAS ⊃SAAS is the case.
1 https://github.com/i40-Tools/RAMIOntology.

---
### Page 7

The Semantic Asset Administration Shell 165
Fig.3. Overview on the most important classes and properties of the SAAS
(For full visualization see http://www.visualdataweb.de/webvowl/#iri=https://raw.
githubusercontent.com/i40-Tools/RAMIOntology/master/rami.ttl).
5 Mapping to RDF
The Administration Shell object (AAS) is the root of every Asset Administra-
tion Shell. Listing1.1 shows an example XML snippet. As the root entity, it is
also the entrypoint for traversing the SAAS graph. A native mapping is always
possible if the identifier is already applied in the form of an URI. However, also
International Registration Data Identifiers (IRDI)and any other custom format
is allowed. While IRDIs in case of the wide-spread eCl@ss system can – with
significant additional efforts – being mapped to URIs, this is in general a very
hardanderror-pronechallenge2.Thisbecomesevenharderwhenregardingpro-
prietaryorcustomidentifiers.Inaddition,customidentifiersmaycontainspecial
characters as spaces or several hash signs. These characters are percent encoded
(# → %23, changing the appearance of identifiers. As a result, only native URI
identifiers can be mapped without risk, not only for AAS identifiers but also for
the other sets in the following.
A consequence of this decision is also that the ‘Has Semantics’ class and
the ‘semanticId’ property of the AAS data model becomes native to all objects.
Moreover, it implies that all URIs are not only uniquely identifying its data
objectbutalsosupplythesemanticdefinitionoftheirmeaning.Thisratherstrict
2 Forinstance,templatesforeCl@ssIDs,e.g.26-04-07-02(High-voltagecurrent),may
map to https://www.eclasscontent.com/index.php?id=26040702.

---
### Page 8

166 S. R. Bader and M. Maleshkova
1 <?xml version="1.0"?>
2 <aas:aasenv xmlns:IEC61360="http://www.admin-shell.io/...">
3 <aas:assetAdministrationShells>
4 <aas:assetAdministrationShell>
5 <aas:idShort>RaspberryPiModel3B+</aas:idShort>
6 <aas:identification idType="URI">
7 http://iais.fraunhofer.de/.../raspberry_pi_3b_plus
8 </aas:identification>
9 <aas:assetRef>
10 <aas:keys>
11 <aas:key type="Asset" local="true" idType="URI">
12 https://iais.fraunhofer.de/.../rspbry/755003377
13 </aas:key>
14 </aas:keys>
15 </aas:assetRef>
16 ...
17 </aas:assetAdministrationShell>
18 </aas:assetAdministrationShells>
19 </aas:aasenv>
Listing 1.1. XML serialization of the Raspberry Pi AAS.
requirement can be further aligned with the Linked Data Principles if URIs are
alsoenforcedtopointtoactualresources.However,dereferencableURIsarenot
a requirement for now but should be seen as a preferable best practice.
The asset objects (A) constitute the link from the AAS to the real-world
thing. As assets themselves only contain a very brief description, only the class
assertions(rdf:type),thename(rdfs:label),descriptions(rdfs:comment)andthe
kind attribute are translated to A .
RDF
Submodels (S) and SubmodelElements are the core information carrier of
the Asset Administration Shell. The basic structure of the submodel serves as a
bracketforseveralSubmodelElements.AbstractSubmodelElementscanbereal-
ized by Operations, ReferenceElements, Files, binary objects (Blob) and Prop-
erties. Properties have further attributes such as a key, value, value type and
several others. In order to align the Property class with the graph model of
RDF, each instance is transformed to a respective rdf:Property. Therefore, a
distinct class ‘Property’ does not exist in SAAS. The alternative usage of n-
ary relations, which would further allow the linking of more attributes to the
relation, was discarded in order to sustain cleaner graphs. Consequently, not all
Property objects can be translated to the SAAS model.3
Mainly, attributes and properties are converted to triples and identifiers are
restricted to URIs. Therefore, all identifiers of attributes become globally valid,
as URIs are globally valid. It has been deliberately decided against n-ary con-
structs with blank nodes and an explicit property class, which would have been
closer to the XML and JSON influenced data model. The reason is that an
3 Examples can be found at https://github.com/i40-Tools/RAMIOntology/tree/
master/AssetAdministrationShell examples.

---
### Page 9

The Semantic Asset Administration Shell 167
1 _:AssetShellMap a rr:TriplesMap ;
2 ...
3 rr:subjectMap [
4 rml:reference "identification" ;
5 rr:class rami:AdminShell ] ;
6 rr:predicateObjectMap [
7 rr:predicateMap [ rr:constant rdfs:label ] ;
8 rr:objectMap [
9 rml:reference "idShort" ;
10 rr:termType rr:Literal ;
11 rr:datatype xsd:string ]
12 ] ; ...
Listing 1.2. Example RML TriplesMap excerpt.
1 <http://iais.fraunhofer.de/en/aas/examples/raspberry_pi_3b_plus> a rami:AssetShell;
2 rdfs:label "RaspberryPiModel3B+";
3 rami:hasAsset "http://iais.fraunhofer.de/en/aas/devices/rspbry/755003377"; ...
Listing 1.3. Equivalent representation to Listing 1.1 as RDF/Turtle.
therebycreatedgraphincreasesincomplexitywhileitscomprehensibilitysignif-
icantly decreases and the information content stays the same.4
Conceptdescriptionobjects(CD)serveaslocaldictionariesforusedentities.
Astheproliferationofdefinitionsandmetadatadirectlywiththeproductivedata
eases its interpretation, Concept Descriptions increase the degree of interoper-
ability between AAS providing and consuming components. RDF and Linked
Data however propagate the usage of dereferencing URIs in order to retrieve
metadata. In that sense, Linked Data conventions can reduce the amount of
transmitted data. On the other hand, not all relevant Industrie 4.0 components
are able to actively request such metadata. The possibility to independently
open outgoing interactions beyond the restricted shop floor network is usually
also a security risk and is not a good practice. Therefore, Concept Descriptions
are a valuable feature to ship metadata and to ensure a common understanding
on the shipped AAS. The mapping itself is provided as RML TripleMaps (see
Listing1.2) and can be executed with the open-source tool RMLMapper5.
6 Reasoning
RDFandRDFSalreadycontaintrivialentailmentrulesets6.AsRDFandRDFS
are very general vocabularies, the allowed reasoning focuses on the syntactic
position(subject,predicate,object)ofentitiesinRDFgraphs.Forinstance,the
information that p is an instance of the class Property can be inferred from
the fact that a triple with p at the predicate position exists. Although rule
4 Full example: https://github.com/i40-Tools/RAMIOntology/tree/master/rml
mapping/mapping examples.
5 Accessible at https://github.com/RMLio/rmlmapper-java.
6 https://www.w3.org/TR/rdf11-mt/.

---
### Page 10

168 S. R. Bader and M. Maleshkova
entailments of this kind are certainly correct, the created amount of explicit
data increasessignificantly while theinformation content stays nearlythesame.
In order to illustrate the power of reasoning based on the SAAS, selected
rule sets using owl:sameAs and rdfs:subClassOf properties have been prepared.
The rules are encoded in N3 according to Stadtmu ̈ller et al. in order to use
theirLinkedDataIntegrationandReasoningEngine[10].Inadditiontothetwo
entailment regimes, both consisting of several single rules7, the SAAS ontology
with its inherent axioms is integrated onthefly.Section9.3 presentstheresults.
7 Schema Validation
The AAS presents a closed-world model. As such, the definitions of classes and
propertiesmustberegardedasrestrictionsandsimplyreusingproperties,which
were introduced for class A, for class B usually causes a violation of the model.
RDF on the other hand does by default allow all not excluded patterns. Nev-
ertheless, industrial use cases require verifiable statements on the data content
but also its structure.
The Shapes Constraint Language (SHACL) [9] introduces a W3C recom-
mendationforvalidationmechanismsonRDFgraphs.Thedefinitionofrequired
attributes, cardinality of relations or datatype restrictions in the form of shapes
is an important aspect to enable data quality assurance in any productive sys-
tem. Some tools are already created to assist the creation of SHACL shapes,
e.g. a Prot ́eg ́e plugin and as a part of TopBraid Composer. As SHACL shapes
are also defined in RDF, they share the same format as the validated data in
contrast to e.g. plain SPARQL Rules. This eases the required technology stack
and reduces the amount of used libraries.
TheSAASsuppliesrespectiveshapesforallitsclasses8.Theseshapesmainly
check for mandatory properties but also check the existence of label and com-
ment annotations. In addition, the shapes are essential in order to check the
incoming data during the exchange of Asset Administration Shells. Further-
more, the shapes can also be used to describe input and output specifications.
For instance, an Industrie 4.0 component can postulate that its API requires
data objects conforming to the Asset Shape and will output Submodel objects
as defined by the Submodel Shape.
8 Use Cases
WeusethreedifferentAssetAdministration Shellsinordertoevaluateourapp-
roach.Allofthemarereflectingthespecificationsfrom[1]andareintheAASX
file format. The corresponding descriptions are included in XML files contained
in the AASX files.
7 rdfs9andrdfs11from[7],transitivity,symmetryandreplaceabilitycharacteristicfor
owl:sameAs.
8 https://github.com/i40-Tools/RAMIOntology/tree/master/schema.

---
### Page 11

The Semantic Asset Administration Shell 169
Raspberry Pi. The first Asset Administration Shell represents a Raspberry
Pi 3B+ (see Listing1.1). Three Submodels are included, namely one for the
technical characteristics, one containing documentation material as the product
sheet and a usage manual, as well as one submodel explaining the asset itself.
Here, the asset is one specific Raspberry Pi (kind=instance) and not referring
to the type of product of all Raspberry Pis, which have been produced or will
ever be produced (kind=type). Therefore, the description is only valid for one
and only one Raspberry Pi. The AAS delivers 52 SubmodelElements.
Automation Controller. AAS2 describes an electronic controller for automa-
tionfacilities.Asitisnotapprovedasanofficialartifact,theprovidingcompany
aswellasitsdetailscanunfortunatelynotbepublished.AAS2containsoneasset,
three submodels and more than 100 SubmodelElements.
Multi-protocol Controller.Thethirdusecase(AAS3)representsaninternet-
capable controller unit with multiple protocol support. Like AAS2, this Asset
AdministrationShellisnotofficiallypublishedyet.However,noneoftheauthors
of this paper was involved in the creation of either AAS2 or AAS3. The third
use case includes one Asset with eight Submodels and more than 150 Submod-
elElements.
9 Experimental Evaluation
We evaluate the AAS to SAAS mapping by examining the results and the per-
formance of the three use cases (see Table1). As a reference to estimate the
information coverage, the number of XML nodes of the AAS serializations are
provided. In addition, the amount of unique leaves of the three XML trees are
noted,asthesenumbersbetterreflectthesingleinformationcontentoftheAAS.
Table1 also presents the numbers of generated triples by the RMLMapper. The
comparison indicates, as already mentioned, that not the whole expressiveness
of AAS can be transported to the SAAS version. This is due to the fact that
some constructs can not being represented sufficiently in RDF (for instance the
Property class) but also many original entities contain redundant information.
EspeciallytheConceptDescriptions repeatmanyattributes,whicharecollapsed
by the mapping process and only added once.
Table 1. Results of the SAAS mapping and RDF serialization.
#XMLLeaves/ AAS #Triples SAAS SAAS SAAS SAAS
#XMLNodes (XML) (XML) (nquad) (turtle) (JSON-LD)
RaspberryPi 1161/2864 148KB 510 40KB 86KB 32KB 51KB
AAS2 925/2604 91KB 459 17KB 58KB 12KB 20KB
AAS3 2651/6743 313KB 1154 43KB 156KB 31KB 52KB

[TABLE]
#XMLLeaves/
#XMLNodes | AAS
(XML) | #Triples | SAAS
(XML) | SAAS
(nquad) | SAAS
(turtle)
1161/2864 | 148KB | 510 | 40KB | 86KB | 32KB
925/2604 | 91KB | 459 | 17KB | 58KB | 12KB
2651/6743 | 313KB | 1154 | 43KB | 156KB | 31KB
[/TABLE]

---
### Page 12

170 S. R. Bader and M. Maleshkova
9.1 Mapping Time
Thenecessaryoverheadintermsofcomputationtimemeasuredinmillisecondsis
presentedinFig.4,inadditiontotheaveragemappingtimesoutlinedinthelast
column of Table1. The time was measured on a regular laptop (Win10, 16GB,
Inteli5-73002,60GHz)usingabashemulation.ThedifferentRDFserializations
doinfluencetheexecutiontime,indicatingthatthewritingisnotthebottleneck.
While the average mapping time of the Raspberry Pi AAS (2,7s) and AAS2
(3,1s) are rather close, the duration for AAS3 (5,7s) is significantly higher. The
variationbetweentheselectedusecasesreflectsthedifferencesintheirXMLfile
size.Thiscouldindicatethattheoverallbehaviorisnearlylinear.However,each
of the 19 TripleMaps leads to a reloading and reiteration of the whole XML file.
Overcoming this expensive process would speed up the process significantly but
is out of the scope for this paper.
Fig.4. Mapping times for the three Asset Administration Shells.
9.2 Data Overhead
RDFisingeneralnotaneffectivedataformatintermsofstorageefficiency.Nev-
ertheless, the syntax requirements of the AAS and especially its XML schema
create already significant overhead for the original AAS model. As depicted in
Table1,allRDFserializationsreducethenecessarystoragesize.Especiallynote-
worthy is the difference between the original XML file size and the RDF/XML
serialization. This is mostly due to the usage of namespaces in the RDF/XML
version,whichreducesthenotedURIs.Itshouldbementionedthatforallserial-
izations the mapping step (m) and the serialization (ser) were executed directly
by the mapping engine.
Nevertheless,theresultingcostsintermsofstoragerequirementsandcommu-
nicationbandwidthdonotexceedtheonescreatedbytheoriginalAssetAdmin-
istrationShells.Consequently,alldevicesandscenarioscapableofhandlingAAS
are also sufficient for the operation of SAAS. Furthermore, the possible serial-
ization of SAAS as both XML and JSON should enable AAS implementations
to quickly adapt to SAAS objects in their original file format.

---
### Page 13

The Semantic Asset Administration Shell 171
Table 2. Added triples by the different rule sets.
Triples sameAs sameAs subClassOf subClassOf both both
(original) (triples) (time) (triples) (time) (triples) (time)
RaspberryPi 510 959 2,760ms 771 2,719ms 1,217 2,808ms
AAS2 459 452 3,057ms 367 2,368ms 570 2,313ms
AAS3 1154 1,115 2,776ms 818 2,677ms 1,343 2,668ms
9.3 Reasoning
Three different rule sets have been applied to all use cases. All rule sets contain
a web request to the ontology source file in order to load the class hierarchy
and any other relevant axioms of the data model itself. The first one also adds
several rules reflecting the symmetry and transitivity of owl:sameAs as well as
the fact that same instances share all properties and annotations of each other.
The second rule set contains subclass statements as encoded by the rules rdfs9
and rdfs11 [7]. The third set combines both to the most expressive reasoning
set. Table2 gives an overview of the amount of created triples. rdfs:subClassOf,
owl:sameAs andthecombinationofbothentailmentsareshownwiththeamount
of uniquely added triples and the average reasoning time.
We use the Linked Data-Fu engine [10]. The preparation of the reasoning
engine, involving the parsing of the rule files, takes around 1s. The following
web request, the download of the ontology, the evaluation of the rules and the
serialization to a n-triple file is then executed. The duration distribution of ten
repetitions is shown in Fig.5. One can see that the whole process takes between
2,3and3,3s,nearlyindependentlyoftheamountofinputs(AAS3issignificantly
larger than the graph for the Raspberry Pi) and the expressiveness of the rule
sets (the second set is leading to way less results than the others).
As the rule sets are only regarding the structure of the ontology, the infer-
encing of context-dependent knowledge is not yet possible. In order to reach
productively usable information, domain-specific axioms tailored to the actu-
ally contained or expected data is necessary. However, we can show that the
reasoning process with complex rules is applicable in an acceptable amount of
time.
9.4 Schema Validation
The evaluation times of the SHACL shapes are shown in Fig.6. On average, the
execution of all shapes takes 46,2s and the execution of one single shape 1,8s.
All shapes have been executed a total of ten times.
About2sarerequiredforsettingupthevalidationtoolandparsingthedata
shape (the Asset Administration Shell) and the single class shape. The size of
theAssetAdministrationShellhasnosignificantimpactontheachievedresults.
Regarding these conditions, we claim that the necessary effort is acceptable for
a typical Industrie 4.0 scenario as the validation itself is not necessary for every
restricteddevices.Thisisduetothefactthatthevalidationofdatatakeseither

[TABLE]
Triples
(original) | sameAs
(triples) | sameAs
(time) | subClassOf
(triples) | subClassOf
(time) | both
(triples)
510 | 959 | 2,760ms | 771 | 2,719ms | 1,217
459 | 452 | 3,057ms | 367 | 2,368ms | 570
1154 | 1,115 | 2,776ms | 818 | 2,677ms | 1,343
[/TABLE]

---
### Page 14

172 S. R. Bader and M. Maleshkova
Fig.5. SAAS Reasoning duration. Fig.6. Schema validation performance.
placeatdevelopmentordeploymenttimewheretimeisnotcritical.Inaddition,
the validation is important for the higher-level data analytical services which
usually run on more powerful machines or are even hosted in the cloud.
10 Conclusion and Outlook
We presented a semantic version of the Administration Admin Shell, a mapping
from its XML serialization to any RDF serialization, schema validation shapes
and a brief set of reasoning rules. In that sense, we showed the lifting process of
the AAS data to a semantic integration layer.
This is one step to an automated integration of Industrie 4.0 components.
We showed how existing, non-customized tools can work with the RDF model
of the AAS and execute their task without prior configuration. This enables the
implementation of real interoperable pipelines and data-driven workflows, not
only on the data format and syntax level but also regarding the meaning of the
data. Furthermore, the examined overhead of the SAAS model and showed that
therequirementsdonotexceedtherequirementssetbytheoriginalAASmodel.
The mapping provided in this paper outlines the data lifting to the SAAS
RDF model. The lowering of RDF to the original AAS data model has not yet
been achieved. Furthermore, the main benefit of the semantic model is, besides
itsformalizedmeaning,theinterlinkingwithotherdefinitionsandtheintegration
of additional sources.
For now, only the data provisioning capabilities of the AAS are defined.
In the next step, the provisioning and invocation of operations through Asset
Administration Shells will be specified. Using semantically defined descriptions
oftherespectiveinterfaces,theirinputandoutputparametersandtheprovided
services will allow the Industrie 4.0 community to rely on the huge amount
of expertise and experience with Web Services and Semantic Web Services in
particular. This way, the goal of truly interoperable and flexible manufacturing
workflows,wheresoftwareandhardware,materialsandproducts,costumersand
suppliers form on demand information chains, benefits from the huge amount of
existing research in the area.

---
### Page 15

The Semantic Asset Administration Shell 173
Wewillfurtherextendourworkinordertokeepthesemanticmodelsaligned
withtheprogressoftheAssetShellspecification.Furthermore,weprovidefeed-
back and outline established best practices to the manufacturing community.
Furthermore,weseetwomainchallengeswhichmustbetackledbythesemantic
community. First, the core potential of the semantic web – the seamless inte-
grationofheterogeneousdevices,servicesanddatasources–stilllackssufficient
numbers of implemented use cases and deployed scenarios in practice. Second,
the reoccurring discussion on identifiers in distributed settings is a huge chance
fortheestablishedpracticesoftheSemanticWebandLinkedDatainparticular.
However, the benefits of (dereferencable) URIs are still underestimated in the
manufacturing community, mostly because of missing experiences.
References
1. Barnstedt, E., et al.: Details of the Asset Administration Shell. Technical Report
Part 1, Plattform Industrie 4.0 (2018). https://www.plattform-i40.de/PI40/
Redaktion/DE/Downloads/Publikation/2018-verwaltungsschale-im-detail.html
2. Das, S., Sundara, S., Cyganiak, R.: R2RML: RDB to RDF Mapping Language,
W3C Recommendation. World Wide Web Consortium (W3C), Cambridge, MA
(2012). www.w3.org/TR/r2rml
3. Diedrich,C.,etal.:Semanticinteroperabilityforassetcommunicationwithinsmart
factories.In:22ndInternationalConferenceonEmergingTechnologiesandFactory
Automation (ETFA), pp. 1–8. IEEE (2017)
4. Dimou, A., Vander Sande, M., Colpaert, P., Verborgh, R., Mannens, E., Van de
Walle,R.:RML:agenericlanguageforintegratedRDFmappingsofheterogeneous
data. In: LDOW (2014)
5. Grangel-Gonz ́alez,I.,Halilaj,L.,Auer,S.,Lohmann,S.,Lange,C.,Collarana,D.:
AnRDF-basedapproachforimplementingIndustry4.0ComponentswithAdmin-
istration Shells. In: 21st International Conference on Emerging Technologies and
Factory Automation (ETFA), pp. 1–8. IEEE (2016)
6. Grangel-Gonz ́alez, I., Halilaj, L., Coskun, G., Auer, S., Collarana, D., Hoffmeis-
ter, M.: Towards a semantic administrative shell for industry 4.0 components. In:
International Conference on Semantic Computing (ICSC), pp. 230–237 (2016)
7. Hayes, P.J., Patel-Schneider, P.F.: Rdf 1.1 Semantics. W3C Recommendation
(2014). https://www.w3.org/TR/rdf11-mt/
8. Katti,B.,Plociennik,C.,Ruskowski,M.,Schweitzer,M.:SA-OPC-UA:introducing
semantics to OPC-UA application methods. In: 14th International Conference on
Automation Science and Engineering (CASE), pp. 1189–1196. IEEE (2018)
9. Knublauch, H., Kontokostas, D.: Shapes Constraint Language (SHACL). W3C
Candidate Recommendation 11(8) (2017)
10. Stadtmu ̈ller, S., Speiser, S., Harth, A., Studer, R.: Data-fu: a language and an
interpreterforinteractionwithread/writelinkeddata.In:Proceedingsofthe22nd
International Conference on World Wide Web. ACM (2013)
11. Tantik,E.,Anderl,R.:Integrateddatamodelandstructurefortheassetadminis-
tration shell in industrie 4.0. Procedia CIRP 60, 86–91 (2017)

---
### Page 16

174 S. R. Bader and M. Maleshkova
Open Access This chapter is licensed under the terms of the Creative Commons
Attribution 4.0 International License (http://creativecommons.org/licenses/by/4.0/),
which permits use, sharing, adaptation, distribution and reproduction in any medium
or format, as long as you give appropriate credit to the original author(s) and the
source, provide a link to the Creative Commons license and indicate if changes were
made.
The images or other third party material in this chapter are included in the
chapter’s Creative Commons license, unless indicated otherwise in a credit line to the
material. If material is not included in the chapter’s Creative Commons license and
your intended use is not permitted by statutory regulation or exceeds the permitted
use, you will need to obtain permission directly from the copyright holder.

[TABLE]
 | 
 | 
[/TABLE]
