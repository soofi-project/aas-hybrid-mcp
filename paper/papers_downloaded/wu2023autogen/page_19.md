D ApplicationDetails
A1: MathProblemSolving
Scenario 1: Autonomous Problem Solving. We perform both qualitative and quantitative eval-
uations in this scenario. For all evaluations, we use GPT-4 as the base model, and pre-install the
“sympy” package in the execution environment. We compare AutoGen with the following LLM-
basedagentsystems:
• AutoGPT: The out-of-box AutoGPT is used. We initialize AutoGPT by setting the purpose to
“solvemathproblems”,resultingina“MathSolverGPT”withauto-generatedgoals.
• ChatGPT+Plugin: WeenabletheWolframAlphaplugin(amathcomputationengine)intheOpe-
nAIwebclient.
• ChatGPT+Code Interpreter: This is a recent feature in OpenAI web client. Note that the above
twopremiumfeaturesfromChatGPTrequireapaidsubscriptiontobeaccessedandarethemost
competitivecommercialsystems.
• LangChainReAct+Python: WeusePythonagentfromLangChain. Tohandleparsingerrors,we
set“handle parsing errors=True”,andusethedefaultzero-shotReActprompt.
• Multi-AgentDebate(Liangetal.,2023): Wemodifiedthecodeofthemulti-agentdebatetoper-
formevaluation. Bydefault,therearethreeagents: anaffirmativeagent,anegativeagent,anda
moderator.
We also conducted preliminary evaluations on several other multi-agent systems, including
BabyAGI,CAMEL,andMetaGPT.Theresultsindicatethattheyarenotsuitablechoicesforsolving
mathproblemsoutofthebox. Forinstance,whenMetaGPTistaskedwithsolvingamathproblem,
itbeginsdevelopingsoftwaretoaddresstheproblem,butmostofthetime,itdoesnotactuallysolve
theproblem. WehaveincludedthetestexamplesinAppendixE.
Table2:QualitativeevaluationoftwomathproblemsfromtheMATHdatasetwithintheautonomous
problem-solvingscenario. EachLLM-basedsystemistestedthreetimesoneachoftheproblems.
Thistablereportstheproblem-solvingcorrectnessandsummarizesthereasonsforfailure.
Correctness FailureReason
AutoGen 3/3 N/A.
AutoGPT 0/3 TheLLMgivescodewithouttheprintfunctionsothe
resultisnotprinted.
ChatGPT+Plugin 1/3 ThereturnfromWolframAlphacontains2simplified
results,includingthecorrectanswer,butGPT-4always
choosesthewronganswer.
ChatGPT+CodeInterpreter 2/3 Returnsawrongdecimalresult.
LangChainReAct 0/3 LangChaingives3differentwronganswers.
Multi-AgentDebate 0/3 Itgives3differentwronganswersduetocalculationerrors.
(a)Evaluationonthefirstproblemthataskstosimplifyasquarerootfraction.
Correctness FailureReason
AutoGen 2/3 Thefinalanswerfromcodeexecutioniswrong.
AutoGPT 0/3 TheLLMgivescodewithouttheprintfunctionsothe
resultisnotprinted.
ChatGPT+Plugin 1/3 Foronetrial,GPT-4gotstuckbecauseitkeepsgiving
wrongqueriesandhastobestopped.Anothertrialsimply
givesawronganswer.
ChatGPT+CodeInterpreter 0/3 Itgives3differentwronganswers.
LangChainReAct 0/3 LangChaingives3differentwronganswers.
Multi-AgentDebate 0/3 Itgives3differentwronganswers.
(b)Evaluationonthesecondnumbertheoryproblem.
Forthequalitativeevaluation,weutilizetwolevel-5problemsfromtheMATHdataset,testingeach
problemthreetimes. Thefirstprobleminvolvessimplifyingasquarerootfraction,andthesecond
19
Correctness
3/3
0/3
1/3
2/3
0/3
0/3

Correctness
2/3
0/3
1/3
0/3
0/3
0/3

