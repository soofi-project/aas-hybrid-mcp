# Tool Call

Source: tool_call_emnlp_2025_alignment_efficient_tool_calling.pdf


---
### Page 1

Alignment for Efficient Tool Calling of Large Language Models
HongshenXu1,4* ZihanWang1,4* ZichenZhu1,4 LeiPan3
XingyuChen1,4 ShuaiFan3,4 LuChen1,2,4,5† KaiYu1,4,5†
1X-LANCELab,MoEKeyLabofArtificialIntelligence,AIInstitute
SchoolofComputerScience,ShanghaiJiaoTongUniversity,Shanghai,China
2ShanghaiInnovationInstitution,Shanghai,China
3AISpeechCo.,Ltd.,Suzhou,China
4JiangsuKeyLabofLanguageComputing,Suzhou,China
5 SuzhouLaboratory,Suzhou,China
{xuhongshen, kai.yu}@sjtu.edu.cn
Abstract
Find the greatest common divisor of 957 and 1537.
Recentadvancementsintoollearninghaveen-
Fast & Inaccurate Our Method
abled large language models (LLMs) to in-
Find the ...
tegrate external tools, enhancing their task The answer is 87.
performance by expanding their knowledge
boundaries. However, relying on tools of- Slow & Accurate
tenintroducestrade-offsbetweenperformance,
speed, and cost, with LLMs sometimes ex- math tool Ans: 29 I u ’m se n m o a t t s h u r t e o . o I l w s . i . l . l t S h u a r t e t , h I’ e m a c n o s n w f e id r e is n . t ..
hibiting overreliance and overconfidence in
tool usage. This paper addresses the chal-
lenge of aligning LLMs with their knowl-
edgeboundariestomakemoreintelligentde-
50
cisions about tool invocation. We propose a
multi-objectivealignmentframeworkthatcom- 25
binesprobabilisticknowledgeboundaryestima- 0
math search reasoning
tionwithdynamicdecision-making,allowing tools tools tools
LLMs to better assess when to invoke tools
based on their confidence. Our framework
includes two methods for knowledge bound-
ary estimation—consistency-based and abso-
lute estimation—and two training strategies
forintegratingtheseestimatesintothemodel’s
decision-makingprocess. Experimentalresults
on various tool invocation scenarios demon-
stratetheeffectivenessofourframework,show-
ingsignificantimprovementsintoolefficiency
byreducingunnecessarytoolusage.
1 Introduction
The objective of tool learning is to enable large
language models (LLMs; Gemini Team, 2023;
Achiam et al., 2023; Dubey et al., 2024) to ac-
quire the capability to effectively utilize external
tools,therebyenhancingtheirperformanceacross
variousdownstreamtasks(Schicketal.,2023;Hao
etal.,2023;Hsiehetal.,2023;Tangetal.,2023).
ToolscanberegardedasextensionsofanLLM’s
knowledgeorcapabilityboundaries. Byinvoking
tools, models can accomplish tasks beyond their
knowledgeboundariesandevenaccessinformation
fromdifferentmodalities(Zengetal.,2022).
*Equalcontributions.
†ThecorrespondingauthorsareLuChenandKaiYu.
Proceedingsofthe2025ConferenceonEmpiricalMethodsinNaturalLanguageProcessing,pages17776–17792
November4-9,2025©2025AssociationforComputationalLinguistics
)%(
ecnailer-loot-revO 40
20
0
math search reasoning
tools tools tools
)%(
ecnedifnocrevO
Auto Tool Our Method
Figure 1: Our method effectively enables LLMs to
switch between answering independently and calling
tools(upperpart),therebyreducingthemodel’sover-
relianceandoverconfidenceintools(lowerpart).
While tools can enhance LLM’s task perfor-
mance, it is important to note that solving tasks
throughtoolinvocationoftenrequiresmoresteps,
longer completion times, and additional tool-
callingcosts. Forexample,inquestion-answering
scenarios involving search tools, the model must
first generate a query for the retrieval tool, wait
for the search results, and then process these re-
sultstoproduceafinalanswer. Incontrast,direct
answeringinvolvessimplygeneratingaresponse.
This introduces a trade-off problem between per-
formanceandspeed. Unfortunately,recentstudies
have shown that O1-like LLMs struggle to strike
abalancebetweenthesetwoaspects: exhibitover-
thinking (Chen et al., 2024) in simple reasoning
tasks and underthinking (Wang et al., 2025) in
moredifficultones. Similarly,weobservethatthe
sameissuearisesintoolusagescenarios. Current
LLMs exhibit over-tool-reliance, invoking tools
evenwhentaskscouldbecompletedindependently,
whilealsoexhibitingoverconfidencebyrefusingto
17776

[TABLE]

Auto Tool Our Method
)%(
)%(
ecnailer-loot-revO 40
50 ecnedifnocrevO
20
25
0 0
math search reasoning math search reasoning
tools tools tools tools tools tools
[/TABLE]

[TABLE]
 |  |  |  |  |  |  | 
 |  |  |  |  |  |  | 
 |  |  |  |  |  |  | 
 |  |  |  |  |  |  | 
[/TABLE]

[TABLE]
 |  |  |  |  |  |  | 
 |  |  |  |  |  |  | 
 |  |  |  |  |  |  | 
 |  |  |  |  |  |  | 
[/TABLE]

---
### Page 2

usetoolswhennecessary. Thisinconsistencymir- 2 RelatedWork
rorsthechallengesfacedbyO1-likemodels,under-
miningthemodel’stoolintelligenceandincreasing 2.1 LLMAlignment
taskcompletioncostsinreal-worldscenarios.
LLMalignmentseekstotrainlanguagemodelsto
Inthiswork,weaimtoimprovehowLLMsde-
act in accordance with the user’s intent, utilizing
cide when and how to use external tools for task
methodssuchassupervisedfine-tuning(Weietal.,
completion. The main challenge is aligning the
2022;Chungetal.,2022;Zhangetal.,2023), di-
model’s behavior with its knowledge boundaries,
rectpreferenceoptimization(DPO)(Rafailovetal.,
allowing it to determine when a tool is needed
2024),orreinforcementlearningfromhumanfeed-
based on its confidence. Instead of treating the
back(RLHF)(Stiennonetal.,2020;Ouyangetal.,
model’s knowledge as simply "known" or "un-
2022; Glaese et al., 2022). Most works focus
known" (Yang et al., 2023c), we propose a more
on enhancing the instruction-following capabili-
nuanced approach that accounts for uncertainty.
ties (Sanh et al., 2021; Wei et al., 2022), helpful-
This approach recognizes an "uncertain region"
ness(Dingetal.,2023;Xuetal.,2023),harmless-
where the model assigns probabilistic estimates
ness(SolaimanandDennison,2021;Benderetal.,
toitsknowledge,enablingbetterdecision-making
2021), and honesty (Cui et al., 2023; Yang et al.,
thatbalancestasksuccessandtoolusagecosts.
2023b) of LLMs. In addition, some works pro-
Weintroduceanalignmentframeworkforeffi-
posedaligningmodelswiththeirknowledgebound-
cienttoolcallingthatcombinesprobabilisticknowl-
aries(Xuetal.,2024b;Yangetal.,2023c),specif-
edgeboundaryestimationwithdynamicdecision-
ically by training LLMs to reject unknown ques-
making. Ourapproachhastwomaincomponents:
tions. However,theseapproachesassumeabinary
1) Knowledge Boundary Estimation: we pro-
viewofthemodel’sknowledgeboundary—either
posetwomethodstoassessthemodel’sknowledge:
themodelknowstheansweroritdoesnot. Incon-
consistency-basedestimationbasedonagreement
trast, our work posits that knowledge boundaries
andusingexternalgroundtruthtoevaluatetheav-
aremorenuancedandexistwithinagrayarea. We
erage accuracy of multiple model samplings. 2)
proposedynamicallydeterminingthemodel’sbe-
Knowledge Boundary Modeling: we construct
haviorwithinthisambiguousregion,dependingon
differentdatatoexhibitimplicitmodeling,where
thespecificapplicationscenario.
the model makes decisions based on predefined
thresholds of knowledge certainty, and explicit
modeling, where the model outputs both an an- 2.2 ToolLearning
swerandaconfidencescore. Thisframeworkhelps
Recent advancements in tool learning have en-
themodelusetoolsmoreefficiently,invokingthem
abledLLMstoeffectivelyintegrateexternaltools,
onlywhennecessary,thusimprovingperformance
enhancing real-time knowledge retrieval, multi-
while reducing costs. Our approach is evaluated
modalfunctionalities,anddomain-specificexper-
acrossmultipletool-usescenarios,demonstratinga
tise (Yang et al., 2023a; Gupta and Kembhavi,
significantreductioninunnecessarytoolinvocation
2023;Jinetal.,2024). Methodsrangefromlever-
andanimprovementinoveralltoolefficiency. Our
agingin-contextlearningfortooldescriptionsand
contributionscanbesummarizedasfollows:
demonstrations(Hsiehetal.,2023)toexplicittrain-
ing on tool-enriched datasets (Patil et al., 2023;
• We propose a multi-objective alignment Tang et al., 2023; Qin et al., 2023). Some works
frameworkforefficienttoolinvocation,along have also investigated how to accomplish tasks
withcorrespondingevaluationmetrics. withinalimitednumberoftoolinvocations(Zheng
et al., 2024; Huang et al., 2023) and how to call
tools more reliably (Xu et al., 2024a; Gui et al.,
• Weproposethetoolalignmentalgorithmsand
2024; Zhang et al., 2024). However, previous re-
correspondingdatagenerationmethods.
search on tool invocation has largely overlooked
thecorrelationbetweentoolusageandthemodel’s
• Weconductextensiveexperimentsacrossmul- knowledge boundaries. Additionally, there has
tipletoolinvocationscenarios,demonstrating beennounifiedevaluationmetricproposedforas-
theeffectivenessofourapproach. sessingefficienttoolinvocation.
17777

---
### Page 3

3 ProblemFormulation where y , y , y , y represent correct re-
nc tc nw tw
sponseswithouttoolusage,correctresponseswith
3.1 LLMAlignment
toolusage,incorrectresponseswithouttoolusage,
With the rapid development LLMs, ensuring and incorrect responses with tool usage, respec-
their alignment with human instructions, prefer- tively. Thisorderingreflectstheprinciplethatan
ences, and values has become a crucial research ideal LLM should solve problems independently
area (Wang et al., 2024). Alignment approaches whenever possible, resorting to tool usage only
are designed to optimize model responses based whennecessary,whilealsoavoidingincorrectan-
onpredefinedobjectivessuchashelpfulness,truth- swersandunnecessarytoolcalls.
fulness, and safety. Specifically, given an input
prompt x and an alignment goal helpfulness, we 3.3 EvaluationMethodology
employthefollowingscoringprincipletorepresent Toquantifythetradeoffbetweenhelpfulnessand
thealignmentobjective: toolcost,wedefineabenefit-costutilityfunction
asfollows:
s(x,y ) > s(x,y ), (1)
h u
u(y) = 1 (y) α 1 (y), (5)
wherey h andy u representahelpfulresponseand helpfulness − · cost
anunhelpfulresponse,respectively. Thepreference where 1 (y), 1 (y) equal to 1 when
helpfulness tool
order can be determined through human annota- the response y is correct or contains tool calling,
tion(Ouyangetal.,2022)orascoringmodel(Gao respectively. αrepresentsthecostassociatedwith
etal.,2023a)trainedwithhumanpreferencedata. tool usage. The overall utility of a model on a
Thecollectedpreferencedatacanbefurtherlever- datasetwithN samplesisthencomputedas:
agedtotrainrewardmodelsorfine-tuneLLMpoli-
N
1
cies,therebyimprovingalignmentwithhumanex-
Utility = u(y ) = Acc α TR, (6)
i
pectations. N − ·
i=1
X
3.2 Multi-ObjectiveAlignmentforEfficient whereAccandTRrepresenttheoverallaccuracy
ToolCalling andtoolusageratioonthedataset,respectively.
Theparameterαiscrucial,asitdeterminesthe
Whilealignmentwithhelpfulnessisessential,effi-
relativepenaltyoftoolusage. Alargerαindicates
cienttoolcallingintroducesadditionalalignment
ahighersensitivitytocostoragreaterpenaltyfor
challenges. Awell-alignedLLMshouldnotonly
invoking tools. If α is too high, the model may
provide helpful responses but also minimize un-
completelyavoidtoolusage,evenwhennecessary.
necessary tool usage, as excessive tool calls in-
Conversely,ifαistoolow,themodelmayoveruse
creaseinferencelatencyandcomputationalcosts.
tools. Therefore, selecting a moderate α ensures
Therefore,weproposeamulti-objectivealignment
a balanced tradeoff between efficiency and effec-
frameworkthatbalanceshelpfulnessandtoolcost.
tiveness. Furthermore,thecostoftoolusagevaries
First,wedefinealignmentobjectivesseparately
across different tasks and tools. To account for
forhelpfulnessandtoolcost. Thehelpfulnessalign-
thesedifferences,αcanbesetdynamicallybased
mentobjectivefollows:
onthespecifictoolbeingused. Empirically,inour
s(x,y c ) > s(x,y w ), (2) study, we assign α values of 0.2, 0.4, and 0.6 to
calculators,searchengines,andexternalLLMrea-
wherey representsacorrectresponse,andy rep-
c w
soning,respectively. Thedifferentαvaluesreflect
resentsanincorrectresponse. Simultaneously,for
the increasing computational cost and inference
toolcost,wedefine:
latencyassociatedwiththesetools.
s(x,y ) > s(x,y ), (3)
n t
4 Methodology
wherey representsaresponsewithouttoolusage,
n
4.1 FrameworkforEfficientToolLearning
andy representsaresponsewithtoolusage. Com-
t
bining these two objectives, our final alignment The key to enabling efficient tool calling lies in
formulationbecomes: aligningLLMswiththeirownknowledgebound-
aries. Unlike a binary classification of knowl-
s(x,y ) > s(x,y ) > s(x,y ) > s(x,y ),
nc tc nw tw edge into "known" and "unknown," human cog-
(4)
nition—andbyextension,LLMs—operateswithin
17778

---
### Page 4

Objective Kn-Bound Estimation Kn-Bound Modeling
Consistency Implicit (Auto)
Known Uncertain Unknown E>e
87 87
Sure, I’m confident
Find the greatest 29 5/10 E cons Find the ... E that the answer is 29.
common divisor of E<e
... 29
957 and 1537. Train Data I’m not sure about the
87 3 ... /10 ( , ) m a a n t s h w e e m r. a S t o ic , a I l w t i o ll o u ls s . e ..
( , )
Absolute Explicit (Manual) ( , , E )
Groundtruth: 29 Train Data
Direct
Tool Call
Answer The answer is 29.
Cost Sensitivity 87 Find the ... E My confidence
Helpfulness A αα > B com 9 Fi 5 n m 7 d o a t n n h d e d i g 1 v r 5 i e s 3 o a 7 r t . e o s f t 2 ... 9 7/10 T In r f a e i r n ence estimation is 60%.
E >e 29
3/10 pred
Efficiency A D n i s r w e e c r t > T C o a o l l l 87 E abs E pred E pred <e math tool
Figure2: Theoverallpipelineofknowledgeboundarymodelingmethods.
aspectrum. AsshownintheleftpartofFigure2, 4.2 EstimatingKnowledgeBoundaries
thereexistsalarge"uncertainregion"wherethe
Weproposetwomethodsforknowledgeboundary
model can only assign a probabilistic estimate to
estimationasshowninthemiddlepartofFigure2:
itsknowledge. Previousworksthatenforceastrict
binary classification fail to capture this nuanced Consistency-BasedEstimation Thismethodre-
understanding, leading to inaccurate estimations liesonself-consistency. Weassumethatifamodel
andsuboptimaltoolinvocationstrategies. produceshighlyconsistentoutputsacrossmultiple
samplesforagivenquestion,itpossessesastronger
graspoftheunderlyingknowledge. Tooperational-
To achieve effective tool use, the model must ize this, we measure the variance in the model’s
firstdevelopanawarenessofitsknowledgebound- sampled responses and use it as an indicator of
aries and then leverage this understanding to ad- knowledge certainty. Higher consistency implies
justitsdecision-makingprocess. Thisperspective greaterconfidenceinthemodel’sknowledge.
aligns with the efficiency objective discussed in
AbsoluteEstimationviaGroundTruth While
priorsections: amodelthatperceivesknowledge
consistency-basedestimationisuseful,itdoesnot
inbinarytermswillstruggletoadjustitsbehavior
directly leverage external validation. To address
undervaryingcostconsiderations(representedby
this,weintroduceanabsoluteestimationmethod
α). If a model simply categorizes knowledge as
basedongroundtruthcorrectness. Werepeatedly
either"known"or"unknown,"itwilleitheralways
samplemodelresponsesforthesamequestionand
invokeatoolforuncertaincasesoralwaysanswer
computetheaverageaccuracyusinggroundtruth.
directly,ignoringcost-sensitiveoptimization.
This provides an externally validated measure of
the model’s knowledge, correcting for potential
biasesinself-estimation.
We propose a solution where the model learns
to estimate its knowledge uncertainty probabilis-
4.3 TrainingApproaches
tically rather than making binary classifications.
Tointegrateknowledgeboundaryestimationinto
Thisallowsforgreaterflexibilityintoolinvocation.
themodel’sbehavior,weemploytwoSFTstrate-
Dependingondifferentvaluesofα(whichrepre-
giesasshownintherightpartofFigure2: implicit
sent different real-world tool costs), we can train
modelingandexplicitmodeling.
themodeltodynamicallyadjustitsbehavior. This
canbeimplementedimplicitlythroughcontrolled ImplicitModeling Inthisapproach,themodelis
trainingdatadistributionsorexplicitlybyhaving trainedtodirectlyoutputactions(eitheranswering
themodeloutputconfidenceestimatesthatcanbe directly or invoking a tool) based on pre-defined
thresholdedatinferencetimetodeterminewhether decision rules. Specifically, we sort all training
atoolshouldbeinvoked. samplesbasedontheirestimatedknowledgescores
17779

[TABLE]
87
5/10
[/TABLE]

[TABLE]
 | 
[/TABLE]

[TABLE]


[/TABLE]

---
### Page 5

andsetathreshold: samplesabovethisthreshold ChatGPT.Computationisperformedusingasym-
arelabeledfordirectanswering,whilethosebelow bolic calculator as a tool, implemented via code
it are labeled for tool invocation. Since different executionforprecisemathematicalevaluation.
valuesofαcorrespondtodifferenttoolusagepref- Knowledge-based QA (Retrieval-Augmented
erences,wetrainseparateSFTmodelswithvary- Generation). To evaluate factual knowledge re-
ingthresholdstoadapttodifferentscenarios. This trieval, we use TriviaQA (Joshi et al., 2017), a
methodisefficientduringinference,asthemodel widelyusedquestion-answeringdataset. Wesam-
onlyneedstogenerateasingleresponseperquery. ple10,000instancesfortrainingandusethe11,313
However,itrequiresmultipleroundsoftrainingfor instancedevelopmentsetforevaluation,astheoffi-
differentvaluesofα. cialtestsetgroundtruthisunavailable. Toenhance
factual accuracy, we integrate a retrieval system,
ExplicitModeling Unlikeimplicitmodeling,ex-
leveraging Pyserini (Lin et al., 2021)—a Python
plicitmodelingtrainsthemodeltooutputbothan
toolkit designed for reproducible information re-
answer and an associated knowledge confidence
trievalwithsparseanddenserepresentations.
score. Thisallowsdynamicadjustmentoftoolinvo-
ComplexReasoning(ReasoningModel). Toeval-
cationdecisionsatinferencetimewithoutrequiring
uatemulti-stepreasoningtasks,weusetheMATH
separate SFT models for different α values. Dur-
dataset (Hendrycks et al., 2021) with its original
inginference,wesetathresholdontheconfidence
train-test split. Given the inherent complexity of
score: ifthescoreisabovethethreshold,themodel
mathematical reasoning, we employ DeepSeek-
answersdirectly;otherwise,itinvokesatool. This
R1 (DeepSeek-AI et al., 2025) as a tool for rea-
approacheliminatestheneedforretrainingbutin-
soning,leveragingitsstrongproblem-solvingcapa-
troducesadditionalinferencelatency,aseachquery
bilities. However,thiscomesatatrade-off: higher
requiresbothananswerandanuncertaintyestima-
computationalcostandslowerinferencespeed.
tionbeforedecidingwhethertouseatool.
Eachmethodhasitsadvantagesanddrawbacks. 5.1.2 Baselines
ImplicitModelinghasFasterinference(singlere- Thebaselinemethodsarecategorizedintotwoma-
sponse generation) but requires multiple training jorgroups: Prompt-based andUncertainty-based.
runs for different α values. Explicit Modeling is AllpromptsusedarelistedinAppendixF.
more flexible at inference time (threshold tuning
Prompt-based Prompt-based methods govern
withoutretraining)butslowerduetothetwo-step
how the model interacts with external tools and
generationprocess. Inourexperiments,weevalu-
determines its tool usage behavior. The Baseline
atebothapproachestodeterminethemosteffective
(w/otool)approachhasthemodelanswerqueries
strategyforefficienttoolcalling.
entirelyonitsown,relyingonlyoninternalknowl-
edge. The Baseline (all tool) forces the model to
5 Experiments
alwaysinvokeatool. TheAutotoolmethodallows
5.1 ExperimentSetup themodeltodecidewhentouseatoolbasedonits
estimatedconfidence. ICLtool(10-shot)provides
5.1.1 TaskScenarios
themodelwith10exampleinteractions(5correct,
We evaluate our approach across three scenarios,
5incorrect)tobetterguideitsdecisiononwhether
each requiring a specific external tool: symbolic
toanswerdirectlyoruseatool. Thesebaselinesare
computation via a calculator, factual retrieval us-
newlydesignedtoreflectintuitivetool-usestrate-
ing a retrieval-augmented generation (Gao et al.,
giesundervaryingassumptionsoftoolaccessibility
2023b) system, and complex reasoning with a
andcost(seeAppendixAfordetails).
strongreasoningmodel. SeeAppendixDformore
detailedexperimentalsetup. Uncertainty-based. Uncertainty-basedmethods
ArithmeticComputation(Calculator). Toevalu- estimate the confidence of model-generated an-
atemathematicalcomputationcapabilities,wecon- swers,whichweleveragetodeterminetheoptimal
structanarithmeticdatasetfollowing LiuandLow utilitybysearchingforthebestconfidencethresh-
(2023). Inputnumbersaresampledonalogarith- old. Weexplorefourapproaches: Rawlogits(Lyu
micscaletoensurediversemagnitudeswithmini- etal.,2024),P(True)(Kadavathetal.,2022),Ver-
malduplication. Toenhancelinguisticdiversity,we balizedConfidence(Tianetal.,2023),andAgree-
usehundredsofinstructiontemplatesgeneratedby ment (Self-Consistency) (Lyu et al., 2024), each
17780

---
### Page 6

providing a different way to assess model confi-
100
dence(seeAppendixBfordetails).
80
5.1.3 TrainingDetails 60
We use two baseline models: LLAMA-3.1-
40
8B-INSTRUCTandQWEN-2.5-7B-INSTRUCT.To
20
align with our experimental setup, we customize
theDeepSpeed-Chat(Yaoetal.,2023)framework. 0
0.0 0.5 1.0
The training process adopts a learning rate of
5 10 5 andabatchsizeof128. Allothertrain-
−
×
ing parameters are set to the default parameters
in DeepSpeed-Chat. By default, 10,000 samples
areusedforSupervisedFine-Tuning. Allmodels
undergotrainingfor2epochsonA800GPUs(see
AppendixCformoredetails).
5.2 MainResults
Table 1 compares the performance of all evalu-
atedmethods. Ourapproachachievesthehighest
utility scores across three scenarios, demonstrat-
ingitseffectivenessinbalancingtasksuccessand
tool efficiency. Among our methods, Absolute-
basedknowledgeboundaryestimationoutperforms
Consistency-basedestimation,asexternalsupervi-
sionviagroundtruthlabelsenablesmoreaccurate
boundaryestimationandbettertoolinvocationde-
cisions. Ourapproachmaintainsaccuracycompa-
rabletothebestmethodswhilereducingtoolusage
bynearly50%comparedtofullyautomaticbase-
lines. It also matches the Baseline (All Tools) in
accuracywhilesignificantlyloweringrelianceon
externaltools,reducingcomputationalcosts. Our
training-basedmethodfurtherenhancesefficiency
compared to Auto Tool, achieving better perfor-
mancewhilereducingtoolusage. Thisvalidatesthe
effectivenessofrefiningtoolinvocationalignment
withthemodel’sinternalknowledgeboundary.
5.3 OverconfidenceandOver-tool-reliance
Weanalyzehowimplicitmodelingshapemodelbe-
haviorbyadjustingtheSFTdataratio,whichrep-
resentstheproportionoftrainingsampleswithtool
invocation. Asthisratioincreases,themodel’scon-
fidence estimation and reliance on external tools
shift. Figure 3 illustrates how the SFT data ra-
tio influences both overconfidence and over-tool-
reliance. AhigherSFTdataratioincreasesreliance
on tools, leading to more tool invocation while
reducingthemodel’soverconfidenceinitsknowl-
edge. Conversely,alowerSFTdataratiodecreases
tool reliance but increases overconfidence. Each
datasetexhibitsanoptimalSFTdataratio,where
)%(
egatnecreP
Arithmetic + Calculator TriviaQA + RAG
100
80
60
Optimal: 0.3
Optimal: 0.4
40
20
0
0.0 0.5 1.0
Math + Reasoner
100
80
Overconfidence
60
Optimal: 0.3 Over-tool-reliance
40
Total issues
20
0
0.0 0.5 1.0
SFT Data Ratio
Figure3: Trade-offbetweenoverconfidenceandover-
tool-reliancewithdifferentSFTdataratios.
thiscombinedproportionisminimized,balancing
modelconfidenceandtooldependency. Thisturn-
ingpointinFigure3servesasaguidelineforop-
timal model selection. At this ratio, the model
maintains a well-calibrated knowledge boundary
whileminimizingunnecessarytoolusage.
5.4 InferenceTime
Sincetoolinvocationaddscomputationaloverhead,
weassessinferencecostbymeasuringactualexe-
cutiontime. UsingVLLM(Kwonetal.,2023)on
NVIDIAA800GPUs(seeAppendixEfordetailed
experimentalsetup),wecomputeper-sampleinfer-
encetimeandaggregatethetotalruntimeacrossthe
dataset. Figure4illustratesthetrade-offbetween
inference time and performance, where methods
positionedtowardstheupper-leftcornerachievea
morefavorablebalance. Ourapproachconsistently
demonstrates superior efficiency, attaining either
higherperformanceatthesameinferencetimeor
reduce latency while maintaining accuracy. By
optimizingtoolusage,ourmethodreducescompu-
tationalcostwhilemaintainingcomparableperfor-
mance, ensuring efficient real-world deployment
andmakingitwell-suitedforpracticalapplications.
5.5 AblationStudy
5.5.1 ImplictModelingMethods
To understand how implicit modeling affects our
utility, we perform an ablation study to see how
different Supervised Fine-Tuning (SFT) data ra-
tios impact the model’s behavior. The data ratio
17781

[TABLE]
 |  | 
 |  | 
 |  | 
Optimal | : 0.4 | 
 |  | 
[/TABLE]

[TABLE]
 |  | 
 |  | 
Optimal: 0 | .3 | 
 |  | 
 |  | 
[/TABLE]

[TABLE]
 |  |  | 
 |  |  | 
Optimal: 0 | .3 |  | 
 |  |  | 
 |  |  | 
[/TABLE]

---
### Page 7

Arithmetic+Calculator TriviaQA+RAG Math+Reasoner
Type Method
Acc ToolRate Utility(0.2) Acc ToolRate Utility(0.4) Acc ToolRate Utility(0.6)
↑ ↓ ↑ ↑ ↓ ↑ ↑ ↓ ↑
Llama3.18B
Baseline(w/otool) 63.0 0.0 63.0 62.5 0.0 62.5 51.4 0.0 51.4
Baseline(alltool) 99.0 100.0 79.0 95.8 100.0 55.8 96.2 100.0 36.2
Prompt-based Autotool 90.3 75.0 75.3 89.5 78.0 58.3 73.1 50.1 43.0
ICLtool(10-shot) 91.6 62.6 79.2 85.6 69.5 57.8 53.2 4.9 50.3
Rawlogits 90.7 54.6 79.8 74.3 16.9 67.5 59.0 9.9 53.1
P(True) 90.4 65.1 77.4 87.4 59.2 63.7 84.4 61.6 47.4
Uncertainty-based verb.1Stop-1 65.5 7.8 63.9 77.4 32.8 64.3 64.1 16.3 54.3
verb.2Stop-1 69.1 16.1 65.9 74.8 20.9 66.3 62.0 16.7 52.0
agreement(consistency) 77.3 22.4 72.8 87.3 45.7 69.0 71.7 28.5 54.6
IMPLICIT-LOGITS 80.0 33.7 73.3 74.5 24.6 64.7 85.5 56.7 51.5
Training-based E IM X P P L L I I C C I I T T - - C L O O N G S IT IS S TENCY 8 8 9 0 . . 5 1 6 3 5 0 . . 5 9 7 7 6 3 . . 4 9 7 7 5 7 . . 8 0 2 2 6 5 . . 8 1 6 6 5 7 . . 1 0 8 8 4 4 . . 9 4 4 5 7 1 . . 5 6 5 5 6 3 . . 4 6
IMPLICIT-ABSOLUTE 96.7 45.2 87.7 91.1 42.3 74.2 93.1 55.5 59.8
EXPLICIT-CONSISTENCY 90.7 61.7 78.4 76.9 25.9 66.5 84.1 45.7 56.7
EXPLICIT-ABSOLUTE 93.3 33.8 86.5 82.9 29.7 71.0 79.5 35.6 58.1
Qwen2.57B
Baseline(w/otool) 67.0 0.0 67.0 51.1 0.0 51.1 74.9 0.0 74.9
Baseline(alltool) 99.0 100.0 79.0 94.7 100.0 54.7 96.2 100.0 36.2
Prompt-based Autotool 95.7 83.4 79.0 90.4 89.6 54.6 77.1 24.5 62.4
ICLtool(10-shot) 91.2 32.9 84.6 74.5 33.8 61.0 75.1 1.8 74.0
Rawlogits 95.1 47.8 85.5 86.6 61.7 61.9 86.9 34.1 66.4
P(True) 94.2 63.4 81.5 79.1 53.1 57.9 86.0 30.7 67.6
Uncertainty-based verb.1Stop-1 68.9 4.9 67.9 81.2 55.9 58.8 75.6 6.9 71.5
verb.2Stop-1 78.9 22.4 74.4 79.5 51.5 58.9 83.9 20.2 71.8
agreement(consistency) 91.6 22.4 87.1 86.2 47.9 67.0 97.8 38.6 74.6
IMPLICIT-LOGITS 83.9 22.8 79.3 81.3 56.1 58.9 91.9 52.9 60.2
Training-based E IM X P P L L I I C C I I T T - - C L O O N G S IT IS S TENCY 8 8 4 2 . . 2 7 2 1 7 7 . . 2 2 7 7 8 9 . . 8 3 8 8 3 4 . . 2 2 6 5 0 8 . . 1 1 5 6 9 1 . . 2 0 9 9 2 6 . . 9 9 5 5 3 4 . . 9 9 6 6 0 4 . . 6 0
IMPLICIT-ABSOLUTE 97.6 37.9 90.1 90.7 59.1 67.1 93.9 29.0 76.5
EXPLICIT-CONSISTENCY 90.7 61.7 78.4 72.9 23.9 63.3 89.9 22.3 76.5
EXPLICIT-ABSOLUTE 97.3 28.8 91.5 80.3 30.3 68.2 90.1 21.2 77.4
Table1: Performancecomparisononthreetoolcallingscenarios. Theutilityistheoverallevaluationmetricof
accuracyandtoolrate. Alargerαindicatesahighercostsensitivityandagreaterpenaltyforinvokingtools.
ratiomakesthemodelanswerquestionsindepen-
dently,reducingcosts. Thekeyistofindtheright
balance so the model efficiently decides when to
use tools based on the situation. Figure 5 shows
how the data ratio affects the model’s utility. At
first,utilityincreasesastheratiogoesup,reaching
apeakbeforedropping. Thebestratioisdifferent
foreachdatasetanddependsonhowmuchthetool
costs. If tool costs are high, the optimal ratio is
lower. This shows that our implicit modeling ap-
proachhelpsthemodelmakesmartchoicesbased
ontaskcosts,balancingaccuracyandefficiency.
5.5.2 ExplicitModelingMethods
Unlike implicit approaches, explicit modeling al-
lowsthemodeltodirectlyoutputconfidencescores
alongsideitspredictions,enablingthreshold-based
Figure4: Performancevs. inferencetime(seconds).
decision-making for tool invocation. To further
evaluateitseffectiveness,wecompareexplicitmod-
meansthepercentageoftrainingexampleswhere eling with uncertainty-based baselines, as both
themodelusesatooltogettheanswerinsteadof methods fundamentally rely on confidence esti-
answering on its own. We keep the total dataset mation to determine knowledge boundaries. To
size the same but change this ratio to see how it ensureafaircomparison,weadjusttheconfidence
affectsthemodel’spreferenceforusingtoolsoran- thresholdtocontrolthetoolinvocationratio,sys-
sweringdirectly. Thishelpsusfindthebestbalance tematicallyvaryingthethresholdtoassessmodel
basedoncost. Whenusingatoolischeap,ahigher performance at different levels of tool usage. As
ratiomakesthemodelusetoolsmoreoften,which shown in Figure 6 illustrates the relationship be-
improvesaccuracybyusingexternalresources. On tweentoolinvocationrateandmodelperformance
theotherhand,iftoolusageisexpensive,alower acrossvariousconfidencethresholds. Explicitmod-
17782

[TABLE]
62.5 0.0 62.5
95.8 100.0 55.8
89.5 78.0 58.3
85.6 69.5 57.8
74.3 16.9 67.5
87.4 59.2 63.7
77.4 32.8 64.3
74.8 20.9 66.3
87.3 45.7 69.0
74.5 24.6 64.7
75.8 26.8 65.1
77.0 25.1 67.0
91.1 42.3 74.2
76.9 25.9 66.5
82.9 29.7 71.0
[/TABLE]

[TABLE]
51.1 0.0 51.1
94.7 100.0 54.7
90.4 89.6 54.6
74.5 33.8 61.0
86.6 61.7 61.9
79.1 53.1 57.9
81.2 55.9 58.8
79.5 51.5 58.9
86.2 47.9 67.0
81.3 56.1 58.9
83.2 60.1 59.2
84.2 58.1 61.0
90.7 59.1 67.1
72.9 23.9 63.3
80.3 30.3 68.2
[/TABLE]

---
### Page 8

90
80
70
60
50
40
30
0.0 0.2 0.4 0.6 0.8 1.0
SFT Data Ratio
ytilitU
Arithmetic + Calculator
90
80
70
60
50
40
30
0.0 0.2 0.4 0.6 0.8 1.0
SFT Data Ratio
ytilitU
TriviaQA + RAG
90
80
70
60
50
40
30
0.0 0.2 0.4 0.6 0.8 1.0
SFT Data Ratio
ytilitU
Math + Reasoner
Figure5: EffectofSFTDataRatioonUtility. Theratiorepresentstheproportionoftrainingsamplesinwhichthe
modelinvokesatoolratherthanansweringdirectly.
1.00
0.95
0.90
0.85
0.80
0.75
0.70
0.65
0.60
0.00 0.25 0.50 0.75 1.00
ycaruccA
Arithmetic + Calculator TriviaQA + RAG
1.00 100
0.95
0.90 80
0.85
0.80 60
0.75
40 0.70
0.65 20
0.60
0.55 0
0.00 0.25 0.50 0.75 1.00 0.0 0.2 0.4 0.6 0.8 1.0
Math + Reasoner 1.00
0.95
0.90 agreement(consistency)
0.85
P(True)
0.80 Raw Logits
0.75
verb. 1S top-1 0.70 verb. 2S top-1
0.65 EXPLICIT-ABSOLUTE
0.60
0.55
0.50
0.00 0.25 0.50 0.75 1.00
Tool Usage Ratio
Figure6: Comparisonoftoolinvocationstrategies: ex-
plicitmodelingvs. uncertainty-basedbaselines.
eling consistently outperforms uncertainty-based
baselines at all invocation ratios, demonstrating
itsabilitytoprovideamorereliableestimationof
knowledge boundaries. The performance gap re-
mainsstable,highlightingtherobustnessofexplicit
confidence modeling. By leveraging these confi-
dence scores, our approach enables finer control
overtoolinvocation,optimizingtasksuccesswhile
reducingunnecessarycomputationaloverhead.
5.6 KnowledgeBoundaryAlignment
Toexaminewhetherthemodellearnsaboutknowl-
edge boundary, we compare our method with
auto_toolintermsoftoolinvocationdistribution.
Figure 7 presents tool usage across different ac-
curacy levels. Higher accuracy reflects a better
understanding of the problem. An ideal model
should rely on tools for challenging cases while
minimizingtooluseforconfidentlyansweredques-
tions. However,auto_toolexhibitsanearlyuni-
form tool invocation pattern, suggesting it lacks
awarenessofitsknowledgeboundaries. Incontrast,
)%(
egasU
looT
Arithmetic + Calculator TriviaQA + RAG
100
80
60
40
20
0
0.0 0.2 0.4 0.6 0.8 1.0
Math + Reasoner
100
80
60 auto_tool (Tool Usage)
auto_tool (Over-tool-reliance)
IMPLICIT-ABSOLUTE (Tool Usage) 40 IMPLICIT-ABSOLUTE (Over-tool-reliance)
20
0
0.0 0.2 0.4 0.6 0.8 1.0
Average Accuracy
Figure 7: Comparison of tool usage and over-tool-
relianceacrossdifferentaccuracylevels.
ourmethodshowsagradualdeclineintoolusage
asaccuracyincreases,indicatingadaptivetoolin-
vocationbasedonknowledgeconfidence. Wealso
analyzeover-tool-reliance,wherethemodeluses
tools unnecessarily despite being capable of an-
sweringcorrectly. Figure7showsthatthebaseline
exhibits increasing over-tool-reliance with accu-
racy, leading to unnecessary computational over-
head. Conversely, our method reduces over-tool-
reliance,enablingmoreintelligentinvocations.
6 Conclusion
In this work, we introduced a novel approach to
improveLLMs’decision-makingregardingwhen
andhowtouseexternaltools. Byincorporatingthe
conceptofan"uncertainregion"andprobabilistic
knowledge boundary estimation, our framework
enables more informed and efficient tool usage.
Throughextensiveexperiments,wedemonstrated
that our approach reduces unnecessary tool calls,
improvingperformanceandcost-effectiveness. By
combining implicit and explicit modeling tech-
17783

[TABLE]
 |  |  |  |  |  | 
 |  |  |  |  |  | 
 |  |  |  |  |  | 
 |  |  |  |  |  | 
 |  |  |  |  |  | 
 |  |  |  |  |  | 
[/TABLE]

[TABLE]
 |  |  |  |  |  | 
 |  |  |  |  |  | 
 |  |  |  |  |  | 
 |  |  |  |  |  | 
 |  |  |  |  |  | 
 |  |  |  |  |  | 
[/TABLE]

[TABLE]
 |  |  |  |  |  | 
 |  |  |  |  |  | 
 |  |  |  |  |  | 
 |  |  |  |  |  | 
 |  |  |  |  |  | 
 |  |  |  |  |  | 
[/TABLE]

[TABLE]
 |  |  | 
 |  |  | 
 |  |  | 
 |  |  | 
 |  |  | 
 |  |  | 
 |  |  | 
[/TABLE]

[TABLE]
 |  |  | 
 |  |  | 
 |  |  | 
 |  |  | 
 |  |  | 
 |  |  | 
 |  |  | 
[/TABLE]

[TABLE]
 |  |  |  |  |  |  |  |  |  |  |  |  | 
 |  |  |  |  |  |  |  |  |  |  |  |  | 
 |  |  |  |  |  |  |  |  |  |  |  |  | 
 |  |  |  |  |  |  |  |  |  |  |  |  | 
 |  |  |  |  |  |  |  |  |  |  |  |  | 
 |  |  |  |  |  |  |  |  |  |  |  |  | 
[/TABLE]

[TABLE]
 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | 
 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | 
 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | 
 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | 
 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | 
[/TABLE]

[TABLE]
 |  |  | 
 |  |  | 
 |  |  | 
 |  |  | 
 |  |  | 
 |  |  | 
 |  |  | 
 |  |  | 
[/TABLE]

[TABLE]
 |  |  |  |  |  |  |  |  |  |  |  |  |  | 
 |  |  |  |  |  |  |  |  |  |  |  |  |  | 
 |  |  |  |  |  |  |  |  |  |  |  |  |  | 
 |  |  |  |  |  |  |  |  |  |  |  |  |  | 
 |  |  |  |  |  |  |  |  |  |  |  |  |  | 
 |  |  |  |  |  |  |  |  |  |  |  |  |  | 
[/TABLE]

---
### Page 9

niques, we provide the model with greater flexi- betoobig? InProceedingsofthe2021ACMconfer-
bility in real-time decisions. Our work advances enceonfairness,accountability,andtransparency,
pages610–623.
LLMs’toolintelligence,ensuringmorejudicious
andefficienttoolinvocation. Futureworkcanex- Xingyu Chen, Jiahao Xu, Tian Liang, Zhiwei He,
plorefurtherrefinementsandbroaderapplications. Jianhui Pang, Dian Yu, Linfeng Song, Qiuzhi Liu,
MengfeiZhou, ZhuoshengZhang, etal.2024. Do
notthinkthatmuchfor2+3=? ontheoverthinking
Acknowledgments
ofo1-likellms. arXivpreprintarXiv:2412.21187.
ThisworkisfundedbytheChinaNSFCProjects HyungWonChung,LeHou,ShayneLongpre,Barret
(62120106006, 92370206, and U23B2057) and Zoph,YiTay,WilliamFedus,YunxuanLi,Xuezhi
Wang,MostafaDehghani,SiddharthaBrahma,etal.
Shanghai Municipal Science and Technology
2022. Scalinginstruction-finetunedlanguagemodels.
Projects(2021SHZDZX0102and25X010202846).
arXivpreprintarXiv:2210.11416.
Limitations Ganqu Cui, Lifan Yuan, Ning Ding, Guanming Yao,
WeiZhu,YuanNi,GuotongXie,ZhiyuanLiu,and
Thisworkprimarilyproposesanalignmentframe- MaosongSun.2023. Ultrafeedback: Boostinglan-
guage models with high-quality feedback. arXiv
work for efficient tool invocation, evaluated
preprintarXiv:2310.01377.
throughexperimentsonthreedatasets. Ontheone
hand,thenumberoftoolsusedintheseexperiments DeepSeek-AI,DayaGuo,DejianYang,HaoweiZhang,
JunxiaoSong,RuoyuZhang,RunxinXu,QihaoZhu,
islimited,withaselectionofthreerepresentative
ShirongMa,PeiyiWang,XiaoBi,XiaokangZhang,
tools: amathematicalcalculator,asearchengine,
XingkaiYu,YuWu,Z.F.Wu,ZhibinGou,Zhihong
andanexternallargemodel. Thischoiceismoti- Shao,ZhuoshuLi,ZiyiGao,AixinLiu,BingXue,
vatedbythefactthatmosttoolspossesshighlyspe- BingxuanWang,BochaoWu,BeiFeng,ChengdaLu,
Chenggang Zhao, Chengqi Deng, Chenyu Zhang,
cific knowledge. For example, tools that retrieve
Chong Ruan, Damai Dai, Deli Chen, Dongjie Ji,
weather information for a particular day contain
Erhang Li, Fangyun Lin, Fucong Dai, Fuli Luo,
knowledge that does not overlap with that of the GuangboHao,GuantingChen,GuoweiLi,H.Zhang,
model, requiring the model to invoke the tool to Han Bao, Hanwei Xu, Haocheng Wang, Honghui
complete the task. On the other hand, different Ding, Huajian Xin, Huazuo Gao, Hui Qu, Hui Li,
Jianzhong Guo, Jiashi Li, Jiawei Wang, Jingchang
modelsandknowledgesourcescanalsobeframed
Chen, JingyangYuan, JunjieQiu, JunlongLi, J.L.
astools,meaningthatthediscussioninthiswork Cai,JiaqiNi,JianLiang,JinChen,KaiDong,Kai
onmodelingknowledgeboundariesremainshighly Hu, Kaige Gao, Kang Guan, Kexin Huang, Kuai
valuable. Inaddition,theexperimentsinthiswork Yu,LeanWang,LecongZhang,LiangZhao,Litong
Wang,LiyueZhang,LeiXu,LeyiXia,Mingchuan
wereconductedononlytwoopen-sourcemodels,
Zhang, Minghua Zhang, Minghui Tang, Meng Li,
asobtainingbaselinedataforclosed-sourcemodels
Miaojun Wang, Mingming Li, Ning Tian, Panpan
presentssignificantchallenges. Forinstance,meth- Huang,PengZhang,QianchengWang,QinyuChen,
ods such as uncertainty estimation often require QiushiDu, RuiqiGe, RuisongZhang, RuizhePan,
Runji Wang, R. J. Chen, R. L. Jin, Ruyi Chen,
accesstospecifictokenlogits,whicharedifficult
Shanghao Lu, Shangyan Zhou, Shanhuang Chen,
to obtain for proprietary models. This limitation
ShengfengYe,ShiyuWang,ShuipingYu,Shunfeng
affectsthegeneralizabilityoftheexperimentalre- Zhou,ShutingPan,S.S.Li,ShuangZhou,Shaoqing
sults,astheperformanceofclosed-sourcemodels Wu,ShengfengYe,TaoYun,TianPei,TianyuSun,
T. Wang, Wangding Zeng, Wanjia Zhao, Wen Liu,
maydifferinwaysthatcannotbecapturedwithout
WenfengLiang, WenjunGao, WenqinYu, Wentao
directaccesstotheirinternals.
Zhang,W.L.Xiao,WeiAn,XiaodongLiu,Xiaohan
Wang,XiaokangChen,XiaotaoNie,XinCheng,Xin
Liu,XinXie,XingchaoLiu,XinyuYang,XinyuanLi,
References XuechengSu,XuhengLin,X.Q.Li,XiangyueJin,
XiaojinShen,XiaoshaChen,XiaowenSun,Xiaoxi-
JoshAchiam,StevenAdler,SandhiniAgarwal,Lama angWang,XinnanSong,XinyiZhou,XianzuWang,
Ahmad, Ilge Akkaya, Florencia Leoni Aleman, XinxiaShan,Y.K.Li,Y.Q.Wang,Y.X.Wei,Yang
DiogoAlmeida,JankoAltenschmidt,SamAltman, Zhang, Yanhong Xu, Yao Li, Yao Zhao, Yaofeng
ShyamalAnadkat,etal.2023. Gpt-4technicalreport. Sun,YaohuiWang,YiYu,YichaoZhang,YifanShi,
arXivpreprintarXiv:2303.08774. YiliangXiong,YingHe,YishiPiao,YisongWang,
YixuanTan,YiyangMa,YiyuanLiu,YongqiangGuo,
EmilyMBender, TimnitGebru, AngelinaMcMillan- YuanOu,YuduanWang,YueGong,YuhengZou,Yu-
Major, and Shmargaret Shmitchell. 2021. On the jiaHe, YunfanXiong, YuxiangLuo, YuxiangYou,
dangersofstochasticparrots: Canlanguagemodels YuxuanLiu,YuyangZhou,Y.X.Zhu,YanhongXu,
17784

---
### Page 10

YanpingHuang,YaohuiLi,YiZheng,YuchenZhu, Cheng-YuHsieh,Si-AnChen,Chun-LiangLi,Yasuhisa
Yunxian Ma, Ying Tang, Yukun Zha, Yuting Yan, Fujii, Alexander Ratner, Chen-Yu Lee, Ranjay Kr-
Z.Z.Ren,ZehuiRen,ZhangliSha,ZheFu,Zhean ishna, and Tomas Pfister. 2023. Tool documenta-
Xu, Zhenda Xie, Zhengyan Zhang, Zhewen Hao, tionenableszero-shottool-usagewithlargelanguage
ZhichengMa,ZhigangYan,ZhiyuWu,ZihuiGu,Zi- models. ArXivpreprint,abs/2308.00675.
jiaZhu,ZijunLiu,ZilinLi,ZiweiXie,ZiyangSong,
Zizheng Pan, Zhen Huang, Zhipeng Xu, Zhongyu YueHuang,JiawenShi,YuanLi,ChenruiFan,Siyuan
Zhang,andZhenZhang.2025. Deepseek-r1: Incen- Wu, Qihui Zhang, Yixin Liu, Pan Zhou, Yao Wan,
tivizing reasoning capability in llms via reinforce- NeilZhenqiangGong,etal.2023. Metatoolbench-
mentlearning. Preprint,arXiv:2501.12948. markforlargelanguagemodels: Decidingwhether
to use tools and which to use. arXiv preprint
Ning Ding, Yulin Chen, Bokai Xu, Yujia Qin, Zhi arXiv:2310.03128.
Zheng,ShengdingHu,ZhiyuanLiu,MaosongSun,
andBowenZhou.2023. EnhancingChatLanguage QiaoJin,YifanYang,QingyuChen,andZhiyongLu.
ModelsbyScalingHigh-qualityInstructionalCon- 2024. GeneGPT:augmentinglargelanguagemodels
versations. ArXivpreprint,abs/2305.14233. withdomaintoolsforimprovedaccesstobiomedical
information. Bioinformatics,40(2):btae075.
AbhimanyuDubey,AbhinavJauhri,AbhinavPandey,
AbhishekKadian,AhmadAl-Dahle,AieshaLetman, MandarJoshi,EunsolChoi,DanielSWeld,andLuke
Akhil Mathur, Alan Schelten, Amy Yang, Angela Zettlemoyer.2017. Triviaqa: Alargescaledistantly
Fan,etal.2024. Thellama3herdofmodels. arXiv supervisedchallengedatasetforreadingcomprehen-
preprintarXiv:2407.21783. sion. arXivpreprintarXiv:1705.03551.
Leo Gao, John Schulman, and Jacob Hilton. 2023a.
SauravKadavath,TomConerly,AmandaAskell,Tom
Scaling laws for reward model overoptimization.
Henighan, Dawn Drain, Ethan Perez, Nicholas
InInternationalConferenceonMachineLearning,
Schiefer,ZacHatfield-Dodds,NovaDasSarma,Eli
pages10835–10866.PMLR.
Tran-Johnson, et al. 2022. Language models
(mostly) know what they know. arXiv preprint
Yunfan Gao, Yun Xiong, Xinyu Gao, Kangxiang Jia,
arXiv:2207.05221.
JinliuPan,YuxiBi,YiDai,JiaweiSun,andHaofen
Wang. 2023b. Retrieval-augmented generation for
Woosuk Kwon, Zhuohan Li, Siyuan Zhuang, Ying
large language models: A survey. arXiv preprint
Sheng, Lianmin Zheng, Cody Hao Yu, Joseph E.
arXiv:2312.10997.
Gonzalez, Hao Zhang, and Ion Stoica. 2023. Effi-
cientmemorymanagementforlargelanguagemodel
Gemini Team. 2023. Gemini: A Family of
servingwithpagedattention. InProceedingsofthe
Highly Capable Multimodal Models. Preprint,
ACMSIGOPS29thSymposiumonOperatingSystems
arXiv:2312.11805.
Principles.
Amelia Glaese, Nat McAleese, Maja Trebacz, John
Jimmy Lin, Xueguang Ma, Sheng-Chieh Lin, Jheng-
Aslanides,VladFiroiu,TimoEwalds,MaribethRauh,
HongYang,RonakPradeep,andRodrigoNogueira.
LauraWeidinger,MartinChadwick,PhoebeThacker,
2021. Pyserini: A python toolkit for reproducible
etal.2022. Improvingalignmentofdialogueagents
informationretrievalresearchwithsparseanddense
via targeted human judgements. arXiv preprint
representations. In Proceedings of the 44th Inter-
arXiv:2209.14375.
nationalACMSIGIRConferenceonResearchand
DevelopmentinInformationRetrieval,pages2356–
AnchunGui,JianLi,YongDai,NanDu,andHanXiao.
2362.
2024. Lookbeforeyouleap:Towardsdecision-aware
andgeneralizabletool-usageforlargelanguagemod-
TiedongLiuandBryanKianHsiangLow.2023. Goat:
els. arXivpreprintarXiv:2402.16696.
Fine-tuned llama outperforms gpt-4 on arithmetic
Tanmay Gupta and Aniruddha Kembhavi. 2023. Vi- tasks. arXivpreprintarXiv:2305.14201.
sualprogramming: Compositionalvisualreasoning
withouttraining. InInProceedingsoftheIEEE/CVF Qing Lyu, Kumar Shridhar, Chaitanya Malaviya,
ConferenceonComputerVisionandPatternRecog- Li Zhang, Yanai Elazar, Niket Tandon, Mari-
nition(CVPR2023),pages14953–14962. anna Apidianaki, Mrinmaya Sachan, and Chris
Callison-Burch. 2024. Calibrating large language
ShiboHao,TianyangLiu,ZhenWang,andZhitingHu. models with sample consistency. arXiv preprint
2023. ToolkenGPT:AugmentingFrozenLanguage arXiv:2402.13904.
Models with Massive Tools via Tool Embeddings.
ArXivpreprint,abs/2305.11554. LongOuyang,JeffreyWu,XuJiang,DiogoAlmeida,
CarrollWainwright,PamelaMishkin,ChongZhang,
DanHendrycks,CollinBurns,SauravKadavath,Akul SandhiniAgarwal,KatarinaSlama,AlexRay,etal.
Arora, Steven Basart, Eric Tang, Dawn Song, and 2022. Training languagemodelsto followinstruc-
Jacob Steinhardt. 2021. Measuring mathematical tions with human feedback. Advances in Neural
problemsolvingwiththemathdataset. NeurIPS. InformationProcessingSystems,35:27730–27744.
17785

---
### Page 11

Shishir G. Patil, Tianjun Zhang, Xin Wang, and overtheplace: Ontheunderthinkingofo1-likellms.
Joseph E. Gonzalez. 2023. Gorilla: Large Lan- arXivpreprintarXiv:2501.18585.
guageModelConnectedwithMassiveAPIs. ArXiv
preprint,abs/2305.15334. JasonWei, MaartenBosma, VincentY.Zhao, Kelvin
Guu, Adams Wei Yu, Brian Lester, Nan Du, An-
YujiaQin,ShihaoLiang,YiningYe,KunlunZhu,Lan
drew M. Dai, and Quoc V. Le. 2022. Finetuned
Yan,YaxiLu,YankaiLin,XinCong,XiangruTang,
Language Models are Zero-Shot Learners. In The
BillQian,SihanZhao,RunchuTian,RuobingXie,
TenthInternationalConferenceonLearningRepre-
Jie Zhou, Mark Gerstein, Dahai Li, Zhiyuan Liu,
sentations, ICLR 2022, Virtual Event, April 25-29,
and Maosong Sun. 2023. ToolLLM: Facilitating
2022.OpenReview.net.
Large Language Models to Master 16000+ Real-
worldAPIs. Preprint,arXiv:2307.16789.
Can Xu, Qingfeng Sun, Kai Zheng, Xiubo Geng,
PuZhao,JiazhanFeng,ChongyangTao,andDaxin
RafaelRafailov,ArchitSharma,EricMitchell,Christo-
Jiang. 2023. WizardLM: Empowering Large Lan-
pherDManning,StefanoErmon,andChelseaFinn.
guage Models to Follow Complex Instructions.
2024. Directpreferenceoptimization:Yourlanguage
Preprint,arXiv:2304.12244.
modelissecretlyarewardmodel. AdvancesinNeu-
ralInformationProcessingSystems,36.
Hongshen Xu, Su Zhu, Zihan Wang, Hang Zheng,
VictorSanh,AlbertWebson,ColinRaffel,StephenH DaMa,RuishengCao,ShuaiFan,LuChen,andKai
Bach, Lintang Sutawika, Zaid Alyafeai, Antoine Yu.2024a. Reducingtoolhallucinationviareliability
Chaffin, Arnaud Stiegler, Teven Le Scao, Arun alignment. arXivpreprintarXiv:2412.04141.
Raja, et al. 2021. Multitask prompted training en-
ableszero-shottaskgeneralization. arXivpreprint HongshenXu,ZichenZhu,DaMa,SituoZhang,Shuai
arXiv:2110.08207. Fan, Lu Chen, and Kai Yu. 2024b. Rejection im-
provesreliability: Trainingllmstorefuseunknown
TimoSchick,JaneDwivedi-Yu,RobertoDessì,Roberta questionsusingrlfromknowledgefeedback. arXiv
Raileanu,MariaLomeli,LukeZettlemoyer,Nicola preprintarXiv:2403.18349.
Cancedda,andThomasScialom.2023. Toolformer:
Language Models Can Teach Themselves to Use
Linyao Yang, Hongyang Chen, Zhao Li, Xiao Ding,
Tools. ArXivpreprint,abs/2302.04761.
andXindongWu.2023a. ChatGPTisnotEnough:
EnhancingLargeLanguageModelswithKnowledge
IreneSolaimanandChristyDennison.2021. Process
GraphsforFact-awareLanguageModeling. ArXiv
foradaptinglanguagemodelstosociety(palms)with
preprint,abs/2306.11489.
values-targeteddatasets. AdvancesinNeuralInfor-
mationProcessingSystems,34:5861–5873.
Yuchen Yang, Houqiang Li, Yanfeng Wang, and
Nisan Stiennon, Long Ouyang, Jeffrey Wu, Daniel YuWang.2023b. Improvingthereliabilityoflarge
Ziegler, Ryan Lowe, Chelsea Voss, Alec Radford, languagemodelsbyleveraginguncertainty-awarein-
DarioAmodei,andPaulFChristiano.2020. Learn- contextlearning. arXivpreprintarXiv:2310.04782.
ingtosummarizewithhumanfeedback. Advances
inNeuralInformationProcessingSystems,33:3008– YuqingYang,EthanChern,XipengQiu,GrahamNeu-
3021. big,andPengfeiLiu.2023c. Alignmentforhonesty.
arXivpreprintarXiv:2312.07000.
QiaoyuTang,ZiliangDeng,HongyuLin,XianpeiHan,
QiaoLiang,andLeSun.2023. ToolAlpaca: General- Zhewei Yao, Reza Yazdani Aminabadi, Olatunji
izedToolLearningforLanguageModelswith3000 Ruwase, Samyam Rajbhandari, Xiaoxia Wu, Am-
SimulatedCases. Preprint,arXiv:2306.05301. marAhmadAwan,JeffRasley,MinjiaZhang,Cong-
long Li, Connor Holmes, et al. 2023. Deepspeed-
Katherine Tian, Eric Mitchell, Allan Zhou, Archit
chat: Easy, fast and affordable rlhf training of
Sharma,RafaelRafailov,HuaxiuYao,ChelseaFinn,
chatgpt-like models at all scales. arXiv preprint
andChristopherDManning.2023. Justaskforcali-
arXiv:2308.01320.
bration: Strategiesforelicitingcalibratedconfidence
scoresfromlanguagemodelsfine-tunedwithhuman
Andy Zeng, Maria Attarian, Brian Ichter, Krzysztof
feedback. arXivpreprintarXiv:2305.14975.
Choromanski, Adrian Wong, Stefan Welker, Fed-
ericoTombari,AveekPurohit,MichaelRyoo,Vikas
XinpengWang,ShitongDuan,XiaoyuanYi,JingYao,
Sindhwani,etal.2022. Socraticmodels: Compos-
ShanlinZhou,ZhihuaWei,PengZhang,Dongkuan
ingzero-shotmultimodalreasoningwithlanguage.
Xu, Maosong Sun, and Xing Xie. 2024. On the
arXivpreprintarXiv:2204.00598.
essence and prospect: An investigation of align-
ment approaches for big models. arXiv preprint
arXiv:2403.04204. ShengyuZhang,LinfengDong,XiaoyaLi,SenZhang,
XiaofeiSun,ShuheWang,JiweiLi,RunyiHu,Tian-
YueWang,QiuzhiLiu,JiahaoXu,TianLiang,Xingyu weiZhang,FeiWu,etal.2023. Instructiontuning
Chen, Zhiwei He, Linfeng Song, Dian Yu, Juntao forlargelanguagemodels: Asurvey. arXivpreprint
Li,ZhuoshengZhang,etal.2025. Thoughtsareall arXiv:2308.10792.
17786

---
### Page 12

Yuxiang Zhang, Jing Chen, Junjie Wang, Yaxin Liu, decisionsguidedpurelybypromptinstructions. It
Cheng Yang, Chufan Shi, Xinyu Zhu, Zihao Lin, offersanaturalandcompetitivebaselineforcom-
HanwenWan,YujiuYang,etal.2024. Toolbehonest:
parison with approaches that incorporate explicit
A multi-level hallucination diagnostic benchmark
confidencetrainingorreinforcement.
for tool-augmented large language models. arXiv
preprintarXiv:2406.20015.
ICLTool(10-ShotIn-ContextLearning) This
Yuanhang Zheng, Peng Li, Ming Yan, Ji Zhang, Fei methodextendstheAutoToolbaselinebyprepend-
Huang, and Yang Liu. 2024. Budget-constrained ing10in-contextexamples(5correctanswerswith-
tool learning with planning. arXiv preprint
out tools, and 5 correct answers with tools) that
arXiv:2402.15960.
demonstratewhentouseoravoidtoolinvocation.
The goal of this baseline is to assess whether the
A Prompt-basedMethods modelcanlearnatool-usedecisionpolicyimplic-
itly from in-context demonstrations. By provid-
We implement four prompt-based baseline meth-
ing examples of both high-confidence (tool-free)
odstofacilitateafairandinterpretablecomparison
andlow-confidence(tool-required)responses,the
acrossvaryingtool-usestrategies. Thesebaselines
modelisexpectedtogeneralizeandapplysimilar
aredesignedtorepresentintuitiveandcommonly
decisioncriteriatonewinputs.
useddecisionpatternsalongthespectrumoftool
accessibilityandreliance. Below, weprovidede- B UncertaintyEstimationMethods
taileddescriptionsandthedesignrationaleforeach
Thissectionprovidesacomprehensiveoverviewof
baseline.
theuncertaintyestimationtechniquesemployedin
Baseline(w/otool) Inthissetting,themodelis our study. These methods aim to quantify model
instructed to answer each question using only its confidenceinitspredictions,helpingregulatetool
internalparametricknowledge,withoutaccessto invocationanddecision-making.
anyexternaltool. Thisbaselineservestoevaluate
RawLogits. Thisapproachestimatesconfidence
the model’s raw performance without any form
usingthemodel’slogitvalues,specificallybycom-
of external assistance. It provides a lower bound
putingtheexponentialoftheaveragelogprobabil-
forperformance,isolatingthecontributionofthe
ityofthegeneratedtokens. Thismetricismathe-
model’sinternalmemory. Moreover, itallowsus
maticallyequivalenttothereciprocalofperplexity,
to quantify the incremental benefits gained from
wherelowerperplexityindicateshigherconfidence,
toolusageandtoidentifyscenarioswheretoolsare
effectivelycapturinghowcertainthemodelisinits
essentialforaccurateresponses.
prediction.
Baseline (all tool) The model is required to al-
Agreement (Consistency-based). In this
ways utilize external tool outputs—such as re-
method, confidence is determined by measuring
trieveddocumentsorcalculatorresults—whengen-
the proportion of generated responses that align
erating an answer, irrespective of its confidence
with the most frequently predicted answer. A
level. This baseline simulates an over-reliance
higher agreement percentage suggests greater
on tools, representing a naïve strategy where the
internal consistency in the model’s responses,
modeldefaultstotoolusageregardlessofnecessity.
therebyindicatingastrongerlevelofconfidencein
It approximates an upper bound on task perfor-
itsgeneratedoutput.
manceundertheassumptionthattooloutputsare
generallyhelpful. Atthesametime,ithighlights P(True). This method involves prompting the
thetrade-offbetweenperformanceandtoolusage model to explicitly assess the correctness of its
cost,particularlyinsettingssensitivetolatencyor own response. The confidence score is derived
resourceconstraints. from the normalized probability assigned to the
‘True’token,reflectingthemodel’sself-evaluated
AutoTool(Zero-Shot) Themodelispromptedto
likelihoodthatitsansweriscorrect.
makeabinarydecisiononwhethertoinvokeatool,
basedsolelyonitsinternalconfidence,withoutany VerbalizedConfidence: 1-StageTop-k(Verb. 1S
fine-tuningorin-contextexamples. Thisbaseline Top-k). In this one-stage approach, the model
evaluates the model’s zero-shot uncertainty esti- generatesthetopk candidateanswersalongwith
mationcapabilityanditsabilitytomaketool-use theirrespectiveprobabilitiesinasinglepass. The
17787

---
### Page 13

highest-rankedansweranditsassignedprobability predictedanswer. Ahigheragreementpercentage
serveasanindicatorofconfidence,offeringadirect suggestsgreaterinternalconsistencyinthemodel’s
estimationofthemodel’scertaintyinitsresponse. responses, thereby indicating a stronger level of
confidenceinitsgeneratedoutput.
VerbalizedConfidence: 2-StageTop-k(Verb. 2S
Top-k). Unlikethesingle-stagemethod,thistwo- ABSOLUTE Thismethodestimatesthemodel’s
stage approach first prompts the model to gener- confidencebymeasuringtheproportionofgener-
atemultiplecandidateanswersandthenseparately atedresponsesthatalignwithexternalsupervision
assigns probabilities to each of them in a second (i.e.,theground-truthlabels). Itusesexternalsig-
inferencestep. Thefinalconfidencescoreiscom- nalstocalibratethemodel’sconfidence.
putedbasedontheseprobabilities,allowingfora
refinedestimationthataccountsforpotentialself- D ExperimentalSetup
correction.
Theseuncertaintyestimationtechniquesplaya ArithmeticComputation. Forarithmetictasks,
crucialroleincalibratingtoolinvocationdecisions, weuseadatasetconsistingof10,000trainingsam-
ensuringthatexternaltoolsareutilizedeffectively plesand1,000testsamples. Toensurethequality
basedonthemodel’sconfidenceinitsownpredic- ofgeneratedarithmeticexpressions, wefilterout
tions. To optimize utility, we sort all confidence any syntactically incorrect or malformed expres-
scoresacrossresponsesanduseeachuniquescore sions that do not conform to standard arithmetic
asapotentialthreshold,systematicallyevaluating formats. Symbolic computation is performed us-
itsimpactontoolinvocation. ing the SymPy library, which provides a robust
frameworkforsymbolicmathematicsandequation
C TrainingDetails evaluation.
We use two baseline models: LLAMA-3.1-
Knowledge-based QA (TriviaQA). For
8B-INSTRUCTandQWEN-2.5-7B-INSTRUCT.To
knowledge-based question answering, we ran-
align with our experimental setup, we customize
domly select 10,000 training instances from the
theDeepSpeed-Chat(Yaoetal.,2023)framework.
full TriviaQA training set. The retrieval system
The training process adopts a learning rate of
is employed only during inference and does
5 10 5 andabatchsizeof128. Allothertrain-
× − not participate in training. During training, the
ing parameters are set to the default parameters
model is only exposed to the tool invocation
in DeepSpeed-Chat. By default, 10,000 samples
format, but actual retrieval is not performed.
areusedforSupervisedFine-Tuning. Allmodels
We follow the Pyserini setup for TriviaQA and
undergotrainingfor2epochsonA800GPUs.
utilize a sparse retriever to retrieve the top 100
We train our models by leveraging the confi-
highest-scoring passages. To improve retrieval
dence scores estimated from the aforementioned
accuracy, we further filter passages that contain
methods. Specifically, the model is trained us-
the correct answer and refine the selection using
ing these different confidence estimation strate-
ChatGPT, eliminating irrelevant noisy passages.
gies—LOGITS, CONSISTENCY, and ABSO-
This ensures that the retrieved information is
LUTE—as supervisory signals to guide and cal-
reliable,preventingerroneoustoolinvocationfrom
ibrateitslearningprocess.
negativelyimpactingfinalperformance.
LOGITS Thisapproachestimatesconfidenceus-
ComplexReasoning(MATH). Formathemati-
ingthemodel’slogitvalues,specificallybycomput-
calproblem-solving,weprocesstheMATHdataset
ingtheexponentialoftheaveragelogprobability
following its original settings. We utilize a total
ofthegeneratedtokens. Thismetricismathemat-
of 7500 training samples and 5000 test samples,
ically equivalent to the reciprocal of perplexity,
adheringstrictlytothedataset’sofficialevaluation
wherelowerperplexityindicateshigherconfidence,
protocoltoensureconsistencyandcomparability
effectivelycapturinghowcertainthemodelisinits
withpriorwork. WeemployDeepSeek-R1(671B)
prediction.
as the external reasoning model, deploying it lo-
CONSISTENCY Inthismethod,confidenceis callyusingVLLMonaclusterof32NVIDIAA800
determinedbymeasuringtheproportionofgener- GPU.Themodeloperatesinazero-shotsetting. To
atedresponsesthatalignwiththemostfrequently mitigateexcessiveinferencelatency,weinstructthe
17788

---
### Page 14

model to generate concise responses while main-
tainingreasoningcompleteness. Despitethiscon-
straint, DeepSeek-R1 still significantly surpasses
ourprimarymodelsinresponsetime.
E InferenceTimeExperimentalSetup
For inference time evaluation, we employ the
VLLM framework and conduct experiments on
two NVIDIA A800 GPUs. To obtain a precise
measurementofrawinferencelatency,weprocess
input samples sequentially, without applying any
parallelization techniques such as batching. We
measure only the pure inference time, excluding
anyoverheadfromdataloading. Allotherparame-
tersremainattheirdefaultsettings,andthemodel
is loaded in bfloat16 format to optimize memory
usagewhilepreservingnumericalprecision.
F PromptsUsedinExperiments
F.1 PromptsUsedinDifferentPrompt-based
Methods
The prompts used for different datasets are pre-
sented in the following sections. Table 2 shows
thepromptsfortheMATHdataset,Table3con-
tainsthepromptsfortheArithmeticdataset,and
Table 4 presents the prompts for the TriviaQA
dataset.
F.1.1 PromptsforMATHDataset
Table2liststhepromptsusedfordifferentmethods
whenevaluatingtheMATHdataset.
F.1.2 PromptsforArithmeticDataset
Table3liststhepromptsusedfordifferentmethods
whenevaluatingtheArithmeticdataset.
F.1.3 PromptsforTriviaQADataset
Table4liststhepromptsusedfordifferentmethods
whenevaluatingtheTriviaQAdataset.
F.2 PromptsUsedinDifferent
Uncertainty-basedMethods
ThepromptsareshowninTable5.
F.3 QuestionTemplates
Theexamplesofarithmeticquestiontemplatesare
shownin 6.
17789

---
### Page 15

Baseline(w/otool)-MATH
Giventhefollowingproblem,breakitdownintostepsandreasonthrougheachpartbeforearrivingatafinalconclusion.
YourfinalanswerMUSTbeenclosedin\boxed{}.
Problem:{question}
Baseline(alltool)-MATH
Giventhefollowingproblem,breakitdownintostepsandreasonthrougheachpartbeforearrivingatafinalconclusion.
YourfinalanswerMUSTbeenclosedin\boxed{}.
Problem:{question}
AutoTool-MATH
Giventhefollowingproblem.Ifyoucansolveitdirectlywithconfidence,yourfinalanswermustbein\boxed{}format.
Ifyoucannotsolveitdirectly,callthetoolimmediatelywithoutreasoning,usingthisformat:
{{
"tool_name":"math_solver"
}}
Problem:{question}
ICLTool(10-shot)-MATH
Giventhefollowingproblem.Ifyoucansolveitdirectlywithconfidence,yourfinalanswermustbein\boxed{}format.
Ifyoucannotsolveitdirectly,callthetoolimmediatelywithoutreasoning,usingthisformat:
{{
"tool_name":"math_solver"
}}
Examples:{example}
Problem:{question}
Table2: PromptsUsedinDifferentMethodsforMATHDataset.
Baseline(w/otool)-Arithmetic
Giventhefollowingproblem,providethefinalanswerdirectly.
Problem:{question}
Yourresponseshouldonlybe"Thefinalansweris[answer]"where[answer]istheresponsetotheproblem.
Baseline(alltool)-Arithmetic
Useacalculatortosolvethequestion.FormatyouroutputasaJSONobjectinthefollowingstructure:
{{
"calculator":"<expression>"
}}
Problem:{question}
AutoTool-Arithmetic
Ifyouareconfidentinyouranswer,outputthefinalanswerdirectly.Ifunsure,usethecalculatortoolandrespondwitha
JSONobjectformattedas:
{{
"tool_name":"calculator"
}}
Problem:{question}
ICLTool(10-shot)-Arithmetic
Ifyouareconfidentinyouranswer,outputthefinalanswerdirectly.Ifunsure,usethecalculatortoolandrespondwitha
JSONobjectformattedas:
{{
"tool_name":"calculator"
}}
Examples:{example}
Problem:{question}
Table3: PromptsUsedinDifferentMethodsforArithmeticDataset.
17790

---
### Page 16

Baseline(w/otool)-TriviaQA
Answerthefollowingquestion. Yourresponseshouldonlybe"Thefinalansweris[answer]"where[answer]isthe
responsetotheproblem.
Problem:{question}
Baseline(alltool)-TriviaQA
{documents}
Basedontheinformationinthisdocument,answerthefollowingquestionaccurately.
Problem:{question}
AutoTool-TriviaQA
Answerthefollowingquestiondirectlyifyouareconfidentinyourknowledge.Ifyouareuncertainorneedtoretrieve
information,respondwithaJSONobjectinthefollowingformat:
{{
"tool_name":"search_info"
}}
Problem:{question}
ICLTool(10-shot)-TriviaQA
Answerthefollowingquestiondirectlyifyouareconfidentinyourknowledge.Ifyouareuncertainorneedtoretrieve
information,respondwithaJSONobjectinthefollowingformat:
{{
"tool_name":"search_info"
}}
Examples:{example}
Problem:{question}
Table4: PromptsUsedinDifferentMethodsforTriviaQADataset.
Logits-basedPrompt
Youareahelpfulassistant.
Answerthefollowingquestionasaccuratelyaspossible.
Question:{question}
P(true)Prompt
Youareahelpfulassistant.YoushouldjudgewhethertheanswertothegivenquestionisTrueorFalse.Pleaseonlyreply
withasimpleword"True"or"False".
Answerthefollowingquestionsasaccuratelyaspossible.
Question:{question}
Answer:{answer}
Istheaboveanswercorrect?(True/False)
ConsistencyPrompt
Youareahelpfulassistant.
Answerthefollowingquestionasaccuratelyaspossible.ProvideONLYthedirectanswerwithoutanyexplanation.
Question:{question}
Verb.1Stop1Prompt
Youareahelpfulassistant,andyouarealwayscompletelyhonestandDIRECTinyourresponses.
Provideabrief,conciseansweralongwithanexplicitconfidencepercentage(0-100%)aboutthecorrectnessofyour
response.
Question:{question}
Verb.2Stop1Prompt
Youareahelpfulassistant,alwayscompletelyhonestanddirectinyourresponses.Youarealsotransparentaboutyour
confidencelevelandcanhonestlysharehowcertainyouareabouttheanswer.
Question:{question}
Answer:{previous_answer}
Howconfidentareyouintheaboveanswer(0-100%)?
Table5: PromptsUsedinUncertainy-BasedEstimationMethods.
17791

---
### Page 17

ArithmeticQuestionTemplates
Computetheresultof{input}.
•
Answerthefollowingquestion:{input}
◦
Determine{input}
•
Canyousolvefor{input}?
◦
Calculate{input}.
•
Helpmedeterminethevalueof{input}.
◦
Pleasecalculate{input}
•
Canyousolveandprovidethevalueof{input}?
◦
Whatdoes{input}yield?
•
Assistmeincalculating{input}.
◦
Evaluate{input}andletmeknowthecomputedvalue.
•
Canyoucomputethevalueof{input}?
◦
Computethis:{input}.
•
Determinethenumericvalueresultingfrom{input}.
◦
Canyouprovideastepwisesolutionforevaluating{input}?
•
Solvethismathproblem:{input}
◦
Computethemathematicalexpression{input}andyieldtheresult.
•
Solvethisproblem:{input}
◦
Whatisthevalueof{input}?
•
Canyoutellmetheresultof{input}?
◦
.
.
.
Table 6: Examples of arithmetic question templates generated by ChatGPT, where {input} is substituted with
arithmeticquestionsusingtworandomlyselectedintegers.
17792
