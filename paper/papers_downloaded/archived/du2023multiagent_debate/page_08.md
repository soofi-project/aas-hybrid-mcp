Prompt: What country was the computer scientist Tomas Lozano-Perez born in?
Round 1 Agent 1: Tomas Lozano-Perez, a renowned Agent 2: Tomas Lozano-Perez, a renowned
computer scientist, was born in Spain. ✗ computer scientist, was born in Havana, Cuba. ✓
Round 2 Agent 1: I apologize for the confusion. After further Agent 2: I apologize for the conflicting responses.
research, I can confirm that Tomas Lozano-Perez, Upon further research, I can confirm that Tomas
the renowned computer scientist, was actually born Lozano-Perez was born in Havana, Cuba.
✓ ✓
in Cuba. Thank you for bringing this to my attention.
Figure9:ExpressingUncertaintywithMultipleAnswers.Forfactsthatalanguagemodelisuncertainabout,
differentlanguageagentsgeneratedifferentfacts. Debatecausesagentstoconvergetoonefactthatismore
accurate,butnotnecessarilyalwaysfactuallycorrect.
(a) (b)
Figure10:(a)PerformancewithIncreasedAgents.Performanceimprovesasthenumberofunderlyingagents
involvedindebateincreases.(b)PerformancewithIncreasedRounds.Performancerisesasthenumberof
roundsofunderlyingdebateincreases.
85.0
82.5
80.0
77.5
75.0
72.5
70.0
1.0 1.5 2.0 2.5 3.0 3.5 4.0
Debate Rounds
ecnamrofreP
Performance vs Number of Debating Agents
EffectofDebateLengthonAccuracy Asdiscussed Short Debate Prompt
inSection2.2,theunderlyingconvergencetimeinthe Long Debate Prompt
debatebetweenagentscanbecontrolledbytheextent
towhichagentsareencouragedtomaintaintheiropin-
ions. In Figure 12, we consider the effect of short
andlong-formpromptsdiscussedinFigure3. Wefind
thatdebatesusinglongerpromptsleadtoslowercon-
vergencetocorrectanswers, butalsoleadtoabetter
finalconsensusonthecorrectanswer. Weprovidean
analysisofconsensusbetweenagentsinFigure14. Figure 12: Performance vs Debate Length.
Prompts which induce longer debate improve
Using Different Initialization Prompts In our ex-
performance.
perimentsweusethesamepromptsforallagents. We
alsoconsidertheeffectofusingdifferentquestions,wherewefirstinstructeachlanguagemodelto
behavelikeadifferentpersona(professor,doctor,mathematician)ontheMMLUdataset. Wefound
thatimprovedperformanceonMMLUfrom71.1to74.2withdifferentagents,suggestingfurther
gainscanbeobtainedwithdifferentinitializationprompts.
90
85
80
75
70
1 2 3 4 5
Agents
ecnamrofreP
Summarization. While in the majority of experi- Performance vs Number of Debating Agents
ments in the paper we directly concatenate the re- Concat
sponsesofotheragentsascontextforanagenttogener- Summarize
ateanewresponse,thisisexpensivewhenthenumber
ofagentsinvolvedindebategetslarge. Wemayalter-
nativelyfirstsummarizetheresponsesfromallother
agentsintoasingleresponsethatweprovidetoagent
ateachroundformoreefficientdebate. Weapplythis
strategyinFigure10toenabletheuseoffiveormore
agentsindebate. InFigure13,weanalyzetheeffect
compared to directly concatenating the responses of Figure 13: Effect of Summarization. When
otheragents. Wefindthisimprovestheperformanceof there are many agents in a debate, responses
debate,suggestingthatsummarizationisanothertool fromotheragentsmaybefirstsummarizedand
thatcanfurtherimprovemultiagentdebate. thengivenascontext,reducingcontextlength.
Thisoperationimprovesperformance.
UtilizingDifferentLanguageModels Ourexisting
debateresultsarereportedusingmultipleinstancesofachatGPTlanguagemodel. Wefurtherassess
8
 |  |  | b)
(a | ) | ( | b)

 |  |  |  |  |  | 
 |  |  |  |  |  | 
 |  |  |  |  |  | 
 |  |  |  |  |  | 
 |  |  |  |  |  | 
 |  |  |  |  |  | 

 |  |  |  | 
 |  |  |  | 
 |  |  |  | 
 |  |  |  | 
 |  |  |  | 
 |  |  |  | 

 |  |  |  |  |  |  | 
 | Sh
Lo | ort Deba
ng Debat | te Pro
e Prom | mpt
pt |  |  | 
 |  |  |  |  |  |  | 
 |  |  |  |  |  |  | 
 |  |  |  |  |  |  | 
 |  |  |  |  |  |  | 
 |  |  |  |  |  |  | 
 |  |  |  |  |  |  | 

 | Concat |  |  |  |  | 
 | Summ | arize |  |  |  | 
 |  |  |  |  |  | 
 |  |  |  |  |  | 
 |  |  |  |  |  | 
 |  |  |  |  |  | 
 |  |  |  |  |  | 

