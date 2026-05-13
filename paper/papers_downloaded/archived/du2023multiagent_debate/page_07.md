Question: Six positive integers are written on the Question: You suspect that your patient has an
faces of a cube. Each vertex is labeled with the enlarged submandibular salivary gland. You expect
product of the three numbers on the faces adjacent to the enlarged gland: A) to be palpable intraorally. B)
the vertex. If the sum of the numbers on the vertices to be palpable extraorally. C) to be palpable both
is equal to 1001, then what is the sum of the numbers intra-and extraorally. D) only to be detectable by
written on the faces? A) 18. B) 13. C) 1001. D) 31. radiographical examination.
Round 1 Agent 1: A ✗ Agent 2: C ✗ Agent 3: D ✓ Agent 1: C ✓ Agent 2: B ✗ Agent 3: C ✓
Round 2 Agent 1: D ✓ Agent 2: D ✓ Agent 3: D ✓ Agent 1: C ✓ Agent 2: C ✓ Agent 3: C ✓
Figure8:IllustrationofMMLU.Illustrationofdebatewhenansweringfactualtasks.Reasoningomitted.
Model Biographies MMLU ChessMoveValidity
SingleAgent 66.0±2.2 63.9±4.8 29.3±2.6
SingleAgent(Reflection) 68.3±2.9 57.7±5.0 38.8±2.9
Multi-Agent(Debate) 73.8±2.3 71.1±4.6 45.2±2.9
Table2:MultiagentDebateImprovesFactualAccuracyMulti-agentdebateimprovesthefactualaccuracy.
• MMLU.Next,weassessthefactualityoflanguagemodelsinrespondingtodifferentfactualknowl-
edgequestionstypicallylearnedandassessedindifferentexams. WeutilizetheexistingMMLU
dataset[8]tobenchmarktheaccuracyofresponses.
• Chess Move Validity. Lastly,westudythehallucinationsinlanguagemodelswhenplanning
undertothegivenrulesofanexistingenvironmentorgame. Specifically,wemeasurethevalidity
ofpossiblemovesinagameofChessgivenbyBIG-BenchChess-StateTrackingBenchmark [27]
taskofchess-moveprediction. Inthistask,anagentisgivenasetofnextmoves,andmustmakea
validnextmoveofapieceonaboard.
Baselines. WeusethesamebaselinesasinSection3.1. Themultiagent(majority)isnotdirectly
applicableinthissettingasindividualresponsesarenoteasilycomparable,andsoweomitbaseline
comparisonwiththemajorityvotinginthissetting.
Results. We analyze the performance of each method in Table 2. We found that approaches
basedonreflectionledtopoorperformanceinthefactualitysetting. Incontrast,debategivesthe
bestperformanceinthissettingalso,andsignificantlyoutperformseachbaseline. Weillustratea
debatebetweenagentsonthebiographytaskinFigure7andonMMLUinFigure8. Wefoundthat
multiagentdebateimprovedandsettledonbulletsthatweremoreconsistentacrossagents.
We found that different language agents tended to give different answers when the underlying
languagemodelwasuncertainaboutthequestion. However,directlyaskingeachagentabouttheir
confidence [10]oftheanswerledtohighconfidenceassessmentsoneachanswer. However,when
thesedifferentlanguageagentswereaskedtocommunicatewitheachother,eachagentwouldquickly
changetheiropiniontoaconsensusanswerwhichwasmoreaccurate. WeillustratethisinFigure9.
Interestingly,wefoundthatonfactsthatthelanguagemodelwasconfidentin(i.e. manyinstancesof
thesamemodelallgavethesameanswer),itwasverydifficulttoconvinceanagenttochangetheir
opinion,suggestingthat“easeofpersuasion”maybeamethodtoassessfactualconfidence.
3.3 Analysis: UnderstandingMultiagentDebate
Finally,weanalyzehowmultiagentdebateimprovestheunderlyinglanguagegenerationprocedure
inlanguagemodels.
NumberofAgents. First,weanalyzetheimpactofagentsnumberindebate. InFigure10(a),we
increasethenumberofagentsusedindebate,whilefixingthedebatelengthtobetwo. Onarithmetic,
performance monotonically increases with the increased number of agents. For larger number
ofagents,wefirstsummarizeallagentresponseswithchatGPTinsteadofdirectlyconcatenating
responsesduetocontextlengtherror.
RoundsofDebate Next,weanalyzetheimpactofthenumberofroundsofdebateinmultiagent
debate. InFigure10(b),weincreasethedebatelengthbetweenagents,whilefixingthenumberof
agentstothree. Wefindthatonthearithmetictask,theperformancealsomonotonicallyincreases
withdebatelength. However,wefoundthatadditionaldebateroundsabovefourledtoasimilarfinal
performanceto4roundsofdebate.
7
Question: Six positive integers are written on the Question: You suspect that your patient has an
faces of a cube. Each vertex is labeled with the enlarged submandibular salivary gland. You expect
product of the three numbers on the faces adjacent to the enlarged gland: A) to be palpable intraorally. B)
the vertex. If the sum of the numbers on the vertices to be palpable extraorally. C) to be palpable both
is equal to 1001, then what is the sum of the numbers intra-and extraorally. D) only to be detectable by
written on the faces? A) 18. B) 13. C) 1001. D) 31. radiographical examination.
Round 1 Agent 1: A ✗ Agent 2: C ✗ Agent 3: D ✓ Agent 1: C ✓ Agent 2: B ✗ Agent 3: C ✓
Round 2 Agent 1: D ✓ Agent 2: D ✓ Agent 3: D ✓ Agent 1: C ✓ Agent 2: C ✓ Agent 3: C ✓ | 
 | Agent 3: C ✓
 | Agent 3: C ✓

Agent 1: A ✗
Agent 1: D ✓

Agent 2: C ✗
Agent 2: D ✓

Agent 3: D ✓
Agent 3: D ✓

Agent 1: C ✓
Agent 1: C ✓

Agent 2: B ✗
Agent 2: C ✓

