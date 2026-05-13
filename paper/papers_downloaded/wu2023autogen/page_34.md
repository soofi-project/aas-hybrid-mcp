E Exampleoutputsfromapplications
Inthissection,weincludeexampleoutputsfromthefollowingapplicationsandsystems:
• ApplicationA1: autonomoussolvingprocessofoneproblemwith: ChatGPT+Plugin(Table8),
AutoGen(Table9),LangChainReAct(Table10),AutoGPT(Table11),Multi-AgentDebate(Ta-
ble12),andChatGPT+CodeInterpreter(Table14).
• Application A4: an OptiGuide problem with AutoGen (Table 15) and ChatGPT + Code Inter-
preter(Table13).
• Application A1: preliminary evaluation on several alternative multi-agent systems: BabyAGI
(Table16),CAMEL(Table17),andMetaGPT(Table18).
Table8: ApplicationA1,Scenario1: Autonomousmathproblem-solving. ChatGPT+Plugin(Wol-
framAlpha)onthefirstqualitativeexample. TheresponsefromWolframcontainsthecorrectan-
swer,butChatGPTselectedthewrongone.
Action ChatGPT+Plugin
g Input Completelysimplifyandrationalizethedenominator:
√ √
160 245
√ × √
252 108
(cid:240) REQUESTTOWOLFRAM:
1 {
2 "input": "simplify (sqrt(160)/sqrt(252))*
3 (sqrt(245)/sqrt(108))"
4 }
RESPONSEFROMWOLFRAM
1 Query:
2 "simplify (sqrt(160)/sqrt(252))*(sqrt(245)/sqrt(108))"
3
4 Input interpretation:
5 simplify | sqrt(160)/sqrt(252)x sqrt(245)/sqrt(108)
6
7 Results:
8 (5 sqrt(42))/27
9
10 (5 sqrt(14/3))/9
11
12 Decimal approximation:
13 1.2001371663718259686974013770533327143898526494552...
14
15 Wolfram|Alpha website result for "simplify
16 (sqrt(160)/sqrt(252))*(sqrt(245)/sqrt(108))":
17 [link]
(cid:240) Thecompletelysimplifiedandrationalizedformofthegivenexpressionis:
(cid:112)
5 14/3
9
Indecimalform,thisisapproximately1.200137166371825968697401377053332714...
34
1 {
2 "input": "simplify (sqrt(160)/sqrt(252))*
3 (sqrt(245)/sqrt(108))"
4 }

1 Query:
2 "simplify (sqrt(160)/sqrt(252))*(sqrt(245)/sqrt(108))"
3
4 Input interpretation:
5 simplify | sqrt(160)/sqrt(252)x sqrt(245)/sqrt(108)
6
7 Results:
8 (5 sqrt(42))/27
9
10 (5 sqrt(14/3))/9
11
12 Decimal approximation:
13 1.2001371663718259686974013770533327143898526494552...
14
15 Wolfram|Alpha website result for "simplify
16 (sqrt(160)/sqrt(252))*(sqrt(245)/sqrt(108))":
17 [link]

