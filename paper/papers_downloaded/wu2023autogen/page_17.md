human input mode = ‘NEVER’. This enables LLM as a backend, and one can either use the
LLMormanuallygeneratediversesystemmessagestosimulatedifferentusecases.
5. DespitethenumerousadvantagesofAutoGenagents,therecouldbecases/scenarioswhereother
libraries/packagescouldhelp. Forexample: (1)For(sub)tasksthatdonothaverequirements
forback-and-forthtrouble-shooting,multi-agentinteraction,etc.,aunidirectional(noback-and-
forthmessageexchange)pipelinecanalsobeorchestratedwithLangChain(LangChain,2023),
LlamaIndex(Liu,2022),Guidance(Guidance,2023),SemanticKernel(Semantic-Kernel,2023),
Gorilla(Patiletal.,2023)orlow-levelinferenceAPI(‘autogen.oai’providesanenhancedLLM
inference layer at this level) (Dibia, 2023). (2) When existing tools from LangChain etc. are
helpful,onecanusethemastoolbackendsforAutoGenagents.Forexample,onecanreadilyuse
tools,e.g.,WolframAlpha,fromLangChaininAutoGenagent.(3)Forspecificapplications,one
maywanttoleverageagentsimplementedinotherlibraries/packages. Toachievethis,onecould
wrapthoseagentsasconversableagentsinAutoGenandthenusethemtobuildLLMapplications
through multi-agent conversation. (4) It can be hard to find an optimal operating point among
manytunablechoices,suchastheLLMinferenceconfiguration.Blackboxoptimizationpackages
like‘flaml.tune’(Wangetal.,2021)canbeusedtogetherwithAutoGentoautomatesuchtuning.
B.2 FutureWork
Thisworkraisesmanyresearchquestionsandfuturedirectionsand.
Designingoptimalmulti-agentworkflows: Creatingamulti-agentworkflowforagiventaskcan
involve many decisions, e.g., how many agents to include, how to assign agent roles and agent
capabilities, how the agents should interact with each other, and whether to automate a particular
partoftheworkflow. Theremaynotexistaone-fits-allanswer,andthebestsolutionmightdepend
onthespecificapplication.Thisraisesimportantquestions:Forwhattypesoftasksandapplications
aremulti-agentworkflowsmostuseful? Howdomultipleagentshelpindifferentapplications? For
agiventask,whatistheoptimal(e.g.,cost-effective)multi-agentworkflow?
Creating highly capable agents: AutoGen can enable the development of highly capable agents
thatleveragethestrengthsofLLMs,tools,andhumans. Creatingsuchagentsiscrucialtoensuring
thatamulti-agentworkflowcaneffectivelytroubleshootandmakeprogressonatask. Forexample,
weobservedthatCAMEL,anothermulti-agentLLMsystem, cannoteffectivelysolveproblemsin
mostcasesprimarilybecauseitlacksthecapabilitytoexecutetoolsorcode. Thisfailureshowsthat
LLMs and multi-agent conversations with simple role playing are insufficient, and highly capable
agentswithdiverseskillsetsareessential. Webelievethatmoresystematicworkwillberequiredto
developguidelinesforapplication-specificagents,tocreatealargeOSSknowledgebaseofagents,
andtocreateagentsthatcandiscoverandupgradetheirskills(Caietal.,2023).
Enablingscale,safety,andhumanagency: Section3showshowcomplexmulti-agentworkflows
canenablenewapplications, andfutureworkwillbeneededtoassesswhetherscalingfurthercan
help solve extremely complex tasks. However, as these workflows scale and grow more complex,
it may become difficult to log and adjust them. Thus, it will become essential to develop clear
mechanismsandtoolstotrackanddebugtheirbehavior. Otherwise,thesetechniquesriskresulting
inincomprehensible,unintelligiblechatteramongagents(Lewisetal.,2017).
Ourworkalsoshowshowcomplex,fullyautonomousworkflowswithAutoGencanbeuseful,but
fullyautonomousagentconversationswillneedtobeusedwithcare. Whiletheautonomousmode
AutoGen supports could be desirable in many scenarios, a high level of autonomy can also pose
potentialrisks,especiallyinhigh-riskapplications(Amodeietal.,2016;Weld&Etzioni,1994). As
a result, building fail-safes against cascading failures and exploitation, mitigating reward hacking,
outofcontrolandundesiredbehaviors,maintainingeffectivehumanoversightofapplicationsbuilt
with AutoGen agents will become important. While AutoGen provides convenient and seamless
involvementofhumansthroughauserproxyagent,developersandstakeholdersstillneedtounder-
standanddeterminetheappropriatelevelandpatternofhumaninvolvementtoensurethesafeand
ethicaluseofthetechnology(Horvitz,1999;Amershietal.,2019).
17
