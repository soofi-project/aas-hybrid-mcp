ycaruccA
Single Model Multi-Model Debate
100
75
50
25
0
Biographies MMLU Chess Move Arithmetic Grade School Chess Move
Validity Math Optimality
Figure1:MultiagentDebateImprovesReasoningandFactualAccuracy.Accuracyoftraditionalinference
andourmulti-agentdebateoversixbenchmarks(chessmoveoptimalityreportedasanormalizedscore)
lightoftheresponsesofotheragents. Theresultingquorumofmodelscanholdandmaintainmultiple
chainsofreasoningandpossibleanswerssimultaneouslybeforeproposingthefinalanswer.
We find that our debate approach outperforms single model baselines such as zero-shot chain of
thought [11]andreflection [26,18]onavarietyofsixreasoning,factuality,andquestion-answering
tasks. Using both multiple model agents and multiple rounds of debate are important to achieve
the best performance. Given an initial query, we find that individual model instances propose a
diverserangeofanswersdespitebeingthesamemodelclass(althoughwealsoinvestigatethecaseof
mixingdifferentmodeltypes,suchaschatGPT [21]andBard [23]). Afterdebatingandexamining
theresponsesofothermodelinstances,wefindthatthepopulationalmostalwaysconvergesona
singleandmoreaccuratecommonanswer. Debateresultsarealsolesslikelytoincludefalsefacts
thatmodelsareinternallyuncertainof. Thisisbecauseasthedebateprogresses,individualmodel
instancestendtodisagreeonuncertainfactsandomitthemfromtheanswer(Figure7). Lastly,we
findthatdebatedoesnotjustacttoamplifyonecorrectanswerinamodelquorum-wefindmany
caseswhereallthemodelsinitiallymakeincorrectpredictions,butthenarriveatthecorrectanswer
asdebateprogresses(Figure4,11).
Weusethesamemethodologyandprompttemplatesforallourtasksandrequireonlyblack-box
accesstolanguagemodelgenerations–nomodel-internalinformationsuchaslikelihoodsorgradients
isneeded. Thisallowsourmethodtobeusedwithcommonpublicmodelsservinginterfaces. The
method is also orthogonal to other model generation improvements such as retrieval or prompt
engineering(infact,wecombineourdebatemethodwithzero-shotchainofthought). Whilethe
debateprocessismorecostly,requiringmultiplemodelinstancesandrounds,itarrivesatsignificantly
improvedanswersandmaybeusedtogenerateadditionalmodeltrainingdata,effectivelycreatinga
modelself-improvementloop.
To help evaluate the effect of our approach on factual accuracy, we introduce a new benchmark
and dataset evaluating factual accuracy of famous computer scientist biographies. We find that
contemporarylanguagemodelshaveanespeciallyhightendencytohallucinatefactuallyincorrect
biographies,oftenmisrepresentingtherelevantinstitutionsanddates. Moreover,thesefactsoften
inconsistentacrossdifferentlanguagemodelinstances. Byaskingmodelstocometoaconsensus
acrosstheiranswers,suchinconsistentfactsmaybeeitherremovedorcorrected.
Insummary,ourworkcontributesthefollowing. First,wepresentanovelapproachtoimproving
factualcorrectnessandreasoningaccuracyincontemporarylanguagemodels,leveragingamulti-
agentdebateprocessbetweenmodels. Second,weintroduceanewbenchmarkoffactualcorrectness
whichcontemporarylanguagemodelsstrugglewith. Finally,weevaluatetheperformanceofour
debate procedure in language generation, both in terms of the number of agents, the underlying
roundsofdebate,andthepromptsthatelicitsuchbehavioracrossasetofsixdifferentreasoningand
factualaccuracytasks.
2 LanguageGenerationthroughMultiagentDebate
Wepresentanapproachtogeneratelanguageresponsesthroughmultiagentdebate. Weprovidean
overviewofourapproachinSection2.1. Wefurtherdiscussconvergencetoconsensusinthedebate
processinSection2.2. TheoveralloverviewofourapproachisshowninFigure2.
2
 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | 
 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | 
 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | 
 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | 
 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | 

