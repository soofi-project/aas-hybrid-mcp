A Appendix
Inthisappendix,weprovideadditionalanalysisandvisualizationsofthedebatesusedinthemain
paperinSectionA.1. WefurtherprovidedetailedexperimentaldetailsoneachdatasetinSectionA.2.
A.1 AdditionalResults
95
90
85
80
75
70
65
1.0 1.5 2.0 2.5 3.0 3.5 4.0
Debate Rounds
susnesnoC
ConsensusBetweenAgents. InFigure14,weillus- Consensus vs Number of Debating Agents
tratetheconsensusbetweenagentsusingeithershortor
longconsensuspromptsdiscussedinFigure3. Theuse
ofdebatepromptsthatencourageagentstoadaptmore
totheopinionsofotheragentsimprovesconsensus.
Additional Qualitative Visualizations. We added
additionalqualitativevisualizationsofthedebatepro-
Short Debate Prompt
cess. In Figure 16, Figure 17, Figure 18, Figure 19, Long Debate Prompt
Figure20,weillustratedebatesbetweenagentsinthe
GSM8Kdatasetwhichresultinthecorrectanswer. In
Figure14: EffectofPromptsonConsensus.
Figure21,Figure22,Figure23,wefurtherillustrate
Usingashortdebatepromptinducesfastercon-
debatesinGSM8Kwhichleadtotheincorrectanswer.
sensusbetweenagents
Wefurtherprovideanexampleillustrationofdebatein
arithmeticinFigure24,arithmeticwithsummarizationofindividualresponsesofagentsinFigure25,
MMLUinFigure26,adebatewiththefullcontentsbiographiesinFigure27,anddebateinchessin
Figure28. Ingeneral,wefoundthatdebateimprovedtheperformanceoffinalgeneratedanswers,
thoughsometimesanswerswouldconvergetotheincorrectvalue.
A.2 EvaluationDetails
Weprovideddetailedevaluationdetailsforeachsettinginthepaper. Werunallexperimentsusing
thegpt-3.5-turbo-0301model. Weprovideatablelistingthepromptsusedtopromptmodels
andinitializedebateinTable15.
Arithmetic. Toevaluatethearithmetictask,wegeneratedsixrandomintegersforeachtaskbetween
0and30. Wethenevaluatedtheextenttowhichthecorrectintegeranswerwascorrectlyobtained.
Weevaluatedmodelsononehundredgeneratedarithmetictasks.
GradeSchoolMath. ToevaluatetheGSM8Ktask,weevaluatedtheaccuracyatwhichmodels
wereabletoobtainthefinalcorrectanswer,asextractedfromabox. Weevaluatedmodelsonone
hundredgradeschoolmathproblems.
Chess. Toevaluatethechessreasoningtask,weusedchessgamesfromhttps://www.pgnmentor.
com/players/Adams.zip. WeaskedchatGPTtopredictthenextmoveforwhitetomoveatturn
14andreportedtherelativeStockfishpawnscorewithsearchdepth20afterexecutingthesuggested
movefromchatGPT.Weevaluatedmodelsonthreehundredselectedchessgames.
Biographies. Toevaluatethebiographiestask,wecompareeachgeneratedbulletpointbiography
forapersonwithagroundtruthsetoffactsaboutthepersonextractedfromWikipedia. Weiteratively
loopthrougheachgroundtruthfact,andvalidatetheextenttowhichthegeneratedbiographymatches
a particular bullet by prompting chatGPT with the prompt: Consider the following biography of
<person>: <generatedbiography>Istheabovebiographyaboveconsistentwiththefactbelow?
<groundtruthbullet>Giveasingle-wordanswer,yes,no,oruncertain. Wethenevaluateandreport
thepercentageofgroundbulletsthatchatGPTreturnseitheryesornoon. Weignoredgroundtruth
bulletsthatchatGPTreturnsreturneduncertain.
Wefoundthisevaluationmetricprovidedafastwaytoevaluatehowrelativelycorrectagenerated
bulletpointbiographyis. However,wefoundthatgeneratedfactscouldcontainincorrectinformation
thatwasnotcapturedinthegroundtruthbulletandthuscouldnotbevalidatedthroughthismetric.
Nevertheless, we believe this evaluation scheme estimates the relative accuracy of a generated
biography.
MMLU. ToevaluateMMLU,wemeasuredtheaccuracyinwhichmodelswereabletoselectthe
correct multiple-choice answer in each problem. We evaluated models on one hundred selected
MMLUquestionsrandomlydistributedacrosseachofthesubjectareas.
13
 |  |  |  |  |  |  |  | 
 |  |  |  |  |  |  |  | 
 |  |  |  |  |  |  |  | 
 |  |  |  |  |  |  |  | 
 |  |  |  |  |  |  |  | 
 |  |  |  |  |  |  |  | 
 |  |  |  |  | Short | Debate | Promp | t
 |  |  |  |  |  |  |  | 
 |  |  |  |  | Long | Debate | Prompt | 

