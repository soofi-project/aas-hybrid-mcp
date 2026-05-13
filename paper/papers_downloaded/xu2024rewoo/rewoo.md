# REWOO

Source: rewoo.pdf


---
### Page 1

ReWOO: Decoupling Reasoning from Observations
for Efficient Augmented Language Models
BinfengXu ZhiyuanPeng BowenLei
billxbf@gmail.com jerrypeng1937@gmail.com bowenlei@stat.tamu.edu
SubhabrataMukherjee YuchenLiu DongkuanXu
subhabrata.mukherjee@microsoft.com yliu322@ncsu.edu dxu27@ncsu.edu
Abstract
AugmentedLanguageModels(ALMs)blendthereasoningcapabilitiesofLarge
LanguageModels(LLMs)withtoolsthatallowforknowledgeretrievalandaction
execution. ExistingALMsystemstriggerLLMthoughtprocesseswhilepulling
observations from these tools in an interleaved fashion. Specifically, an LLM
reasonstocallanexternaltool,getshaltedtofetchthetool’sresponse,andthen
decidesthenextactionbasedonallprecedingresponsetokens. Suchaparadigm,
thoughstraightforwardandeasytoimplement,oftenleadstohugecomputation
complexityfromredundantpromptsandrepeatedexecution. Thisstudyaddresses
suchchallengesforthefirsttime,proposingamodularparadigmReWOO(Reasoning
WithOutObservation)thatdetachesthereasoningprocessfromexternalobserva-
tions,thussignificantlyreducingtokenconsumption. Comprehensiveevaluations
acrosssixpublicNLPbenchmarksandacurateddatasetrevealconsistentperfor-
manceenhancementswithourproposedmethodology. Notably,ReWOOachieves
5×tokenefficiencyand4%accuracyimprovementonHotpotQA,amulti-steprea-
soningbenchmark.Furthermore,ReWOOdemonstratesrobustnessundertool-failure
scenarios. Beyondpromptefficiency,decouplingparametricmodulesfromnon-
parametrictoolcallsenablesinstructionfine-tuningtooffloadLLMsintosmaller
languagemodels,thussubstantiallyreducingmodelparameters. Ourillustrative
workoffloadsreasoningabilityfrom175BGPT3.5into7BLLaMA,demonstrating
thesignificantpotentialfortrulyefficientandscalableALMsystems. Fullcode,
model,anddataarereleasedforreproduction.1
1 Introduction
Thereisatrendingparadigm[1;2;3;4;5;6;7;8]tocouplelargelanguagemodels(LLMs)with
externalpluginsortools,enablingLLMstointeractwithenvironment[9;10]andretrieveup-to-date
knowledge. Thetool-augmentedLLMs,oftenreferredtoasaugmentedlanguagemodels(ALMs),
have fueled several prevailing applications like Auto-GPT [11] for autonomous task executions.
ExistingeffortsonALMshavebeenwidelygroundedinthepromptingparadigmsimilartoReAct[1],
whichinterleavesverbalreasoningandtool-callingconsecutively.
Such paradigm, however, introduces frequent execution and suspension of LLMs, together with
potentiallyhugecostintermsoftokenconsumption.LLMsgeneratetokensconditionedontheformer
context. Wheninteractingwithexternaltools,anLLMhastobehaltedfortoolresponse. Moreover,
the APIs of black-box LLMs, such as ChatGPT, are stateless. To resume the token generation,
all the historical tokens (including context prompt, exemplars, all previous reasoning traces and
observations)arefedintotheLLM,leadingtosignificantpromptredundancy. ThecommercialLLM
serviceprovidedbyOpenAIchargesintermsoftokenconsumption. Thereby,promptredundancy
1Projectrepo:https://github.com/billxbf/ReWOO.
Preprint.Underreview.
3202
yaM
32
]LC.sc[
1v32381.5032:viXra

---
### Page 2

Planner Worker
<Context prompt> For the following tasks, ...
<Exemplars> For example ... #E1= Wikipedia[The Hennchata]
What is the name of the cognac house that makes the main Evidence: The Hennchatais a cocktail consisting of
ingredient in The Hennchata? Hennessy cognac...
Plan: Search for more information about The
Hennchata. #E2= LLM[What is the main ingredient of The Hennchata?
#E1 = Wikipedia[The Hennchata] Given context: The Hennchatais a cocktail consisting of
Plan: Find out the main ingredient of The Hennchata. Hennessy cognac...]
#E2 = LLM[What is the main ingredient of The Evidence:Hennessy cognac
Hennchata? Given context: #E1]
Plan: Search for more information about the main #E3= Wikipedia[Hennessy cognac]
ingredient. Evidence:Jas Hennessy & Co., commonly known ...
#E3 = Wikipedia[#E2]
Plan: Find out the cognac house that makes the main #E4= LLM[What is the name of the cognac house that
ingredient. makes the main ingredient Hennessy cognac? Given
#E4 = LLM[What is the name of the cognac house that context: Jas Hennessy & Co., commonly known ...]
makes the main ingredient #E2? Given context: #E3] Evidence:Jas Hennessy & Co.
Solver
<Context prompt> Solve the task given provided plans and evidence ...
Plan: Search for more information about The Hennchata.
Evidence: The Hennchata is a cocktail consisting of Hennessy cognac and Mexican rice horchata agua fresca ...
Plan: Find out the main ingredient of The Hennchata.
Evidence: Hennessy cognac
Plan: Search for more information about the main ingredient.
Evidence: Jas Hennessy & Co., commonly known simply as Hennessy (French pronunciation: [ɛnɛsi])...
Plan: Find out the cognac house that makes the main ingredient.
Evidence: Jas Hennessy & Co.
Answer: Jas Hennessy & Co
Figure1: WorkflowofReWOO.Givenaquestion,Plannercomposesacomprehensiveblueprintof
interlinkedplanspriortotoolresponse. TheblueprintinstructsWorkertouseexternaltoolsand
collectevidence. Finally,plansandevidencearepairedandfedtoSolverfortheanswer.
bringssubstantialexpensetoaverageusers2. However,tothebestofourknowledge,thereisnoprior
workexploringtoreducethetokenconsumptionofALMs.
This paper proposes ReWOO , a novel prompting paradigm for ALMs. As illustrated in Figure 1,
ReWOO compartmentalizes the key components of an ALM: step-wise reasoning, tool-calls, and
summarization,intothreeseparatemodules: Planner,Worker,andSolver. Plannerbreaksdowna
taskandformulatesablueprintofinterdependentplans,eachofwhichisallocatedtoWorker. Worker
retrievesexternalknowledgefromtoolstoprovideevidence. Solversynthesizesalltheplansand
evidencetogeneratetheultimateanswertotheinitialtask. AsshowninFigure2,ReWOOseparates
thereasoningprocessofLLMsfromexternaltools,avoidingtheredundancyofinterleavedprompts
in observation-dependent reasoning, thereby significantly reducing token usage and enhancing
promptingefficiency.
ToholisticallyevaluateReWOO,weconductex-
periments over six multi-step and knowledge-
intensive NLP benchmarks and a curated
dataset. Evaluation baselines of ReWOO in-
cludetwonon-ALMpromptingmethods,Direct
Prompting, and Chain-of-Thought prompting
(CoT) [12], and a prevailing ALM paradigm,
ReAct[1],featuringobservation-dependentrea-
soning. Figure 3 provides an averaged per-
formanceoverbenchmarksinTable2,demon-
stratingconsistentefficiencygainofReWOOover Figure3: Overallbenchmarkperformanceofdif-
itsobservation-dependentcounterpart. Further- ferentmethods.
more, we demonstrate the potential of ReWOO
forsystemparameterefficiencythroughinstructiontuning [13]andSpecialization [14]. Weobserve
2Singlerequesttosolveamulti-steptaskwithAuto-GPTeasilyexceeds$1(excludingAPIcosts).
2

[TABLE]
<Context prompt>
Plan
Evidence
Plan
Evidence
Plan
Evidence
Plan
Evidence
[/TABLE]

[TABLE]
 |  |  |  | 
 |  |  |  | 
 |  |  |  | 
 |  |  |  | 
 |  |  |  | 
 |  |  |  | 
[/TABLE]

[TABLE]
 |  |  |  |  |  | 
 |  |  |  |  |  | 
 |  |  |  |  |  | 
 |  |  |  |  |  | 
 |  |  |  |  |  | 
 |  |  |  |  |  | 
[/TABLE]

---
### Page 3

(a) Reasoning with Observation (b) ReWOO
Worker
#E
<context> Tool Tool Tool Tool Tool
Tool
LLM <exemplars> Planner
Task <context>
Tool
<exemplars>
Tool
T A O Task
T A O P E
T A O
User
T A
User Solver
Figure2: In(a)observation-dependentreasoning,thetaskrequestedfromauserisfirstwrapped
with context prompt and exemplars, then fed into an LLM to initiate a reasoning process. The
LLMgeneratesathought(T)andanaction(A),thenwaitsfortheobservation(O)fromtools. The
observation is stacked into the prompt history to start the next LLM call. In ReWOO (b), Planner
producesatoncealistofinterdependentplans(P)andcallsWorkertofetchevidence(E)fromtools.
ThePandEarecombinedwiththetask,andthenfedintoSolverforthefinalanswer. Notethatin
(a),thecontextandexemplarsarerepeatedlyfedintotheLLM,resultinginpromptredundancy.
thatLLaMa7Bfine-tunedwithasmallnumberofepochscanbeonparwithGPT3.5inazero-shot
setup,underscoringthecapabilityofReWOOtofacilitatelightweightandscalableALMdeployment.
Contributions. Our contributions to the field of ALM can be summarized as follows: (1) We
identify and assess reasoning ability of LLMs without explicit observations (termed foreseeable
reasoning). Extensiveexperimentsshowthatforeseeablereasoningcanbeharnessedtoencourage
prompt-efficientALMs. (2)Weintroduceamodularframework,ReWOO,designedtocapitalizeon
theforeseeablereasoningabilityoflanguagemodels. Comprehensivetestingsuggeststhat,compared
totheprevalentthought-action-observationstyleALMs,ReWOOcanachievecomparableorsuperior
performancewhilesubstantiallyreducingtokenusage. Inaddition,ReWOOexhibitsgreaterrobustness
inreal-worldscenarios. (3)Wedemonstrateapipelinetooffloadthegeneralabilityofforeseeable
reasoningfromLLMsintosmallerlanguagemodels,enablingthesmallermodeltoutilizeunseen
tools in zero-shot setups. This research highlights the potential of ReWOO towards scalable and
parameter-efficientALM.
2 Methodology
A salient ability of humans is to predict possible outcomes from to-be-conducted actions. The
foreseenoutcomeofactionusuallyturnsouttobeinstructiveenoughforadaptingandplanningon
thenextsteps. Similarly,wedesignaframeworkdescribedbelow.
2.1 ReWOOwithPlan-Work-SolveParadigm
PlannerleveragestheforeseeablereasoningofLLMstocomposeasolutionblueprint. Concretely,
it contains consecutive tuples (Plan,#E) where Plan represents a descriptive message of the
currentstep,and#E ,subscriptedbystepnumbers,isaspecialtokentostorepresumablycorrect
s
evidencefromcorrespondingdesignatedWorker[Instruction]. ThisparadigmenablesReWOOtotackle
multi-stepandcomplextasks,particularlythosewhereasubsequentstepdependsontheobservations
ofpriorsteps,byreferringto#E frompreviousstepsintheinstructionsgiventoWorkers.
s
WorkerenablesReWOOtointeractwiththeenvironmentthroughtool-calls. OncePlannerprovides
a blueprint, designated Workers are invoked with instruction input, and populate #E with real
s
evidenceorobservations.
Solver processes all plans and evidence to formulate a solution to the original task or problem,
suchasprovidinganswersinQAtasksorreturningtheworkstatusforactionrequests. Wenote
3

[TABLE]
 | #E
Tool
Tool
Tool | 
[/TABLE]

[TABLE]

Planner
[/TABLE]

[TABLE]
<exemplars>
Task
[/TABLE]

[TABLE]
<context> | 
<exemplars> | 
[/TABLE]

[TABLE]
T | A
[/TABLE]

---
### Page 4

thatpromptingSolvertousetheprovidedplansandevidence"withcaution"enhancestheoverall
performance of ReWOO . We attribute this improvement to Solver’s inherent reasoning ability to
resolvesimpletasksorpartiallycompensateforfailuresinthePlannerorWorker.
2.2 PromptRedundancyReduction
ALMsystemsbasedoninterleavingreasoningandobservationssufferundesirablepromptredundancy
asdepictedinFigure2(a). Consideratypicalobservation-dependentALMsolvingaquestionQ
withkreasoningstepstoderivethefinalresponseR. StartingwithacontextpromptC andagroup
of n exemplars S = {S |i ∈ [1,n]}, ALM iteratively generates tuples of Thought, Action, and
i
Observation(TAOs),denotedas(T ,A ,O ),j ∈[1,k]. LetΘ(p)denotethenumberoftokensfora
j j j
textsequencep. ThetotalnumberofinputtokenscanbecalculatedasEq.(1).
k−1 (cid:32) j (cid:33)
(cid:88) (cid:88)
#TokenTAO =Θ(C+S+Q)+ Θ C+S+Q+ (T +A +O )
I t t t
j=1 t=1
k−1
(cid:88)
=kΘ(Q)+kΘ(C)+kΘ(S)+ (k−j)Θ(T +A +O ) (1)
j j j
(cid:124) (cid:123)(cid:122) (cid:125) (cid:124) (cid:123)(cid:122) (cid:125) (cid:124) (cid:123)(cid:122) (cid:125)
j=1
Question Context Exemplars
(cid:124) (cid:123)(cid:122) (cid:125)
TAOs
Theequationabovesuggeststhatduplicatedandidenticalpromptsareusedasinputredundantly.
SinceΘ(C)andΘ(S)areusuallynontrivial,inputtokensquadraticallygrowoversizeasthenumber
ofstepskincreases,usuallyleadingtotokenlimitexcess,ridiculouslyhighcomputation,andtime
expenses. On the contrary, ReWOO avoids such interleaving pattern as illustrated in Figure 2 (b).
Specifically,let(P ,Eˆ ,E ),j ∈[1,k]betheplan,evidencevariable#E andevidenceresponseat
j j j
stepj,ThetotalinputtokensforReWOOis:
k
(cid:88)
#TokenReWOO =Θ(C +S+Q)+Θ(C +Q+ P +E )
I planner solver j j
j=1
k
(cid:88)
≈ 2Θ(Q) +2Θ(C)+ Θ(S) + Θ(P +E ) (2)
j j
(cid:124) (cid:123)(cid:122) (cid:125) (cid:124) (cid:123)(cid:122) (cid:125) (cid:124)(cid:123)(cid:122)(cid:125)
j=1
Question Context Exemplars
(cid:124) (cid:123)(cid:122) (cid:125)
PEs
Itishardtoquantitativelymeasurethedifferencebetweenthetwomethodswithoutexplicitknowledge
ofpromptingsetup. However,ifweempiricallyequalize#TAOswith#PEs,thenEq.(1)differsfrom
Eq.(2)linearlybysizeofQ,C,S andquadraticallybysizeofT,A,Otothetermk. Suchanalysis
directlysuggeststhatasatasksenttoALMbecomesincreasinglycomplicated, thusintroducing
morereasoningsteps,ReWOOcansavesubstantiallylargeramountsofcomputationcostsinALM
systems. NotethatsomeLLM-basedtoolspotentiallyintroduceadditionaltokenconsumption. These
tokensarealsocountedinourexperiments.
2.3 ParameterEfficiencybySpecialization
AcommonconcernofALMsisthatbindingparametriclanguagemodelsandnon-parametrictool
calls complicates end-to-end training [2]. To mitigate this problem, Toolformer [15] fine-tunes
languagemodelsontool-augmentedcorpusinaself-supervisedway. Similarly,ReAct makesan
attempt to fine-tune reasoning ability on collected reasoning traces from HotpotQA [16]. These
approaches,however,aretestedinlimitedsetups. Concretely,Toolformerislimitedinanindependent
samplingoftools,thusfailingtofunctiononmulti-stepreasoningtasks. ReAct’sapproachinfine-
tuningcompletesthought-action-observationstrajectoriesisunproventogeneralizewellintounseen
tasksortoolset.
ReWOOdecouplesreasoningfromtool-calls,allowingtooptimizethegenericabilityofforeseeable
reasoningonaPlannermodulebecausenotoolresponseisexposedduringfine-tuning. Inspired
byrecentSpecializationframework[14],weattempttoelicitforeseeablereasoningfromGPT-3.5
and offload into LLaMa 7B [17] as depicted in Figure 4. We start by using text-davinci-003 to
infer4000(Plan,#E)blueprintsonmixedtrainingdataofHotpotQAandTriviaQA.Followingthe
4

---
### Page 5

Bootstrapping
Self-instruct Instruction-tuning
text-davinci-003 Instruction-tuning
LLaMa7B Alpaca 7B Planner 7B
Figure4: OffloadingforeseeablereasoningfromGPT-3.5intoAlpaca7B.AsmallLLaMaLMis
fine-tunedonself-instructeddatageneratedbyGPT-3.5,producingAlpaca,endowedwithgeneral
reasoningability. Alpacaisthenfurtherfine-tunedonblueprintsgeneratedbyGPT-3.5,leadingto
Planner7B,amodelspecializinginforeseeablereasoning.
bootstrappingmethod[18],wesamplethoseleadingtocorrectanswers,yieldingapproximately2000
Plannerinstructiondata. ApretrainedLLaMa7Bisinstructionfine-tunedon52kself-instructdataset,
producingAlpaca[13]7Bthatapproximatesgeneralabilityoftext-davinci-003. Subsequently,we
furtherfine-tuneAlpaca-7BonthePlannerinstructiondatatoobtaina7BPlannermodelspecialized
inforeseeablereasoning. Finally,weassessthepotentialofSpecializationonmultiplebenchmarks,
replacingtheReWOOPlannerwithGPT-3.5,Alpaca7B,andPlanner7B.
3 Experiments
WeevaluateReWOOagainststate-of-the-artpromptingparadigmsacrossawiderangeofNLPbench-
marks. Toemphasizethenecessityofutilizingexternaltools,wecurateadatasetwhereanswering
requiresup-to-dateexternalknowledge. Notably,ReWOOnotonlyconsistentlyreducestokenusage
butalsomatchesorevenoutperformsReActinalltasks.
3.1 Setups
TasksandDatasets. (a)CommonKnowledgeandReasoning. Suchtasksrequirebothdomain-
specificknowledgeandlogicalreasoning. Fourdatasetsareleveragedforevaluation. HotpotQA[16],
a multi-hop reasoning QA task over diversified domains; TriviaQA[19], reading comprehension
followedbychallengingQAs, wherewehidethereadingcontexttoencouragesearching. Sport-
sUnderstanding[20], a factual QA benchmark from BigBench[21] over in-depth sports domain
knowledge;andStrategyQA[22],anopendomainQAtaskwhereanswersrequirestepsofreasoning.
(b) Arithmetic and Scientific Reasoning. Such tasks include GSM8K[23] comprised of grade
schoolmathproblems,andPhysicsQuestions[24]onhighschoolphysicsquestions. (c)Curated. To
challengeALMswithupdatedknowledge,wecreatedaQAdatasetoverStateoftheUnionAddress
2023,denotedasSOTUQA.Asaninstance,"IsSpeakeroftheHousethisyearolderthanlastyear?"
expectsALMstodiscoverSpeakeroftheHouse2023fromprovidedSOTUdocument,and2022
fromanonlinesearch,thencomparingages.InadditiontoSOTUQA,wecurateasetoftasksaligning
withreal-worldALMapplications(demonstratedintheAppendix),includingrecommendationfor
restaurants,stocktrading,AIdrawing,etc.
Baselines. Weconsiderthefollowingpromptingparadigms: (a)DirectPrompt: astandardzero-shot
paradigmthatpromptsanLLMtodirectlysolvetasksoranswerquestions. Thisbaselinereflects
thelanguagemodel’sgroundperformancewithoutexplicitreasoningortoolutilization. (b)Chain-
of-Thought(CoT):promptinganLLMto"thinkstepbystep"withanexemplartodemonstrate
intermediateverbalreasoningformat. Thismethodembodiesthemodels’explicitreasoningability
withouttool-calling. (c)ReAct: aprevailingpromptingparadigminALMsasexplainedinFigure2.
5

[TABLE]

Alpaca 7B
[/TABLE]

[TABLE]

Planner 7B
[/TABLE]

---
### Page 6

Slightly differing from the original implementation, a short description of the provided tools is
appendedintothecontextprompttoenablezero-shotevaluation.
Exemplars. ForReWOOPlanner,wemanuallycrafti={6,1,1}trajectoriesoutoftrainingdatafrom
HotpotQA,TriviaQA,andGSM8K,respectively. Theseexemplarsconsistofreasoningtemplates
coveringinformationretrieval("Findout...","Searchfor..."),comparison("Compare... with... on
..."),equationsolving("Let... bex,solve...")andcalculating("Calculate..."). ForPhysicsQuestions,
SportsUnderstanding,andStrategyQA,weshiftourinterestsintosystematicgeneralizability,therefore
providingonly1exemplarfromirrelevantbenchmarks.Thenumberofreasoningstepskinexemplars
istypically2or3. AllexemplarquestionsusedinReWOOPlannerareequivalentlyprovidedtoReAct
inathought-action-observationmanner. ReActreleasedtheexemplarsusedonHotpotQA.Forafair
comparison,wekeepusingthesameexemplarsasReActforReWOO.
ActionSpace. WeprovideawiderangeoftoolstoassistLLMsinretrievingextraknowledgeand
interactingwiththeenvironment,including(1)Wikipedia[query],asearchengineforWikipedia,
functioningidenticallyassearch[entity]intheoriginalReActimplementation. (2)Google[query],
search result snippet from Google SERP. (3) WolframAlpha[query], search/computation result
fromWolframAlphaAPI.(4)LLM[prompt], aseparatesingleLLM.(5)Calculator[prompt], a
program-aidedLLM[25]. (6)SearchDoc[query],indexsearchoverprivatedocuments. Forcurated
tasksinvolvingmuchmorediverseandcomplexreal-worldinteractions,weadditionallyprovide
a set of tools like Location[query], Stock[query], Twitter[query], Yelp[query], Email[request],
TradeStock[request]andDraw[prompt](SeeAppendixforexamples).
Available tools for different bench-
marks are shown in Table 1. To en- Benchmark Wiki LLM WolfAlf Calc Google SrchDoc
sure a fair comparison, we align all
HotpotQA ✓ ✓
availabletoolsprovidedtoReWOOand
ReAct. TriviaQA ✓ ✓
Evaluation Metrics. Common per- GSM8K ✓ ✓ ✓
formancemetricssuchasexactmatch StrategyQA ✓ ✓ ✓ ✓ ✓
(EM)andcharacter-levelF1scoreare
PhysicsQA ✓ ✓ ✓ ✓ ✓
employedinourexperiments. More-
over, as observed in [1], the correct SportsU. ✓ ✓ ✓ ✓ ✓
answerstosomebenchmarkquestions SOTUQA ✓ ✓ ✓ ✓
arenotunique. Forexample,respond-
ing"CA."fortheground-truth"Cali-
Table1: AvailabletoolsforALMsindifferentbenchmarks.
fornia"shouldalsobeconsideredcor-
rect. Therefore,aGPT-4-basedscorer
isusedtomeasurethesemanticaccuracyofanswers. Ontheotherhand,efficiencycanbemeasured
intermsoftotaltokenusageinLLMs(includingtokensconsumedbyLLM-basedtools),thenumber
ofreasoningsteps3andaveragetokenexpenseinUSDfor1kqueries.
Fine-tuning. Wemanagetofine-tune7BLLaMa-basedmodelsonasingleRTX4090usingLoRA
[26]. Detailedfine-tuninngparametersforAlpaca7BandPlanner7BpresentedinAppendix.
3.2 ResultsandObservations
3.2.1 ComparisonbetweenPromptingParadigms
ReWOO excels over ReAct consistently. Table 2 shows the main evaluation results on public
benchmarksandcurateddatasetbasedongpt-3.5-turbo. UndertheALMsetups,weobservethesheer
winofReWOOoverReActinallbenchmarks. Averagingoversixpublicbenchmarks,ReWOOisableto
reducetokenusageby64%withanabsoluteaccuracygainof4.4%. Suchresultsimplythesuccess
ofReWOOinelicitingforeseeablereasoningcapabilityofLLMs,aswellasthesignificantefficiency
boostofReWOOagainstprevailingobservation-dependentALMsystems.
ALMs perform well on curated task As shown in Table 2(SOTUQA), both ReWOO and ReAct,
assistedwithexternaltools,clearlyoutperformDirectPromptingandCoT.ReWOOoutperformsReAct
by 8% absolute accuracy, while consuming 43% less tokens. We believe that the evaluation of
documentQAlikeSOTUQAmorecloselyfeaturesreal-worldALMapplicationsthanpreceding
3ForCoTandReAct,#steps=#thoughts;ForReWOO,#steps=#plans+1includingtheextraSolverstep.
6

[TABLE]
TriviaQA | ✓ | ✓ |  |  |  | 
[/TABLE]

[TABLE]
StrategyQA | ✓ | ✓ | ✓ | ✓ | ✓ | 
[/TABLE]

[TABLE]
SportsU. | ✓ | ✓ | ✓ | ✓ | ✓ | 
[/TABLE]

---
### Page 7

Dataset Paradigm #Tools n Acc F1 EM #Tokens #Steps $Cost
1k
Direct 0 0 37.8 36.2 28.0 55.5 1.00 0.11
HotpotQA CoT 0 1 41.6 30.8 22.4 481.9 1.79 0.96
1000 REACT 2 6 40.8 39.6 32.2 9795.1 4.97 19.59
ReWOO 2 6 42.4 40.1 30.4 1986.2 4.45 3.97
Direct 0 0 80.6 74.0 64.2 43.4 1.00 0.09
TriviaQA CoT 0 1 78.6 71.7 60.1 199.2 2.08 0.40
1000 REACT 2 1 59.4 53.2 47.4 4212.9 5.21 8.43
ReWOO 2 1 66.6 60.6 51.8 1340.9 3.55 2.68
Direct 0 0 26.8 14.4 — 101.1 1.00 0.20
GSM8K CoT 0 1 67.4 62.7 — 495.6 3.45 0.99
1000 REACT 3 1 62.0 37.3 — 1874.3 2.86 3.75
ReWOO 3 1 62.4 36.2 — 1089.3 3.21 2.18
Direct 0 0 64.6 64.6 64.6 41.8 1.00 0.08
StrategyQA CoT 0 1† 56.0 56.0 56.0 170.5 1.85 0.34
300 REACT 5 1† 64.6 64.6 64.6 1686.3 2.58 3.37
ReWOO 5 1† 66.6 66.6 66.6 1287.1 3.20 2.57
Direct 0 0 52.8 12.6 — 132.2 1.00 0.26
PhysicsQA CoT 0 1† 62.2 15.2 — 346.8 3.07 0.69
53 REACT 5 1† 64.1 16.2 — 2163.3 2.77 4.33
ReWOO 5 1† 66.0 14.0 — 1225.7 2.56 2.45
Direct 0 0 68.0 68.0 68.0 47.63 1.00 0.10
SportsU. CoT 0 1† 53.3 47.5 45.3 215.9 1.78 0.43
300 REACT 5 1† 58.6 51.9 49.3 1720.0 2.64 3.44
ReWOO 5 1† 61.3 55.8 55.3 854.2 3.04 1.71
Direct 0 0 52.7 15.3 — 52.2 1.00 0.10
SOTUQA CoT 0 1† 60.8 21.2 — 227.4 2.08 0.45
Curated REACT 5 1† 64.8 42.7 — 1840.3 2.43 3.68
ReWOO 5 1† 70.2 44.8 — 1048.8 2.24 2.09
Table2: EvaluationresultsonpublicNLPbenchmarks. ForHotpotQA,TriviaQA,andGSM8K,
promptsareconfiguredwithtoolsandexemplarslabeledfromthesamebenchmarks;Othertasks
alignwithpracticalscenarios,whereweuseastaticout-of-taskexemplartoinstructoutputformat
(whichcanbeseenaszero-shot),andacommonlargetoolset. ndenotesthenumberofexemplars. †:
Out-of-taskexemplar. Underline: Bestperformingparadigm. Bold: BestperformingALM.
public NLP benchmarks. In addition, we showcase several ReWOO trajectories in the Appendix,
featuringrealworldALMapplicationssuchasrestaurantrecommendationandAIpainting.
ExtraneoustoolscompromiseALMperformance. AnotherfindingfromTable2isthatDirect
PromptingandCoT,wherewedon’tprovideanyexternaltool,outperformbothALMparadigms.
ThisobservationleadsustoconductanablationstudyontheeffectofincrementingtoolsinALMs.
WestartwiththesamesetupsforHotpotQAwhileincrementallyaddingoneextratooltoReWOOand
ReAct.Figure5showsthatwhileapowerfultoollikeGoogletemporarilyboostsaccuracy,thegeneral
trendgoesdownasweintroducemoretoolsin-context. Qualitatively,weinvestigate20questions
where2-toolReWOOsucceedswhile7-toolReWOOfails,observingthat17ofthetrajectoriesinvolve
toolmisuse,suchasemployingYelp[query]tosearchforacelebrity. Thisexperimentindicatesthat
unnecessarytoolsareharmfultoALMsbypotentiallyintroducingextraneouscontents.
ReWOOisrelativelyrobustupontoolfailure.ItiscommoninALMsystemsthattoolsmalfunction
andreturnerrors. TocomparetherobustnessofReWOOandReActundersuchsituation,weforceall
toolstorespond"Noevidencefound.". Table3impliesthatReAct-likeALMsystemsarehighly
fragilewhenintermediatetoolsfail.Ontheotherhand,ReWOOislesscompromisedundertoolfailures
atasmallercost.
7

[TABLE]
Paradigm | #Tools n |  | Acc F1 EM |  |  |  |  | 
Direct
CoT | 0 0
0 1 |  | 37.8 36.2 28.0
41.6 30.8 22.4 |  |  |  |  | 
REACT | 2 | 6 | 40.8 | 39.6 | 32.2 | 9795.1 | 4.97 | 19.59
ReWOO | 2 | 6 | 42.4 | 40.1 | 30.4 | 1986.2 | 4.45 | 3.97
Direct
CoT | 0 0
0 1 |  | 80.6 74.0 64.2
78.6 71.7 60.1 |  |  |  |  | 
REACT | 2 | 1 | 59.4 | 53.2 | 47.4 | 4212.9 | 5.21 | 8.43
ReWOO | 2 | 1 | 66.6 | 60.6 | 51.8 | 1340.9 | 3.55 | 2.68
Direct
CoT | 0 0
0 1 |  | 26.8 14.4 —
67.4 62.7 — |  |  |  |  | 
REACT | 3 | 1 | 62.0 | 37.3 | — | 1874.3 | 2.86 | 3.75
ReWOO | 3 | 1 | 62.4 | 36.2 | — | 1089.3 | 3.21 | 2.18
Direct
CoT | 0 0
0 1† |  | 64.6 64.6 64.6
56.0 56.0 56.0 |  |  |  |  | 
REACT | 5 | 1† | 64.6 | 64.6 | 64.6 | 1686.3 | 2.58 | 3.37
ReWOO | 5 | 1† | 66.6 | 66.6 | 66.6 | 1287.1 | 3.20 | 2.57
Direct
CoT | 0 0
0 1† |  | 52.8 12.6 —
62.2 15.2 — |  |  |  |  | 
REACT | 5 | 1† | 64.1 | 16.2 | — | 2163.3 | 2.77 | 4.33
ReWOO | 5 | 1† | 66.0 | 14.0 | — | 1225.7 | 2.56 | 2.45
Direct
CoT | 0 0
0 1† |  | 68.0 68.0 68.0
53.3 47.5 45.3 |  |  |  |  | 
REACT | 5 | 1† | 58.6 | 51.9 | 49.3 | 1720.0 | 2.64 | 3.44
ReWOO | 5 | 1† | 61.3 | 55.8 | 55.3 | 854.2 | 3.04 | 1.71
Direct
CoT | 0 0
0 1† |  | 52.7 15.3 —
60.8 21.2 — |  |  |  |  | 
REACT | 5 | 1† | 64.8 | 42.7 | — | 1840.3 | 2.43 | 3.68
ReWOO | 5 | 1† | 70.2 | 44.8 | — | 1048.8 | 2.24 | 2.09
[/TABLE]

---
### Page 8

Method Acc #Tokens $Cost 1k 45
Normal
REACT 40.8 9795.1 21.29 43
ReWOO 42.4 1986.2 3.97
∆withtool-failure 41
REACT -40.8 +851.1 +1.70
ReWOO -29.2 -110.8 -0.22 39
∆withgpt-3.5-turbo→text-davinci-003
37
R R e E W A O C O T + +1 2 . . 7 6 - - 4 9 6 0 6 .5 .8 - - 0 0 . . 1 9 8 3 No tool + s Goo + gl C e alcula + t W or olfra m +Ye + lp SearchD + o T c witter
Table3: PerformancechangeonHotpotQA
when (1) all tools return "No evidence
found"(2)replacingLLM.
ycaruccA
ReWOO
ReAct
Figure 5: Performance degraded on HotpotQA
whenincrementallyaddingextraneoustools.
Conversation-aligningRLHFinALM.ToexploretheeffectofRLHF,wereplacegpt-3.5-turbo
basedLLMsusedinHotpotQAwithtext-davinci-003. Table3showsthattext-davinci-003outper-
formsgpt-3.5-turbowithfewerstepsandtokenusage,implyingthatconversationRLHFslightly
harmscommonsensereasoningabilityofALMs.
3.3 Fine-tuningandSpecializationofLLM
0.9
0.8
0.7
0.6
0.5
0.4
0.3
0.2
HotpotQA TriviaQA GSM8K StrategyQA
ycaruccA
Following the Specialization framework from GPT-3.5
Alpaca 7B
Figure 4, we obtain Alpaca 7B and Planner
Planner 7B
7B approximating general ability and foresee-
ablereasoningfromGPT3.5,respectively. Both
LMsarecomparedagainsttheoriginalGPT-3.5
performanceinazero-shotsetup. Figure6re-
flectsthatthesemethods,whenpluggedintothe
Plannermodule,match25×largerGPT-3.5in
HotpotQA,TriviaQA,andStrategyQA.Further-
more,generalaccuracygainfromAlpaca7Bto
Planner7BimplieseffectivenessofSpecializa-
tion. Qualitatively,whilethetraininginstruction
dataset only demonstrates Wikipedia[query] Figure6:PerformanceeffectofchangingtheLLM
andLLM[prompt],wesurprisinglyobservethat, inReWOO.Planner7BistunedonHotpotQAand
TriviaQA
ifpairedwithin-contextdescriptions, Planner
7B is increasingly capable of reasoning with
Google[query]andCalculator[prompt]thanAlpaca. Furthereffortsarerequiredtopushthelimitsof
Specialization,whichweleaveforfuturestudies. Mostimportantly,ourresultsillustratethepotential
ofReWOOparadigminoffloadinggeneralforeseeablereasoningintodistilledsmalllanguagemodels,
substantiallyimprovingsystemparameterefficiencyandscalability.
4 LimitationsandFutureWork
Wenoticethatforcertaintaskswherelittlecontextabouttheenvironmentisavailable,fullyrelying
onforeseeablereasoningbecomesimpractical. ConsiderthefollowingtaskfromAlfWorld[27]:
Youareinthemiddleofaroom. Lookingquicklyaroundyou,youseeadrawer2,ashelf5,a
drawer1,ashelf4,asidetable1,adrawer5,ashelf6,ashelf1,ashelf9,acabinet2,asofa1,
acabinet1,ashelf3,acabinet3,adrawer3,ashelf11,ashelf2,ashelf10,adresser1,a
shelf12,agarbagecan1,aarmchair1,acabinet4,ashelf7,ashelf8,asafe1,andadrawer
4. Yourtaskisto: putsomevaseinsafe.
SinceaPlannerhasnopriorknowledgeabouttheenvironment,ithastoenumerateallpossibleplans
thatcanpotentiallyleadtosomevase. ThenumberofreasoningstepsofPlannerinsuchtasksis
equivalenttotheworst-casecomplexityofobservation-dependentreasoning.
8

[TABLE]
 |  |  |  |  |  |  |  | 
 |  |  |  |  |  | R
R | eWOO
eAct | 
 |  |  |  |  |  |  |  | 
 |  |  |  |  |  |  |  | 
 |  |  |  |  |  |  |  | 
 |  |  |  |  |  |  |  | 
 |  |  |  |  |  |  |  | 
 |  |  |  |  |  |  |  | 
 |  |  |  |  |  |  |  | 
[/TABLE]

[TABLE]
GPT-3.5 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | 
 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | 
 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | 
 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | 
 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | 
 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | 
 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | 
 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | 
 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | 
 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | 
 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | 
 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | 
 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | 
 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | 
 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | 
 | Hot | pot | QA |  | Tri | via | QA |  | GS | M | 8K | S | tra | teg | yQ | 
 | Pe | rf | orm |  | nce | ef | fec |  | ofc | ha | ng |  | gt | he | LL | 
[/TABLE]

---
### Page 9

TheexampleaboveimpliesthatarobustALMsystemshouldnotbebuiltonasingleton–itlooks
promising to wire different nodes of LLMs, tools, and sub-models into a directed acyclic graph
(DAG)sothateachnodefunctionsforitspredesignatedtasksorganically. 4 Directionstofurther
improvetheefficiencyandperformanceofsuchALMsystemsinclude(1)Offloadingspecialized
abilitiesfromfoundationLLMsintosmallermodels. Section3.3demonstratethepossibilityfor
smallLMsspecializing[14]ingeneralforeseeablereasoning. Weexpectthatwithagreaternumber
ofopendomaininstructions,foreseeablereasoningcanbeevenmoreholisticallyoffloaded. Other
parametricnodesintheDAG,suchasaSolver,canbefine-tunedalike. (2)Toolrepresentation
learning. InmanycasesfromHotpotQA,WikipediaandGooglecanbothleadtothecorrectanswer,
indicatingacertainlevelofsimilaritybetweenthosetools. Wecansetupamodeltominimizethe
energyamongsimilar-functioningWorkers. Toolrepresentationsallowustoparametrizethewhole
ALMsystemandthereforeenablingend-to-endtraining. (3)Graphoptimization. Furthermore,we
shouldbeabletooptimizeDAGexecutionthroughmultiplegraphandconcurrencyalgorithms.
5 RelatedWork
Tool-augmentedLLMs. Whenpromptedproperly,LLMsdemonstratetheabilityofreasoningto
solvetasksusingevidenceandlogic,suchascommonsensereasoning,mathematicalreasoning,and
symbolicreasoning[2]. Severalworksinjectstheintermediatereasoningstepswithdiversetools,
enablingLLMstoretrieveup-to-dateworldknowledgeandsolvingmorecomplextasks. SearchAPIs
areleveragedtoavoidhallucinationsandprovidecomprehensiveinformationformoretrustworthy
textgeneration[1;10;29]. High-levelroboticsAPIsareusedtoinstructroboticstofinishphysical
worldtasks[9;30;31;32]. Calculator[23],codeinterpreter[25],andmathematicalprover[33]are
usedtofixthecalculationerror,executethegeneratedcode,andprovethecomplexmathematical
theory,respectively. Therearealsoworksthatusemultipletoolstosolvevariousnaturallanguage
processingandcomputervisiontasks,suchasToolformer[15]andVisualChatGPT[34]. Inaddition,
thetaskcanbedecomposed,andtheproblemcanbebettersolvedusingmulti-stepreasoningand
actions,suchasReAct[1],ART[35],MM-ReAct[3],andTaskMatrix.AI[4]. Ourworkposesanew
perspectivetotool-augmentedLLMsforlarge-scalereal-worldapplications: ReWOOtoreducetoken
expensewhileattainingcomparableorevenbetterperformance.
Efficient LLMs. Efficient LLMs is a lasting research topic, particularly with the prevailing of
ChatGPT. Various approaches[26; 36; 37; 13; 38; 39; 40; 41; 42] have been proposed to reduce
the cost of fine-tuning and deploying LLMs. A prevailing direction is to reduce model scale,
e.g.,usinginstructiontuning[37;13]toalignasmallandlocally-hostedLLMwiththeassistance
fromlarge-scaleblack-boxLLMs. Thecomputationcostduringtuningcanbefurtherreducedby
LoRA[26],adapters[40;41],prompttuning[39;38],etc. However,theseapproachesofteninvolve
themodificationsofmodelstructuresandtheupdateofmodelparameters,hinderingtheapplication
toblack-boxLLMs. Incontrast,promptengineeringforefficientLLMs,thoughrarelystudied,is
flexibleandstraightforward. ItdemandsnointernalinformationofLLMsandcanbereadilyapplied
toanyoff-the-shelfblack-boxlanguagemodelslikeOpenAIChatGPTandGooglePaLM.Following
thisdirection,ourworkgivesthefirstexplorationofpromptingforefficienttool-augmentedLLMs.
6 Conclusion
WepresentReWOO,amodularALMframeworktosolvemulti-stepreasoningtasksefficientlyby
decouplingreasoningfromtoolfeedbackandobservations. Theoreticaldecompositionofprompt
tokensestablishesthatReWOOisabletosubstantiallyreducepromptingredundancyinprevailing
Thought-Action-ObservationALMsystems. ComprehensiveexperimentsonbothpublicNLPbench-
marksandcuratedtasksrevealsuperiorperformanceofReWOOinachievingboostedperformance
withmuchlesstokenconsumption. AsidestudyalsoshowsthatReWOOhasrelativelyrobustper-
formance under tool-failure cases. Our study further unveils the potential for generic reasoning
offloadingviainstructiontuningandspecialization. FutureimprovementsbeyondReWOObasedALM
systemsinvolvemodularLLMfine-tuning,toolrepresentationlearning,andsystemgraphlearning
andoptimization. Wedemonstratethatourworklaysasolidfoundationfortheseadvancements,
inchingusclosertotrulyscalableAGI.
4RecentprojectslikeLangChain[28]have,tosomeextent,featuredthisidea.
9

---
### Page 10

References
[1] ShunyuYao,JeffreyZhao,DianYu,NanDu,IzhakShafran,KarthikNarasimhan,andYuanCao. Re-
act: Synergizingreasoningandactinginlanguagemodels. InInternationalConferenceonLearning
Representations,2023.
[2] GrégoireMialon,RobertoDessì,MariaLomeli,ChristoforosNalmpantis,RamPasunuru,RobertaRaileanu,
BaptisteRozière,TimoSchick,JaneDwivedi-Yu,AsliCelikyilmaz,etal. Augmentedlanguagemodels:a
survey. arXivpreprintarXiv:2302.07842,2023.
[3] ZhengyuanYang,LinjieLi,JianfengWang,KevinLin,EhsanAzarnasab,FaisalAhmed,ZichengLiu,
CeLiu,MichaelZeng,andLijuanWang. Mm-react: Promptingchatgptformultimodalreasoningand
action. arXivpreprintarXiv:2303.11381,2023.
[4] Yaobo Liang, Chenfei Wu, Ting Song, Wenshan Wu, Yan Xia, Yu Liu, Yang Ou, Shuai Lu, Lei Ji,
ShaoguangMao,etal. Taskmatrix.ai:Completingtasksbyconnectingfoundationmodelswithmillionsof
apis. arXivpreprintarXiv:2303.16434,2023.
[5] YujiaQin,ShengdingHu,YankaiLin,WeizeChen,NingDing,GanquCui,ZheniZeng,YufeiHuang,
ChaojunXiao,ChiHan,etal. Toollearningwithfoundationmodels. arXivpreprintarXiv:2304.08354,
2023.
[6] GeunwooKim,PierreBaldi,andStephenMcAleer. Languagemodelscansolvecomputertasks. arXiv
preprintarXiv:2303.17491,2023.
[7] NoahShinn,BeckLabash,andAshwinGopinath. Reflexion:anautonomousagentwithdynamicmemory
andself-reflection. arXivpreprintarXiv:2303.11366,2023.
[8] AndresMBran,SamCox,AndrewDWhite,andPhilippeSchwaller. Chemcrow: Augmentinglarge-
languagemodelswithchemistrytools. arXivpreprintarXiv:2304.05376,2023.
[9] AnthonyBrohan,YevgenChebotar,ChelseaFinn,KarolHausman,AlexanderHerzog,DanielHo,Julian
Ibarz,AlexIrpan,EricJang,RyanJulian,etal. Doasican,notasisay:Groundinglanguageinrobotic
affordances. InConferenceonRobotLearning,pages287–318.PMLR,2023.
[10] ReiichiroNakano,JacobHilton,SuchirBalaji,JeffWu,LongOuyang,ChristinaKim,ChristopherHesse,
ShantanuJain,VineetKosaraju,WilliamSaunders,etal. Webgpt:Browser-assistedquestion-answering
withhumanfeedback. arXivpreprintarXiv:2112.09332,2021.
[11] Auto-gpt: An autonomous gpt-4 experiment. https://github.com/Significant-Gravitas/
Auto-GPT,2023. [Online;accessed13-May-2023].
[12] JasonWei,XuezhiWang,DaleSchuurmans,MaartenBosma,EdChi,QuocLe,andDennyZhou. Chain
ofthoughtpromptingelicitsreasoninginlargelanguagemodels. arXivpreprintarXiv:2201.11903,2022.
[13] RohanTaori,IshaanGulrajani,TianyiZhang,YannDubois,XuechenLi,CarlosGuestrin,PercyLiang,
andTatsunoriBHashimoto. Alpaca:Astrong,replicableinstruction-followingmodel. StanfordCenterfor
ResearchonFoundationModels.https://crfm.stanford.edu/2023/03/13/alpaca.html,2023.
[14] YaoFu,HaoPeng,LituOu,AshishSabharwal,andTusharKhot. Specializingsmallerlanguagemodels
towardsmulti-stepreasoning. arXivpreprintarXiv:2301.12726,2023.
[15] TimoSchick,JaneDwivedi-Yu,RobertoDessì,RobertaRaileanu,MariaLomeli,LukeZettlemoyer,Nicola
Cancedda,andThomasScialom. Toolformer:Languagemodelscanteachthemselvestousetools. arXiv
preprintarXiv:2302.04761,2023.
[16] ZhilinYang,PengQi,SaizhengZhang,YoshuaBengio,WilliamWCohen,RuslanSalakhutdinov,and
ChristopherDManning. Hotpotqa:Adatasetfordiverse,explainablemulti-hopquestionanswering. arXiv
preprintarXiv:1809.09600,2018.
[17] HugoTouvron,ThibautLavril,GautierIzacard,XavierMartinet,Marie-AnneLachaux,TimothéeLacroix,
BaptisteRozière,NamanGoyal,EricHambro,FaisalAzhar,etal. Llama:Openandefficientfoundation
languagemodels. arXivpreprintarXiv:2302.13971,2023.
[18] EricZelikman,JesseMu,NoahDGoodman,andYuhuaiTonyWu.Star:Self-taughtreasonerbootstrapping
reasoningwithreasoning. 2022.
[19] MandarJoshi, EunsolChoi, DanielSWeld, andLukeZettlemoyer. Triviaqa: Alargescaledistantly
supervisedchallengedatasetforreadingcomprehension. arXivpreprintarXiv:1705.03551,2017.
[20] Ethan Kim. Sports understanding. https://github.com/google/BIG-bench/tree/main/
bigbench/benchmark_tasks/sports_understanding,2022. [Online;accessed13-May-2023].
[21] AhmadGhazal,TilmannRabl,MinqingHu,FrancoisRaab,MeikelPoess,AlainCrolotte,andHans-Arno
Jacobsen. Bigbench:Towardsanindustrystandardbenchmarkforbigdataanalytics. InProceedingsofthe
2013ACMSIGMODinternationalconferenceonManagementofdata,pages1197–1208,2013.
10

---
### Page 11

[22] MorGeva,DanielKhashabi,EladSegal,TusharKhot,DanRoth,andJonathanBerant. Didaristotle
usealaptop? aquestionansweringbenchmarkwithimplicitreasoningstrategies. Transactionsofthe
AssociationforComputationalLinguistics,9:346–361,2021.
[23] KarlCobbe,VineetKosaraju,MohammadBavarian,MarkChen,HeewooJun,LukaszKaiser,Matthias
Plappert, JerryTworek, JacobHilton, ReiichiroNakano, etal. Trainingverifierstosolvemathword
problems. arXivpreprintarXiv:2110.14168,2021.
[24] IanDBeatty,WilliamJGerace,WilliamJLeonard,andRobertJDufresne. Designingeffectivequestions
forclassroomresponsesystemteaching. Americanjournalofphysics,74(1):31–39,2006.
[25] LuyuGao,AmanMadaan,ShuyanZhou,UriAlon,PengfeiLiu,YimingYang,JamieCallan,andGraham
Neubig. Pal:Program-aidedlanguagemodels. arXivpreprintarXiv:2211.10435,2022.
[26] EdwardJHu,YelongShen,PhillipWallis,ZeyuanAllen-Zhu,YuanzhiLi,SheanWang,LuWang,and
WeizhuChen. Lora:Low-rankadaptationoflargelanguagemodels. arXivpreprintarXiv:2106.09685,
2021.
[27] Mohit Shridhar, Xingdi Yuan, Marc-Alexandre Côté, Yonatan Bisk, Adam Trischler, and Matthew
Hausknecht. Alfworld:Aligningtextandembodiedenvironmentsforinteractivelearning. arXivpreprint
arXiv:2010.03768,2020.
[28] Langchain. https://github.com/hwchase17/langchain,2023. [Online;accessed13-May-2023].
[29] AngelikiLazaridou,ElenaGribovskaya,WojciechStokowiec,andNikolaiGrigorev. Internet-augmented
language models through few-shot prompting for open-domain question answering. arXiv preprint
arXiv:2203.05115,2022.
[30] JackyLiang,WenlongHuang,FeiXia,PengXu,KarolHausman,BrianIchter,PeteFlorence,andAndy
Zeng.Codeaspolicies:Languagemodelprogramsforembodiedcontrol.arXivpreprintarXiv:2209.07753,
2022.
[31] DannyDriess,FeiXia,MehdiSMSajjadi,CoreyLynch,AakankshaChowdhery,BrianIchter,Ayzaan
Wahid,JonathanTompson,QuanVuong,TianheYu,etal. Palm-e:Anembodiedmultimodallanguage
model. arXivpreprintarXiv:2303.03378,2023.
[32] SaiVemprala,RogerioBonatti,ArthurBucker,andAshishKapoor.Chatgptforrobotics:Designprinciples
andmodelabilities. 2023,2023.
[33] AlbertQJiang,SeanWelleck,JinPengZhou,WendaLi,JiachengLiu,MatejaJamnik,TimothéeLacroix,
YuhuaiWu, andGuillaumeLample. Draft, sketch, andprove: Guidingformaltheoremproverswith
informalproofs. arXivpreprintarXiv:2210.12283,2022.
[34] ChenfeiWu,ShengmingYin,WeizhenQi,XiaodongWang,ZechengTang,andNanDuan. Visualchatgpt:
Talking,drawingandeditingwithvisualfoundationmodels. arXivpreprintarXiv:2303.04671,2023.
[35] Bhargavi Paranjape, Scott Lundberg, Sameer Singh, Hannaneh Hajishirzi, Luke Zettlemoyer, and
Marco Tulio Ribeiro. Art: Automatic multi-step reasoning and tool-use for large language models.
arXivpreprintarXiv:2303.09014,2023.
[36] HaokunLiu,DerekTam,MohammedMuqeeth,JayMohta,TenghaoHuang,MohitBansal,andColinA
Raffel. Few-shotparameter-efficientfine-tuningisbetterandcheaperthanin-contextlearning. Advances
inNeuralInformationProcessingSystems,35:1950–1965,2022.
[37] BaolinPeng,ChunyuanLi,PengchengHe,MichelGalley,andJianfengGao. Instructiontuningwithgpt-4.
arXivpreprintarXiv:2304.03277,2023.
[38] BrianLester,RamiAl-Rfou,andNoahConstant. Thepowerofscaleforparameter-efficientprompttuning.
arXivpreprintarXiv:2104.08691,2021.
[39] DavidWingate,MohammadShoeybi,andTaylorSorensen. Promptcompressionandcontrastivecondi-
tioningforcontrollabilityandtoxicityreductioninlanguagemodels. arXivpreprintarXiv:2210.03162,
2022.
[40] NeilHoulsby,AndreiGiurgiu,StanislawJastrzebski,BrunaMorrone,QuentinDeLaroussilhe,AndreaGes-
mundo,MonaAttariyan,andSylvainGelly. Parameter-efficienttransferlearningfornlp. InInternational
ConferenceonMachineLearning,pages2790–2799.PMLR,2019.
[41] JunxianHe,ChuntingZhou,XuezheMa,TaylorBerg-Kirkpatrick,andGrahamNeubig. Towardsaunified
viewofparameter-efficienttransferlearning. arXivpreprintarXiv:2110.04366,2021.
[42] ZhoujunCheng,JungoKasai,andTaoYu.Batchprompting:Efficientinferencewithlargelanguagemodel
apis. arXivpreprintarXiv:2301.08721,2023.
12

---
### Page 12

Appendix
A AdditionalObservations
A.1 TokenDecomposition
WedecomposethetokenusageofdifferentpromptparadigmsonHotpotQAintodifferentcomponents
–contextprompts,exemplars,andintermediatesteps. FigureA.1showsthat,comparedtoReWOO,
ReAct consumes significantly more tokens in exemplars. We attribute this gap to the following
reasons: (1)Exemplarsarerepetitivelypromptedforthenumberofreasoningsteps(approximately5
timesintheHotpotQAexperiment),whereasReWOOhasnosuchrepetition;(2)Exemplarsusedin
theReActparadigminevitablyincludeObservationateachreasoningstep,whichcanoccasionally
bealengthyresultfromaWikipediapage. Incontrast,exemplarsusedinReWOOdon’tcontainany
explicitobservations.
7000
6000
5000
4000
3000
2000
1000
0
ReWOO ReAct
egasU
nekoT
Context
Exemplars
Intermediate
Figure7: DecompositionoftokenusageonHotpotQA.
A.2 WhyReWOOoutperformsReAct
ThesuperioraccuracyofReWOOoverReActelicitssurprise, givenourhumanpropensitytobase
futureactionsoncurrentandpreviousobservationsformoreaccuratemoves,ratherthanformulating
comprehensive plans in advance. To further explore such seemingly paradoxical findings, we
randomlyselect100failurecasesfromHotpotQAforbothmethodsandprobeintothefailurereasons.
We label each trajectory with one or more of the following tags: (1) Bad Reasoning, where we
findthereasoningtrajectorymisleadsordeviatesfromthequestion;(2)ToolInefficacy,observed
whenWikipedia[query]isunabletoretrievepertinentinformation. (3)TokenExcess,whereinthe
maximum4096tokenlimitofGPT-3.5isreached,typicallyasaresultofanexcessivenumberof
reasoningsteps;(4)AnswerMiss,whereallreasoningandtoolresponsesareconsideredright,butthe
modelfailstodeducethecorrectanswer;(5)AmbiguousQuestion,ascenarioinwhichtheoriginal
taskeithercontainsanerroneousoroutdatedground-truthlabeloracceptsmultiplevalidanswers.
BadReason. ToolInefficacy TokenExcess AnswerMiss AmbiguousQ.
ReAct 76 20 18 3 17
ReWOO 51 29 0 11 17
WefindthatabadtoolresponseeasilyruinsthereasoningtraceofReAct,resultinginaninfinite
actionlooporrepetition. Infact,weobserveacommonscenarioinReActwhentoolAfails,and
ReActattemptstoinvoketoolB.TheniftoolBfailsaswell,ReActturnsbacktoinvoketoolAagain,
andsoonuntilhittingthetokenlimit. Besides,wefindthatwhenthenumberofreasoningstepsgoes
abovefour,thecontextpromptofReActbecomesextremelylengthy,sometimesleadingtodeviation
fromtheoriginalproblem.
Ontheotherhand,ReWOOcanusuallygenerateareasonableplanningtrajectoryindependentfrom
toolfailures. Suchplans,though"reasonable",cansometimesbeineffectivebecauseofincorrect
13

[TABLE]
7000
Context
6000 Exemplars
Intermediate
5000 egasU
4000
nekoT
3000
2000
1000
0
ReWOO ReAct | Context |  |  |  |  |  |  |  |  | 
 | Exemplars
Intermediate |  |  |  |  |  |  |  |  | 
 |  |  |  |  |  |  |  |  |  | 
 |  |  |  |  |  |  |  |  |  | 
 |  |  |  |  |  |  |  |  |  | 
 |  |  |  |  |  |  |  |  |  | 
 |  |  |  |  |  |  |  |  |  | 
 |  |  |  |  |  |  |  |  |  | 
 |  |  |  |  |  |  |  |  |  | 
 |  |  |  |  |  |  |  |  |  | 
[/TABLE]

[TABLE]
 | BadReason. | ToolInefficacy | TokenExcess | AnswerMiss | AmbiguousQ.
ReAct | 76 | 20 | 18 | 3 | 17
ReWOO | 51 | 29 | 0 | 11 | 17
[/TABLE]

---
### Page 13

expectations. Forinstance,ReWOOusesWikipedia[query]toretrieveinformationaboutaperson,then
itassumesthattheageofthatpersonexistsinthesearchresults,therebyusinganLLM[prompt]later
toextracthisage. SuchanassumptioncanbeerroneouswhentheWikipediaresultsdon’tactually
containhisage. Besides,weobservethatSolversometimesgivesthewrongconclusionevenifall
plansandevidencearesolid. WethinkabetterSolverpromptorprovidingasimpleexemplarcould
mitigatethisissue.
B ImplementationDetails
B.1 InstructionTuning
When instruction-tuning Alpaca 7B, we use the low-rank adaptation (LoRA) following a frame-
workimplementedinhttps://github.com/tloen/alpaca-lora. Thistrickallowsustofine-
tune and specialize Planner 7B model on a single RTX 4090. We use batch-size=128, learning
rate=1e-4, cutff_len=1024 with lora_r=8, and train upon Alpaca 7B (https://huggingface.
co/tloen/alpaca-lora-7b)for10epochs. ThespecializedPlanner7Bisuploadedtohttps:
//huggingface.co/rewoo/planner_7B. Thismodelcanfurtherbenefitfrommoreinstruction
planningdataanddeliberatetrainingsetups.
B.2 Prompts
HerebywedisclosethecontextpromptsandexemplarsusedinReWOO.Thetooldescriptionsand
exemplarsaresubjecttosetupsatruntime. Notably,ReWOOisageneralparadigmandpromptsare
notnecessarilyfixed. Weencouragereadersanduserstoadjustthepromptstailoredtotheirown
needs.
–PLANNER–
Forthefollowingtask,makeplansthatcansolvetheproblemstepbystep. Foreachplan,indicate
whichexternaltooltogetherwithtoolinputtoretrieveevidence. Youcanstoretheevidenceintoa
variable#Ethatcanbecalledbylatertools. (Plan,#E1,Plan,#E2,Plan,...)
Toolscanbeoneofthefollowing:
(1)Google[input]: WorkerthatsearchesresultsfromGoogle. Usefulwhenyouneedtofindshort
andsuccinctanswersaboutaspecifictopic. Theinputshouldbeasearchquery.
(2)Wikipedia[input]: WorkerthatsearchforsimilarpagecontentsfromWikipedia. Usefulwhen
youneedtogetholisticknowledgeaboutpeople,places,companies,historicalevents,orother
subjects. Theresponseislongandmightcontainsomeirrelevantinformation. Theinputshould
beasearchquery.
(3)WolframAlpha[input]: UsefulwhenyouneedtosolveaMathematicalorAlgebraicequation.
Inputshouldbeanequationorfunction.
(4)Calculator[input]: Acalculatorthatcancomputearithmeticexpressions. Usefulwhenyou
needtoperformmathcalculations. Inputshouldbeamathematicalexpression
(5) LLM[input]: A pretrained LLM like yourself. Useful when you need to act with general
worldknowledgeandcommonsense. Prioritizeitwhenyouareconfidentinsolvingtheproblem
yourself. Inputcanbeanyinstruction.
(6)SearchSOTU[input]:Avectorstorethatsearchesforsimilarandrelatedcontentinadocument:
state_of_the_union. Theresultisahugechunkoftextrelatedtoyoursearchbutcanalsocontain
irrelevantinfo. Theinputshouldbeasearchquery.
Forexample,
Task: Thomas,Toby,andRebeccaworkedatotalof157hoursinoneweek. Thomasworkedx
hours. Tobyworked10hourslessthantwicewhatThomasworked,andRebeccaworked8hours
lessthanToby. HowmanyhoursdidRebeccawork?
Plan: GivenThomasworkedxhours,translatetheproblemintoalgebraicexpressionsandsolve
withWolframAlpha. #E1=WolframAlpha[Solvex+(2x−10)+((2x−10)−8)=157]
Plan: FindoutthenumberofhoursThomasworked. #E2=LLM[Whatisx,given#E1]
Plan: CalculatethenumberofhoursRebeccaworked. #E3=Calculator[(2∗#E2−10)−8]
Begin! Describe your plans with rich details. Each Plan should be followed by only one #E.
<Yourtask>
14

---
### Page 14

– SOLVER –
Solvethefollowingtaskorproblem. Tosolvetheproblem,wehavemadestep-by-stepPlanand
retrievedcorrespondingEvidencetoeachPlan. Usethemwithcautionsincelongevidencemight
containirrelevantinformation.
<Plans+Evidence>
NowsolvethequestionortaskaccordingtoprovidedEvidenceabove. Respondwiththeanswer
directlywithnoextrawords.
<Yourtask>
C Trajectories
Inthefollowingsection,weshowseveralreasoningtrajectoriesofReActandReWOOontheevaluated
datasets. AllthepromptingandtoolsaresetupasdiscussedinSection3.1.
C.1 HotpotQA
ReAct
Question: Who made the 1989 comic book, the film version of which Jon Raymond Polito
appearedin?
Thought: IneedtosearchJonRaymondPolito,findthefilmversionheappearedin,thenfind
whomadethe1989comicbook.
Action: Search[JonRaymondPolito]
Observation: JonRaymondPolito(December29,1950–September1,2016)wasanAmerican
characteractor. Inafilmandtelevisioncareerspanning35years,heamassedover220credits.
NotabletelevisionrolesincludedDetectiveSteveCrosettiinthefirsttwoseasonsofHomicide:
Lifeon theStreetand asPhil Bartolionthe firstseasonof CrimeStory. Healso appearedin
severalfilmsincludingTheRocketeer,TheCrowandGangsterSquad,aswellashisworkwith
theCoenbrothers. Heappearedinfiveoftheirfilms,includingMiller’sCrossing,BartonFink
andTheBigLebowski. Politoalsoportrayedlegendary"hungryi"nightclubimpresarioEnrico
BanducciinalargesupportingroleinTimBurton’s2014filmBigEyesstarringAmyAdamsand
ChristophWaltz.
Thought: JonRaymondPolitoappearedinTheRocketeer,TheCrow,GangsterSquad,Miller’s
Crossing,BartonFink,TheBigLebowski,andBigEyes. IneedtosearchTheRocketeerandfind
whomadethe1989comicbook.
Action: Search[TheRocketeer]
15

[TABLE]
Action
Observation
[/TABLE]

---
### Page 15

Observation: TheRocketeer(releasedinternationallyasTheAdventuresoftheRocketeer)is
a1991AmericanperiodsuperherofilmfromWaltDisneyPicturesandTouchstonePictures. It
wasproducedbyCharlesGordon,LawrenceGordon,andLloydLevin,directedbyJoeJohnston,
and stars Billy Campbell, Jennifer Connelly, Alan Arkin, Timothy Dalton, Paul Sorvino, and
TinyRonTaylor. Itisbasedonthecharacterofthesamenamecreatedbycomicbookartistand
writerDaveStevens. Setin1938LosAngeles,California,TheRocketeertellsthestoryofstunt
pilot,CliffSecord,whodiscoversahiddenrocketpackthathethereafterusestoflywithoutthe
needofanaircraft. HisheroicdeedssoonattracttheattentionofHowardHughesandtheFBI,
who are hunting for the missing rocket pack, as well as the Nazi operatives that stole it from
Hughes. DevelopmentforTheRocketeerstartedasfarbackas1983,whenStevenssoldthefilm
rightstothecharacter. SteveMinerandWilliamDearconsidereddirectingTheRocketeerbefore
Johnstonsignedon. ScreenwritersDannyBilsonandPaulDeMeohadcreativedifferenceswith
Disney,causingthefilmtolanguishindevelopmenthell. Thestudioalsointendedtochangethe
trademarkhelmetdesign;DisneyCEOMichaelEisnerwantedastraightNASA-typehelmet,but
Johnstonconvincedthestudiootherwise. JohnstonalsohadtoconvinceDisneytolethimcast
actorBillyCampbellintheleadrole. FilmingforTheRocketeerlastedfromSeptember19,1990,
toJanuary22,1991. ThevisualeffectssequenceswerecreatedanddesignedbyIndustrialLight
&MagicandsupervisedbyanimationdirectorWesTakahashi. ThefilmwasreleasedonJune21,
1991,andreceivedpositivereviewsfromcritics. PlansforRocketeersequelswereabandoned
afterthefilmunderperformedattheboxoffice,grossingonly46millionona35millionbudget.
However,atelevisionseriesbasedonthefilm,withCampbellreprisinghisrole,premieredon
DisneyJuniorinNovember2019. Inearly1991,ToyBizhadtherightstoamassiveRocketeer
toyline,includingdifferentversionsofCliff;thiswasakintotheKennerProductsBatmantoy
lines. Severalprototypesweremade,butthetoylinewaspromptlyshutdown;Disneypulledthe
licensefromToyBizleavingonlyJustToyshavingtherights.
Thought: TheRocketeerisbasedonthecharacterofthesamenamecreatedbycomicbook
artistandwriterDaveStevens. SoDaveStevensmadethe1989comicbook.
Action: Finish[DaveStevens]
ReWOO
Question: Who made the 1989 comic book, the film version of which Jon Raymond Polito
appearedin?
–PLANNER–
Plan: SearchformoreinformationaboutJonRaymondPolito.
#E1=Wikipedia[JonRaymondPolito]
Plan: Searchformoreinformationaboutthe1989comicbook.
#E2=LLM[Whatisthenameofthe1989comicbook? Givencontext: #E1]
Plan: Searchformoreinformationaboutthefilmversionofthecomicbook.
#E3=Wikipedia[#E2filmversion]
Plan: Findoutwhomadethe1989comicbook.
#E4=LLM[Whomadethe1989comicbook #E2? Givencontext: #E3]
–SOLVER–
Plan: SearchformoreinformationaboutJonRaymondPolito.
Evidence: JonRaymondPolito(December29,1950–September1,2016)wasanAmerican
characteractor. Inafilmandtelevisioncareerspanning35years,heamassedover220credits.
NotabletelevisionrolesincludedDetectiveSteveCrosettiinthefirsttwoseasonsofHomicide:
Lifeon theStreetand asPhil Bartolionthe firstseasonof CrimeStory. Healso appearedin
severalfilmsincludingTheRocketeer,TheCrowandGangsterSquad,aswellashisworkwith
theCoenbrothers. Heappearedinfiveoftheirfilms,includingMiller’sCrossing,BartonFink
andTheBigLebowski. Politoalsoportrayedlegendary"hungryi"nightclubimpresarioEnrico
BanducciinalargesupportingroleinTimBurton’s2014filmBigEyesstarringAmyAdamsand
ChristophWaltz.
Plan: Searchformoreinformationaboutthe1989comicbook.
Evidence: TheRocketeer.
Plan: Searchformoreinformationaboutthefilmversionofthecomicbook.
16

[TABLE]
Plan
#E1
Plan
#E2
Plan
#E3
Plan
#E4
[/TABLE]

[TABLE]
Plan
Evidence
[/TABLE]

[TABLE]
Plan
Evidence
Plan
[/TABLE]

---
### Page 16

Evidence: TheRocketeer(releasedinternationallyasTheAdventuresoftheRocketeer)isa
1991 American period superhero film from Walt Disney Pictures and Touchstone Pictures. It
wasproducedbyCharlesGordon,LawrenceGordon,andLloydLevin,directedbyJoeJohnston,
and stars Billy Campbell, Jennifer Connelly, Alan Arkin, Timothy Dalton, Paul Sorvino, and
TinyRonTaylor. Itisbasedonthecharacterofthesamenamecreatedbycomicbookartistand
writerDaveStevens. Setin1938LosAngeles,California,TheRocketeertellsthestoryofstunt
pilot,CliffSecord,whodiscoversahiddenrocketpackthathethereafterusestoflywithoutthe
needofanaircraft. HisheroicdeedssoonattracttheattentionofHowardHughesandtheFBI,
who are hunting for the missing rocket pack, as well as the Nazi operatives that stole it from
Hughes. DevelopmentforTheRocketeerstartedasfarbackas1983,whenStevenssoldthefilm
rightstothecharacter. SteveMinerandWilliamDearconsidereddirectingTheRocketeerbefore
Johnstonsignedon. ScreenwritersDannyBilsonandPaulDeMeohadcreativedifferenceswith
Disney,causingthefilmtolanguishindevelopmenthell. Thestudioalsointendedtochangethe
trademarkhelmetdesign;DisneyCEOMichaelEisnerwantedastraightNASA-typehelmet,but
Johnstonconvincedthestudiootherwise. JohnstonalsohadtoconvinceDisneytolethimcast
actorBillyCampbellintheleadrole. FilmingforTheRocketeerlastedfromSeptember19,1990,
toJanuary22,1991. ThevisualeffectssequenceswerecreatedanddesignedbyIndustrialLight
&MagicandsupervisedbyanimationdirectorWesTakahashi. ThefilmwasreleasedonJune21,
1991,andreceivedpositivereviewsfromcritics. PlansforRocketeersequelswereabandoned
afterthefilmunderperformedattheboxoffice,grossingonly46millionona35millionbudget.
However,atelevisionseriesbasedonthefilm,withCampbellreprisinghisrole,premieredon
DisneyJuniorinNovember2019. Inearly1991,ToyBizhadtherightstoamassiveRocketeer
toyline,includingdifferentversionsofCliff;thiswasakintotheKennerProductsBatmantoy
lines. Severalprototypesweremade,butthetoylinewaspromptlyshutdown;Disneypulledthe
licensefromToyBizleavingonlyJustToyshavingtherights.
Plan: Findoutwhomadethe1989comicbook.
Evidence: DaveStevens.
DaveStevens.
C.2 TriviaQA
ReAct
Question: WhofeaturedonMelanieC’snumberonesingleNeverBeTheSameAgainin2000,
anddiedinacaraccidentin2002?
Thought: IneedtosearchMelanieC’snumberonesingleNeverBeTheSameAgain,findwho
featuredonit,thenfindiftheydiedinacaraccidentin2002.
Action: Search[NeverBeTheSameAgain]
Observation: "NeverBetheSameAgain"isasongbyBritishsinger-songwriterMelanieCfrom
theBritishgirlgroupSpiceGirls,featuringAmericanrapperLisa"LeftEye"LopesofAmerican
girlgroupTLC.Itwasreleasedon20March2000asthethirdsinglefromherfirstsoloalbum,
NorthernStar(1999). Thesongwasco-writtenbyMelanieC,producerRhettLawrence,PaulF.
CruzandLopes. "NeverBetheSameAgain"enteredatthetopoftheUKSinglesChart,beating
Moloko’s "The Time Is Now" to the summit and it was Melanie C’s firstsolo single to reach
numberone. Itsold144,936copiesinitsfirstweekandwasBritain’seighteenthbest-sellingsong
of2000. Thesongwassuccessfulinothermarkets, toppingthechartsinsevencountriesand
receivingpositiveacclaim. ByApril2021,thesonghadsoldmorethan477,000copiesinUK.
ThemusicvideowasdirectedbyFrancisLawrence. ItshowsMelanieCwakingupinafuturistic
homeandpracticingtaichiwithLopes.
Thought:Lisa"LeftEye"LopesfeaturedonMelanieC’snumberonesingleNeverBeTheSame
Againin2000. IneedtosearchLisa"LeftEye"Lopesandfindifshediedinacaraccidentin
2002.
Action: Search[Lisa"LeftEye"Lopes]
17

[TABLE]
Plan
Evidence
DaveStevens.
[/TABLE]

[TABLE]
Action
Observation
[/TABLE]

---
### Page 17

Observation: LisaNicoleLopes(May27,1971–April25,2002),betterknownbyherstage
nameLeftEye,wasanAmericanrapperandsinger.ShewasamemberoftheR&BgirlgroupTLC,
alongsideTionne"T-Boz"WatkinsandRozonda"Chilli"Thomas. Besidesrappingandsinging
backing vocals on TLC recordings, Lopes was the creative force behind the group, receiving
moreco-writingcreditsthantheothermembers. Shealsodesignedsomeoftheiroutfitsandthe
stagefor‘FanMailTour’andcontributedtothegroup’simage,albumtitles,artworks,andmusic
videos. ThroughherworkwithTLC,LopeswonfourGrammyAwards.Duringherbriefsolo
career,LopesscoredtwoUStop10singleswith"NotTonight"and"UKnowWhat’sUp",aswell
asoneUKnumber-onesinglewith"NeverBetheSameAgain",thelatteracollaborationwith
MelanieCoftheBritishgirlgroupSpiceGirls. Shealsoproducedanothergirlgroup,Blaque,
whoscoredaplatinumalbumandtwoUStop10hits. LopesremainstheonlymemberofTLCto
havereleasedasoloalbum. OnApril25,2002,Lopeswaskilledinacarcrashwhileshootinga
documentaryinHonduras. Thevehicleshewasinswervedofftheroadtoavoidhittinganother
vehiclethatstoppedabruptlyinfrontofthem. ThedocumentarywasreleasedasTheLastDaysof
LeftEyeandairedonVH1inMay2007.
Thought:Lisa"LeftEye"LopesfeaturedonMelanieC’snumberonesingleNeverBeTheSame
Againin2000anddiedinacaraccidentin2002.
Action: Finish[Lisa"LeftEye"Lopes]
ReWOO
Question: WhofeaturedonMelanieC’snumberonesingleNeverBeTheSameAgainin2000,
anddiedinacaraccidentin2002?
–PLANNER–
Plan: SearchformoreinformationaboutMelanieC.
#E1=Wikipedia[MelanieC]
Plan: FindoutwhofeaturedonMelanieC’snumberonesingleNeverBeTheSameAgainin
2000.
#E2= LLM[Who featured on Melanie C’s number one single Never Be The Same Again in
2000? Givencontext: #E1]
Plan: Searchformoreinformationaboutthefeaturedartist.
#E3=Wikipedia[#E2]
Plan: Findoutifthefeaturedartistdiedinacaraccidentin2002.
#E4=LLM[Did #E2dieinacaraccidentin2002? Givencontext: #E2]
–SOLVER–
Plan: SearchformoreinformationaboutMelanieC.
Evidence:Couldnotfind[MelanieC].Similar:[’MelanieC’,’MelanieCdiscography’,’Melanie
C(album)’,’ITurntoYou(MelanieCsong)’,’IWantCandy’,’NorthernStar(MelanieCalbum)’,
’MelB’,’Melanie’,"IDon’tKnowHowtoLoveHim",’Reason(MelanieCalbum)’]
Plan: FindoutwhofeaturedonMelanieC’snumberonesingleNeverBeTheSameAgainin
2000.
Evidence: LisaLeftEyeLopes.
Plan: Searchformoreinformationaboutthefeaturedartist.
18

[TABLE]
Plan
#E1
Plan
[/TABLE]

[TABLE]
Plan
#E3
Plan
#E4
[/TABLE]

[TABLE]
Plan
Evidence
[/TABLE]

[TABLE]
Evidence
Plan
[/TABLE]

---
### Page 18

Evidence: LisaNicoleLopes(May27,1971–April25,2002),betterknownbyherstagename
LeftEye,wasanAmericanrapperandsinger. ShewasamemberoftheR&BgirlgroupTLC,
alongsideTionne"T-Boz"WatkinsandRozonda"Chilli"Thomas. Besidesrappingandsinging
backing vocals on TLC recordings, Lopes was the creative force behind the group, receiving
moreco-writingcreditsthantheothermembers. Shealsodesignedsomeoftheiroutfitsandthe
stagefor‘FanMailTour’andcontributedtothegroup’simage,albumtitles,artworks,andmusic
videos. ThroughherworkwithTLC,LopeswonfourGrammyAwards.Duringherbriefsolo
career,LopesscoredtwoUStop10singleswith"NotTonight"and"UKnowWhat’sUp",aswell
asoneUKnumber-onesinglewith"NeverBetheSameAgain",thelatteracollaborationwith
MelanieCoftheBritishgirlgroupSpiceGirls. Shealsoproducedanothergirlgroup,Blaque,
whoscoredaplatinumalbumandtwoUStop10hits. LopesremainstheonlymemberofTLCto
havereleasedasoloalbum. OnApril25,2002,Lopeswaskilledinacarcrashwhileshootinga
documentaryinHonduras. Thevehicleshewasinswervedofftheroadtoavoidhittinganother
vehiclethatstoppedabruptlyinfrontofthem. ThedocumentarywasreleasedasTheLastDays
ofLeftEyeandairedonVH1inMay2007. Plan: Findoutifthefeaturedartistdiedinacar
accidentin2002.
Evidence: Yes.
LisaLeftEyeLopes.
C.3 GSM8K
ReAct
Question: Johndecidestobuysomebirds. Hegot50dollarsfromeachofhis4grandparents. If
eachbirdcosts$20,howmanywingsdidallthebirdshave?
Thought: I need to know how many birds John can buy with the money he got from his
grandparents.
Action: Calculator[(50*4)/20]
Observation: 10.0
Thought: NowIknowhowmanybirdsJohncanbuy. Ineedtoknowhowmanywingsallthe
birdshave. Action: Calculator[10.0*2]
Observation: 20.0
Thought: Inowknowthefinalanswer
Action: Finish[20.0wings]
ReWOO
Question: Johndecidestobuysomebirds. Hegot50dollarsfromeachofhis4grandparents. If
eachbirdcosts$20,howmanywingsdidallthebirdshave?
–PLANNER–
Plan: CalculatethetotalamountofmoneyJohnreceivedfromhis4grandparents.
#E1=Calculator[50*4]
Plan: Calculatethetotalcostofallthebirds.
#E2=Calculator[20*(#E1/20)]
Plan: CalculatethetotalnumberofbirdsJohncanbuy.
#E3=Calculator[#E1/20]
Plan: Calculatethetotalnumberofwingsallthebirdshave.
#E4=Calculator[#E3*2]
–SOLVER–
Plan: CalculatethetotalamountofmoneyJohnreceivedfromhis4grandparents.
19

[TABLE]
Evidence
LisaLeftEyeLopes
[/TABLE]

[TABLE]
Action
Observation
Thought
[/TABLE]

[TABLE]
Observation
Thought
Action
[/TABLE]

[TABLE]
Plan
#E1
Plan
#E2
Plan
#E3
Plan
#E4
[/TABLE]

---
### Page 19

Evidence: 200
Plan: Calculatethetotalcostofallthebirds.
Evidence: 200.0
Plan: CalculatethetotalnumberofbirdsJohncanbuy.
Evidence: 10.0
Plan: Calculatethetotalnumberofwingsallthebirdshave.
Evidence: 20.0
20
C.4 StrategyQA
ReAct
Question: Answerwith’Yes’or’No’: Isitsociallyacceptabletowearanicondepictingcrucifix-
ion?
Thought: I’mnotsureabouttheculturalandsocialnormsregardingwearingacrucifixionicon.
Action: Google[Isitsociallyacceptabletowearacrucifixionicon?]
Observation:Protestantsusethecrossasthesymbolofourfaith,notacrucifix....Isitacceptable
towearacrucifix,ifyouarenotpracticingbutstillrespect...
Thought: Thesearchresultsarenotclearonwhetheritissociallyacceptableornot. Ineedmore
information.
Action: LLM[Whatistheculturalandsocialsignificanceofwearingacrucifixionicon?]
Observation: Symboloffaith.
Thought: TheLLM’sresponseisnothelpful. Ineedtotryadifferentapproach.
Action: Wikipedia[Crucifixioniconculturalsignificance]
Observation: Couldnotfind[Crucifixioniconculturalsignificance]. Similar: [’Crucifixionof
Jesus’, ’Christian symbolism’, ’Cultural impact of Madonna’, ’Jesus in Christianity’, ’Jesus’,
’Depiction of Jesus’, ’Ascension of Jesus’, ’Transfiguration of Jesus’, ’Repatriation (cultural
property)’,’Limbo’]
Thought: Ineedtorephrasemysearchquerytogetmorerelevantresults.
Action: Google[Culturalsignificanceofwearingacrucifixionicon]
Observation: AdefiningsymboloftheChristianfaith,thecrossisrecognizedgloballyasasign
oflove,loss,salvationandgratitude,andisdepictedin...
Thought:Basedonthesearchresults,itseemsthatwearingacrucifixioniconissociallyacceptable
inChristiancultures.
Action: LLM[Whataretheculturalnormsregardingwearingacrucifixionicon?]
Observation: Varies.
Thought:TheLLM’sresponseisnothelpful. Ineedtomakeadecisionbasedontheinformation
Ihavegathered.
Action:Finish[ItisgenerallysociallyacceptabletowearacrucifixioniconinChristiancultures.]
ReWOO
Question: Answerwith’Yes’or’No’: Isitsociallyacceptabletowearanicondepictingcrucifix-
ion?
–PLANNER–
Plan: Searchformoreinformationaboutcrucifixion
#E1=Wikipedia[Crucifixion]
Plan: Findoutifitissociallyacceptabletowearanicondepictingcrucifixion
#E2=LLM[Isitsociallyacceptabletowearanicondepictingcrucifixion? Givencontext: #E1]
20

[TABLE]
Evidence
Plan
Evidence
Plan
Evidence
Plan
Evidence
20
[/TABLE]

[TABLE]
Thought
Action
Observation
[/TABLE]

[TABLE]
Action
Observation
Thought
Action
Observation
[/TABLE]

[TABLE]
Action
Observation
[/TABLE]

[TABLE]
Action
Observation
Thought
[/TABLE]

[TABLE]
Plan
#E1
Plan
#E2
[/TABLE]

---
### Page 20

–SOLVER–
Plan: Searchformoreinformationaboutcrucifixion
Evidence: Crucifixionisamethodofcapitalpunishmentinwhichthevictimistiedornailedto
alargewoodencrossorbeamandlefttohanguntileventualdeath. Itwasusedasapunishment
bythePersians,CarthaginiansandRomans,amongothers. Crucifixionhasbeenusedinpartsof
theworldasrecentlyasthe21stcentury.ThecrucifixionofJesusiscentraltoChristianity,andthe
cross(sometimesdepictingJesusnailedtoit)isthemainreligioussymbolformanyChristian
churches.
Plan: Findoutifitissociallyacceptabletowearanicondepictingcrucifixion
Evidence: Yes.
Yes.
C.5 PhysicsQuestion
ReAct
Question: Duringtheirphysicsfieldtriptotheamusementpark,TylerandMariatookarideron
theWhirligig. TheWhirligigrideconsistsoflongswingswhichspininacircleatrelativelyhigh
speeds. Aspartoftheirlab,TylerandMariaestimatethattheriderstravelthroughacirclewitha
radiusof5.7mandmakeoneturnevery7.1seconds. Determinethespeedoftheridersonthe
Whirligig.
Thought: IneedtocalculatethespeedoftheridersontheWhirligig.
Action: WolframAlpha[speedofarideronawhirligigwitharadiusof5.7mandoneturnevery
7.1seconds]
Observation: WolframAlphawasn’tabletoanswerit
Thought: Ineedtocalculatethespeedusingtheformulaforangularvelocity.
Action: Calculator[(2*3.14*5.7)/7.1]
Observation: 5.041690140845071
Thought: Inowknowthefinalanswer
Action: Finish[TheridersontheWhirligigtravelataspeedof5.041690140845071m/s.]
ReWOO
Question: Duringtheirphysicsfieldtriptotheamusementpark,TylerandMariatookarideron
theWhirligig. TheWhirligigrideconsistsoflongswingswhichspininacircleatrelativelyhigh
speeds. Aspartoftheirlab,TylerandMariaestimatethattheriderstravelthroughacirclewitha
radiusof5.7mandmakeoneturnevery7.1seconds. Determinethespeedoftheridersonthe
Whirligig.
–PLANNER–
Plan: Usetheformulaforlinearvelocitytocalculatethespeedoftheriders.
#E1=LLM[Whatistheformulaforlinearvelocity?]
Plan: Identifythevaluesneededtosolveforthespeedoftheriders.
#E2=LLM[Whatvaluesareneededtosolveforlinearvelocityinthisproblem?]
Plan: Usethegiveninformationtocalculatethespeedoftheriders.
#E3=Calculator[2*3.14*5.7/7.1]
–SOLVER–
Plan: Usetheformulaforlinearvelocitytocalculatethespeedoftheriders.
Evidence: v=d/t
Plan: Identifythevaluesneededtosolveforthespeedoftheriders.
Evidence: Time,distance.
21

[TABLE]
Plan
Evidence
[/TABLE]

[TABLE]
Plan
Evidence
Yes.
[/TABLE]

[TABLE]
Thought
Action
[/TABLE]

[TABLE]
Observation
Thought
Action
Observation
Thought
Action
[/TABLE]

[TABLE]
Plan
#E1
Plan
#E2
Plan
#E3
[/TABLE]

[TABLE]
Plan
Evidence
Plan
Evidence
[/TABLE]

---
### Page 21

Plan: Usethegiveninformationtocalculatethespeedoftheriders.
Evidence: 5.041690140845071
5.041690140845071m/s
C.6 SportsUnderstanding
ReAct
Question: Determinewhetherthefollowingstatementorstatementsareplausibleorimplausible:
JorgeSolerenteredtheattackingzone
Thought: IneedtodetermineifJorgeSolerenteredtheattackingzone.
Action: LLM[DidJorgeSolerentertheattackingzone?]
Observation: Yes.
Thought: Inowknowthefinalanswer.
Action: Finish[Plausible](wrong)
ReWOO
Question: Determinewhetherthefollowingstatementorstatementsareplausibleorimplausible:
JorgeSolerenteredtheattackingzone
–PLANNER–
Plan: UseGoogletosearchfornewsarticlesaboutJorgeSolerenteringtheattackingzone.
#E1=Google[JorgeSolerattackingzone]
–SOLVER–
Plan: UseGoogletosearchfornewsarticlesaboutJorgeSolerenteringtheattackingzone.
Evidence: JorgeSolercareerbattingstatisticsforMajorLeague,MinorLeague,andpostseason
baseball.
Implausible
C.7 SOTUQA
ReAct
Question: BasedonStateoftheUnionAddress2023: Whatarethedifferenceintherolesof
McConnellandChuckSchumer?
Thought: IneedtofindinformationabouttherolesofMcConnellandChuckSchumerinthe
StateoftheUnionAddress2023.
Action:SearchSOTU[McConnellandChuckSchumerrolesinStateoftheUnionAddress2023]
22

[TABLE]
Plan
Evidence
5.041690140845071m/s
[/TABLE]

[TABLE]
Thought
Action
Observation
Thought
Action
[/TABLE]

[TABLE]
Plan
#E1
[/TABLE]

[TABLE]
Plan
Evidence
[/TABLE]

---
### Page 22

Observation: FollowingisatranscriptofPresidentBiden’sStateoftheUnionaddressin2023.
Mr. Speaker. MadamVicePresident. OurFirstLadyandSecondGentleman.
MembersofCongressandtheCabinet. Leadersofourmilitary.
Mr. ChiefJustice,AssociateJustices,andretiredJusticesoftheSupremeCourt.
Andyou,myfellowAmericans.
Istarttonightbycongratulatingthemembersofthe118thCongressandthenewSpeakerofthe
House,KevinMcCarthy.
Mr. Speaker,Ilookforwardtoworkingtogether.
IalsowanttocongratulatethenewleaderoftheHouseDemocratsandthefirstBlackHouse
MinorityLeaderinhistory,HakeemJeffries.
CongratulationstothelongestservingSenateLeaderinhistory,MitchMcConnell.
AndcongratulationstoChuckSchumerforanothertermasSenateMajorityLeader,thistimewith
anevenbiggermajority.
AndIwanttogivespecialrecognitiontosomeonewhoIthinkwillbeconsideredthegreatest
Speakerinthehistoryofthiscountry,NancyPelosi.
Thought: ThesearchresultdidnotprovidetheinformationIwaslookingfor. Ineedtotrya
differentapproach.
Action: LLM[WhatarethedifferencesintherolesofMitchMcConnellandChuckSchumerin
theStateoftheUnionAddress2023?]
Observation: McConnell: Preside. Schumer: Deliverresponse.
Thought:I now know the roles of McConnell and Chuck Schumer in the State of the Union
Address2023.
Action:Finish[McConnellpresidedovertheaddresswhileChuckSchumerdeliveredtheresponse.]
ReWOO
Question: BasedonStateoftheUnionAddress2023: Whatarethedifferenceintherolesof
McConnellandChuckSchumer?
–PLANNER–
Plan: UseSearchSOTUtofindrelevantsectionsoftheStateoftheUnionAddress2023that
mentiontherolesofMcConnellandChuckSchumer.
#E1=SearchSOTU["McConnellChuckSchumerrolesdifference"]
Plan: SummarizethedifferencesintherolesofMcConnellandChuckSchumer.
#E2=LLM["SummarizethedifferencesintherolesofMcConnellandChuckSchumerbased
on #E1."]
–SOLVER–
Plan: UseSearchSOTUtofindrelevantsectionsoftheStateoftheUnionAddress2023that
mentiontherolesofMcConnellandChuckSchumer.
Evidence: FollowingisatranscriptofPresidentBiden’sStateoftheUnionaddressin2023.
Mr. Speaker. MadamVicePresident. OurFirstLadyandSecondGentleman.
MembersofCongressandtheCabinet. Leadersofourmilitary.
Mr. ChiefJustice,AssociateJustices,andretiredJusticesoftheSupremeCourt.
Andyou,myfellowAmericans.
Istarttonightbycongratulatingthemembersofthe118thCongressandthenewSpeakerofthe
House,KevinMcCarthy.
Mr. Speaker,Ilookforwardtoworkingtogether. Ialsowanttocongratulatethenewleaderofthe
HouseDemocratsandthefirstBlackHouseMinorityLeaderinhistory,HakeemJeffries.
CongratulationstothelongestservingSenateLeaderinhistory,MitchMcConnell.
AndcongratulationstoChuckSchumerforanothertermasSenateMajorityLeader,thistimewith
anevenbiggermajority.
AndIwanttogivespecialrecognitiontosomeonewhoIthinkwillbeconsideredthegreatest
Speakerinthehistoryofthiscountry,NancyPelosi.
Plan: SummarizethedifferencesintherolesofMcConnellandChuckSchumer.
Evidence: McConnellisSenateMajorityLeader,SchumerisSenateMinorityLeader.
23

[TABLE]
Observation
Thought
[/TABLE]

[TABLE]
#E1
Plan
#E2
[/TABLE]

[TABLE]
Plan
Evidence
[/TABLE]

---
### Page 23

McConnellisSenateMajorityLeader,SchumerisSenateMinorityLeader.
C.8 OtherOpen-domainCuratedTasks
Followingareseveralcuratedtasksfeaturingreal-worldALMusecases. Weadditionallyprovidea
widerrangeofretrievalandactingtoolstodemonstratethepotentialofReWOO.
Additionaltoolsinclude:
Yelp[input]: Workerthatgivesrestaurantinformationincludingreviews,ratingsandpricesfromYelp.
Inputshouldbeasearchquery.
Twitter[input]: WorkerthatsearchesresultsfromTwitter. Usefulwhenyouneedtofindtweetsabout
atopic. Inputshouldbeasearchquery.
Location[input]: Workerthatretrievesuser’scurrentlocation. Inputshouldbeempty
Time[input]: Workerthatretrievescurrenttime. Inputshouldbeempty
Email[input]: WorkerthatcansendEmails. Usefulwhenyouneedtosendsomeoneemail. Input
shouldbeinthreeparts: thetargetemailaddress,subjectandbody,separatedbyasemicolon.
Stock[input]: Workerthatretrievescurrentstockmarketanalysisandrecommendations. Inputshould
beempty.
TradeStock[input]: WorkerthatconnectstoBackTradertooperateatradingstrategy. Inputshouldbe
intwoparts,Stocktickerandindicatorlevel,separatedbysemicolon.
Draw[input]: Workerthatcandrawandsaveapicturebasedonyourprompt. Inputshouldbea
descriptivepromptforyourpicture.
Tryingtogetsomecoffee. IstherearecommendedCafenearby?
–PLANNER–
Plan: Findouttheuser’scurrentlocation. #E1=Location[]
Plan: SearchforrecommendedCafeneartheuser’scurrentlocation.
#E2=Yelp[Cafenear #E1]
–SOLVER–
Plan: Findouttheuser’scurrentlocation.
Evidence: JerseyCity,NJ,07302
Plan: SearchforrecommendedCafeneartheuser’scurrentlocation.
Evidence: SemicolonCafe. Ratings: 4.5stars;Pricerangeis$$. Phonenumber: (201)332-8148.
Reviewerssay: SemicolonCafeisoneofmyfavoritegotosinJerseyCity! Ilovetheflavorsin
theirsandwichesandtheirlattesarewonderful. Thestaffarealsosuperniceandmakeyoufeel
welcomed. Theirshavediceistasty,sweet,andtheperfecttreatafteralongday. Thisplaceisa
10/10,wouldrecommend.
Yes,SemicolonCafeis1.6milesawayandhas4.5stars.
WriteprofYannLeCunanemail,askingifhe’shiringTAfor2023FallDS-1008DeepLearning.
–PLANNER–
Plan: Retrieveuser’scurrentlocation.
#E1=Location[]
Plan: Retrievecurrenttime.
#E2=Time[]
24

[TABLE]
Plan
Plan
#E2
[/TABLE]

[TABLE]
Plan
Evidence
Plan
Evidence
[/TABLE]

[TABLE]
Plan
#E1
Plan
#E2
[/TABLE]

---
### Page 24

Plan: SearchforYannLeCun’semailaddress.
#E3=Google[YannLeCun’semailaddress]
Plan: Composeemailwithtargetaddress,subjectandbody.
#E4=Email[#E3;DS-1008DeepLearningTA2023Fall;HiProf. YannLeCun,Iamwriting
toinquireaboutanyTApositionopeningsforyourDS-1008DeepLearningcoursein2023Fall
semester. Iamveryinterestedinthecourseandwouldlovetocontributetotheclass. Thankyou
foryourtime. Bestregards,[Name]]
–SOLVER–
Plan: Retrieveuser’scurrentlocation.
Evidence: JerseyCity,NJ,07302
Plan: Retrievecurrenttime.
Evidence: 6:12PMEST,May8,2023
Plan: SearchforYannLeCun’semailaddress.
Evidence: @lecun.org. @fb.com. @courant.nyu.edu.
Plan: Composeemailwithtargetaddress,subjectandbody.
Evidence: emailsent
Subject: RequestforTAPositionfor2023FallDS-1008DeepLearning
DearProfessorLeCun,
Iamwritingtoinquireifyouarehiringteachingassistantsforyour2023FallDS-1008DeepLearning
course. IamcurrentlylocatedinJerseyCity,NJ,07302andthetimehereis5:44PMEST,May4,
2023.
IampassionateaboutdeeplearningandIbelievemyknowledgeandexperienceinthefieldwould
makemeanidealcandidateforthisposition. Iameagertolearnmoreaboutthepositionanddiscuss
howIcancontributetothecourse.
Thankyouforyourtimeandconsideration.
Sincerely,[YourName]
Isthereanystockyourecommendbuyingtoday?
–PLANNER–
Plan: Retrievecurrentlocation.
#E1=Location[]
Plan: Retrievecurrenttime.
#E2=Time[]
Plan: Retrievestockmarketanalysisandrecommendation.
#E3=Stock[]
Plan: ConnecttoBackTradertooperateatradingstrategy.
#E4=TradeStock[#E3;indicatorlevel]
–SOLVER–
Plan: Retrievecurrentlocation.
Evidence: JerseyCity,NJ,07302
Plan: Retrievecurrenttime.
Evidence: 5:44PMEST,May4,2023
Plan: Retrievestockmarketanalysisandrecommendation.
Evidence: DPSTshowsBUY_AND_HOLDsignalat$4.03. Confidence: 7.0
Plan: ConnecttoBackTradertooperateatradingstrategy.
Evidence: Noevidencefound
Yes,DPSTat$4.03withaBUY_AND_HOLDsignalandaconfidenceof7.0.
25

[TABLE]
Plan
#E3
Plan
#E4
[/TABLE]

[TABLE]
Plan
Evidence
Plan
Evidence
Plan
Evidence
Plan
Evidence
Subject: RequestforTAPositionfor2023FallDS-1008DeepLearning
DearProfessorLeCun,
Iamwritingtoinquireifyouarehiringteachingassistantsforyour2023FallDS-1008DeepLearning
course. IamcurrentlylocatedinJerseyCity,NJ,07302andthetimehereis5:44PMEST,May4,
2023.
IampassionateaboutdeeplearningandIbelievemyknowledgeandexperienceinthefieldwould
makemeanidealcandidateforthisposition. Iameagertolearnmoreaboutthepositionanddiscuss
howIcancontributetothecourse.
Thankyouforyourtimeandconsideration.
Sincerely,[YourName]
[/TABLE]

[TABLE]
Plan
#E1
Plan
#E2
Plan
#E3
Plan
#E4
[/TABLE]

[TABLE]
Plan
Evidence
Plan
Evidence
Plan
Evidence
Plan
Evidence
Yes,DPSTat$4.03withaBUY_AND_HOLDsignalandaconfidenceof7.0.
[/TABLE]

---
### Page 25

Drawalogoformyproject–ItmodularizesPlanner,Worker,andSolvertosolvehardtaskslike
humans. ItrepresentstheembryoofAGIinanefficientandscalableway.
–PLANNER–
Plan: Generateasketchforthelogo.
#E1=Draw[AsketchofaPlanner,aSolver,andbunchofWorkersconnectedtogether,repre-
sentingtheembryooffutureAGIinacostefficientway.]
Plan: Enhancethesketchtomakeitlookmoreprofessional.
#E2=Draw[Enhance #E1tomakeitlookmoreprofessional.]
–SOLVER–
Drawalogoformyproject–ItmodularizesPlanner,Worker,andSolvertosolvehardtaskslike
humans. ItrepresentstheembryoofAGIinanefficientandscalableway.
Plan: Generateasketchforthelogo.
Evidence: Drawingsavedtomy_pic.png
Plan: Enhancethesketchtomakeitlookmoreprofessional.
Evidence: Noevidencefound
Drawingsavedtomy_pic.png. Enhancethesketchtomakeitlookmoreprofessional.
26

[TABLE]
Plan
#E1
[/TABLE]

[TABLE]
Plan
#E2
[/TABLE]

[TABLE]
Plan
Evidence
Plan
Evidence
Drawingsavedtomy_pic.png. Enhancethesketchtomakeitlookmoreprofessional.
[/TABLE]
