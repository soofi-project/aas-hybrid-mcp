• MetaGPT:MetaGPT(Hongetal.,2023)isaspecializedLLMapplicationbasedonamulti-agent
conversationframeworkforautomaticsoftwaredevelopment. TheyassigndifferentrolestoGPTs
tocollaborativelydevelopsoftware. TheydifferfromAutoGenbybeingspecializedsolutionsto
acertainscenario,whileAutoGenisagenericinfrastructuretofacilitatebuildingapplicationsfor
variousscenarios.
Thereareafewotherspecializedsingle-agentormulti-agentsystems,suchasVoyager(Wangetal.,
2023a)andGenerativeAgents(Parketal.,2023),whichweskipduetolowerrelevance. InTable1,
wesummarizedifferencesbetweenAutoGenandthemostrelevantmulti-agentsystems.
Table1: SummaryofdifferencesbetweenAutoGenandotherrelatedmulti-agentsystems. infras-
tructure: whetherthesystemisdesignedasagenericinfrastructureforbuildingLLMapplications.
conversation pattern: the types of patterns supported by the implemented systems. Under the
‘static’pattern, agenttopologyremainsunchangedregardlessofdifferentinputs. AutoGenallows
flexible conversation patterns, including both static and dynamic patterns that can be customized
based on different application needs. execution-capable: whether the system can execute LLM-
generated code; human involvement: whether (and how) the system allows human participation
duringtheexecutionprocessofthesystem. AutoGenallowsflexiblehumaninvolvementinmulti-
agentconversationwiththeoptionforhumanstoskipprovidinginputs.
Aspect AutoGen Multi-agentDebate CAMEL BabyAGI MetaGPT
Infrastructure ✓ ✗ ✓ ✗ ✗
Conversationpattern flexible static static static static
Execution-capable ✓ ✗ ✗ ✗ ✓
Humaninvolvement chat/skip ✗ ✗ ✗ ✗
15
