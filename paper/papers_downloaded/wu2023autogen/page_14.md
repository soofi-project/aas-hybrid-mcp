A RelatedWork
WeexamineexistingLLM-basedagentsystemsorframeworksthatcanbeusedtobuildLLMappli-
cations. Wecategorizetherelatedworkintosingle-agentandmulti-agentsystemsandspecifically
provideasummaryofdifferentiatorscomparingAutoGenwithexistingmulti-agentsystemsinTa-
ble 1. Note that many of these systems are evolving open-source projects, so the remarks and
statementsaboutthemmayonlybeaccurateasofthetimeofwriting. Wereferinterestedreadersto
detailedLLM-basedagentsurveys (Xietal.,2023;Wangetal.,2023b)
Single-AgentSystems:
• AutoGPT: AutoGPT is an open-source implementation of an AI agent that attempts to au-
tonomouslyachieveagivengoal(AutoGPT,2023). Itfollowsasingle-agentparadigminwhich
itaugmentstheAImodelwithmanyusefultools,anddoesnotsupportmulti-agentcollaboration.
• ChatGPT+(withcodeinterpreterorplugin): ChatGPT,aconversationalAIserviceoragent,
can now be used alongside a code interpreter or plugin (currently available only under the pre-
miumsubscriptionplanChatGPTPlus)(OpenAI,2023). ThecodeinterpreterenablesChatGPT
toexecutecode,whilethepluginenhancesChatGPTwithawiderangeofcuratedtools.
• LangChain Agents: LangChain is a general framework for developing LLM-based applica-
tions (LangChain, 2023). LangChain Agents is a subpackage for using an LLM to choose a
sequenceofactions.TherearevarioustypesofagentsinLangChainAgents,withtheReActagent
beinganotableexamplethatcombinesreasoningandactingwhenusingLLMs(mainlydesigned
for LLMs prior to ChatGPT) (Yao et al., 2022). All agents provided in LangChain Agents fol-
lowasingle-agentparadigmandarenotinherentlydesignedforcommunicativeandcollaborative
modes. Asignificantsummaryofitslimitationscanbefoundin(Woolf,2023). Duetotheselim-
itations,eventhemulti-agentsystemsinLangChain(e.g.,re-implementationofCAMEL)arenot
based on LangChain Agents but are implemented from scratch. Their connection to LangChain
liesintheuseofbasicorchestrationmodulesprovidedbyLangChain,suchasAImodelswrapped
byLangChainandthecorrespondinginterface.
• Transformers Agent: Transformers Agent (HuggingFace, 2023) is an experimental natural-
languageAPIbuiltonthetransformersrepository. Itincludesasetofcuratedtoolsandanagent
to interpret natural language and use these tools. Similar to AutoGPT, it follows a single-agent
paradigmanddoesnotsupportagentcollaboration.
AutoGendiffersfromthesingle-agentsystemsabovebysupportingmulti-agentLLMapplications.
Multi-AgentSystems:
• BabyAGI:BabyAGI(BabyAGI,2023)isanexampleimplementationofanAI-poweredtaskman-
agement system in a Python script. In this implemented system, multiple LLM-based agents
are used. For example, there is an agent for creating new tasks based on the objective and the
result of the previous task, an agent for prioritizing the task list, and an agent for completing
tasks/sub-tasks. As a multi-agent system, BabyAGI adopts a static agent conversation pattern,
i.e.,apredefinedorderofagentcommunication,whileAutoGensupportsbothstaticanddynamic
conversationpatternsandadditionallysupportstoolusageandhumaninvolvement.
• CAMEL: CAMEL (Li et al., 2023b) is a communicative agent framework. It demonstrates
how role playing can be used to let chat agents communicate with each other for task comple-
tion. Italsorecordsagentconversationsforbehavioranalysisandcapabilityunderstanding. An
Inception-promptingtechniqueisusedtoachieveautonomouscooperationbetweenagents. Un-
likeAutoGen,CAMELdoesnotnativelysupporttoolusage,suchascodeexecution. Althoughit
isproposedasaninfrastructureformulti-agentconversation,itonlysupportsstaticconversation
patterns,whileAutoGenadditionallysupportsdynamicconversationpatterns.
• Multi-AgentDebate: Tworecentworksinvestigateandshowthatmulti-agentdebateisaneffec-
tivewaytoencouragedivergentthinkinginLLMs(Liangetal.,2023)andtoimprovethefactuality
and reasoning of LLMs (Du et al., 2023). In both works, multiple LLM inference instances are
constructedasmultipleagentstosolveproblemswithagentdebate. EachagentissimplyanLLM
inference instance, while no tool or human is involved, and the inter-agent conversation needs
to follow a pre-defined order. These works attempt to build LLM applications with multi-agent
conversation, while AutoGen, designed as a generic infrastructure, can be used to facilitate this
developmentandenablemoreapplicationswithdynamicconversationpatterns.
14
