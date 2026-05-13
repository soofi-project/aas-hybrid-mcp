B ExpandedDiscussion
TheapplicationsinSection3showhowAutoGennotonlyenablesnewapplicationsbutalsohelps
renovate existing ones. For example, in A1 (scenario 3), A5, and A6, AutoGen enabled the cre-
ationofmulti-agentconversationsthatfollowadynamicpatterninsteadofafixedback-and-forth.
And in both A5 and A6, humans can participate in the activities together with multiple other AI
agents in a conversational manner. Similarly, A1-A4 show how popular applications can be reno-
vated quickly with AutoGen. Despite the complexity of these applications (most of them involve
more than two agents or dynamic multi-turn agent cooperation), our AutoGen-based implementa-
tionremainssimple,demonstratingpromisingopportunitiestobuildcreativeapplicationsandalarge
spaceforinnovation. Inreflectingonwhythesebenefitscanbeachievedintheseapplicationswith
AutoGen,webelievethereareafewreasons:
• Easeofuse: Thebuilt-inagentscanbeusedout-of-the-box,deliveringstrongperformanceeven
withoutanycustomization. (A1,A3)
• Modularity: Thedivisionoftasksintoseparateagentspromotesmodularityinthesystem. Each
agent can be developed, tested, and maintained independently, simplifying the overall develop-
mentprocessandfacilitatingcodemanagement. (A3,A4,A5,andA6)
• Programmability:AutoGenallowsuserstoextend/customizeexistingagentstodevelopsystems
satisfyingtheirspecificneedswithease.(A1-A6).Forexample,withAutoGen,thecoreworkflow
codeinA4isreducedfromover430linesto100lines,fora4xsaving.
• Allowinghumaninvolvement: AutoGenprovidesanativemechanismtoachievehumanpartici-
pationand/orhumanoversight. WithAutoGen,humanscanseamlesslyandoptionallycooperate
withAIstosolveproblemsorgenerallyparticipateintheactivity. AutoGenalsofacilitatesinter-
activeuserinstructionstoensuretheprocessstaysonthedesiredpath. (A1,A2,A5,andA6)
• Collaborative/adversarial agent interactions: Like many collaborative agent systems (Dong
etal.,2023),agentsinAutoGencanshareinformationandknowledge,tocomplementeachother’s
abilitiesandcollectivelyarriveatbettersolutions. (A1,A2,A3,andA4). Analogously,incertain
scenarios,someagentsarerequiredtoworkinanadversarialway. Relevantinformationisshared
amongdifferentconversationsinacontrolledmanner,preventingdistractionorhallucination.(A4,
A6). AutoGensupportsbothpatterns,enablingeffectiveutilizationandaugmentationofLLMs.
B.1 GeneralGuidelinesforUsingAutoGen
BelowwegivesomerecommendationsforusingagentsinAutoGentoaccomplishatask.
1. Consider using built-in agents first. For example, AssistantAgent is pre-configured to be
backed by GPT-4, with a carefully designed system message for generic problem-solving via
code. The UserProxyAgent is configured to solicit human inputs and perform tool execution.
Manyproblemscanbesolvedbysimplycombiningthesetwoagents. Whencustomizingagents
foranapplication,considerthefollowingoptions: (1)humaninputmode,terminationcondition,
code execution configuration, and LLM configuration can be specified when constructing an
agent;(2)AutoGensupportsaddinginstructionsinaninitialusermessage,whichisaneffective
waytoboostperformancewithoutneedingtomodifythesystemmessage;(3)UserProxyAgent
canbeextendedtohandledifferentexecutionenvironmentsandexceptions, etc.; (4)whensys-
tem message modification is needed, consider leveraging the LLM’s capability to program its
conversationflowwithnaturallanguage.
2. Startwithasimpleconversationtopology.Considerusingthetwo-agentchatorthegroupchat
setup first, as they can often be extended with the least code. Note that the two-agent chat can
be easily extended to involve more than two agents by using LLM-consumable functions in a
dynamicway.
3. Try to reuse built-in reply methods based on LLM, tool, or human before implementing a
custom reply method because they can often be reused to achieve the goal in a simple way
(e.g.,thebuilt-inagentGroupChatManager’sreplymethodreusesthebuilt-inLLM-basedreply
functionwhenselectingthenextspeaker,ref. A5inSection3).
4. When developing a new application with UserProxyAgent, start with humans always in
the loop, i.e., human input mode=‘ALWAYS’, even if the target operation mode is more au-
tonomous. This helps evaluate the effectiveness of AssistantAgent, tuning the prompt, dis-
coveringcornercases,anddebugging. Onceconfidentwithsmall-scalesuccess,considersetting
16
