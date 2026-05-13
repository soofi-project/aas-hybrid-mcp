# Plan And Solve

Source: plan-and_execute.pdf


---
### Page 1

Plan-and-Solve Prompting: Improving Zero-Shot Chain-of-Thought
Reasoning by Large Language Models
LeiWang1 WanyuXu2 YihuaiLan ZhiqiangHu3 YunshiLan4
RoyKa-WeiLee3 Ee-PengLim1∗
1SingaporeManagementUniversity
2SouthwestJiaotongUniversity
3SingaporeUniversityofTechnologyandDesign
4EastChinaNormalUniversity
Abstract
35
Largelanguagemodels(LLMs)haverecently
30
beenshowntodeliverimpressiveperformance
invariousNLPtasks. Totacklemulti-steprea- 25
soningtasks,few-shotchain-of-thought(CoT)
20
prompting includes a few manually crafted
step-by-stepreasoningdemonstrationswhich 15
enableLLMstoexplicitlygeneratereasoning
10
steps and improve their reasoning task accu-
racy. To eliminate the manual effort, Zero- 5
shot-CoTconcatenatesthetargetproblemstate-
mentwith“Let’sthinkstepbystep”asanin-
put prompt to LLMs. Despite the success of
Zero-shot-CoT, it still suffers from three pit-
falls: calculation errors, missing-step errors,
andsemanticmisunderstandingerrors. Toad-
dressthemissing-steperrors,weproposePlan-
and-Solve(PS)Prompting. Itconsistsoftwo
components: first,devisingaplantodividethe
entiretaskintosmallersubtasks,andthencar-
rying out the subtasks according to the plan.
Toaddressthecalculationerrorsandimprove
the quality of generated reasoning steps, we
extend PS prompting with more detailed in-
structionsandderivePS+prompting. Weeval-
uate our proposed prompting strategy on ten
datasetsacrossthreereasoningproblems. The
experimentalresultsoverGPT-3showthatour
proposedzero-shotpromptingconsistentlyout-
performsZero-shot-CoTacrossalldatasetsby
a large margin, is comparable to or exceeds
Zero-shot-Program-of-ThoughtPrompting,and
hascomparableperformancewith8-shotCoT
promptingonthemathreasoningproblem. The
codecanbefoundathttps://github.com/AGI-
Edgerunners/Plan-and-Solve-Prompting.
1 Introduction
Large language models (LLMs) (Brown et al.,
2020; Thoppilan et al., 2022; Chowdhery et al.,
2022)haverecentlyprovenhighlyeffectiveinvar-
ious NLP tasks. Unlike the previous pre-trained
languagemodels(PTMs)(Devlinetal.,2019;Liu
∗Correspondingauthor.
)%(
oitaR
Calculation Error
Step Missing Error
Semantic Misunderstanding 27
12
7
Figure1:Erroranalysisof46GSM8Kproblemswithin-
correctanswersreturnedbyZero-shot-CoTusingGPT-
3LLM.FollowingWeietal.(2022b)andWangetal.
(2022a), we assign “Calculation Error” (7%), “Step
MissingError”(12%),or“Semanticmisunderstanding
Error”(27%)toeachincorrectanswer.
etal.,2019),theseLLMsaretypicallyprovidedas
aservice,withnoaccesstomodelparametersdue
tocommercialconsiderationsandpotentialrisksof
misuse (Sun et al., 2022). Thus, it is challenging
tofine-tuneLLMsfordownstreamtasks(Heetal.,
2021; Houlsby et al., 2019; Devlin et al., 2019).
Instead,weleverageLLMstosolvecomplexrea-
soningproblemsbyelicitingtheirstrongreasoning
abilitiesovertheirembeddedknowledgeusingin-
structions(ortriggersentences). Sofar,LLMshave
shownimpressiveabilitiestosolvenewreasoning
problems by simply conditioning them on a few
illustrativeexamples(i.e.,few-shotlearning)ora
prompttosolvenewproblemswithoutillustrative
examples(i.e.,zero-shotlearning).
Totacklemulti-stepcomplexreasoningtasksus-
ing LLMs, Wei et al. (2022b) proposes few-shot
chain-of-thought(CoT)prompting,whichenables
LLMstoexplicitlygeneratetheintermediaterea-
soningstepsbeforepredictingthefinalanswerwith
a few manual step-by-step reasoning demonstra-
tionexamples. In(Kojimaetal.,2022),Zero-shot
CoTeliminatestheneedformanuallycraftedex-
amplesinpromptsbyappending“Let’sthinkstep
by step” to the target problem fed to LLMs such
3202
yaM
62
]LC.sc[
3v19040.5032:viXra

[TABLE]
Calculation Error
Step Missing Error
Semantic Misunderstanding |  |  |  | 27
 |  |  |  | 
12
7 |  |  |  | 
 |  |  |  | 
rroran | alysiso | f46G | SM8K | proble
[/TABLE]

---
### Page 2

asGPT-3. Thissimplepromptingstrategysurpris- et al., 2022b)). The results of our experiments
inglyenablesLLMstoyieldperformancesimilar withGPT-3showthatourproposedZero-shot-PS+
tofew-shotCoTprompting. promptingconsistentlyoutperformsZero-shot-CoT
Despite the remarkable success of Zero-shot- across all reasoning problems and datasets by a
CoT in solving multi-step reasoning tasks, its re- largemargin,andiscomparabletoorexceedsZero-
sultsonasampleof100arithmetictestexamples shot-Program-of-Thought(PoT)Prompting(Chen
stillpointtothreepitfalls(asshowninFigure1): etal.,2022)). Furthermore,althoughPS+prompt-
(i) Calculation errors (in 7% of test examples): ingdoesnotrequiremanualdemonstrationexam-
Theseareerrorsinthecalculationleadingtowrong ples,ithasaperformancesimilartoan8-shotCoT
answers; (ii) Missing Step errors (in 12% of test promptinginarithmeticreasoning.
examples): Theseoccurwhensomeintermediate Overall,ourresultssuggestthat(a)Zero-shotPS
reasoning step(s) is missed-out especially when promptingiscapableofgeneratingahigher-quality
therearemanystepsinvolved;(iii)Semanticmis- reasoningprocessthanZero-shot-CoTprompting,
understanding (in 27% of test examples): There as the PS prompts provide more detailed instruc-
are other errors in semantic understanding of the tions guiding the LLMs to perform correct rea-
problemandcoherenceofreasoningstepslikelyto soningtasks;(b)Zero-shotPS+promptingoutper-
becausedbytheinsufficientcapabilityofLLMs. formsFew-shotmanual-CoTpromptingonsome
datasets, indicating that in some instances it has
To address the issue of Zero-shot-CoT caused
thepotentialtooutperformmanualFew-shotCoT
bymissingreasoningsteps,weproposePlan-and-
prompting,whichhopefullywillsparkfurtherde-
Solve (PS) Prompting. It consists of two compo-
velopment of new CoT prompting approaches to
nents: first,devisingaplantodividetheentiretask
elicitreasoninginLLMs.
intosmallersubtasks,andthencarryingoutthesub-
tasksaccordingtotheplan. Inourexperiments,we
2 Plan-and-SolvePrompting
simplyreplace“Let’sthinkstepbystep”ofZero-
shot-CoTwith“Let’sfirstunderstandtheproblem Overview. We introduce PS prompting, a new
anddeviseaplantosolvetheproblem. Then,let’s zero-shotCoTpromptingmethod,whichenables
carry out the plan and solve the problem step by LLMstoexplicitlydeviseaplanforsolvingagiven
step”(seeFigure2(b)). problemandgeneratetheintermediatereasoning
processbeforepredictingthefinalanswerforthe
To address the calculation errors of Zero-shot-
inputproblem. Asopposedtopriorfew-shotCoT
CoTandimprovethequalityofgeneratedreason-
approaches where step-by-step few-shot demon-
ingsteps,weaddmoredetailedinstructionstoPS
strationexamplesareincludedintheprompt,the
prompting. Specifically,weextenditwith“extract
zero-shot PS prompting method does not require
relevantvariablesandtheircorrespondingnumer-
demonstration examples, and its prompt covers
als”and“calculateintermediateresults(payatten-
the problem itself and a simple trigger sentence.
tiontocalculationandcommonsense)”instructions.
SimilartoZero-shot-CoT,Zero-shotPSprompting
ThispromptingvariantiscalledthePS+prompting
consists of two steps. In step 1, the prompt first
strategy (see Figure 3 (b)). Despite its simplic-
makesaninferenceusingtheproposedprompting
ity, PS+ strategy greatly improves the quality of
templatetogeneratethereasoningprocessandthe
the generated reasoning process. Moreover, this
answertoaproblem. Instep2, itextractsthean-
prompting strategy can be easily customized to
swerforevaluationbyusingtheanswerextraction
solveavarietyofproblemsotherthanmathreason-
prompting,suchas“Therefore,theanswer(arabic
ing,suchascommonsenseandsymbolicreasoning
numerals)is”.
problems.
We evaluate our proposed prompting on six 2.1 Step1: PromptingforReasoning
math reasoning datasets, including AQuA (Ling Generation
et al., 2017), GSM8K (Cobbe et al., 2021), Mul-
To solve the input problem while avoiding errors
tiArith, AddSub, SingleEq, and SVAMP (Patel
resulting from incorrect calculation and missing
etal.,2021),twocommonsensereasoningdatasets
reasoning steps, this step aims to construct tem-
(CommonsenseQA(Talmoretal.,2019)andStrat-
platestomeetthefollowingtwocriteria:
egyQA(Gevaetal.,2021)),andtwosymbolicrea-
soning datasets (Last Letter and Coin Flip (Wei • The templates should elicit LLMs to deter-

---
### Page 3

Figure 2: Example inputs and outputs of GPT-3 with (a) Zero-shot-CoT prompting, (b) Plan-and-Solve (PS)
prompting,and(c)answerextractionprompting. WhileZero-shot-CoTencouragesLLMstogeneratemulti-step
reasoningwith“Let’sthinkstepbystep”,itmaystillgeneratewrongreasoningstepswhentheproblemiscomplex.
UnlikeZero-shot-CoT,PSpromptingfirstasksLLMstodeviseaplantosolvetheproblembygeneratingastep-by-
stepplanandcarryingouttheplantofindtheanswer.
minesubtasksandaccomplishthesubtasks. tions. Specifically,“payattentiontocalculation”is
addedtothetriggersentencetorequesttheLLMsto
• The templates should guide LLMs to pay
performcalculationsasaccuratelyaspossible. To
moreattentiontocalculationsandintermedi-
reduceerrorsresultingfrommissingnecessaryrea-
ateresultsandtoensurethattheyarecorrectly
soningsteps,weinclude“extractrelevantvariables
performedasmuchaspossible.
andtheircorrespondingnumerals”toexplicitlyin-
structtheLLMsnottoignorerelevantinformation
Tomeetthefirstcriterion,wefollowZero-shot-
in the input problem statement. We hypothesize
CoTandfirstconverttheinputdataexampleinto
a prompt with a simple template “Q: [X]. A: thatiftheLLMsleaveouttherelevantandimpor-
[T]”. Specifically, the input slot [X] contains tantvariables,itismorelikelytomissoutrelevant
reasoningsteps. Correlationanalysisofgenerated
the input problem statement and a hand-crafted
instruction is specified in the input slot [T] to contentofvariableandthemissingreasoningstep
errors,showninFigure5,empiricallysupportsthis
triggerLLMstogenerateareasoningprocessthat
hypothesis (correlation value is less than 0). Ad-
includes a plan and steps to complete the plan.
ditionally,weadd“calculateintermediateresults”
In Zero-shot-CoT, the instruction in the input
slot [T] includes the trigger instruction ‘Let’s to the prompt to enhance LLM’s ability to gener-
think step by step”. Our Zero-shot PS prompting ate relevant and important reasoning steps. The
method instead includes the instructions “devise specific example is illustrated in Figure 3(b). At
a plan” and “carry out the plan” as shown in the end of Step 1, LLM generates the reasoning
textwhichincludestheanswer. Forexample,the
Figure 2(b). Thus, the prompt would be “Q:
[X]. A: Let’sfirstunderstandtheproblem and generated reasoning text in Figure 3(b) includes
deviseaplantosolvetheproblem. Then,let’s
“CombinedweightofGraceandAlex=125+498
carryouttheplanandsolvetheproblemstepby =623pounds”. Thestrategyofaddingspecificde-
step.” scriptionstothetriggersentencerepresentsanew
waytoimprovezero-shotperformanceoncomplex
We then pass the above prompt to the LLM
reasoning.
whichsubsequentlyoutputsareasoningprocess. In
accordancewithZero-shot-CoT,ourmethoduses
2.2 Step2: PromptingforAnswerExtraction
thegreedydecodingstrategy(1outputchain)for
generatingoutputbydefault. Similar to Zero-shot-CoT, we devise another
Tomeetthesecondcriterion,weextendtheplan- promptinStep2togettheLLMtoextractthefinal
basedtriggersentencewithmoredetailedinstruc- numerical answer from the reasoning text gener-

---
### Page 4

Figure3: ExampleinputsandoutputsofGPT-3with(a)Plan-and-Solve(PS)Promptingand(b)Plan-and-Solve
promptingwithmoredetailedinstructions(PS+prompting). PS+promptinggreatlyimprovesthequalityofthe
generatedreasoningprocess.
atedinStep1. Thispromptincludestheanswerex- ofmathwordproblemsrequiringmultiplereason-
tractioninstructionappendedtothefirstpromptfol- ingstepsandoperations,(4)theAddSub(Hosseini
lowedbytheLLMgeneratedreasoningtext. This et al., 2014) dataset of addition and subtraction
way,LLMisexpectedtoreturnthefinalanswerin arithmetic word problems, (5) the AQUA (Ling
thedesiredform. et al., 2017) dataset of algebraic word problems
Based on the example in Figure 3(b), the with natural language rationales, and (6) the Sin-
prompt used in Step 2 will include “Q: Grace gleEq(Koncel-Kedziorskietal.,2015)datasetof
weighs 125 pounds ··· Variables: Grace: single-equation grade-school algebra word prob-
125 pounds ··· Answer: Combined weight of lems with multiple math operations over non-
Grace and Alex = 125 + 498 = 623 pounds. negativerationalnumbersandonevariable;Com-
Therefore,theanswer(arabicnumerals)is”. For monsenseReasoning: (7)theCSQA(Talmoretal.,
this example, the final answer returned by LLM 2019)benchmarkdatasetofmultiple-choiceques-
is“623”. tionsthatrequiredifferenttypesofcommonsense
knowledge to obtain the correct answers; and (8)
3 ExperimentalSetup the StrategyQA (Geva et al., 2021) benchmark
datasetwithquestionsrequiringmulti-stepreason-
3.1 Benchmarks
ing but the reasoning steps are not given. Hence,
Theproposedmethodisevaluatedonthetenbench- theyaretobeinferred;SymbolicReasoning: (9)
mark datasets from three categories of reason- theLastLetterConcatenation(Weietal.,2022b)
ing problems: Arithmetic Reasoning: (1) the dataset of questions requiring the last letters of
GSM8K(Cobbeetal.,2021)datasetofhighqual- wordsinanametobeconcatenated(e.g.,“James
itylinguisticallydiversegradeschoolmathword Brown”→“sn”),and(10)theCoinFlip(Weietal.,
problems created by human problem writers, (2) 2022b) dataset of questions on whether a coin is
theSVAMP(Pateletal.,2021)benchmarkofone- stillheadsupafteritisflippedornotflippedbased
unknown arithmetic word problems for up-to-4 on steps given in the questions. Table 1 shows
grade level students by making simple changes datasetstatistics.
toasetofproblemsfromanotherexistingdataset,
(3) the MultiArith (Roy and Roth, 2016) dataset

---
### Page 5

Table1:Detailsofdatasetsbeingevaluated.Math:arith- amples for AQuA and Last Letters, 7 examples
meticreasoning. CS:commonsensereasoning. Sym.:
forCSQA,and6examplesforStrategyQAassug-
symbolicreasoning.
gestedintheoriginalpapers,Weietal.(2022b)and
Dataset Domain #Samples Ave.words Answer Zhangetal.(2022). Evaluationmetricswise,we
followManual-CoT(Weietal.,2022b)andreport
MultiArith Math 600 31.8 Number
AddSub Math 395 31.5 Number theaccuracyofallmethodsacrossdatasets.
GSM8K Math 1319 46.9 Number
AQUA Math 254 51.9 Option
4 ExperimentalResults
SingleEq Math 508 27.4 Number
SVAMP Math 1000 31.8 Number
CSQA CS 1221 27.8 Option 4.1 MainResults
StrategyQA CS 2290 9.6 Yes/No
LastLetters Sym. 500 15.0 String ArithmeticReasoning. Table2reportstheaccu-
CoinFlip Sym. 500 37.0 Yes/No racycomparisonofourmethodandexistingzero-
shot and few-shot methods on the arithmetic rea-
3.2 Zero-shotandFew-shotBaselines soningdatasets. Inthezero-shotsetting, ourPS+
prompting(i.e.,PSpromptingwithmoredetailed
We compare our proposed zero-shot PS and PS+
instructions) consistently outperforms Zero-shot-
prompting methods with three types of prompt-
CoT across all arithmetic reasoning datasets by
ing baselines: (1) Zero-shot baselines. We in-
a large margin. Specifically, PS+ prompting im-
cludezero-shot-CoT(Kojimaetal.,2022)andzero-
provestheaccuracyoverZero-shotCoTbyatleast
shot-PoT(Chenetal.,2022). Theformerappends
5% for all datasets except GSM8K which sees a
“Let’s think step by step” to the prompt without
2.9%improvement. Theexceptioncouldbedueto
anydemonstrationexamples. ThelatterusesLLM
(mainlyOpenAICodex1)togenerateaPythonpro- GSM8Kbeingamorechallengingdatasetfromthe
linguisticscomplexityaspect. PSpromptingalso
gramandthenderiveananswerbyexecutingthe
outperformsZero-shot-CoTacrossalldatasets,and
generated program on a Python interpreter; (2)
enjoys2.5%higheraverageaccuracythanthatof
Few-shotwithmanualdemonstrations. Manual-
Zero-shotCoT.
CoT(Weietal.,2022b)createseighthand-crafted
examplesasdemonstrations. (3)Few-shotwithau- Compared with another competitive Zero-shot
tomaticdemonstrations. Auto-CoT(Zhangetal., baseline, PoT, the performance of PS(+) and PS
2022)automaticallyselectedexamplesbycluster- promptingsarestillimpressive. PS+promptingout-
ingwithdiversityandgeneratesreasoningchains performsPoTonfiveoutofsixarithmeticdatasets.
usingzero-shot-CoTtoconstructdemonstrations. PSpromptingalsooutperformsPoTonthreearith-
metic datasets. The results suggest that adding
3.3 Implementations more detailed instructions to the prompt can ef-
fectivelyelicithigher-qualityreasoningstepsfrom
FollowingAuto-CoT(Zhangetal.,2022),weuse
LLMs.
the public GPT-3 (Brown et al., 2020) (175B) as
Comparedwiththefew-shotmethods,Manual
the backbone language model, which is one of
the most widely-used LLMs with public APIs2. CoTandAuto-CoT,PS+promptingyieldsanaver-
ageaccuracy(76.7%)slightlylowerthanManual-
Sincetext-davinci-003isanupgradedver-
CoT(77.6%)buthigherthanAuto-CoT(75.9%).
sion of text-davinci-002, which can pro-
Whilethisisanunfaircomparison,thisresultindi-
duce higher-quality writing, accommodate more
catesthatzero-shotpromptingcanoutperformfew-
complexinstructions,andperformbetteratlonger-
shot CoT prompting, which hopefully will spark
form content generation, We report the results
furtherdevelopmentofnewwayswithalessman-
using text-davinci-003 engine for GPT-3
ualefforttoeffectivelyelicitreasoninginLLMs.
in the main paper. We set the temperature to 0
(argmaxsampling)throughoutourexperimentsfor
CommmonsenseReasoning. Table3showsthe
thegreedydecodingstrategy. Wealsoincludetwo
resultsoncommonsensereasoningdatasets: Com-
few-shot baselines, Manual-CoT and Auto-CoT,
monsenseQA and StrategyQA. We only include
weuse8demonstrationexamplesforMultiArith,
ourbetterzero-shotPS+promptingstrategyinthis
GSM8K, AddSub, SingleEq, and SVAMP, 4 ex-
comparison. Zero-shotPoTisexcludedasitdoes
1https://openai.com/blog/openai-codex/ not work on this problem. While PS+ prompt-
2https://beta.openai.com/docs/models/gpt-3 ingunderperformsFew-Shot-CoT(Manual)onthis

---
### Page 6

Table2: Accuracycomparisononsixmathreasoningdatasets. Thebestandsecondbestresultsareboldfacedand
underlinedrespectively.
Setting Method(text-davinci-003) MultiArith GSM8K AddSub AQuA SingleEq SVAMP Average
CoT 83.8 56.4 85.3 38.9 88.1 69.9 70.4
PoT 92.2 57.0 85.1 43.9 91.7 70.8 73.5
Zero-Shot
PS(ours) 87.2 58.2 88.1 42.5 89.2 72.0 72.9
PS+(ours) 91.8 59.3 92.2 46.0 94.7 75.7 76.7
Manual-CoT 93.6 58.4 91.6 48.4 93.5 80.3 77.6
Few-Shot
Auto-CoT 95.5 57.1 90.8 41.7 92.1 78.1 75.9
Zero-shot-Cot
Table3: Accuracyoncommonsensereasoningdatasets. Zero-shot-PS+
Method CSQA StrategyQA
Few-Shot-CoT(Manual) 78.3 71.2
Zero-shot-CoT 65.2 63.8
Zero-shot-PS+(ours) 71.9 65.4
Table4: Accuracyonsymbolicreasoningdatasets.
w/o SC w/ SC w/o SC w/ SC
Method LastLetter CoinFlip
Figure 4: Results of methods with and without self-
Few-Shot-CoT(Manual) 70.6 100.0
consistency(SC)onGSM8KandSVAMP.
Zero-shot-CoT 64.8 96.8
Zero-shot-PS+(ours) 75.2 99.6
75.7%)onGSM8KandSVAMP,respectively. The
former also consistently outperforms Zero-shot-
problem, it consistently outperforms Zero-shot- CoTwithSC(70.7%and81.7%)onGSM8Kand
CoTonCommonsenseQA(71.9%vs. 65.2%)and SVAMP,respectively,althoughZero-shotCoTalso
StrategyQA(65.4%vs. 63.8%)datasets. enjoysimprovementwiththeselfconsistencyap-
proach.
Symbolic Reasoning. Table 4 shows the accu-
racy of PS+ prompting against Zero-shot-CoT
EffectofPrompts. Table5demonstratesacom-
andFew-shot-CoTonsymbolicreasoningdatasets:
parison of the performance of 6 different input
LastLettersandCoinFlip. Zero-shotPoTisagain
prompts. Prompts 1 and 2 are used in Zero-shot
excludedasitisnotdesignedfortheproblem. On
CoTandZero-shotPoTrespectively. Therestare
LastLetters,ourZero-shotPS+prompting(75.2%)
variations of prompts used in Step 1 of the Zero-
outperformsManual-CoT(70.6%)andZero-shot-
shotPS+promptingstrategieswithgreedydecod-
CoT(65.2%). OnCoinFlip,Zero-shotPS+prompt-
ing. WeobservethatPrompt3withvariablesand
ing (99.6%) is slightly worse than Manual-CoT
numeral extraction performs worse than Prompt
(100.0%) but outperforms Zero-shot-CoT by a
1 of Zero-shot-CoT. The reason is that Prompt 3
good margin (96.8%). More examples from the
doesn’tincludeinstructionsfordevisingandcom-
experimentresultscanbefoundinAppendixA.2.
pleting a plan. However, the other prompts of
Zero-shot-PS+ perform well as we add more in-
4.2 Analysis
structions about intermediate results calculation,
Results of Prompting with Self-Consistency.
plan design, and implementation. The above re-
Self-consistency(Wangetal.,2022b)(SC)ispro-
sultsconcludethatLLMsarecapableofgenerating
posed to reduce randomness in LLM’s output by
high-quality reasoning text when the prompts in-
generating N reasoning results and determining
cludemoredetailedinstructionstoguidetheLLMs.
thefinalanswerbymajorityvoting. WithSC,the
Morepromptsfordifferentreasoningproblemscan
methods’ results are usually expected to be con-
befoundinAppendixA.1.
sistent and better. Hence, we evaluate Zero-shot
PS+promptingwithSConGSM8KandSVAMP ErrorAnalysis. Toqualitativelyevaluatetheim-
datasets. We set the temperature to 0.7 and N to pactoftheZero-shot-PS+promptingoncalculation
10 for experiments with SC. Figure 4 shows that errors and reasoning steps missing errors, we ex-
PS+ prompting with SC (73.7% and 84.4%) sub- amine the distribution of errors on the GSM8K
stantiallyoutperformsthatwithoutSC(58.7%and dataset. We first randomly sample 100 problems

[TABLE]


[/TABLE]

[TABLE]
Zero-shot-Cot
Zero-shot-PS+
[/TABLE]

---
### Page 7

Table 5: Performance comparison of trigger sentences measured on GSM8K and SVAMP datasets with
text-davinci-003 except for No. 2 (code-davinci-002). (*1) means the trigger sentence used in
Zero-shot-CoT(Kojimaetal.,2022). (*2)meansthetriggersentenceusedinZero-shot-PoT(Chenetal.,2022).
No. TriggerSentence GSM8K SVAMP
1 Let’sthinkstepbystep. (*1) 56.4 69.9
importmath
importnumpyasnp
#Question:example[’question’]
2 #Answerthisquestionbyimplementingasolver()function. (*2) 57.0 70.8
defsolver():
#Let’swriteaPythonprogramstepbystep,andthenreturntheanswer
#Firstly,weneeddefinethefollowingvariable:
Extractvariablesandassigntheircorrespondingnumerals tothesevariables
3 50.5 69.5
firstandthensolvetheproblemstepbystep.
Firstly,extractvariablesandtheircorrespondingnumerals.Then,calculate
4 54.8 70.8
intermediatevariables.Finally,solvetheproblemstepbystep.
Let’sfirstunderstandtheproblemanddeviseaplantosolvetheproblem.
5 58.2 72.0
Then,let’scarryouttheplanandsolvetheproblemstepbystep.
Let’sfirstunderstandtheproblem,extractrelevantvariablesandtheir
correspondingnumerals,andmakeaplan.Then,let’scarryouttheplan,
6 calculateintermediatevariables(payattentiontocorrectnumerical 59.3 75.7
calculationandcommonsense),solvetheproblemstepbystep,andshow
theanswer.
Table 6: Distribution of error types of 100 examples ingstepsleadingtofewercalculationerrors.
fromGSM8KwhereZero-shot-CoT,zero-shotPS(Zero-
shot-PS)prompting,andzero-shotPS+promptingget
Correlation Analysis of Generated Reasoning
incorrectfinalanswers.
andErrorTypes. Toobtaindeeperinsightinto
Method Calculation Missing Semantic the impact of PS+ prompting on error types, we
Zero-shot-CoT 7% 12% 27% examine the correlation between the sub-parts of
the generated reasoning and error types. Specifi-
Zero-shot-PS 7% 10% 26%
Zero-shot-PS+ 5% 7% 27% cally, weanalyzetheexistenceofvariabledefini-
tion,reasoningplan,andsolutioninthegenerated
reasoning text and correlate them with the three
from GSM8K, generate the reasoning text, and
errortypes. Thesetofproblemsusedforthisanal-
extract answers using Zero-Shot-CoT, Zero-shot-
ysis study is the same as that used in the earlier
PS,andZero-shot-PS+promptingstrategies. Zero-
error type analysis. Figure 5 shows the correla-
Shot-CoTgeneratedincorrectfinalanswersfor46
tion matrix among the existence of variable defi-
of the problems, 43 for Zero-shot-PS, and 39 for
nitions, plans, solutions and three different types
Zero-shot-PS+. Subsequently,weanalyzeandde-
of errors. It is observed that both variable defini-
termine the error types of all these problems as
tionandplanexistenceshaveanegativecorrelation
showninTable6.
withcalculationerrorsandmissing-reasoning-step
The analysis results show that PS+ prompting errors. TheZero-shot-PS+promptcanfurtherim-
achieves the least calculation (5%) and missing- provetheperformanceofLLMsonmathematical
step (7%) errors, and semantic understanding er- reasoningproblemsbyreducingcalculationerrors
rors comparable to Zero-shot-CoT. Zero-shot-PS andmissing-reasoning-steperrors.
hasslightlymoreerrorsbutisstillbetterthanZero-
shot-CoT. Their plan-and-solve prompts thus ef- Exploring the Presence of Plans in PS Predic-
fectively guide the LLMs to generate clear and tions. Toascertainthepresenceofaplanineach
completereasoningsteps. Moreover,theadditional prediction made by PS, we conducted a random
detailed instructions in PS+ prompting (i.e., “ex- samplingof100dataexamplesandexaminedtheir
tract relevant variables and their corresponding corresponding predictions. Our analysis reveals
numerals”and“calculateintermediatevariables”) that90ofthe100predictionsindeedincorporated
enabletheLLMstogeneratehigh-qualityreason- aplan. Thisobservationindicatestheemergence

[TABLE]
Ex | tract | vari | able
[/TABLE]

[TABLE]
their | cor | re | spondin | gnu | mer | als
[/TABLE]

[TABLE]
 |  |  | ex | tractv |  | ari | ables
int | er | me | di | at | evar | iable | 
[/TABLE]

[TABLE]
their | cor | re | spondin | gnu | mer
[/TABLE]

[TABLE]
cal | cu | late
[/TABLE]

[TABLE]
dev | isea | plan
[/TABLE]

[TABLE]
arry | outt | he | plan
[/TABLE]

[TABLE]
 |  |  |  |  |  |  |  |  |  |  |  |  | ex | tract |  | relev | ant | varia | ble |  |  | 
cor | re | spondi |  |  | ngn | umer |  | als |  |  | make |  | a | plan |  | .Then,let’sc |  |  | arry | out | the | plan
cal | cu | late |  | int | erm | edi | at | evari |  | ables |  | (pay |  | at | ten | tion | toco | rrec | tnu | meri | cal | 
ca | lc | ula | tion |  | and | com |  | mo | nsense), |  |  |  |  |  |  |  |  |  |  |  |  | 
[/TABLE]

---
### Page 8

CalculationStep MissingSemantic
selbairaV
nalP
noituloS
5.2 PromptingMethods
To exploit the reasoning ability in LLMs, Wei
0.6
-0.41 -0.56 0.76
0.4 etal.(2022b)proposeChain-of-Thoughtprompt-
0.2 ing,appendingmultiplereasoningstepsbeforethe
-0.02 -0.83 0.7 0.0 answer to the input question. With this simple
0.2 few-shotpromptingstrategy,LLMsareabletoper-
0.4 formmuchbetterincomplexreasoningproblems.
-0.42 0.076 0.24
0.6
Subsequently, many works (Wang et al., 2022a;
0.8
Suzgunet al.,2022; Shaikhet al.,2022; Saparov
Figure5: Correlationanalysisofgeneratedreasoning and He, 2022) propose to further improve CoT
anderrortypesofrandomlysampled100dataexamples prompting in different aspects, including prompt
fromGSM8KforZero-shot-PS+.
format (Chen et al., 2022), prompt selection (Lu
etal.,2022),promptensemble(Wangetal.,2022b;
ofstrongplanningabilitiesinrecentLLMssuchas
Lietal.,2022;Wengetal.,2022;Fuetal.,2022),
GPT-3.5andGPT-4.
problem decomposition (Zhou et al., 2022; Khot
et al., 2022; Dua et al., 2022; Press et al., 2022),
5 RelatedWork andplanning(Yaoetal.,2022;Huangetal.,2022;
Wangetal.,2023;Liuetal.,2023;Sunetal.,2023;
5.1 ReasoninginNLP Yao et al., 2023). Chen et al. (2022) introduced
PoTpromptingtouseLLMswithcodepre-training
It is well known that complex reasoning prob-
towriteaprogramasarationalefordisentangling
lems are challenging for NLP models, and such
computationfromreasoning. Todoawaywithman-
problemsincludemathematicalreasoning(Cobbe
ualeffort, Kojimaetal.(2022)proposedZero-shot-
et al., 2021; Patel et al., 2021; Ling et al., 2017;
CoT to elicit reasoning step generation without
Koncel-Kedziorskietal.,2016)(requiringtheabil-
exemplars. To leverage the benefit of demonstra-
ity to understand mathematical concepts, calcu-
tionexamplesandminimizemanualeffort, Zhang
lation, and multi-step reasoning), commonsense
etal.(2022)designedAuto-CoT.Itfirstautomat-
reasoning(Talmoretal.,2019;Gevaetal.,2021)
icallyobtainsk examplesbyclusteringthegiven
(requiring the ability to make judgments based
dataset. It then follows Zero-shot-CoT to gener-
oncommonsenseknowledge),andlogicalreason-
ate rationales for the selected examples. Finally,
ing (Wei et al., 2022b) (requiring the ability to
demonstrationexamplesareconstructedbyadding
manipulate symbols by applying formal logical
the generated rationales to selected examples as
rules). BeforetheadventofLargeLanguagemod-
CoTprompts. Ourworkisdifferentfromtheabove
els(LLMs), Talmoretal.(2019)trainedtheNLP
worksbyfocusingonelicitingmulti-stepreasoning
model using explanations generated by the fine-
byLLMsinazero-shotapproach. WeaskLLMs
tunedGPTmodelandfoundthatthetrainedmodel
towriteaplantodecomposeacomplexreasoning
yields better performance on commonsense QA
task into multiple reasoning steps. Furthermore,
problems. Hendrycks et al. (2021) attempted
weintroducedetailedinstructionstothepromptto
to fine-tune pretrained language models with la-
avoidobviouserrorsinthereasoningsteps. Were-
beledrationale,butfoundoutthatthesefine-tuned
ferreaderstothesurvey(HuangandChang,2022)
modelscouldnoteasilygeneratehigh-qualityrea-
formorerelatedworks.
soning steps. Recent work by Wei et al. (2022a)
showedthatLLMsdemonstratesstrongreasoning
6 Conclusion
ability when scaled up to tens of billions of pa-
rameters,suchasGPT-3(Brownetal.,2020)and Inthispaper,wefindthatZero-shot-CoTstillsuf-
PaLM(Chowdheryetal.,2022). TheseLLMswith fersfromthreepitfalls: calculationerrors,missing-
afewdemonstrationexemplarscanyieldimpres- reasoning-step errors, and semantic understand-
siveperformanceacrossdifferentNLPtasks. How- ing errors. To address these issues, we introduce
ever,thesemodelsstillperformpoorlyinproblems plan-and-solvepromptingstrategies(PSandPS+
thatrequiremulti-stepreasoning. Thismaybedue prompting). They are new zero-shot prompting
tothefactthatthefewexemplarsprovidedarein- methodsthatguideLLMstodeviseaplanthatdi-
sufficienttounlocktheLLMs’capabilities. videstheentiretaskintosmallersubtasksandthen

[TABLE]
-0.41 | -0.56 | 0.76
-0.02 | -0.83 | 0.7
-0.42 | 0.076 | 0.24
[/TABLE]

---
### Page 9

carriesoutthesubtasksaccordingtotheplan. Eval- otherpeople’ssafety.
uationontendatasetsacrossthreetypesofreason-
ing problems shows PS+ prompting outperforms
References
thepreviouszero-shotbaselinesandperformson
parwithfew-shotCoTpromptingonmultiplearith- Tom Brown, Benjamin Mann, Nick Ryder, Melanie
Subbiah,JaredDKaplan,PrafullaDhariwal,Arvind
meticreasoningdatasets. Overall,ourresultssug-
Neelakantan,PranavShyam,GirishSastry,Amanda
gestthat(a)Zero-shotPS+promptingcangenerate
Askell,etal.2020. Languagemodelsarefew-shot
a high-quality reasoning process than Zero-shot- learners. Advancesinneuralinformationprocessing
CoTpromptingsincethePSpromptscanprovide systems,33:1877–1901.
moredetailedinstructionsguidingtheLLMstoper-
Wenhu Chen, Xueguang Ma, Xinyi Wang, and
formcorrectreasoning;(b)Zero-shotPS+prompt- William W Cohen. 2022. Program of thoughts
ing has the potential to outperform manual Few- prompting: Disentanglingcomputationfromreason-
shot CoT prompting, which hopefully will spark ing for numerical reasoning tasks. arXiv preprint
arXiv:2211.12588.
further development of new CoT prompting ap-
proaches to elicit reasoning in LLMs. Moreover, AakankshaChowdhery,SharanNarang,JacobDevlin,
PS(+)promptingisageneralideathatcanbeused Maarten Bosma, Gaurav Mishra, Adam Roberts,
Paul Barham, Hyung Won Chung, Charles Sutton,
for non-reasoning tasks, and refining the plan is
Sebastian Gehrmann, et al. 2022. PaLM: Scaling
alsoaninterestingidea. Weleavethemforfuture
language modeling with pathways. arXiv preprint
work. arXiv:2204.02311.
Karl Cobbe, Vineet Kosaraju, Mohammad Bavar-
7 Limitations
ian, Jacob Hilton, Reiichiro Nakano, Christopher
Hesse, and John Schulman. 2021. Training veri-
Therearetwolimitationstothiswork. First,ittakes
fiers to solve math word problems. arXiv preprint
efforttodesigntheprompttoguidetheLLMsto
arXiv:2110.14168.
generatecorrectreasoningsteps. TheGPT-3mod-
Jacob Devlin, Ming-Wei Chang, Kenton Lee, and
elsaresensitivetotheexpressionsinprompts. Thus
Kristina Toutanova. 2019. BERT: Pre-training of
weneedtocarefullydesigntheprompts. Second,
deepbidirectionaltransformersforlanguageunder-
theproposedplan-and-solvepromptingcanhelpad- standing. In Proceedings of NAACL, pages 4171–
dressthecalculationerrorsandmissing-reasoning- 4186.
steperrors,butthesemanticmisunderstandinger-
Dheeru Dua, Shivanshu Gupta, Sameer Singh, and
rorsstillremain. Wewillexplorehowtoaddress Matt Gardner. 2022. Successive prompting for
semantic misunderstanding errors by prompting decomposing complex questions. arXiv preprint
arXiv:2212.04092.
insteadofupgradingLLMsinthefuture.
Yao Fu, Hao Peng, Ashish Sabharwal, Peter Clark,
8 Ethics andTusharKhot.2022. Complexity-basedprompt-
ing for multi-step reasoning. arXiv preprint
Weexperimentonsixmathreasoningdatasets,in- arXiv:2210.00720.
cludingAQuA(Lingetal.,2017),GSM8K(Cobbe
MorGeva,DanielKhashabi,EladSegal,TusharKhot,
etal.,2021), MultiArith, AddSub, SingleEq, and
DanRoth,andJonathanBerant.2021. Didaristotle
SVAMP (Patel et al., 2021), two commonsense usealaptop? aquestionansweringbenchmarkwith
reasoningtasks(CommonsenseQA(Talmoretal., implicitreasoningstrategies. TACL,9:346–361.
2019) and StrategyQA (Geva et al., 2021)), and
JunxianHe,ChuntingZhou,XuezheMa,TaylorBerg-
twosymbolictasks(LastLetterandCoinFlip(Wei Kirkpatrick,andGrahamNeubig.2021. Towardsa
et al., 2022b)), where GSM8K and SVAMP use unifiedviewofparameter-efficienttransferlearning.
arXivpreprintarXiv:2110.04366.
theMITLicensecode,AQUAandStrategyQAuse
the Apache-2.0 code, the remaining datasets are DanHendrycks,CollinBurns,SauravKadavath,Akul
unspecified. Arora,StevenBasart,EricTang,DawnSong,andJa-
cobSteinhardt.2021. Measuringmathematicalprob-
The proposed prompts do not collect and use
lem solving with the math dataset. arXiv preprint
personalinformationaboutotherindividuals. The
arXiv:2103.03874.
prompts we used are listed in Appendix. The
MohammadJavadHosseini,HannanehHajishirzi,Oren
prompts in this work do not contain any words
Etzioni,andNateKushman.2014. Learningtosolve
that discriminate against any individual or group.
arithmeticwordproblemswithverbcategorization.
Inthiswork,promptswouldnotnegativelyimpact InEMNLP,pages523–533.

---
### Page 10

Neil Houlsby, Andrei Giurgiu, Stanislaw Jastrzebski, viapolicygradientforsemi-structuredmathematical
Bruna Morrone, Quentin De Laroussilhe, Andrea reasoning. arXivpreprintarXiv:2209.14610.
Gesmundo,MonaAttariyan,andSylvainGelly.2019.
Parameter-efficienttransferlearningfornlp. InIn- Arkil Patel, Satwik Bhattamishra, and Navin Goyal.
ternationalConferenceonMachineLearning,pages 2021. AreNLPmodelsreallyabletosolvesimple
2790–2799.PMLR. math word problems? In Proceedings of NAACL,
pages2080–2094.
Jie Huang and Kevin Chen-Chuan Chang. 2022. To-
wardsreasoninginlargelanguagemodels: Asurvey. OfirPress,MuruZhang,SewonMin,LudwigSchmidt,
arXivpreprintarXiv:2212.10403. NoahASmith,andMikeLewis.2022. Measuring
andnarrowingthecompositionalitygapinlanguage
Wenlong Huang, Pieter Abbeel, Deepak Pathak, and models. arXivpreprintarXiv:2210.03350.
IgorMordatch.2022. Languagemodelsaszero-shot
planners: Extractingactionableknowledgeforem- Subhro Roy and Dan Roth. 2016. Solving gen-
bodiedagents. InInternationalConferenceonMa- eral arithmetic word problems. arXiv preprint
chineLearning,pages9118–9147.PMLR. arXiv:1608.01413.
TusharKhot,HarshTrivedi,MatthewFinlayson,Yao AbulhairSaparovandHeHe.2022. Languagemodels
Fu,KyleRichardson,PeterClark,andAshishSab- aregreedyreasoners:Asystematicformalanalysisof
harwal.2022. Decomposedprompting: Amodular chain-of-thought. arXivpreprintarXiv:2210.01240.
approachforsolvingcomplextasks. arXivpreprint
arXiv:2210.02406. OmarShaikh,HongxinZhang,WilliamHeld,Michael
Bernstein,andDiyiYang.2022. Onsecondthought,
TakeshiKojima,ShixiangShaneGu,MachelReid,Yu-
let’snotthinkstepbystep! biasandtoxicityinzero-
takaMatsuo,andYusukeIwasawa.2022. Largelan-
shotreasoning. arXivpreprintarXiv:2212.08061.
guagemodelsarezero-shotreasoners. arXivpreprint
arXiv:2205.11916. SimengSun, YangLiu, ShuohangWang, Chenguang
Zhu,andMohitIyyer.2023. Pearl: Promptinglarge
Rik Koncel-Kedziorski, Hannaneh Hajishirzi, Ashish
language models to plan and execute actions over
Sabharwal, Oren Etzioni, and Siena Dumas Ang.
longdocuments.
2015. Parsing algebraic word problems into equa-
tions. TransactionsoftheAssociationforComputa-
Tianxiang Sun, Yunfan Shao, Hong Qian, Xuanjing
tionalLinguistics,3:585–597.
Huang, and Xipeng Qiu. 2022. Black-box tuning
for language-model-as-a-service. arXiv preprint
RikKoncel-Kedziorski,SubhroRoy,AidaAmini,Nate
arXiv:2201.03514.
Kushman,andHannanehHajishirzi.2016. MAWPS:
Amathwordproblemrepository. InProceedingsof
Mirac Suzgun, Nathan Scales, Nathanael Schärli, Se-
NAACL,pages1152–1157.
bastian Gehrmann, Yi Tay, Hyung Won Chung,
AakankshaChowdhery,QuocVLe,EdHChi,Denny
YifeiLi,ZeqiLin,ShizhuoZhang,QiangFu,BeiChen,
Zhou,etal.2022. Challengingbig-benchtasksand
Jian-Guang Lou, and Weizhu Chen. 2022. On the
whether chain-of-thought can solve them. arXiv
advanceofmakinglanguagemodelsbetterreasoners.
preprintarXiv:2210.09261.
arXivpreprintarXiv:2206.02336.
Alon Talmor, Jonathan Herzig, Nicholas Lourie, and
WangLing,DaniYogatama,ChrisDyer,andPhilBlun-
JonathanBerant.2019. Commonsenseqa:Aquestion
som.2017. Programinductionbyrationalegenera-
answeringchallengetargetingcommonsenseknowl-
tion: Learningtosolveandexplainalgebraicword
edge. InProceedingsofNAACL-HLT,pages4149–
problems. InProceedingsofthe55thAnnualMeet-
4158.
ingoftheAssociationforComputationalLinguistics
(Volume1: LongPapers),pages158–167.
RomalThoppilan,DanielDeFreitas,JamieHall,Noam
Bo Liu, Yuqian Jiang, Xiaohan Zhang, Qiang Liu, Shazeer, Apoorv Kulshreshtha, Heng-Tze Cheng,
Shiqi Zhang, Joydeep Biswas, and Peter Stone. Alicia Jin, Taylor Bos, Leslie Baker, Yu Du, et al.
2023. Llm+ p: Empowering large language mod- 2022. Lamda: Languagemodelsfordialogapplica-
elswithoptimalplanningproficiency. arXivpreprint tions. arXivpreprintarXiv:2201.08239.
arXiv:2304.11477.
BoshiWang,SewonMin,XiangDeng,JiamingShen,
YinhanLiu,MyleOtt,NamanGoyal,JingfeiDu,Man- You Wu, Luke Zettlemoyer, and Huan Sun. 2022a.
dar Joshi, Danqi Chen, Omer Levy, Mike Lewis, Towardsunderstandingchain-of-thoughtprompting:
Luke Zettlemoyer, and Veselin Stoyanov. 2019. Anempiricalstudyofwhatmatters. arXivpreprint
Roberta: A robustly optimized bert pretraining ap- arXiv:2212.10001.
proach. arXivpreprintarXiv:1907.11692.
XuezhiWang,JasonWei,DaleSchuurmans,QuocLe,
Pan Lu, Liang Qiu, Kai-Wei Chang, Ying Nian Wu, EdChi,andDennyZhou.2022b. Self-consistency
Song-Chun Zhu, Tanmay Rajpurohit, Peter Clark, improves chain of thought reasoning in language
andAshwinKalyan.2022. Dynamicpromptlearning models. arXivpreprintarXiv:2203.11171.

---
### Page 11

ZihaoWang,ShaofeiCai,AnjiLiu,XiaojianMa,and
YitaoLiang.2023. Describe, explain, planandse-
lect: Interactiveplanningwithlargelanguagemodels
enablesopen-worldmulti-taskagents. arXivpreprint
arXiv:2302.01560.
Jason Wei, Yi Tay, Rishi Bommasani, Colin Raffel,
Barret Zoph, Sebastian Borgeaud, Dani Yogatama,
MaartenBosma,DennyZhou,DonaldMetzler,etal.
2022a. Emergentabilitiesoflargelanguagemodels.
arXivpreprintarXiv:2206.07682.
JasonWei,XuezhiWang,DaleSchuurmans,Maarten
Bosma,EdChi,QuocLe,andDennyZhou.2022b.
Chainofthoughtpromptingelicitsreasoninginlarge
languagemodels. InThirty-sixthConferenceonNeu-
ralInformationProcessingSystems(NeurIPS2022).
Yixuan Weng, Minjun Zhu, Shizhu He, Kang Liu,
and Jun Zhao. 2022. Large language models are
reasoners with self-verification. arXiv preprint
arXiv:2212.09561.
Shunyu Yao, Dian Yu, Jeffrey Zhao, Izhak Shafran,
Thomas L. Griffiths, Yuan Cao, and Karthik
Narasimhan. 2023. Tree of thoughts: Deliberate
problemsolvingwithlargelanguagemodels.
Shunyu Yao, Jeffrey Zhao, Dian Yu, Nan Du, Izhak
Shafran,KarthikNarasimhan,andYuanCao.2022.
React: Synergizingreasoningandactinginlanguage
models. ArXiv,abs/2210.03629.
Zhuosheng Zhang, Aston Zhang, Mu Li, and Alex
Smola. 2022. Automatic chain of thought prompt-
ing in large language models. arXiv preprint
arXiv:2210.03493.
Denny Zhou, Nathanael Schärli, Le Hou, Jason Wei,
Nathan Scales, Xuezhi Wang, Dale Schuurmans,
Olivier Bousquet, Quoc Le, and Ed Chi. 2022.
Least-to-most prompting enables complex reason-
ing in large language models. arXiv preprint
arXiv:2205.10625.
A Appendix
Thissectionincludestwoparts: (1)Resultsofall
promptswehavetried;(2)Exampletextsgenerated
by Zero-shot-PS+. Unless otherwise mentioned,
weuseGPT3(text-davinci-003)model.
A.1 ResultsofAllTriggerSentences
Tables7to16listtheresultsofallpromptswehave
triedforeachdataset.
A.2 ExampleOutputsbyZero-shot-PS+
Tables17to25listexampleoutputsgeneratedby
Zero-shot-PS+foreachdataset.

---
### Page 12

Table 7: Performance comparison of prompts used in Step 1 of Zero-shot-PS+ prompting with
text-davinci-003onAQuA.
No. TriggerSetence Accuracy
Let’sfirstunderstandtheproblemanddeviseaplantosolvetheproblem.Then,let’scarryouttheplan
1 42.5
tosolvetheproblemstepbystep.
Let’sfirstunderstandtheproblem,extractallrelevantvariablesandtheircorrespondingnumerals
carefully,anddeviseaplan.Then,let’scarryouttheplan,calculateintermediatevariables(payattention
2 42.9
tocorrectnumericalcalculationandcommonsense),solvetheproblemstepbystepcarefully,andshow
theanswer.
Let’sfirstunderstandtheproblem,extractrelevantcorrectvariablesandtheircorrectcorresponding
numerals,anddevisecompleteplans.Then,let’scarryouttheplan,calculateintermediatevariables
3 43.7
includingextractedvariables(payattentiontocorrectnumericalcalculationandcommonsense),solve
theproblembysingleequations,andshowtheanswer.
Let’sfirstunderstandtheproblem,extractrelevantvariablesandtheircorrespondingnumerals,and
4 makeacompleteplan.Then,let’scarryouttheplan,calculateintermediatevariables(payattentionto 46.0
correctnumericalcalculationandcommonsense),solvetheproblemstepbystep,andshowtheanswer.
Table 8: Performance comparison of prompts used in Step 1 of Zero-shot-PS+ prompting with
text-davinci-003onGSM8K.
No. TriggerSetence Accuracy
Let’sfirstunderstandtheproblemanddeviseaplantosolvetheproblem.Then,let’scarryouttheplan
1 58.2
tosolvetheproblemstepbystep.
Let’sfirstunderstandtheproblem,extractrelevantvariablesandtheircorrespondingnumerals,and
2 deviseaplan.Then,let’scarryouttheplan,calculateintermediatevariables(payattentiontocorrect 58.7
numeralcalculationandcommonsense),solvetheproblemstepbystep,andshowtheanswer.
Let’sfirstunderstandtheproblem,extractrelevantvariablesandtheircorrespondingnumerals,and
3 makeacompleteplan.Then,let’scarryouttheplan,calculateintermediatevariables(payattentionto 59.3
correctnumericalcalculationandcommonsense),solvetheproblemstepbystep,andshowtheanswer.
Table 9: Performance comparison of prompts used in Step 1 of Zero-shot-PS+ prompting with
text-davinci-003onMultiArith.
No. TriggerSetence Accuracy
Let’sfirstunderstandtheproblemanddeviseaplantosolvetheproblem.Then,let’scarryouttheplan
1 87.2
tosolvetheproblemstepbystep.
Let’sfirstunderstandtheproblem,extractrelevantvariablesandtheircorrespondingnumerals,and
2 deviseaplan.Then,let’scarryouttheplan,calculateintermediatevariables(payattentiontocorrect 88.3
numeralcalculationandcommonsense),solvetheproblemstepbystep,andshowtheanswer.
Let’sfirstunderstandtheproblem,extractrelevantvariablesandtheircorrespondingnumerals,and
deviseacompleteplan.Then,let’scarryouttheplan,calculateintermediatevariables(payattention
3 90.5
tothecorrectnessofthecalculationandcommonsense),solvetheproblemstepbystep,andshow
theanswer.
Let’sfirstunderstandtheproblem,extractrelevantvariablesandtheircorrespondingnumerals,and
4 deviseacompleteplan.Then,let’scarryouttheplan,calculateintermediatevariables(payattentionto 91.8
correctnumericalcalculationandcommonsense),solvetheproblemstepbystep,andshowtheanswer.

---
### Page 13

Table 10: Performance comparison of prompts used in Step 1 of Zero-shot-PS+ prompting with
text-davinci-003onSVAMP.
No. TriggerSetence Accuracy
Let’sfirstunderstandtheproblemanddeviseaplantosolvetheproblem.Then,let’scarryouttheplan
1 72.0
tosolvetheproblemstepbystep.
Let’sfirstunderstandtheproblem,extractrelevantvariablesandtheircorrespondingnumerals,and
2 deviseaplan.Then,let’scarryouttheplan,calculateintermediatevariables(payattentiontocorrect 75.4
numeralcalculationandcommonsense),solvetheproblemstepbystep,andshowtheanswer.
Let’sfirstunderstandtheproblem,extractrelevantvariablesandtheircorrespondingnumerals,and
3 makeacompleteplan.Then,let’scarryouttheplan,calculateintermediatevariables(payattentionto 75.7
correctnumericalcalculationandcommonsense),solvetheproblemstepbystep,andshowtheanswer.
Table 11: Performance comparison of prompts used in Step 1 of Zero-shot-PS+ prompting with
text-davinci-003onAddSub.
No. TriggerSetence Accuracy
Let’sfirstunderstandtheproblemanddeviseaplantosolvetheproblem.Then,let’scarryouttheplan
1 87.3
tosolvetheproblemstepbystep.
Let’sfirstunderstandtheproblem,extractrelevantvariablesandtheircorrespondingnumerals,and
2 deviseacompleteplan.Then,let’scarryouttheplan,calculateintermediatevariables(payattentionto 87.8
correctnumericalcalculationandcommonsense),solvetheproblemstepbystep,andshowtheanswer.
Let’sfirstunderstandtheproblem,extractrelevantvariablesandtheircorrespondingnumerals,and
3 deviseaplan.Then,let’scarryouttheplan,calculateintermediatevariables(payattentiontocorrect 92.2
numeralcalculationandcommonsense),solvetheproblemstepbystep,andshowtheanswer.
Table 12: Performance comparison of prompts used in Step 1 of Zero-shot-PS+ prompting with
text-davinci-003onSingleEq.
No. TriggerSetence Accuracy
Let’sfirstunderstandtheproblemanddeviseaplantosolvetheproblem.Then,let’scarryouttheplan
1 92.3
tosolvetheproblemstepbystep.
Let’sfirstunderstandtheproblem,extractrelevantvariablesandtheircorrespondingnumerals,and
2 deviseaplan.Then,let’scarryouttheplan,calculateintermediatevariables(payattentiontocorrect 94.7
numeralcalculationandcommonsense),solvetheproblemstepbystep,andshowtheanswer.
Table 13: Performance comparison of prompts used in Step 1 of Zero-shot-PS+ prompting with
text-davinci-003onCSQA.
No. TriggerSetence Accuracy
1 Let’sdeviseaplanandsolvetheproblemstepbystep. 67.4
Let’sfirstunderstandtheproblem,extractrelevantvariablesandtheircorrespondingnumerals,and
2 deviseacompleteplan.Then,let’scarryouttheplan,calculateintermediatevariables(payattentionto 71.9
correctnumericalcalculationandcommonsense),solvetheproblemstepbystep,andshowtheanswer.
Table 14: Performance comparison of prompts used in Step 1 of Zero-shot-PS+ prompting with
text-davinci-003onStrategyQA.
No. TriggerSetence Accuracy
1 Let’sdeviseaplanandsolvetheproblemstepbystep. 61.5
Let’sdeviseacompleteplan.Then,let’scarryouttheplan,solvetheproblemstepbystep,and
2 63.0
showtheanswer.
Let’sfirstpreparerelevantinformationandmakeaplan.Then,let’sanswerthequestionstepbystep
3 65.4
(payattentiontocommonsenseandlogicalcoherence).

---
### Page 14

Table 15: Performance comparison of prompts used in Step 1 of Zero-shot-PS+ prompting with
text-davinci-003onLastLetters.
No. TriggerSetence Accuracy
1 Let’sdeviseaplanandsolvetheproblemstepbystep. 75.2
Table 16: Performance comparison of prompts used in Step 1 of Zero-shot-PS+ prompting with
text-davinci-003onCoinFlip.
No. TriggerSetence Accuracy
Let’sdeviseacompleteplan.Then,let’scarryouttheplan,solvetheproblemstepbystep,
1 70.6
andshowtheanswer.
2 Let’sfirstdeviseaplan,thensolvetheproblemstepbystep. 72.6
Let’sfirstdeviseaplan,thensolvetheproblemstepbystep.(Distinguishbetweentailupand
3 84.0
headup)
Let’sfirstunderstandtheproblemanddeviseacompleteplan.Then,let’scarryouttheplan,
reasonproblemstepbystep.Everystepanswerthesubquestion"doesthepersonflipand
whatisthecoincurrentstate?",andaccordingtothelastcoinstate,givethefinalanswer
4 94.2
(payattentionthatthecointurnsstateateveryflip).
Plan:
Step1:
Let’sfirstunderstandtheproblemanddeviseacompleteplan.Then,let’scarryouttheplan,
reasonproblemstepbystep.Everystepanswerthesubquestion"doesthepersonflipandwhat
isthecoincurrentstate?",andaccordingtothecoinlaststategivethefinalanswer(payattention
5 99.0
toeveryflip,thecointurnsstate).
Plan:
Step1:
Let’sfirstunderstandtheproblemanddeviseacompleteplan.Then,let’scarryouttheplanand
reasonproblemstepbystep.Everystepanswerthesubquestion,"doesthepersonflipandwhatis
6 99.6
thecoin’scurrentstate?".Accordingtothecoin’slaststate,givethefinalanswer(payattentionto
everyflipandthecoin’sturningstate).

---
### Page 15

Table17: ExampleoutputsbyZero-shot-PS+forAQuA.
Q:Theaveragewagesofaworkerduringafortnightcomprisingof15consecutiveworkingdayswas
$90perday. Duringthefirst7days,hisaveragewagewas$87perdayandtheaveragewageduring
thelast7dayswas$92perday. Whatwashiswageonthe8thday? AnswerChoices: (A)$83(B)
$92(C)$90(D)$97(E)$104
A:Let’sfirstunderstandtheproblem,extractrelevantvariablesandtheircorrespondingnumerals,and
makeacompleteplan.Then,let’scarryouttheplan,calculateintermediatevariables(payattention
tocorrectnumericalcalculationandcommonsense),solvetheproblemstepbystep,andshowthe
answer.
Output:
Variables:
Averagewageduringthefirst7days=87
Averagewageduringthelast7days=92
Averagewageduringthefortnight=90
Plan:
Calculatethetotalwagesearnedduring
thefirst7days.
Calculatethetotalwagesearnedduring
thelast7days.
Calculatethetotalwagesearnedduring
thefortnight.
Calculatethewageonthe8thday.
Calculation:
Totalwagesearnedduringthefirst7days=7x87=609
Totalwagesearnedduringthelast7days=7x92=644
Totalwagesearnedduringthefortnight=15x90=1350
Wageonthe8thday=(1350-609-644)/1=97
Answer: (D)$97.
Q:If27bottlesofsodacostAcents,howmuchwillBbottlescostindollars? AnswerChoices: (A)
AB/2700(B)27/AB(C)AB/270(D)2700/AB(E)100AB/27
A:Let’sfirstunderstandtheproblem,extractrelevantvariablesandtheircorrespondingnumerals,and
makeacompleteplan.Then,let’scarryouttheplan,calculateintermediatevariables(payattention
tocorrectnumericalcalculationandcommonsense),solvetheproblemstepbystep,andshowthe
answer.
Output:
Given:
27bottlesofsodacostAcents
Bbottlesofsoda
Plan:
1. ConvertAcentstodollars
2. CalculatethecostofBbottlesofsoda
Solution:
1. ConvertAcentstodollars: Acents=A/100dollars
2. CalculatethecostofBbottlesofsoda: Bbottlesofsoda=(A/100)*(B/27)=AB/2700dollars
Answer: (A)AB/2700

---
### Page 16

Table18: ExampleoutputsbyZero-shot-PS+forGSM8K.
Q:Jamesdecidestorun3sprints3timesaweek. Heruns60meterseachsprint. Howmanytotal
metersdoesherunaweek?
A:Let’sfirstunderstandtheproblem,extractrelevantvariablesandtheircorrespondingnumerals,and
makeacompleteplan.Then,let’scarryouttheplan,calculateintermediatevariables(payattention
tocorrectnumericalcalculationandcommonsense),solvetheproblemstepbystep,andshowthe
answer.
Output:
Given:
Jamesruns3sprints3timesaweek.
Eachsprintis60meters.
Plan:
WeneedtocalculatethetotalmetersrunbyJamesinaweek.
Calculation:
TotalnumberofsprintsrunbyJamesinaweek=3sprintsx3times=9sprints
TotalmetersrunbyJamesinaweek=9sprintsx60meters=540meters
Answer:
Jamesruns540metersinaweek.
Q: In a dance class of 20 students, 20% enrolled in contemporary dance, 25% of the remaining
enrolledinjazzdance,andtherestenrolledinhip-hopdance. Whatpercentageoftheentirestudents
enrolledinhip-hopdance?
A:Let’sfirstunderstandtheproblem,extractrelevantvariablesandtheircorrespondingnumerals,and
makeacompleteplan.Then,let’scarryouttheplan,calculateintermediatevariables(payattention
tocorrectnumericalcalculationandcommonsense),solvetheproblemstepbystep,andshowthe
answer.
Output:
Given:
Totalnumberofstudents=20
Percentageofstudentsenrolledincontemporarydance=20%
Percentageofstudentsenrolledinjazzdance=25%
Plan:
1. Calculatethenumberofstudentsenrolledincontemporarydance.
2. Calculatethenumberofstudentsremainingaftersubtractingthenumberofstudentsenrolledin
contemporarydance.
3. Calculatethenumberofstudentsenrolledinjazzdance.
4. Calculatethenumberofstudentsenrolledinhip-hopdance.
5. Calculatethepercentageofstudentsenrolledinhip-hopdance.
Calculation:
1. Numberofstudentsenrolledincontemporarydance=20%of20=20%×20=4
2. Numberofstudentsremainingaftersubtractingthenumberofstudentsenrolledincontemporary
dance=20-4=16
3. Numberofstudentsenrolledinjazzdance=25%of16=25%×16=4
4. Numberofstudentsenrolledinhip-hopdance=16-4=12
5. Percentageofstudentsenrolledinhip-hopdance=12/20×100%=60%
Answer:
60%oftheentirestudentsenrolledinhip-hopdance.

---
### Page 17

Table19: ExampleoutputsbyZero-shot-PS+forMultiArith.
Q:Theschoolcafeteriaordered42redapplesand7greenapplesforstudentslunches. But,ifonly9
studentswantedfruit,howmanyextradidthecafeteriaendupwith?
A:Let’sfirstunderstandtheproblem,extractrelevantvariablesandtheircorrespondingnumerals,and
deviseacompleteplan.Then,let’scarryouttheplan,calculateintermediatevariables(payattention
tocorrectnumericalcalculationandcommonsense),solvetheproblemstepbystep,andshowthe
answer.
Output:
Variables:
Redapples=42
Greenapples=7
Studentswantingfruit=9
Plan:
Calculatethetotalnumberofapplesorderedbythecafeteria
Subtractthetotalnumberofapplesorderedbythecafeteriafromthenumberofstudentswantingfruit
Calculation:
Totalnumberofapplesorderedbythecafeteria=42+7=49
Answer:
Extraapples=49-9=40
Q:Carolandhermomwerepickingcarrotsfromtheirgarden. Carolpicked29andhermotherpicked
16. Ifonly38ofthecarrotsweregood,howmanybadcarrotsdidtheyhave?
A:Let’sfirstunderstandtheproblem,extractrelevantvariablesandtheircorrespondingnumerals,and
deviseacompleteplan.Then,let’scarryouttheplan,calculateintermediatevariables(payattention
tocorrectnumericalcalculationandcommonsense),solvetheproblemstepbystep,andshowthe
answer.
Output:
Variables:
Carol: 29
Mom: 16
GoodCarrots: 38
Plan:
Wecancalculatethenumberofbadcarrotsbysubtractingthenumberofgoodcarrotsfromthetotal
numberofcarrotspicked.
Calculation:
TotalCarrotsPicked=Carol+Mom=29+16=45
BadCarrots=TotalCarrotsPicked-GoodCarrots=45-38=7
Answer:
Therewere7badcarrots.

---
### Page 18

Table20: ExampleoutputsbyZero-shot-PS+forSVAMP.
Q:Mombuys70whitet-shirtsintotal. Ifwhitet-shirtscanbepurchasedinpackagesandmom
buys14packages. Howmanywhitet-shirtsdoeseachpackagehave?
A:Let’sfirstunderstandtheproblem,extractrelevantvariablesandtheircorrespondingnumerals,
andmakeanddeviceacompleteplan.Then,let’scarryouttheplan,calculateintermediatevariables
(payattentiontocorrectnumericalcalculationandcommonsense),solvetheproblemstepbystep,
andshowtheanswer.
Output:
Variables:
Totalnumberofwhitet-shirts=70
Numberofpackages=14
Plan:
Wecanusetheequation:
Totalnumberofwhitet-shirts=NumberofpackagesxNumberoft-shirtsperpackage
Calculation:
Numberoft-shirtsperpackage=70/14=5
Answer:
Eachpackagehas5whitet-shirts.
Q:Jesse’sroomsare19feetlongand18feetwide. Ifshehas20roomsinall. Howmuchcarpetdoes
sheneedtocoverthefloorsofallrooms?
A:Let’sfirstunderstandtheproblem,extractrelevantvariablesandtheircorrespondingnumerals,
andmakeanddeviceacompleteplan.Then,let’scarryouttheplan,calculateintermediatevariables
(payattentiontocorrectnumericalcalculationandcommonsense),solvetheproblemstepbystep,
andshowtheanswer.
Output:
RelevantVariables:
Numberofrooms: 20
Lengthofeachroom: 19feet
Widthofeachroom: 18feet
Plan:
Step1: Calculatetheareaofeachroom.
Step2: Multiplytheareaofeachroombythenumberofrooms.
Step3: Showtheanswer.
Calculation:
Step1: Areaofeachroom=LengthxWidth=19feetx18feet=342squarefeet
Step2: Totalareaofallrooms=AreaofeachroomxNumberofrooms=342squarefeetx20rooms
=6840squarefeet
Answer: Jesseneeds6840squarefeetofcarpettocoverthefloorsofallrooms.

---
### Page 19

Table21: ExampleoutputsbyZero-shot-PS+forAddSub.
Q:Therewere28balesofhayinthebarn. Timstackedbalesinthebarntoday. Therearenow54
balesofhayinthebarn. Howmanybalesdidhestoreinthebarn?
A:Let’sfirstunderstandtheproblem,extractrelevantvariablesandtheircorrespondingnumerals,
anddeviseaplan. Then,let’scarryouttheplan,calculateintermediatevariables(payattentionto
correctnumeralcalculationandcommonsense),solvetheproblemstepbystep,andshowtheanswer.
Output:
Given:
Initialnumberofbalesofhayinthebarn=28
NumberofbalesofhayinthebarnafterTimstackedthem=54
Plan:
CalculatethenumberofbalesofhayTimstoredinthebarnbysubtractingtheinitialnumberofbales
ofhayfromthenumberofbalesofhayafterTimstackedthem.
Calculation:
NumberofbalesofhayTimstoredinthebarn=54-28=26
Answer:
Timstored26balesofhayinthebarn.
Q:Therewere6rosesinthevase. Marycutsomerosesfromherflowergarden. Therearenow16
rosesinthevase. Howmanyrosesdidshecut?
A:Let’sfirstunderstandtheproblem,extractrelevantvariablesandtheircorrespondingnumerals,
anddeviseaplan. Then,let’scarryouttheplan,calculateintermediatevariables(payattentionto
correctnumeralcalculationandcommonsense),solvetheproblemstepbystep,andshowtheanswer.
Output:
Given:
Initialnumberofrosesinthevase=6
Finalnumberofrosesinthevase=16
Plan:
Subtracttheinitialnumberofrosesfromthefinalnumberofrosestocalculatethenumberofroses
Marycut.
Calculation:
NumberofrosesMarycut=16-6=10
Answer:
Marycut10rosesfromherflowergarden.

---
### Page 20

Table22: ExampleoutputsbyZero-shot-PS+forSingleEq.
Q:Aftereatingattherestaurant, Sally, Sam, andAlyssadecidedtodividethebillevenly. Ifeach
personpaid45dollars,whatwasthetotalofthebill?
A:Let’sfirstunderstandtheproblem,extractrelevantvariablesandtheircorrespondingnumerals,
anddeviseaplan. Then,let’scarryouttheplan,calculateintermediatevariables(payattentionto
correctnumeralcalculationandcommonsense),solvetheproblemstepbystep,andshowtheanswer.
Output:
Problem: Aftereatingattherestaurant,Sally,Sam,andAlyssadecidedtodividethebillevenly. If
eachpersonpaid45dollars,whatwasthetotalofthebill?
Variables:
-Totalofthebill(T)
-Numberofpeople(N)
-Amountpaidbyeachperson(A)
Numerals:
-N=3
-A=45
Plan:
-Calculatethetotalofthebill(T)bymultiplyingthenumberofpeople(N)bytheamountpaidby
eachperson(A).
Calculation:
T=NxA
T=3x45
T=135
Answer: Thetotalofthebillwas135dollars.
Q:Maryisbakingacake. Therecipewants8cupsofflour. Shealreadyputin2cups. Howmany
morecupsdoessheneedtoadd?
A:Let’sfirstunderstandtheproblem,extractrelevantvariablesandtheircorrespondingnumerals,
anddeviseaplan. Then,let’scarryouttheplan,calculateintermediatevariables(payattentionto
correctnumeralcalculationandcommonsense),solvetheproblemstepbystep,andshowtheanswer.
Output:
Maryneedstoadd8cupsofflourtothecake. Shehasalreadyputin2cups.
Plan:
SubtracttheamountofflourMaryhasalreadyputinfromthetotalamountofflourneeded.
Calculation:
8cups(totalamountofflourneeded)-2cups(amountofflourMaryhasalreadyputin)=6cups
(amountofflourMaryneedstoadd)
Answer: Maryneedstoadd6morecupsofflour.

---
### Page 21

Table23: ExampleoutputsbyZero-shot-PS+forCommonsenseQA.
Q:Whatisaplacethathasabenchnestledintrees? AnswerChoices: (A)statepark(B)busstop(C)
busdepot(D)statue(E)trainstation
A:Let’sfirstunderstandtheproblem,extractrelevantvariablesandtheircorrespondingnumerals,and
deviseacompleteplan.Then,let’scarryouttheplan,calculateintermediatevariables(payattention
tocorrectnumericalcalculationandcommonsense),solvetheproblemstepbystep,andshowthe
answer.
Output:
Thequestionisaskingforaplacethathasabenchnestledintrees. Theanswerchoicesare(A)state
park,(B)busstop,(C)busdepot,(D)statue,and(E)trainstation.
Theansweris(A)statepark. Stateparksaretypicallylocatedinnaturalareaswithtrees,andthey
oftenhavebenchesforvisitorstositandenjoythescenery.
Q:Whereisagoodideabutnotrequiredtohaveafireextinguisher? AnswerChoices: (A)schoolbus
(B)boat(C)house(D)hospital(E)school
A:Let’sfirstunderstandtheproblem,extractrelevantvariablesandtheircorrespondingnumerals,and
deviseacompleteplan.Then,let’scarryouttheplan,calculateintermediatevariables(payattention
tocorrectnumericalcalculationandcommonsense),solvetheproblemstepbystep,andshowthe
answer.
Output:
Thequestionisaskingforagoodideatohaveafireextinguisher,butitisnotrequired. Theanswer
choicesare(A)schoolbus,(B)boat,(C)house,(D)hospital,and(E)school.
The best answer is (C) house. Having a fire extinguisher in a house is a good idea, but it is not
required. Fireextinguishersarenottypicallyrequiredinschoolbuses,boats,hospitals,orschools.

---
### Page 22

Table24: ExampleoutputsbyZero-shot-PS+forStrategyQA.
Q:Doesthecountrythatreceivedthemostgoldmedalsduringthe1976Olympicsstillexist?
A:Let’sfirstpreparerelevantinformationandmakeaplan. Then,let’sanswerthequestionstepby
step(payattentiontocommonsenseandlogicalcoherence).
Output:
Relevantinformation:
-The1976OlympicswereheldinMontreal,Canada.
-Thecountrythatreceivedthemostgoldmedalsduringthe1976OlympicswastheSovietUnion.
Plan:
1. DetermineiftheSovietUnionstillexists.
2. IftheSovietUnionstillexists,answerthequestion.
3. IftheSovietUniondoesnotexist,determinewhichcountriesithasbeenreplacedby. Answer:
1. TheSovietUnionnolongerexists.
2. No,thecountrythatreceivedthemostgoldmedalsduringthe1976Olympicsdoesnotstillexist.
3. The Soviet Union has been replaced by 15 independent countries, including Russia, Ukraine,
Belarus,andKazakhstan.
Q:IstheMonaLisainthesamemuseumastheVenusdeMilo?
A:Let’sfirstpreparerelevantinformationandmakeaplan. Then,let’sanswerthequestionstepby
step(payattentiontocommonsenseandlogicalcoherence).
Output:
Relevantinformation:
MonaLisa: LocatedintheLouvreMuseuminParis,France
VenusdeMilo: LocatedintheLouvreMuseuminParis,France
Plan:
Step1: IdentifythelocationsoftheMonaLisaandtheVenusdeMilo
Step2: Comparethelocations
Answer:
Yes,theMonaLisaandtheVenusdeMiloarebothlocatedintheLouvreMuseuminParis,France.

---
### Page 23

Table25: ExampleoutputsbyZero-shot-PS+forLastLetters.
Q:Takethelastlettersofeachwordsin"LinoMarielAdityaElisabeth"andconcatenatethem
A:Let’sdeviseaplanandsolvetheproblemstepbystep.
Output:
Step1: Takethelastlettersofeachwordinthegivenstring.
Lino: o
Mariel: l
Aditya: a
Elisabeth: h
Step2: Concatenatethelastletters.
Answer: olah
Q:Takethelastlettersofeachwordsin"JackySocorroMarkWanda"andconcatenatethem
A:Let’sdeviseaplanandsolvetheproblemstepbystep.
Output:
Step1: Takethelastlettersofeachword.
Jacky: y
Socorro: o
Mark: k
Wanda: a
Step2: Concatenatetheletters.
Answer: yoka

---
### Page 24

Table26: ExampleoutputsbyZero-shot-PS+forCoinFlip.
Q:Acoinisheadsup. Walterdoesnotflipthecoin. Mikayladoesnotflipthecoin. Larrydoesnotflip
thecoin. Ryandoesnotflipthecoin. Isthecoinstillheadsup? Notethat"flip"heremeans"reverse".
A:Let’sfirstunderstandtheproblemanddeviseacompleteplan. Then,let’scarryouttheplanand
reasonproblemstepbystep. Everystepanswerthesubquestion,"doesthepersonflipandwhatisthe
coin’scurrentstate?". Accordingtothecoin’slaststate,givethefinalanswer(payattentiontoevery
flipandthecoin’sturningstate).
Output:
Plan:
Step1: Walterdoesnotflipthecoin.
Step2: Mikayladoesnotflipthecoin.
Step3: Larrydoesnotflipthecoin.
Step4: Ryandoesnotflipthecoin.
Answer: Yes,thecoinisstillheadsup.
Explanation:
Step1: Walterdoesnotflipthecoin. Therefore,thecoinisstillheadsup.
Step2: Mikayladoesnotflipthecoin. Therefore,thecoinisstillheadsup.
Step3: Larrydoesnotflipthecoin. Therefore,thecoinisstillheadsup.
Step4: Ryandoesnotflipthecoin. Therefore,thecoinisstillheadsup.
Conclusion: Yes,thecoinisstillheadsup.
Q:Acoinisheadsup. Lorenadoesnotflipthecoin. Shanadoesnotflipthecoin. Priscilladoesnot
flipthecoin. Summerdoesnotflipthecoin. Isthecoinstillheadsup? Notethat"flip"heremeans
"reverse"
A:Let’sfirstunderstandtheproblemanddeviseacompleteplan. Then,let’scarryouttheplanand
reasonproblemstepbystep. Everystepanswerthesubquestion,"doesthepersonflipandwhatisthe
coin’scurrentstate?". Accordingtothecoin’slaststate,givethefinalanswer(payattentiontoevery
flipandthecoin’sturningstate).
Output:
Plan:
Step1: Lorenadoesnotflipthecoin.
Step2: Shanadoesnotflipthecoin.
Step3: Priscilladoesnotflipthecoin.
Step4: Summerdoesnotflipthecoin.
Answer:
Step1: Lorenadoesnotflipthecoin. Therefore,thecoinisstillheadsup.
Step2: Shanadoesnotflipthecoin. Therefore,thecoinisstillheadsup.
Step3: Priscilladoesnotflipthecoin. Therefore,thecoinisstillheadsup.
Step4: Summerdoesnotflipthecoin. Therefore,thecoinisstillheadsup.
FinalAnswer: Yes,thecoinisstillheadsup.
