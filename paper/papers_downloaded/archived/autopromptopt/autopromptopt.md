# Autopromptopt

Source: autopromptopt.pdf


---
### Page 1

AutoPDL: Automatic Prompt Optimization for LLM Agents
1 2 2 2
ClaudioSpiess MandanaVaziri LouisMandel MartinHirzel
1UCDavis
2IBMResearch
Abstract The performance of large language models (LLMs) depends on how they are prompted,
withchoicesspanningboththehigh-levelpromptingpattern(e.g.,Zero-Shot,CoT,ReAct,
ReWOO)andthespecificpromptcontent(instructionsandfew-shotdemonstrations).Man-
uallytuningthiscombinationistedious,error-prone,andspecifictoagivenLLMandtask.
Therefore,thispaperproposesAutoPDL,anautomatedapproachtodiscoveringgoodLLM
agent configurations. Our approach frames this as a structured AutoML problem over a
combinatorialspaceofagenticandnon-agenticpromptingpatternsanddemonstrations,us-
ingsuccessivehalvingtoefficientlynavigatethisspace.Weintroducealibraryimplement-
ingcommonpromptingpatternsusingthePDLpromptprogramminglanguage. AutoPDL
solutionsarehuman-readable,editable,andexecutablePDLprogramsthatusethislibrary.
Thisapproachalsoenablessource-to-sourceoptimization,allowinghuman-in-the-loopre-
finementandreuse.EvaluationsacrossthreetasksandsevenLLMs(rangingfrom3Bto70B
parameters)showconsistentaccuracygains(9.21±15.46percentagepoints),upto67.5pp,
andrevealthatselectedpromptingstrategiesvaryacrossmodelsandtasks.
1 Introduction
Largelanguagemodels(LLMs)andLLM-basedagentsexcelatavarietyoftasks,includingquestion
answering,mathwordproblems,andprogramming. TheperformanceofanLLMdependsheavily
on how it is prompted, and there are a variety of popular prompting patterns. These include
zero-shotorfew-shot(Brownetal.2020)promptingwithchain-of-thought(CoT)(Weietal.2022),
zero-shot CoT (Kojima et al. 2022), as well as agentic patterns such as ReAct (Yao et al. 2023) or
ReWOO (Xu et al. 2023). However, given a dataset D
test
with a loss function L, e.g., error rate,
it is not clear which pattern will do best. Furthermore, besides the pattern A, performance also
dependsonthepromptp,includingfew-shotsamplesandinstructions.Theproblemisthustofind
acombinationA∗ ofapatternalongwithanoptimizedpromptthatminimizesL. Thisisusually
p
doneviamanualpromptengineering,butthatistediousandhastoberepeatedifanewLLMcomes
along. Therefore,thispaperexploreshowtofindA∗ usingautomatedmachinelearning(AutoML).
p
Andforuserstotrusttheresultortotweakitfurther,A∗ itselfshouldbeeasytoreadandedit.
p
Agentframeworks,suchasCrewAI(Moura2023)orAutoGen(Q.Wuetal.2023),containpre-
built agent patterns with prompts optimized for proprietary frontier models and common tasks.
Unfortunately,theirpromptsaredeeplyburied(Schluntzetal.2024),makingthemhardtomodify
and adapt to non-frontier models or novel tasks. Moreover, the prompting pattern is fixed to a
variation of ReAct, limiting flexibility in customizing the prompt structure. Prompt optimizers,
suchasDSPy(Khattabetal.2024),optimizefew-shotsamplesforin-contextlearning(ICL)and/or
instructionsinthepromptp. Unfortunately, theydonotautomaticallyselectthepromptingpat-
ternAanddonotreturnhuman-readablecode.
Weformulatetheproblemoffindingagoodpatternandcorrespondingpromptbydefiningand
thenexploringacombinedsearchspace. WewereinspiredbytheAutoMLliteratureoncombined
search spaces of machine-learning algorithms and their hyperparameters (Thornton et al. 2013),
exceptthat(i)insteadofdiscreteorcontinuoushyperparameters,weexploretextualICLsamples,
instructions, and prompting patterns; (ii) instead of classification or regression tasks, we tackle
AnearlierversionofthispaperwaspublishedatAutoML2025.
ThisversionaddsmissingstandarddeviationsinTable1. 1 ©2025theauthors,releasedunderCCBY4.0
5202
voN
3
]GL.sc[
5v56340.4052:viXra

---
### Page 2

generativetasks;and(iii)insteadofmodeltrainingorfine-tuning,wefocusonin-contextlearning.
WeassumeadatasetwithavalidationsetD ,testsetD ,aswellasanexamplebankD for
valid test train
few-shot samples. D is used during the optimization process to evaluate the performance of
valid
a configuration, whereasD is used once upon completion, to evaluate the performance of the
test
bestperformingconfiguration. Asusual,toavoidover-fitting,weassumethesearedisjointfrom
eachother. TheproblemstatementistofindA
p
∗ =argminL(A
p
,D valid),where:
A p∈AP
• A ∈ A ={Zero-Shot,CoT,ReWOO,ReAct} isthepromptingpattern,and
• p = ⟨n,d train ,instr⟩ ∈ P is the prompt, comprising a numbern ≤ |D train| of few-shot samples,
theactualfew-shotsamplesd train ∈ (D train)n,andaninstructioninstr ∈ I. Aconcreteexample
ofP isprovidedinFigureA1andFigureA2.
To avoid getting stuck in local minima while saving compute and finding a solution with a low
loss, we explore the search space A using successive halving (Jamieson et al. 2016). To make
P
the initial search space A user-interpretable, and the final solution A∗ both human readable
P p
and executable, we express them in a YAML-based prompting language, PDL (Vaziri et al. 2024).
PDL’s structured format makes it easy to modify both the initial search space and the optimized
program, and ensures the final solution remains directly executable. We introduce a library for
PDLthatimplementseachofthecommonpromptingpatternsinA. TheinitialsearchspaceA
P
isaYAMLfilewithvariouschoicepointsforAutoMLtodecide. AndthesolutionA∗ isacustom-
p
tailoredPDLprogramoptimizedforthegiventask,asgivenbythedatasetandlossfunction. The
developercanreadoreventweakeitherorbothasdesired.
Weevaluateouroptimizeronthreetasks(questionanswering,math,andprogramming),using
sevenLLMssizedbetween3Band70Bparameters. Wefindthattheoptimizeroftengivesaccuracy
boostsinthe6–30%range,insomecaseshigher. Giventhesametask,differentpatternsA ∈ Ado
bestfordifferentmodels.Conversely,giventhesamemodel,differentpatternsdobestfordifferent
tasks. Besides this variability in the chosen patternA, our experiments also revealed variability
intheoptimizedpromptsp = ⟨n,d train ,instr⟩. Wealsofoundthatwhentrainingdataforataskis
missing,datafromarelatedbutdifferentdatasetcanhelp.Also,whilemostofourexperimentsuse
moderately-sizedopenmodels,wealsoshowouroptimizedsolutionscanbenefitfrontiermodels.
Thispapermakesthreeprimarycontributions:
1. Jointlysearchingpatternandprompt: priorworkinpromptoptimizationhasnotinvestigated
searchingjoint searchspaces,includingagenticpatterns.
2. Noonesizefitsall: wefindthatdifferentmodelssometimeshavedifferingoptimalpromptpat-
ternsforthesamebenchmark,suggestingthatthereisnotonesingleoptimalpromptpattern.
3. Source-to-sourceoptimization:weproposethefirstsource-to-sourceoptimizerforLLMprompt
programs,whereboththeinitialsearchspaceandthefinalsolutionarepromptprogramsinthe
samelanguage,makingthefinalsolutionbothhuman-readableandexecutable.
Overall, this paper shows how to apply AutoML to automatically discover agentic or non-
agenticLLMpromptsandpatternsoptimizedforagiventask. WemakeourAutoPDLimplemen-
tation available at https://github.com/IBM/prompt-declaration-language, and release the repro-
ductionpackageusedfortheexperimentsinthisworktothecommunity.
2 Background
ThispaperusesPDL(Vazirietal.2024)asarepresentationforexploringthesearchspaceofpro-
grams.PDLprogramsaredeclarativeandcombinehumanreadabilitywitheaseofexecution.They
representthecompositionofcallstoLLMsandtools,abstractingawaytheplumbingnecessaryfor
2

---
### Page 3

1 text:
2 - role: tools
3 text: ${ tools }
4 - "Out of 1400 participants, 400 passed the test. What percentage is that?\n"
5 - def: actions
6 model: replicate/ibm-granite/granite-3.1-8b-instruct
7 parser: json
8 spec: [{ name: str, arguments: { expr: str }}]
9 - if: ${ actions[0].name == "calc" }
10 then:
11 lang: python
12 code: result = ${ actions[0].arguments.expr }
Figure1:BasicexampleofaPDLprogram.
suchcompositions. TheoutputoftheoptimizerisalsoaPDLprogram,ratherthansimpletextual
prompts,soitisfullyexecutableandcouldbefurtherrefinedbyadeveloper.
Figure1showsasimplePDLprogramthatusesatooltoansweraquery. PDLisbasedonthe
premisethatinteractionswithanLLMaremainlyforthepurposeofgeneratingdata. So,itallows
userstospecifytheshapeofdatatobegeneratedinadeclarativeway(inYAML),andisagnostic
ofanyprogramminglanguage. ThefirstlineofFigure1specifiesthatwearecreatingsometext.
Next,thefirstblockintheitemizedlistdefinesthetoolsprompt. Line3containsauseofvariable
tools, expressed as a Jinja expression. This variable is defined as the JSON Schema specification
ofacalculatortool(notshowninthisfigure,forthefullprogramseeAppendix8.2). Line4isthe
user query prompt. We do not specify the role explicitly as user is the default role for prompts.
Lines 5 through 8 show a model call. In PDL, the background context is accumulated implicitly,
so the output of all blocks executed so far will be passed to the LLM as a list of input messages.
The result of the model call is assigned to the variable actions (line 5). The model to be called
is specified on line 6 (PDL is based on LiteLLM,1 so this is a LiteLLM model id). Finally, lines 7
and8saythatweparsetheoutputofthemodelasJSONandtype-checkitaccordingtothetype
on line 8. Furthermore, when the inferencing server supports it, model calls with a schema use
constraineddecoding(Willardetal.2023),enforcingsyntacticallycorrectJSON.2
Online9,anif-statementcheckswhethertheoutputoftheLLMasksforthecalculatortool. If
so,weuseaPythoncodeblocktocomputetherequestedtoolcall(lines11and12). Whenweexe-
cutethisprogramusingthePDLinterpreter,weobtainallthemodelinputs,followedbythemodel
output,andfinallytheoutputofthetoolcall. PDLhasarichsetofcontrolstructurestoallowwrit-
ingavarietyofpromptingpatterns,aswellasfunctionstosupportlibraries. Forinstance,Figure3
shows a function call on line 4. In this paper, we consider the problem of automatically tuning
promptsandchoosingpromptingpatternsforagivendataset. Thefollowingsectionexplainsour
approachinfurtherdetail.
3 AutoPDLApproach
Figure2givesanoverviewofourapproach. Referringtothenumbersinthearrows:
(1) The input task is given by two disjoint datasets D
train
and D
valid
and a loss function L.
Thedatasetscomprise ⟨x,y⟩ instances,wherex isaquestion,y isthecorrespondinganswer,and
botharetextstrings. Thelossfunctionevaluatesthequalityofananswery. (2)Thesearchspace
specification A is a YAML file with the optimization variables and their possible values, along
P
withsomehyperparameters. Forexample, indicatesthateachcandidate
num_demonstrations: [0, 3, 5]
willhavezero,three,orfiveICLsamplesrandomlydrawnfromD . Inthecaseofzerodemon-
train
strations, this is equivalent to the zero-shot baseline. If zero is an option, we bias our candidate
1https://github.com/BerriAI/litellm
2PDLadditionallymakesuseoftheheuristicjson-repairpackage.
3

---
### Page 4

Search Space Specification
Input variables: Pattern Library
prompt_pattern:[cot, react, rewoo]
Task num_demonstrations: [0, 3, 5]
system_prompt: [granite_tools, llama3, granite_llama]
initial_test_set_size: 16
max_test_set_size: 1000
num_candidates: 100 Zero-
D parallelism: 5 Shot x y
train
2
x y
1 1
Successive Halving Optimizer CoT ... tho
D x y y
valid n n
1 c 1 l 1 3 x
... ...
A*
loss c k l k p traj 1 tho
function ReWOO ... act 1 obs 1 y
traj ... ...
4 n
x act obs
m m
Solution
defs:
prompt_pattern:react traj 1
n s u y m s _ t d e e m m _ o p n r s o t m r p a t t : i o g n r s a : n i 5 te_tools ReAct ... tho obs y
D test 5 dem d - o a n t - s a t q : r u a e t s i t on i s o : n: Rita put a $120 elliptical machine [...] tr x aj n act
-thought: The down payment Rita made was [...]
-action: '{"name":"Calculator","arguments":[...]'
-observation: 60
-[...]
Figure2:Overviewofourapproach.
samplingtoalwaysincludeonezero-shotcandidate,justincasethatbaselineturnsouttobethe
best-performingconfiguration.
(3) The pattern library consists of four PDL functions. Zero-shot is a baseline that simply
prompts the LLM with x and expects it to return y. CoT refers to chain-of-thought (Wei et al.
2022) with in-context learning (Brown et al. 2020): the input includes a fewx y pairs before the
i i
actualquestionx,andtheoutputincludessomereasoningthoughtthobeforetheactualanswery.
ReWOO(Xuetal.2023)referstoreasoningwithoutobservations. Here,thefew-shotsamplesare
trajectoriestraj . Atrajectorytraj consistsofstepsforaparticularexampleprobleminstancein
i i
D
train
,e.g.,inthecaseofReWOO,thoandactstepsandtheircontents.Incontrasttox
i
y
i
pairs,traj
i
may contain many tho, act and, depending on pattern, obs steps, before reaching the solutiony i .
ThefirstLLMcallinReWOOgeneratesonereasoningthoughtthoandmultipleactionsacti . The
PDLcodeexecuteseachoftheactionsasatoolcalltoobtainthecorrespondingobservationsobsi .
Afinalmodelcallgeneratestheanswerybasedontheobservations.Finally,theReActpattern(Yao
etal.2023)startswithfew-shottrajectoryexamplestraj (briefexamplevisibleunderSolutionA∗
i p
inFigure2)andthequestionx,andthenentersaTAO(thought,action,observation)loop. Ineach
loopiteration,theLLMgeneratesthoandact,thenthePDLcodeexecutestheactionasatoolcall,
andfeedsthetooloutputbackasanobservationobs. AspecialFinishactionbreaksoutoftheloop
toreturntheanswery.
Once inputs (1), (2), and (3) are in place, the suc-
1 text:
cessive halving optimizer runs in a loop. It starts 2 - include: ../../tools.pdl
3 - include: ../../ReAct.pdl
with a small subset D v ⊂ D valid and many candidates 4 - call: ${ react }
C ={c 1 ,...,c k } ⊆ A P sampled from the search space. 5 def: ANSWER
Each iteration uses D to evaluate the corresponding 6 args:
v 7 task: "Question: ${ question }"
d lo i s d s a e t s es l 1 w ,. i . th .,l t k h . e T sm he a n lle e s a t c L h i w te h r i a le tio d n ou k b e l e in p g s t t h h e e s k 2 iz c e an o - f 8 9 m to o o d l e s l : : $ $ { { t m o o o d l e s l } }
10 trajectories: ${ demonstrations }
the validation subset D v . See § 8.3 for the algorithm. 11 - "\nThe answer is ${ ANSWER.answer }"
(4)Afterthelastiteration,thebestremainingcandidate
is the solution A∗. This solution is a set of PDL defini- Figure3:Basic example of PDL program
p
tionswithconcretevaluesfortheoptimizationvariables, usingtheReActpattern.
4

---
### Page 5

e.g., in Figure 2, and a list of ReAct trajectories. (5) This pro-
num_demonstrations: 5 demonstrations: ...
gram can be used on the test set D . For instance, Figure 3 shows a call to the ReAct function
test
thatpasses fromA∗ asanargument.
${demonstrations} p
4 Methodology
Thissectiondescribesthedatasetsused,thetoolsavailabletoagents,andourexperimentalsetup,
includinghowweconstructagenttrajectoriesthatdemonstratetooluseforeachdataset.
4.1 Datasets
We selected datasets that are widely used in the literature, span diverse tools and domains, and
arerepresentativeoftoolcategoriesfrequentlystudiedinpriorwork(e.g.,calculator,search,code
execution). In our experiments, each dataset has three disjoint splits: D to sample few-shot
train
samples from, D to evaluate candidates during optimization, and D to evaluate the final
valid test
chosensolutionuponcompletionofoptimization.
GSM8K. The Grade School Math (Cobbe et al. 2021) dataset consists of 8,792 grade school math
problems. We sample 1,024 problems without replacement from the train set to use as ourD
valid
set,and1,024fromthetestset(consistingof1,319samples)touseasourD . ThisleavesaD
test train
of6,449problems. Eachproblemconsistsofawordproblemx suchas“Whatisfifteenmorethana
quarterof48?”,asequencethoofreasoningsteps,andfinallyaplainnumericanswery following
a special delimiter. For the CoT prompt pattern, we include these reasoning steps directly in the
demonstrations. We use a regular expression to extract the numerical answer from the model
solution,anddefineacorrectsolutionasanexactmatchtothegroundtruthanswer.
GSM-Hard. Gaoetal.(2023)introduceaderivativeofGSM8Kwithvariablesrandomlychangedto
largenumbers,with1,319samples. Unfortunately,GSM-Hardhad132sampleswheretheground
truth was incorrect, and hence we excluded those samples. We split the single set into equally
sized D valid and D test (n = 594), and use the GSM8K training set (6,449 samples) described above
forD
train
(crosstransfer). WeusethesamecorrectnesscriterionasforGSM8K.
FEVER. TheFactExtractionandVERificationdataset(Thorneetal.2018)isaquestion-answering
dataset structured around fact-checking. The original dataset contained 185,445 claims that are
true, false, or unverifiable, and associated with human annotated supporting, refuting, or neu-
tral sentences and their Wikipedia article of origin. We follow the widely used derivative of this
benchmarkinBIG-bench(Srivastavaetal.2023),whichreformulatesitintoatrue-or-falsetaskby
removingunverifiableclaims. Wesample1,024claimsfromthetrainsetasD and1,024from
valid
thetestsetasD . ThisleavesaD of5,696claims. BIG-benchalsodoesnotincludethesup-
test train
portingorrefutingsentences,whichwerecoverbyjoiningontheoriginaldataset,forusee.g.,as
CoTdemonstrations. Toassesscorrectness,wecheckforthepresenceof“true”and“false”inthe
finallineofthemodelresponse. Ifneitherorbotharepresent,wedeemtheresponseasincorrect,
andotherwisethecorrectnessisadirectmatchtothegroundtruth“true”or“false”.
MBPP+. MBPP (Austin et al. 2021) is a dataset of 974 mostly basic Python problems, with each
exampleconsistingofanaturallanguageproblemspecificationx foraself-containedPythonfunc-
tiony,alongwithasingletestcase.Eachproblemhasanextendedsetoftestcasesusedforevalua-
tion,whicharenotshowntothemodel.Liuetal.(2023)foundthatMBPPtestcasesareincomplete,
allowing proposed solutions to pass as correct, despite not matching the problem specification.
Therefore, our experiments are based on MBPP+, which containsa subset of the problems, but a
morecompletesetoftestcasesforeachproblem. Weusethesetestcasestoassessthecorrectness
oftheproposedsolutions. Weusethe374examplesfromtheoriginalMBPPdatasetasD ,and
train
split MBPP+ into D (224 samples) and D (39 samples) based on which split they were in
test valid
5

---
### Page 6

MBPP.ThediscrepancyinnumberofMBPP+samplesisduetotheexclusionofsamplesfoundin
the MBPP trainset, to avoid data contamination. Our ReAct implementation follows Wanget al.
(2024). WedonotimplementReWOOasitisnotreactive,i.e.,cannotincludeexecutionfeedback.
4.2 Tools
Ourpromptlibraryrepresentsactions,i.e.,toolcalls,followingtheJSONtoolcallingschema(Ab-
delazizetal.2024). AnactionisrepresentedasaJSONobjectwithnameandargumentsmapping.
For example, represents a call to a calculator with the
{"action": "Calc", "arguments": {"expr": "48/4"}}
expression to evaluate. The PDL functions implementing the patterns (see Figure 2) accept a list
of tool definitions as an argument. Each element of that list is itself a PDL function. As both the
agents and tools are implemented in PDL, the set of tools for a given task could itself be made a
searchspacedimension,whichweleavetofuturework.
Calculator. For math datasets, we give the agentic approaches access to the Calc tool. This tool
evaluates a cleaned (e.g., replacement of ^ with ∗∗) expression with SymPy, returning the result.
In case of error, the function returns a warning that the expression was invalid, which may help
theagentrecoverfrominvalidinput.
Search. For fact verification, we provide access to the Search tool, which returns the summary
of the first Wikipedia search result for the query. If no results are found, a hint to try again is
returned,orifthetitleistooambiguous,alistofpossibledisambiguations.
Execute. We implement a programming agent for the code generation task, which can execute
arbitrarycodesurroundedinXML-style<execute>tags. ThistoolexecutesthecodeinaPython
shell, which returns the result of the final expression. This allows the agent to test its proposed
solutionagainstthegiventestcasebeforesubmittingitssolution.
Finish. The most basic action is the Finish action, or <solution> tag for the coding agent. This
endstheagent’strajectoryandresultsintheagentreturningthevalueasthesolution.
4.3 ExperimentalSetup
We evaluate the efficacy of our approach by running an optimization process to completion for
each model & dataset pair, and subsequently comparing the task accuracy. As a baseline, we
evaluateeachmodelinazero-shotsetting. Thissettingreflectstheminimaleffortapproachbya
userordeveloper,wheretheydonotincludeanydemonstrationswiththeirqueryortask. Asno
modelweinvestigatewasspecificallytrainedtocreateagentictrajectoriesinazero-shotsetting,
itisnotfeasibletocreateazero-shotsettingunderReActorReWOO.
Fortheoptimizationprocess,weusedaninitialcandidatesetC of100candidatepromptcon-
figurations c i = ⟨A,p⟩ ∈ C per experiment. We fixed the size of the initial validation subset
d
valid
⊆ D
valid
to16. WedefineL(c
i
, d
valid
) =−Accuracy(c
i
, d
valid
) foragivencandidatec
i
,where
accuracyisthefractionind ofcorrectlysolvedproblemsbyc asperthedatasetdefinitionof
valid i
correctness. Foreachcandidatec i ,p = ⟨n,d train ,instr⟩ ∈ P wheren few-shotsamplesortrajecto-
riesd train ∈ (D train)n arerandomlysampledwithreplacement. Thenumberofpossiblevaluesfor
P iscombinatoriallylargeanddependsonthedatasetD train used. Finally,uponcompletionofan
optimizationprocess,theoptimalcandidateisevaluatedonD .
test
Constructing Trajectories. As we are also optimizing over agentic trajectories, we also need a
set of trajectories to sample few-shot samples from. To achieve this, we create a basic agentic
trajectorytraj
i
foreachtrainingexample⟨x
i
,y
i
⟩,followingarule-basedtransformation.Wedesign
and apply a template to each dataset, which is relatively simple and easy to implement for other
datasets (details are provided in § 8.5). Prior work has introduced approaches to bootstrapping
trajectoriese.g.,insoftwareengineering(Panetal.2024),toolusedemonstrations(Lietal.2025),
6

---
### Page 7

and reasoning paths (Zelikman et al. 2022), which could be applied to this problem. While we
acknowledgetheshortcomingsofmanualtemplateconstruction,wearguethisapproachhastwo
strengths: it is generalizable in the sense that templates can be mixed and matched, and that
the trajectories are directly based on the datasets used. Additionally, we wanted to work with
commonlyuseddatasetsthatcoveravarietyoftoolsanddomains,ratherthanemergingdatasets
containingtrajectoriesortoolusedemonstrations.
Models. We aim to study models of various abilities, e.g., natural language or code, various cre-
ators,andvarioussizes,rangingfromsingledigitbillionsofparametersuptotheedgeoffeasibility
onconsumerhardware. WeincludesevenmodelsavailableoninferenceserviceIBMwatsonx3 in
our study. We select three generalist natural language instruction models, Llama 3.1 8B, 3.2 3B,
and3.370Bfromtheopen-sourceandwidelystudiedLLaMafamily(Dubeyetal.2024).Wefurther
selectthreemodelsfromMishraetal.(2024),whichpredateDubeyetal.(2024)byapproximately
3months. WeselectGranite13BInstructV2asageneralistmodel,andGranite20Band34B
CodeInstructascodemodels.WeselectGranite3.18Basanadditionalgeneralistmodel(Gran-
iteTeam2024).Allofourexperimentsusegreedydecoding,i.e.,nosampling,tolimittheimpactof
hyperparameterchoice. Thenumberofmodelsweevaluateislimitedbycostin$/tokentermsand
executiontime. Bystudyingvariousmodels,wedemonstratethegeneralizabilityofourapproach.
Alternative Setups. We evaluate two alternative experimental setups. First, to investigate low-
resource scenarios, we examine whether performance on one dataset can be improved by using
demonstrationsD fromasimilardataset,whileoptimizingw.r.t.D . Forthisexperiment,we
train valid
investigate whether performance on GSM-Hard can be improved by using demonstrations from
GSM8K,whileoptimizingw.r.t.GSM-HardD
valid
. Second,toexploresavingoptimizationcosts,we
assess whether optimized prompt programs of one model can transfer well to a frontier model.
The intuition is that while that might not be the best program for the frontier model, it might at
leastimprovesomewhatoverthebaseline. Tothisend,weevaluatetheoptimizedPDLprograms
of LLaMa3.170BonOpenAI’sgpt-4o-mini-2024-07-18,foreachdataset.
5 Results
This section describes the results of our empirical study to evaluate our AutoPDL approach and
answerthefollowingresearchquestions:
RQ1: TowhatextentdoesAutoPDLimproveaccuracy, andhowmuchdoesthebestsolutionvaryby
taskandmodel?
RQ1 asks to what degree our AutoPDL approach can improve model performance over their
zero-shotbaselineacrossavarietyofcommonlyusedbenchmarks. Wealsoseektoidentifytrends,
ifany,inoptimalconfigurations,e.g.,whethermorefew-shotsisalwaysbetter,orwhethercertain
promptpatternsareparticularlysuitedtocertainproblemdomains.
RQ2:CanAutoPDLmakeupforamissingfew-shotexamplebankforagiventaskbyreusingtheexample
bankfromasimilartask?
RQ2 investigates whether optimizing on one dataset using demonstrations from another, re-
lated,datasetcanresultinhigherperformancethanusingnodemonstrations(zero-shot). ThisRQ
addressesalow-resourcescenarioinwhichalimitedpoolofdemonstrationsexistsinonedataset,
butadatasetfromasimilardomainhasalargepool.
RQ3: DosolutionsfoundbyAutoPDLimproveperformanceonfrontiermodels,evenwhenoptimized
foropen-sourcemodels?
3https://www.ibm.com/watsonx
7

---
### Page 8

Itcanbeexpensivetorunoptimizationagainstcommercialfrontier-modelAPIs. RQ3assesses
whetheroptimizedpromptprogramsaretransferabletodifferent(andlikelystronger)modelsthan
thosetheywereoptimizedwith.
Table1reportstheresultsofouroptimizationandevaluationprocedure. Weperformedthree
completeoptimizationrunsforFEVER,GSM8K,andMBPP+,andreportmeanaccuracy,standard
deviation in percentage points (i.e., absolute, not relative, uncertainty), and the pattern of the
highest scoring run. Across models and datasets, we generally find some improvement over the
zero-shotbaselinewithfew-shotchain-of-thought,oragenticpatternsReActorReWOO.
Table1:Modelaccuraciesacrossdatasetsforbaseline(zero-shot)andoptimizedversions.
Accuracy
Dataset Model BestPattern Runtime
Zero-Shot Optimized Delta
Granite3.18B 72.9% (76.4±3.3)% +3.5pp ReWOO(5shot) 13:53
Granite13BInstructV2 6.5% (74.0±1.4)% +67.5pp ReWOO(3shot) 08:28
Granite20BCode 39.7% (63.1±1.6)% +23.4pp CoT(3shot) 12:03
FEVER Granite34BCode 56.4% (62.6±3.8)% +6.2pp CoT(3shot) 10:07
LLaMA3.18B 68.5% (77.5±0.8)% +9.0pp CoT(3shot) 05:06
LLaMA3.23B 38.0% (66.3±0.9)% +28.3pp ReWOO(5shot) 10:10
LLaMA3.370B 67.6% (78.1±0.6)% +10.5pp ReWOO(3shot) 21:27
Granite3.18B 74.2% (74.2±0.6)% +0.0pp Zero-Shot(Baseline) 08:56
Granite13BInstructV2 23.0% (30.9±1.0)% +7.9pp CoT(3shot) 09:20
Granite20BCode 68.7% (68.7±0.1)% +0.0pp Zero-Shot(Baseline) 09:27
GSM8K Granite34BCode 72.1% (72.1±0.1)% +0.0pp Zero-Shot(Baseline) 08:52
LLaMA3.18B 78.4% (85.3±0.6)% +6.9pp CoT(5shot) 08:48
LLaMA3.23B 71.8% (75.3±0.4)% +3.5pp CoT(3shot) 16:36
LLaMA3.370B 85.5% (95.4±0.2)% +9.9pp CoT(3shot) 07:50
Granite3.18B 62.9% (62.9±0.0)% +0.0pp Zero-Shot(Baseline) 02:14
Granite13BInstructV2 10.7% (19.2±1.2)% +8.5pp ReAct(5shot) 04:02
Granite20BCode 51.8% (51.8±0.4)% +0.0pp Zero-Shot(Baseline) 03:43
MBPP+ Granite34BCode 48.7% (61.3±1.0)% +12.6pp ReAct(3shot) 04:54
LLaMA3.18B 61.2% (62.8±4.0)% +1.6pp ReAct(5shot) 01:45
LLaMA3.23B 58.0% (58.0±0.4)% +0.0pp Zero-Shot(Baseline) 02:01
LLaMA3.370B 71.4% (71.4±0.0)% +0.0pp Zero-Shot(Baseline) 02:27
FEVER. We observed the minimum improvement in Granite 3.1 8B, with a 3.5 percentage
point (pp) improvement, and a maximal improvement of 67.5pp for Granite 13B Instruct V2.
Intermsofpromptpattern,CoTandReWOOareequallyrepresented. ReActwasnottheoptimal
foranyofthemodels. Interestingly,thelargestmodel(LLaMa3.370B)benefitedby10.5ppfrom
3-shotReWOO.FEVERruntimesaregenerallyhigherthantheotherbenchmarks,likelyduetothe
largenumberoftokensinvolvedbyincludingWikipediacontent.
GSM8K. The highest improvement recorded (9.9pp) was for LLaMa 3.3 70B using 3-shot CoT,
while the minimum improvement of 3.5pp was in LLaMa 3.2 3B using 3-shot CoT. ReAct and
ReWOOwerenottheoptimalforanymodel. ForGranite3.18B,Granite20BCode,andGran-
ite 34B Code, no improvement over the zero-shot baseline was identified. This was somewhat
surprising,asgenerallyincludingevensomefew-shotsamplesimprovesperformanceinLLMs.
MBPP+. Several models benefited from execution feedback, as 3 out of 7 had ReAct as the opti-
mal prompt pattern (ReWOO was excluded as described in § 4.3). The greatest improvement of
12.6ppwasinGranite34BCode,and8.5ppinGranite13BInstructV2,likelyduetoitspoor
programming performance as a generalist, non-code model. In contrast, the smaller LLaMa 3.1
8B model had high zero-shot performance of 61.2%, yet still improved by up to 6.2pp (1.6pp on
8

[TABLE]
Dataset | Model | Accuracy |  |  | BestPattern | Runtime
 |  | Zero-Shot | Optimized | Delta |  | 
[/TABLE]

[TABLE]
Granite13BInstructV2 | 6.5% | (74.0±1.4)% | +67.5pp | ReWOO(3shot) | 08:28
[/TABLE]

[TABLE]
Granite34BCode | 56.4% | (62.6±3.8)% | +6.2pp | CoT(3shot) | 10:07
[/TABLE]

[TABLE]
LLaMA3.23B | 38.0% | (66.3±0.9)% | +28.3pp | ReWOO(5shot) | 10:10
[/TABLE]

[TABLE]
GSM8K | Granite3.18B | 74.2% | (74.2±0.6)% | +0.0pp | Zero-Shot(Baseline) | 08:56
 | LLaMA3.370B | 85.5% | (95.4±0.2)% | +9.9pp | CoT(3shot) | 07:50
[/TABLE]

[TABLE]
Granite20BCode | 68.7% | (68.7±0.1)% | +0.0pp | Zero-Shot(Baseline) | 09:27
[/TABLE]

[TABLE]
LLaMA3.18B | 78.4% | (85.3±0.6)% | +6.9pp | CoT(5shot) | 08:48
[/TABLE]

[TABLE]
Granite13BInstructV2 | 10.7% | (19.2±1.2)% | +8.5pp | ReAct(5shot) | 04:02
[/TABLE]

[TABLE]
Granite34BCode | 48.7% | (61.3±1.0)% | +12.6pp | ReAct(3shot) | 04:54
[/TABLE]

[TABLE]
LLaMA3.23B | 58.0% | (58.0±0.4)% | +0.0pp | Zero-Shot(Baseline) | 02:01
[/TABLE]

---
### Page 9

average)withReAct. NoimprovementwasobservedforGranite3.18B,Granite20BCode, or
theotherLLaMamodels.
Table2:ModelaccuraciesonGSM-Hardforcrossoptimizationexperiment.
Accuracy
Dataset Model BestPattern Runtime
Zero-Shot Optimized Delta
Granite3.18B 36.0% (37.8±0.8)% +1.8pp ReAct(5shot,GraniteTools) 23:34
Granite13BInstructV2 4.4% (6.2±0.7)% +1.8pp CoT(5shot) 10:26
Granite20BCode 28.8% (27.2±4.5)% +0.0pp Zero-Shot(Baseline) 11:14
GSM-Hard
Granite34BCode 27.9% (31.0±0.9)% +3.0pp CoT(3shot) 10:20
LLaMA3.23B 26.3% (26.8±0.6)% +0.5pp CoT(5shot) 17:08
LLaMA3.370B 47.3% (53.8±0.4)% +6.5pp CoT(5shot) 11:03
Table3:ModelaccuracyforGPT-4o-minicrossexperimentresults
Accuracy
Dataset Model BestPattern
Zero-Shot Optimized Delta
FEVER GPT-4o-mini 83.7% 87.7% +4.0pp CoT(3shot)
GSM-Hard GPT-4o-mini 45.6% 54.9% +9.3pp ReAct(5shot,GraniteLLaMa)
GSM8K GPT-4o-mini 77.8% 90.9% +13.1pp CoT(5shot)
MBPP+ GPT-4o-mini 72.3% 72.3% +0.0pp Zero-Shot(Baseline)
MissingFew-ShotExampleBank. WeoptimizedthePDLprogramforGSM-Hard,usingGSM8K
demonstrations, three times and report results in Table 2. We found that in most cases, GSM8K
demonstrationswereatleastnotharmfulformodelsonGSM-Hard,withupto6.5ppimprovement
forLLaMa3.370Busing5-shotCoT.
Commercial Frontier Model. To assess whether performance gains in one model can be
achieved in another, we evaluate the optimized PDL programs of LLaMa 3.1 70B on OpenAI’s
gpt-4o-mini-2024-07-18 and report results in Table 3 (we did not use LLaMa 3.3 70B here be-
cause we did this experiment earlier and did not have the time and resources to repeat it for the
finalversionofthispaper). Foralldataset/promptpatternpairsthatresultedinimprovementfor
LLaMa3.170B,wefoundasurprisingimprovementinGPT4o-miniofatleast4pponFEVERus-
ing 3-shot CoT, 9.3pp on GSM-Hard (using GSM8K demonstrations) with 5-shot ReAct (Granite
LLaMainstructions),andupto13.1pponGSM8Kusing5-shotCoT.Thissuggeststhatoptimizing
foranopen-sourcemodelcanalsobenefitaclosed-sourcemodel.
6 RelatedWork
The closest related work is on prompt optimization. APE starts with an LLM-generated set of
candidateprompts,thenperformsrejectionsamplingbasedonevaluationonasubsetofdata(Zhou
et al. 2023). ZOPO incorporates a Neural Tangent Kernel-based derived Gaussian process into
standard zeroth-order optimization for an efficient search of a locally-optimal instruction (Hu et
al.2024). Unlikeourapproach,neitherAPEnorZOPOoptimizefew-shotsamples. Aviarycanalso
jointlyoptimizeoverpromptpattern,instruction,andfew-shotexamples(Narayananetal.2024).
However,itwouldrequirethedefinitionofacustomoperator. CEDARusesademonstrationpool,
fromwhichitretrievesfew-shotexamplesatquerytime(Nashidetal.2023). Unlikeourapproach,
thesefew-shotsamplesareretrievedonaper-inferencebasis,notoptimizedahead-of-time.
EASE leverages embeddings to represent few-shot examples, and uses a neural bandit algo-
rithm to find an ordered set that performs well for test queries from a given task (Z. Wu et al.
2024). An extension of their approach jointly optimizes demonstrations and instructions. How-
ever,theapproachrequiresbothanadditionalembeddingmodel,andthetrainingofanewmodel
9

[TABLE]
Dataset | Model | Accuracy |  |  | BestPattern | Runtime
 |  | Zero-Shot | Optimized | Delta |  | 
[/TABLE]

[TABLE]
Granite13BInstructV2 | 4.4% | (6.2±0.7)% | +1.8pp | CoT(5shot) | 10:26
[/TABLE]

[TABLE]
Granite34BCode | 27.9% | (31.0±0.9)% | +3.0pp | CoT(3shot) | 10:20
[/TABLE]

[TABLE]
LLaMA3.370B | 47.3% | (53.8±0.4)% | +6.5pp | CoT(5shot) | 11:03
[/TABLE]

[TABLE]
Dataset | Model | Accuracy |  |  | BestPattern
 |  | Zero-Shot | Optimized | Delta | 
[/TABLE]

[TABLE]
GSM-Hard | GPT-4o-mini | 45.6% | 54.9% | +9.3pp | ReAct(5shot,GraniteLLaMa)
[/TABLE]

[TABLE]
MBPP+ | GPT-4o-mini | 72.3% | 72.3% | +0.0pp | Zero-Shot(Baseline)
[/TABLE]

---
### Page 10

topredictvalidationscoresfromembeddings. Unlikeourapproach,EASEdoesnotoptimizeover
agenticpatterns.
DSPy optimizes instructions and few-shot samples for a chain of LLM calls (Khattab et al.
2024) (not just a single call like APE or CEDAR). Also, DSPy takes away control over the exact
prompt from the programmer, which our approach preserves. Similarly to DSPy, TextGrad also
optimizes a chain of LLM calls, by using LLMs to back-propagate modifications to instructions
in prompts (Yuksekgonul et al. 2025). However, unlike our approach, neither of these optimize
agenticpatterns.
BPO trains a sequence-to-sequence model on prompts augmented by an LLM incorporating
human preferences, producing a model that improves given input prompts (Cheng et al. 2024).
APOHFintroduceastrategytoselectapairofpromptstoquerytheuserforpreferencefeedback,
whichtheyusetooptimizeLLM-generatedinstructionsonavalidationset(Linetal.2024). How-
ever,neitheroftheseapproachesexplicitlyoptimizedemonstrationsoragenticpatterns.EvoAgent
optimizes the instructions of a population of agents via crossover, mutation, and selection (Yuan
et al. 2024). It then forms an ensemble from the final, fittest, population. GPTSwarm represents
each agent as a graph, then freezes intra-agent edges and optimizes the placement of additional
inter-agent edges (Zhuge et al. 2024). Unlike our approach, neither EvoAgent nor GPTSwarm
optimizetheagenticpatterninsideindividualagents,nordotheyoptimizefew-shotsamples.
Another closely related field of study is AutoML. Auto-sklearn (Feurer et al. 2015) used
Bayesianoptimizationtojointlyperformbothalgorithmselectionandhyperparametersofascikit-
learnpipeline(Buitincketal.2013). Whiledifferent,weseesomeanalogybetweenalgorithmsand
agenticpatterns,andbetweenhyperparametersandfew-shotsamples.DAUBfirstevaluatesmany
candidate models on a small amount of data, then successively reduces candidates and increases
data to ultimately pick a strong model (Sabharwal et al. 2016). The successive-halving algorithm
takesasimilarapproach(Jamiesonetal.2016). Ourapproachisinspiredbythesameincremental
dataallocationidea. WhilebothrandomizedsearchandBayesianoptimizationarepopularinAu-
toML,therearealsomoreintricateapproaches.Forinstance,TPOTusesgeneticalgorithms(Olson
etal.2016),andAlphaD3MusesMonte-Carlotreesearch(Drorietal.2018). Wechosetostartwith
asimplertechniquethatdependslessonawell-behavedoptimizationspace. Thatsaid,exploring
moreadvancedAutoMLoptimizerscouldbefruitfulfutureworkforAutoPDL.Lale(Baudartetal.
2021)treatsAutoMLasasource-to-sourceoptimization,similartothispaper,butunlikeAutoPDL,
ithasnotbeenusedtooptimizeagenticpatternsorprompts.
7 Conclusion
WepresentourAutoPDLapproachforjointlyoptimizingpromptingpatternsandtextualprompts
forlargelanguagemodels,addressingthechallengesassociatedwithmanualpromptengineering.
Byformulatingtheoptimizationasadiscretesearchoverbothagenticandnon-agenticpatterns,
combined withinstructions and few-shot samples, we leveraged successive halvingto efficiently
navigate this search space. Our evaluation across various datasets (FEVER, GSM8K, GSM-Hard,
andMBPP+)andmultiplemodels(fromtheLLaMA,Granite,andGPTfamilies)demonstratessub-
stantialaccuracyimprovements,upto67.5percentagepoints,andaffirmsthatnosingleprompting
strategyuniversallyoutperformsothersacrosstasksandmodels. Additionally,generatingcodein
a YAML-based prompt programming language (PDL) makes it executable, easy to modify, and
readablebyhumans,supportingpracticaladoptionandadaptation.
10

---
### Page 11

References
Abdelaziz, I., Basu, K., Agarwal, M., Kumaravel, S., Stallone, M., Panda, R., Rizk, Y., Bhargav, G.,
Crouse,M.,Gunasekara,C.,Ikbal,S.,Joshi,S.,Karanam,H.,Kumar,V.,Munawar,A.,Neelam,
S., Raghu, D., Sharma, U., Soria, A. M., Sreedhar, D., Venkateswaran, P., Unuvar, M., Cox, D.,
Roukos,S.,Lastras,L.,andKapanipathi,P.(2024).Granite-FunctionCallingModel:Introducing
FunctionCallingAbilitiesviaMulti-taskLearningofGranularTasks.url:https://arxiv.org/abs/
2407.00121(cit.onp.6).
Austin, J., Odena, A., Nye, M., Bosma, M., Michalewski, H., Dohan, D., Jiang, E., Cai, C., Terry,
M., Le, Q., and Sutton, C. (2021). Program Synthesis with Large Language Models. url: http:
//arxiv.org/abs/2108.07732(cit.onp.5).
Baudart,G.,Hirzel,M.,Kate,K.,Ram,P.,Shinnar,A.,andTsay,J.(2021).“PipelineCombinatorsfor
GradualAutoML”.In:AdvancesinNeuralInformationProcessingSystems(NeurIPS),pp.19705–
19718(cit.onp.10).
Brown, T. B., Mann, B., Ryder, N., Subbiah, M., Kaplan, J., Dhariwal, P., Neelakantan, A., Shyam,
P., Sastry, G., Askell, A., Agarwal, S., Herbert-Voss, A., Krueger, G., Henighan, T., Child, R.,
Ramesh,A.,Ziegler,D.M.,Wu,J.,Winter,C.,Hesse,C.,Chen,M.,Sigler,E.,Litwin,M.,Gray,
S., Chess, B., Clark, J., Berner, C., McCandlish, S., Radford, A., Sutskever, I., and Amodei, D.
(2020). Language Models are Few-Shot Learners. url: https://arxiv.org/abs/2005.14165 (cit. on
pp.1,4).
Buitinck,L.,Louppe,G.,Blondel,M.,Pedregosa,F.,Mueller,A.,Grisel,O.,Niculae,V.,Prettenhofer,
P., Gramfort, A., Grobler, J., Layton, R., VanderPlas, J., Joly, A., Holt, B., and Varoquaux, G.
(2013).APIDesignforMachineLearningSoftware:Experiencesfromthescikit-learnProject.url:
https://arxiv.org/abs/1309.0238(cit.onp.10).
Cheng,J.,Liu,X.,Zheng,K.,Ke,P.,Wang,H.,Dong,Y.,Tang,J.,andHuang,M.(2024).“Black-Box
PromptOptimization:AligningLargeLanguageModelswithoutModelTraining”.In:Annual
MeetingoftheAssociationforComputationalLinguistics(ACL),pp.3201–3219(cit.onp.10).
Cobbe,K.,Kosaraju,V.,Bavarian,M.,Chen,M.,Jun,H.,Kaiser,L.,Plappert,M.,Tworek,J.,Hilton,
J.,Nakano,R.,Hesse,C.,andSchulman,J.(2021).TrainingVerifierstoSolveMathWordProblems.
url:http://arxiv.org/abs/2110.14168(cit.onp.5).
Drori,I.,Krishnamurthy,Y.,Rampin,R.,Lourenco,R.d.P.,Ono,J.P.,Cho,K.,Silva,C.,andFreire,J.
(2018).“AlphaD3M:MachineLearningPipelineSynthesis”.In:WorkshoponAutomaticMachine
Learning(AutoML)(cit.onp.10).
Dubey, A. et al. (2024). The Llama 3 Herd of Models. url: http://arxiv.org/abs/2407.21783 (cit. on
p.7).
Feurer,M.,Klein,A.,Eggensperger,K.,Springenberg,J.,Blum,M.,andHutter,F.(2015).“Efficient
and Robust Automated Machine Learning”. In: Conference on Neural Information Processing
Systems(NIPS),pp.2962–2970(cit.onp.10).
Gao, L., Madaan, A., Zhou, S., Alon, U., Liu, P., Yang, Y., Callan, J., and Neubig, G. (2023). “PAL:
Program-aided Language Models”. In: International Conference on Machine Learning (ICML),
pp.10764–10799(cit.onp.5).
GraniteTeam,I.(2024).Granite3.0LanguageModels(cit.onp.7).
Hu, W., Shu, Y., Yu, Z., Wu, Z., Lin, X., Dai, Z., Ng, S.-K., and Low, B. K. H. (2024). “Localized
Zeroth-Order Prompt Optimization”. In: Conference on Neural Information Processing Systems
(NeurIPS),pp.86309–86345(cit.onp.9).
11

---
### Page 12

Jamieson,K.andTalwalkar,A.(2016).“Non-stochasticBestArmIdentificationandHyperparame-
terOptimization”.In:ConferenceonArtificialIntelligenceandStatistics(AISTATS),pp.240–248
(cit.onpp.2,10,17).
Khattab, O., Singhvi, A., Maheshwari, P., Zhang, Z., Santhanam, K., A, S. V., Haq, S., Sharma,
A., Joshi, T. T., Moazam, H., Miller, H., Zaharia, M., and Potts, C. (2024). “DSPy: Compiling
DeclarativeLanguageModelCallsintoSelf-ImprovingPipelines”.In:InternationalConference
onLearningRepresentations(ICLR)(cit.onpp.1,10).
Kojima, T., Gu, S. S., Reid, M., Matsuo, Y., and Iwasawa, Y. (2022). “Large Language Models
AreZero-ShotReasoners”.In:ConferenceonNeuralInformationProcessingSystems(NeurIPS),
pp.22199–22213(cit.onp.1).
Li, C., Xue, M., Zhang, Z., Yang, J., Zhang, B., Wang, X., Yu, B., Hui, B., Lin, J., and Liu, D. (2025).
START:Self-taughtReasonerwithTools.url:https://arxiv.org/abs/2503.04625(cit.onpp.6,18).
Lin,X.,Dai,Z.,Verma,A.,Ng,S.-K.,Jaillet,P.,andLow,B.K.H.(2024).PromptOptimizationwith
HumanFeedback.url:http://arxiv.org/abs/2405.17346(cit.onp.10).
Liu, J., Xia, C. S., Wang, Y., and Zhang, L. (2023). “Is Your Code Generated by ChatGPT Really
Correct?RigorousEvaluationofLargeLanguageModelsforCodeGeneration”.In:Conference
onNeuralInformationProcessingSystems(NeurIPS),pp.21558–21572(cit.onp.5).
Mishra,M.,Stallone,M.,Zhang,G.,Shen,Y.,Prasad,A.,Soria,A.M.,Merler,M.,Selvam,P.,Suren-
dran,S.,Singh,S.,Sethi,M.,Dang,X.-H.,Li,P.,Wu,K.-L.,Zawad,S.,Coleman,A.,White,M.,
Lewis,M.,Pavuluri,R.,Koyfman,Y.,Lublinsky,B.,deBayser,M.,Abdelaziz,I.,Basu,K.,Agar-
wal,M.,Zhou,Y.,Johnson,C.,Goyal,A.,Patel,H.,Shah,Y.,Zerfos,P.,Ludwig,H.,Munawar,A.,
Crouse,M.,Kapanipathi,P.,Salaria,S.,Calio,B.,Wen,S.,Seelam,S.,Belgodere,B.,Fonseca,C.,
Singhee,A.,Desai,N.,Cox,D.D.,Puri,R.,andPanda,R.(7,2024).GraniteCodeModels:AFamily
ofOpenFoundationModelsforCodeIntelligence.Version1.url:http://arxiv.org/abs/2405.04324
(cit.onp.7).
Moura, J. (2023). CrewAI: Framework for orchestrating role-playing, autonomous AI agents. url:
https://github.com/crewAIInc/crewAI(visitedon06/06/2025)(cit.onp.1).
Narayanan,S.,Braza,J.D.,Griffiths,R.-R.,Ponnapati,M.,Bou,A.,Laurent,J.,Kabeli,O.,Wellawatte,
G., Cox, S., Rodriques, S. G., and White, A. D. (2024). Aviary: Training Language Agents on
ChallengingScientificTasks.url:http://arxiv.org/abs/2412.21154(cit.onp.9).
Nashid,N.,Sintaha,M.,andMesbah,A.(2023).“Retrieval-BasedPromptSelectionforCode-Related
Few-ShotLearning”.In:InternationalConferenceonSoftwareEngineering(ICSE),pp.2450–2462
(cit.onp.9).
Olson,R.S.,Urbanowicz,R.J.,Andrews,P.C.,Lavender,N.A.,Kidd,L.C.,andMoore,J.H.(2016).
“Automating Biomedical Data Science Through Tree-Based Pipeline Optimization”. In: Euro-
peanConferenceontheApplicationsofEvolutionaryComputation(EvoApplications),pp.123–137
(cit.onp.10).
Pan, J., Wang, X., Neubig, G., Jaitly, N., Ji, H., Suhr, A., and Zhang, Y. (2024). Training Software
EngineeringAgentsandVerifierswithSWE-Gym.url:http://arxiv.org/abs/2412.21139(cit.on
p.6).
Sabharwal,A.,Samulowitz,H.,andTesauro,G.(2016).“SelectingNear-OptimalLearnersviaIncre-
mentalDataAllocation”.In:ConferenceonArtificialIntelligence(AAAI),pp.2007–2015(cit.on
p.10).
12

---
### Page 13

Schluntz, E. and Zhang, B. (2024). Building effective agents. url: https://www.anthropic.com/
research/building-effective-agents(visitedon06/06/2025)(cit.onp.1).
Srivastava,A.etal.(2023).“BeyondtheImitationGame:QuantifyingandExtrapolatingtheCapa-
bilitiesofLanguageModels”.TransactionsonMachineLearningResearch(TMLR)(cit.onp.5).
Thorne,J.,Vlachos,A.,Christodoulopoulos,C.,andMittal,A.(2018).FEVER:ALarge-ScaleDataset
forFactExtractionandVERification.url:http://arxiv.org/abs/1803.05355(cit.onp.5).
Thornton,C.,Hutter,F.,Hoos,H.H.,andLeyton-Brown,K.(2013).“Auto-WEKA:CombinedSelec-
tionandHyperparameterOptimizationofClassificationAlgorithms”.In:ConferenceonKnowl-
edgeDiscoveryandDataMining(KDD),pp.847–855(cit.onp.1).
Vaziri, M., Mandel, L., Spiess, C., and Hirzel, M. (2024). PDL: A Declarative Prompt Programming
Language.url:http://arxiv.org/abs/2410.19135(cit.onp.2).
Wang,X.,Wang,Z.,Liu,J.,Chen,Y.,Yuan,L.,Peng,H.,andJi,H.(2024).MINT:EvaluatingLLMsin
Multi-turnInteractionwithToolsandLanguageFeedback.url:http://arxiv.org/abs/2309.10691
(cit.onpp.6,17,18).
Wei,J.,Wang,X.,Schuurmans,D.,Bosma,M.,Ichter,B.,Xia,F.,Chi,E.,Le,Q.,andZhou,D.(2022).
“Chain-of-ThoughtPromptingElicitsReasoninginLargeLanguageModels”.In:Conferenceon
NeuralInformationProcessingSystems(NeurIPS),pp.24824–24837(cit.onpp.1,4).
Willard, B. T. and Louf, R. (2023). Efficient Guided Generation for Large Language Models. url:
https://arxiv.org/abs/2307.09702(cit.onp.3).
Wu,Q.,Bansal,G.,Zhang,J.,Wu,Y.,Li,B.,Zhu,E.,Jiang,L.,Zhang,X.,Zhang,S.,Liu,J.,Awadal-
lah, A. H., White, R. W., Burger, D., and Wang, C. (2023). AutoGen: Enabling Next-Gen LLM
ApplicationsviaMulti-AgentConversation.url:https://arxiv.org/abs/2308.08155(cit.onp.1).
Wu, Z., Lin, X., Dai, Z., Hu, W., Shu, Y., Ng, S.-K., Jaillet, P., and Low, B. K. H. (2024). “Prompt
Optimization with EASE? Efficient Ordering-aware Automated Selection of Exemplars”. In:
ConferenceonNeuralInformationProcessingSystems(NeurIPS),pp.122706–122740(cit.onp.9).
Xu, B., Peng, Z., Lei, B., Mukherjee, S., and Xu, D. (2023). ReWOO: Decoupling Reasoning from
Observations for Efficient Augmented Language Models. url: https://arxiv.org/abs/2305.18323
(cit.onpp.1,4).
Yao, S., Zhao, J., Yu, D., Du, N., Shafran, I., Narasimhan, K. R., and Cao, Y. (2023). “ReAct: Syner-
gizing Reasoning and Acting in Language Models”. In: International Conference on Learning
Representations(ICLR)(cit.onpp.1,4).
Yuan,S.,Song,K.,Chen,J.,Tan,X.,Li,D.,andYang,D.(2024).EvoAgent:TowardsAutomaticMulti-
Agent Generation via Evolutionary Algorithms. url: https://arxiv.org/abs/2406.14228 (cit. on
p.10).
Yuksekgonul, M., Bianchi, F., Boen, J., Liu, S., Lu, P., Huang, Z., Guestrin, C., and Zou, J. (2025).
“OptimizingGenerativeAIbyBackpropagatingLanguageModelFeedback”.Nature,639(8055),
pp.609–616(cit.onp.10).
Zelikman,E.,Wu,Y.,Mu,J.,andGoodman,N.D.(2022).“STaR:Self-TaughtReasoner,Bootstrap-
ping Reasoning With Reasoning”. In: Conference on Neural Information Processing Systems
(NeurIPS)(cit.onp.7).
Zhou,Y.,Muresanu,A.I.,Han,Z.,Paster,K.,Pitis,S.,Chan,H.,andBa,J.(2023).“LargeLanguage
Models are Human-Level Prompt Engineers”. In: International Conference on Learning Repre-
sentations(ICLR)(cit.onp.9).
13

---
### Page 14

Zhuge,M.,Wang,W.,Kirsch,L.,Faccio,F.,Khizbullin,D.,andSchmidhuber,J.(2024).“GPTSwarm:
Language Agents as Optimizable Graphs”. In: International Conference on Machine Learning
(ICML)(cit.onp.10).
14

---
### Page 15

8 SupplementalMaterial
8.1 ConcretePromptExample
1 defs:
2 prompt_pattern: cot
3 num_demonstrations: 2
4 demonstrations:
5 data:
6 - question: Tricia is a third of Amilia's age and Amilia is a quarter of Yorick's age. Yorick is twice
7 Eugene's age and Khloe is a third of Eugene's age. Rupert is 10 years older than Khloe but 2 years
8 younger than Vincent who is 22 years old. How old, in years, is Tricia?
9 reasoning: |-
10 Rupert is younger than Vincent by 2 years, so he is 22 years old - 2 years = <<22-2=20>>20 years old.
11 Khloe is 10 years younger than Rupert so she is 20 years old - 10 years = 10 years old.
12 Eugene is 3 times older than Khloe so he is 10 years old * 3 = <<10*3=30>>30 years old.
13 Yorick is twice Eugene's age so he is 30 years old * 2 = <<30*2=60>>60 years old.
14 Amilia is a quarter of Yorick's age so she is 60 years old / 4 = <<60/4=15>>15 years old.
15 Tricia is a third of Amilia's age so she is 15 years old / 3 = <<15/3=5>>5 years old.
16 answer: '5'
17 - question: Emmalyn decided to paint fences in her neighborhood for twenty cents per meter. If there were
18 50 fences in the neighborhood that she had to paint and each fence was 500 meters long, calculate
19 the total amount she earned from painting the fences.
20 reasoning: |-
21 The total length for the fifty fences is 50*500 = <<50*500=25000>>25000 meters.
22 If Emmalyn charged twenty cents to paint a meter of a fence, the total income she got from painting
23 the fences is $0.20*25000 =$5000
24 answer: '5000'
25 instruction: Answer the questions to the best of your abilities.
26 text:
27 - include: CoT.pdl
28 - "${ instruction }\n\n"
29 - call: ${ chain_of_thought }
30 args:
31 examples: ${ demonstrations }
32 question: ${ question }
33 model: ${ model }
FigureA1:Basic example of a concrete prompt configuration in PDL, using CoT pattern and two
demonstrations.
1 Answer the questions to the best of your abilities.
2
3 Question: Tricia is a third of Amilia's age and Amilia is a quarter of Yorick's age. Yorick is twice Eugene's
4 age and Khloe is a third of Eugene's age. Rupert is 10 years older than Khloe but 2 years
5 younger than Vincent
6 who is 22 years old. How old, in years, is Tricia?
7 Answer: Let's think step by step. Rupert is younger than Vincent by 2 years, so he is 22 years
8 old - 2 years = <<22-2=20>>20 years old.
9 Khloe is 10 years younger than Rupert so she is 20 years old - 10 years = 10 years old.
10 Eugene is 3 times older than Khloe so he is 10 years old * 3 = <<10*3=30>>30 years old.
11 Yorick is twice Eugene's age so he is 30 years old * 2 = <<30*2=60>>60 years old.
12 Amilia is a quarter of Yorick's age so she is 60 years old / 4 = <<60/4=15>>15 years old.
13 Tricia is a third of Amilia's age so she is 15 years old / 3 = <<15/3=5>>5 years old.
14 The answer is 5
15
16 Question: Emmalyn decided to paint fences in her neighborhood for twenty cents per meter. If there were 50
17 fences in the neighborhood that she had to paint and each fence was 500 meters long, calculate the total
18 amount she earned from painting the fences.
19 Answer: Let's think step by step. The total length for the fifty fences is 50*500 = <<50*500=25000>>25000 meters.
20 If Emmalyn charged twenty cents to paint a meter of a fence, the total income she got from painting the
21 fences is $0.20*25000 =$5000
22 The answer is 5000
23
24 Question: ${ question }
25 Answer: Let's think step by step.
FigureA2:CorrespondingrenderedpromptconfigurationforFigureA1. Withtheexceptionofthe
non-rendered${ question }variable,thisistheinputtothelanguagemodel.
SeeFigureA1andFigureA2.
15

---
### Page 16

8.2 ToolCallingCode
1 description: tool use
2 defs:
3 tools:
4 data:
5 - name: calc
6 description: Calculator function
7 arguments:
8 expr:
9 type: string
10 description: Arithmetic expression to calculate
11 text:
12 - role: system
13 text: You are Granite, developed by IBM. You are a helpful AI assistant
14 with access to the following tools. When a tool is required to answer
15 the user's query, respond with <|tool_call|> followed by a JSON list of
16 tools used. If a tool does not exist in the provided list of tools,
17 notify the user that you do not have the ability to fulfill the request.
18 contribute: [context]
19 - role: tools
20 text: ${ tools }
21 contribute: [context]
22 - "Out of 1400 participants, 400 passed the test. What percentage is that?\n"
23 - def: actions
24 model: replicate/ibm-granite/granite-3.1-8b-instruct
25 parser: json
26 spec: [{ name: str, arguments: { expr: str }}]
27 - "\n"
28 - if: ${ actions[0].name == "calc" }
29 then:
30 lang: python
31 code: result = ${ actions[0].arguments.expr }
FigureA3:BasicexampleofaPDLprogram.
See FigureA3.
8.3 Optimization
Algorithm1SuccessiveHalvingforPDLOptimization
Require: ProgramcandidatesetC,validationdatasetD valid ,initialvalidationsubsetsizev min ,max-
imumvalidationsubsetsizev
max
1: v ←v min
2: while |C| > 1do
3: d valid ← firstv elementsofD valid s.t.d valid ⊆ D valid and |d valid | =v
4: foreachcandidatec i ∈ C do
5: Computelossl i ← L(c i , d valid )
6: endfor
7: C ←top ⌊|C|/2⌋ candidateswithlowestloss
8: v ← min(v max ,2·v)
9: endwhile
10: return CandidateinC withlowestloss
FigureA4:Illustration of the Successive Halving algorithm used to optimize the PDL program by
pruningpoorcandidatesonprogressivelylargervalidationsubsets.
16

---
### Page 17

Figure A4 describes our optimization algorithm, based on successive halving (Jamieson et al.
2016). The algorithm accepts a candidate set sampled from possible configurations and demon-
strations,avalidationdatasettooptimizeagainst,aninitialvalidationsubsetsize,andamaximum
validationsubsetsize. AutoPDLallowstheusertospecifytheseoptionsinaYAMLconfiguration
file, and ultimately saves its result as a PDL program. This source-to-source transformation en-
ablestheusertomodifyboththesearchspaceandtheresultingoptimizedPDLprogram,allowing
furthermodificationandexecution.
8.4 SearchSpace
ThesearchspaceistheCartesianproductofthefollowingdiscretevariables,eachtakingonevalue
percandidate:
(1) A ∈ A ={Zero-Shot,CoT,ReWOO,ReAct},i.e.,theoverallpromptingpatterntoapply.
(2) Numberofdemonstrationsn ∈ {0, 3, 5}. Weselectedtheseoptionsasarepresentativesweep
acrossnosupervision,moderatefew-shotuse,andanupper-endcase(intermsoftokenwin-
dow). Welimitedthesearchspacetothreeoptionstoavoidcombinatorialexplosionandlimit
experimentcost.
(3) IfA = ReAct, System prompt ∈ {Granite Tools, LLaMa 3, Granite LLaMa}. As the system
prompt instructs the model how to format tool calls, it only has an effect on benchmarks
withJSONtoolcalling(FEVER,GSM8K,andGSM-Hard)forcandidateswiththeReActprompt
pattern.WenotethatonlyforMBPP+,ReWOOisnotincludedasapromptpattern,andthatwe
always include two trajectories displaying iterative refinement, i.e., an example of a solution
failing the example test case, followed by a passing solution, in line with Wang et al. (2024).
Thiseffectivelyincreasesthenumberoftrajectoriesto |traj|+2.
8.5 AgentTrajectoryConstruction
Tooptimizeoveragenticpatternsandtrajectories,werequireasetofexampletrajectoriestouse
duringoptimization. Forthispurpose, wecreateabasicagentictrajectorytraj foreachtraining
i
example ⟨x ,y ⟩,followingarule-basedtransformationoutlinedbelow.
i i
GSM8K. To demonstrate tool use in ReAct, we instead derive a trajectory traj as follows. We
exploit the fact that there is at most one expression per reasoning step, by iterating through the
steps. At each step, we append a ‘thought’ to the trajectory, consisting of the text leading up to
themathexpression, concatenatedwithareflection‘Ineedtocalculate’. Weappendacalculator
tool call with the expression, and an ‘observation’, i.e., the result of the expression. Finally, we
append a thought ‘The answer is ...’, containing the ground truth answer, followed by the finish
action with the answer. We follow the same procedure to create ReWOO trajectories, except we
use slightly different wording, e.g., ‘Calculate xyz’ in place of ‘I need to calculate xyz’, and omit
the final thought and action. Additionally, we use string substitution to replace any assumed
expressionresultsinthetrajectorywiththecorrespondingvariable.
FEVER. Toproduceagenttrajectories,weiterateovereacharticleassociatedwithaclaim,append
a thought ‘I need to search for ...’, followed by the action, an observation containing the article
summary, and finally a thought containing all the relevant sentences associated with that article
for that claim, which we repeat for each article associated with a claim. This procedure is not
idealasthereisnoinherentordertothearticlesorsentences,eventhoughtheremaybeanatural
orderingfollowingtheannotator’sWikipedianavigation. Finally,weappendathought‘Theclaim
is true/false’ and the finish action, both with the ground truth answer. For chain-of-thought, we
performthesameprocedureexceptweonlyincludetheconcatenatedevidencesentences,asthere
isnotooluse.
17

---
### Page 18

MBPP+. Togeneratesampleagenttrajectoriesfromthetrainingset,wefollowtheagentpattern
(withoutfeedback)in-contextexamplesbyWangetal.(2024),whichconsistsoftheproblemx,a
thoughtsuchas“Theintersectioniselementsthatareinbothlists”,anexecuteactionthatcontains
proposed code and an assertion calling the proposed method with the test case input from the
promptandcomparingitsoutput.Thisisthenfollowedbyanobservationcontainingtheexecution
result,i.e.,either“[Executed Successfully with No Output]”orastacktraceback. Thisallows
the agent to iterate on solutions (up to five times in our implementation). We use the full MBPP
train set of 374 problems as D , and split the MBPP+ dataset into D and D based on
train valid test
problemidmembershipinMBPP,leaving39and224validationandtestproblemsrespectively.
To generate synthetic trajectories from the training set, we start with the natural language
specification and single test case (the prompt), append the thought “I should run a solution on
the test case before proposing a solution.”, followed by the ground truth solution and substitute
in the prompt test case following the pattern [solution]res = ...; assert res == ...,
”Expected ... but got ”.format(res). Subsequently,weappendtheobservation“[Executed
Successfully with No Output]”, the thought “There is no more AssertionError. I can
now submit the solution.”, and finally the solution action with the ground truth solution.
This naive approach allows us to provide demonstration trajectories, albeit simplistic ones that
assume the first solution is correct. Sampling a reflection or thought from a strong model may
be beneficial (Li et al. 2025), but we restrict our trajectories to rule based transformations. As
ReWOOisnotreactive,i.e.,withoutexecutionfeedback,itdoesnotmakesenseforMBPP.Hence,
weexcludeitfromourexperiments.
8.6 ResultsPlot
Granite 3.1 8B
Granite 13B Instruct V2
Granite 20B Code
Granite 34B Code
LLaMA 3.1 8B
LLaMA 3.2 3B
LLaMA 3.3 70B
0 20 40 60 80100
ledoM
FEVER GSM8K MBPP+ GSM-Hard
0 20 40 60 80100 0 20 40 60 80100 0 20 40 60 80100
FigureA5:Comparisonofoptimizedpromptprogramperformanceacrossmodelsanddatasets.Each
barbellshowstheaccuracyimprovement,ifany,overthezero-shotbaseline.
InFigureA5,wevisualizetheresultsfromTable1andTable2.
18

[TABLE]
 |  |  |  | 
 |  |  |  | 
 |  |  |  | 
 |  |  |  | 
[/TABLE]

[TABLE]
 |  |  |  | 
[/TABLE]

[TABLE]
 |  |  |  | 
[/TABLE]

[TABLE]
 |  |  |  | 
[/TABLE]

---
### Page 19

8.7 Accuracyvs. iterations
InFigureA6,wevisualizetheaccuracyacrosscandidatesversustheiterationsoftheoptimization
process, including a 95% confidence interval depicting the spread in accuracy across candidates.
Theconfidenceintervaliscomputedusingmeanand1,000bootstraps. Astheiterationsincrease,
thenumberofcandidatesdecreases,whilethesizeofthevalidationsetD increases.
v
19

---
### Page 20

1.0
0.8
0.6
0.4
0.2
0.0
ycaruccA
GSM8K FEVER MBPP+
Granite
20B
Code
GSM-Hard
1.0
0.8
0.6
0.4
0.2
0.0
ycaruccA
LLaMA
3.1
8B
1.0
0.8
0.6
0.4
0.2
0.0
ycaruccA
Granite
13B
Instruct
V2
1.0
0.8
0.6
0.4
0.2
0.0
ycaruccA
Granite
3.1
8B
1.0
0.8
0.6
0.4
0.2
0.0
ycaruccA
Granite
34B
Code
1.0
0.8
0.6
0.4
0.2
0.0
ycaruccA
LLaMA
3.2
3B
1.0
0.8
0.6
0.4
0.2
0.0
0 1 2 3 4 5
Iteration
ycaruccA
0 1 2 3 4 5 0 1 2 3 4 5 0 1 2 3 4 5
Iteration Iteration Iteration
LLaMA
3.3
70B
FigureA6:Accuracyvs.iterationswith95%confidenceinterval.
20
