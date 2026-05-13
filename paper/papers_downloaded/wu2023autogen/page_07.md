80
70
60
50
40
30
20
10
0 AutoGen ChatGPT ChatGPT GPT-4 Multi-AgentLangChain +Code +Plugin Debate ReAct
Methods
)%(
oitaR
sseccuS
80
120 Level-5 problems
69.48% Whole Dataset 70
55.18% 60 52.5%
48.33% 45.0% 50
40
30.0%
26.67% 30 23.33%
20
10
0 F1 Recall
Metrics
(a)A1:PerformanceonMATH(w/GPT-4).
)%(
egatnecreP
AutoGen
AuotGen W/O interactive retrieval 66.65%
DPR 62.59%
58.56%
25.88% 22.79%
15.12%
(b)A2:Q&Atasks(w/GPT-3.5).
100
80
60
40
20
0 AutoGen (3 agent) AutoGen (2 agent) ReAct
Methods
)%( oitaR
sseccuS
Average
Best of 3 100
77%
69% 63% 66% 80 54% 54%
60
40
20
0 F1 Recall
Metrics
(c)A3:PerformanceonALFWorld.
)%( egatnecreP
Multi-GPT4
Single-GPT4
96.00% 98.00% Multi-GPT3.5
88.00% Single-GPT3.5
83.00% 78.00% 72.00%
48.00%
32.00%
(d)A4:PerformanceonOptiGuide.
Figure 4: Performance on four applications A1-A4. (a) shows that AutoGen agents can be used
out of the box to achieve the most competitive performance on math problem solving tasks; (b)
shows that AutoGen can be used to realize effective retrieval augmentation and realize a novel
interactiveretrievalfeaturetoboostperformanceonQ&Atasks;(c)showsthatAutoGencanbeused
to introduce a three-agent system with a grounding agent to improve performance on ALFWorld;
(d) shows that a multi-agent design is helpful in boosting performance in coding tasks that need
safeguards.
2023)withSentenceTransformers(Reimers&Gurevych,2019)asthecontextretriever. Adetailed
workflowdescriptionoftheRetrieval-augmentedChatisprovidedinAppendixD.
WeevaluateRetrieval-augmentedChatinbothquestion-answeringandcode-generationscenarios.
(Scenario 1) We first perform an evaluation regarding natural question answering on the Natural
Questionsdataset(Kwiatkowskietal.,2019)andreportresultsinFigure4b. Inthisevaluation,we
compare our system with DPR (Dense Passage Retrieval) following an existing evaluation6 prac-
tice (Adlakha et al., 2023). Leveraging the conversational design and natural-language control,
AutoGenintroducesanovelinteractiveretrievalfeatureinthisapplication: whenevertheretrieved
context does not contain the information, instead of terminating, the LLM-based assistant would
reply“Sorry,Icannotfindanyinformationabout... UPDATECONTEXT.”whichwillinvokemore
retrievalattempts. Weconductanablationstudyinwhichweprompttheassistantagenttosay“I
don’t know” instead of “UPDATE CONTEXT.” in cases where relevant information is not found,
and report results in Figure 4b. The results show that the interactive retrieval mechanism indeed
playsanon-trivialroleintheprocess. Wegiveaconcreteexampleandresultsusingthisappealing
featureinAppendixD.(Scenario2)WefurtherdemonstratehowRetrieval-augmentedChataidsin
generatingcodebasedonagivencodebasethatcontainscodenotincludedinGPT-4’strainingdata.
EvaluationanddemonstrationdetailsforbothscenariosareincludedinAppendixD.
6TheresultsofDPRwithGPT-3.5showninFigure4barefrom(Adlakhaetal.,2023). WeuseGPT-3.5as
ashorthandforGPT-3.5-turbo.
7
80
120 Level-5 problems
70 69.48% Whole Dataset
60 )%( 55.18%
52.5%
50 oitaR 48.33% 45.0%
40
sseccuS
30.0%
30 26.67%
23.33%
20
10
0
AutoGen ChatGPT ChatGPT GPT-4 Multi-AgentLangChain
+Code +Plugin Debate ReAct
Methods | 80
AutoGen
70 AuotGen W/O interactive retrieval 66.65%
DPR 62.59%
60 58.56%
)%(
50 egatnecreP
40
30 25.88%
22.79%
20 15.12%
10
0
F1 Recall
Metrics

52.5% |  |  | Whole Dataset
55.18%
48.33% |  |  |  |  |  |  |  |  |  |  | 
 |  |  |  |  |  |  |  |  |  |  |  |  |  | 
 |  |  |  |  |  |  |  |  |  |  |  |  |  | 
 |  |  |  |  | 45.0% |  |  |  |  |  |  |  |  | 
 |  |  |  |  |  |  |  |  |  |  |  |  |  | 
 |  |  |  |  |  |  | 30.0% |  |  | 26.67%
23.33% |  |  |  | 
 |  |  |  |  |  |  |  |  |  |  |  |  |  | 
 |  |  |  |  |  |  |  |  |  |  |  |  |  | 

AuotGen W/O interactive retrieval
DPR |  |  |  | 66.65%
62.59%
58.56% |  |  | 
 |  |  |  |  |  |  | 
25.88% |  |  |  |  |  |  | 
 | 22.79%
15.12% |  |  |  |  |  | 
 |  |  |  |  |  |  | 
 |  |  |  |  |  |  | 

100
Average
Best of 3
80 77%
)%( 69%
66%
63%
oitaR
60 54% 54%
sseccuS
40
20
0
AutoGen (3 agent) AutoGen (2 agent) ReAct
Methods | Multi-GPT4
Single-GPT4
100 96.00% 98.00% Multi-GPT3.5
88.00% Single-GPT3.5
)%( 83.00%
80 78.00%
72.00%
egatnecreP
60
48.00%
40
32.00%
20
0
F1 Recall
Metrics

 |  |  |  |  |  |  | Average
Best of 3 |  |  | 
77%
69%
66%
63% |  |  |  |  |  |  |  |  |  | 
 |  |  |  |  |  |  |  |  | 66% | 
 |  |  | 54% |  |  | 54% |  |  |  | 
 |  |  |  |  |  |  |  |  |  | 
 |  |  |  |  |  |  |  |  |  | 
 |  |  |  |  |  |  |  |  |  | 

96.00% 98.00% |  |  |  |  |  |  | Multi-GPT4
Single-GPT4
Multi-GPT3.5 |  |  | 
 | 88.00%
83.00% |  |  |  |  | Single-GPT3.5 |  |  |  | 
 |  |  |  |  |  | 78.00 |  | %
72.00% |  | 
 |  |  |  |  |  |  |  |  |  | 
 |  |  | 48.00% |  |  |  |  |  |  | 
 |  |  |  |  |  |  |  |  |  | 
 |  |  |  |  |  |  |  |  | 32.00% | 
 |  |  |  |  |  |  |  |  |  | 
 |  |  |  |  |  |  |  |  |  | 

