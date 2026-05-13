Question: What is the result of 10+20*23+3-11*18? Question: What is the result of 3+7*9+19-21*18?
Round 1 Agent 1: 269 ✗ Agent 2: 369 ✗ Agent 1: 378 ✗ Agent 2: -351 ✗ Agent 3: -357 ✗
Round 2 Agent 1: 275 ✓ Agent 2: 275 ✓ Agent 1: -293 ✓ Agent 2: -293 ✓ Agent 3: 19 ✗
Question: What is the result of 4+23*6+24-24*12? Question: What is the result of 8+14*15+20-3*26?
Round 1 Agent 1: -244 ✗ Agent 2: -146 ✗ Agent 1: 236 ✗ Agent 2: -214 ✗ Agent 3: 210 ✗
Round 2 Agent 1: -146 ✗ Agent 2: -122 ✓ Agent 1: 160 ✓ Agent 2: 160 ✓ Agent 3: 160 ✓
Round 3 Agent 1: -122 ✓ Agent 2: -122 ✓ Agent 1: 160 ✓ Agent 2: 160 ✓ Agent 3: 160 ✓
Figure4:IllustrationofSolvingMath.Reasoningbetweenagentsisomitted.
Question: Regina wrote 9 novels last year. If Question: Dennis uses 1 pound of butter for every dozen
this is 3 quarters of the number of novelsshe croissants that he makes. He needs to make 6 dozen croissants.
has written this year, how many novels has she The grocery store currently has a promotion for buy one pound
of butter get one half off. If the butter costs $4.00 a pound,
written this year?
how much will it cost him to purchase 6 pounds of butter?
Round 1 Agent 1: 48 ✗ Agent 2: 12 ✓ Agent 1: 18 ✓ Agent 2: 30 ✗
Round 2 Agent 1: 12 ✓ Agent 2: 12 ✓ Agent 1: 18 ✓ Agent 2: 18 ✓
Figure5:IllustrationofSolvingGradeSchoolMath.Reasoningbetweenagentsomitted.
• Arithmetic. Wefirstevaluatetheabilityofmodelstocorrectlyevaluateanarithmeticexpression
(containingaddition,multiplication,andsubtraction)consistingofsixdifferenttwo-digitnumbers.
Forexample: Whatistheresultof12+15*21+0-3*27?
• GSM8K.Next,weconsiderhardermathematicalreasoningtasks. UsingtheGSM8Kdataset[3],
themodelsmustcorrectlysolvegradeschoolmathematicalreasoningtasks.
• Chess Move Prediction. Finally,weconsiderthestrategicreasoningoftheabilityofmodels,
andaskmodelstopredictthebestnextmoveinagameofchess,giventhefirst14movesofachess
gamebetweentwochessgrand-mastersdescribedinPGNnotation[6].
WereporttheaccuracyoffinalanswersinarithmeticandGSM8Ktasksandreportthepawnscore
(advantage) of predicted moves, as estimated by Stockfish in the Chess move prediction tasks.
AdditionaldetailsmaybefoundintheAppendix.
ycaruccA
ksaT
K8MSG
Baselines. Wecompareourapproachtothreealter-
Single Agent Multi-Agent Debate
nativeapproachestogenerateresponsesforreasoning
90%
problems. First, we ask agents to directly generate
responses(singleagent). Next,weconsideraskinglan- 85%
guagemodelstogenerateandthen"self-reflect"onthe
80%
responsesgenerated[26,18]. Finally,weconsidergen-
eratingresponsesusingmultipleagentsandperforming 75%
majority voting [15, 3]. As the focus of our experi-
70%
mentsistoverifytheeffectivenessofmultiagentagent No Chain of With Chain of
debate,werunbothbaselinesandourapproach,using Thought Thought
theidenticalstartingpromptandlanguagemodelacross Figure6: SynergywithOtherMethods. Per-
allevaluations. Weevaluatemodelsinazero-shotset- formanceofdebateincreaseswithuseofChain
ting,withpromptsfoundintheAppendixofthepaper. ofThoughtprompting.
WeusechatGPT-basedlanguagemodel [21]inallourexperimentsexceptthoseinFigure11where
wecomparemultiplelanguagemodels.
Due to computational expense, we evaluate our approach across benchmarks mainly using three
agentswithtworoundsofdebates,althoughwefoundfurthergainswithbothmoreagentsandrounds
ofdebate(Figure10). AdditionalevaluationdetailsarefoundintheAppendix.
QuantitativeResults. InTable1,wereporttheresultsofeachapproachonarithmetic,gradeschool
math,andchessreasoningtask. Ineachtask,weobservethatutilizingmultipledifferentagentsto
generatesolutionsimprovesperformanceoverusingasinglelanguagemodelagenttogeneratea
solution. Simultaneously,wealsoseethatreflection,wherealanguagemodelisaskedtocritique
itsearlygeneration,generallygivesamodestboostinperformance. Multiagentdebate,whichmay
beseenasacombinationofbothreflectionandmultiagentgeneration,givesasubstantialboostin
reasoningacrosseachofthetasks.
5
Question: What is the result of 10+20*23+3-11*18? Question: What is the result of 3+7*9+19-21*18?
Round 1 Agent 1: 269 ✗ Agent 2: 369 ✗ Agent 1: 378 ✗ Agent 2: -351 ✗ Agent 3: -357 ✗
Round 2 Agent 1: 275 ✓ Agent 2: 275 ✓ Agent 1: -293 ✓ Agent 2: -293 ✓ Agent 3: 19 ✗
Question: What is the result of 4+23*6+24-24*12? Question: What is the result of 8+14*15+20-3*26?
Round 1 Agent 1: -244 ✗ Agent 2: -146 ✗ Agent 1: 236 ✗ Agent 2: -214 ✗ Agent 3: 210 ✗
Round 2 Agent 1: -146 ✗ Agent 2: -122 ✓ Agent 1: 160 ✓ Agent 2: 160 ✓ Agent 3: 160 ✓
Round 3 Agent 1: -122 ✓ Agent 2: -122 ✓ Agent 1: 160 ✓ Agent 2: 160 ✓ Agent 3: 160 ✓ | 
 | Agent 3: 210 ✗
 | Agent 3: 160 ✓
 | Agent 3: 160 ✓

Agent 1: 269 ✗
Agent 1: 275 ✓

Agent 2: 369 ✗
Agent 2: 275 ✓

Agent 1: 378 ✗
Agent 1: -293 ✓

Agent 2: -351 ✗
Agent 2: -293 ✓

Agent 3: -357 ✗
Agent 3: 19 ✗

Agent 1: -244 ✗
Agent 1: -146 ✗
Agent 1: -122 ✓

Agent 2: -146 ✗
Agent 2: -122 ✓
Agent 2: -122 ✓

Agent 1: 236 ✗
Agent 1: 160 ✓
Agent 1: 160 ✓

Agent 2: -214 ✗
Agent 2: 160 ✓
Agent 2: 160 ✓

Agent 1: 48 ✗
Agent 1: 12 ✓

Agent 2: 12 ✓
Agent 2: 12 ✓

Agent 1: 18 ✓
Agent 1: 18 ✓

 |  |  |  | 
 |  |  |  | 
 |  |  |  | 
 |  |  |  | 

