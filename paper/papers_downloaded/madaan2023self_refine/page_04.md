Here, thepromptp providesexamplesoffeedbackintheformofinput-output-feedbacktriples
fb
⟨x(k),y(k),fb(k)⟩. Wepromptthemodeltowritefeedbackthatisactionableandspecificviafb(k).
By‘actionable’,wemeanthefeedbackshouldcontainaconcreteactionthatwouldlikelyimprovethe
output. By‘specific’,wemeanthefeedbackshouldidentifyconcretephrasesintheoutputtochange.
Forexample,thefeedbackinFigure2(e)is“Thiscodeisslowasitusesaforloopwhichisbrute
force. Abetterapproachistousetheformula... (n(n+1))/2”. Thisfeedbackisactionable,sinceit
suggeststheaction‘usetheformula...’. Thefeedbackisspecificsinceitmentionsthe‘forloop’.
REFINE Next,SELF-REFINEusesMtorefineitsmostrecentoutput,givenitsownfeedback:
y =M(p ∥x∥y ∥fb ). (3)
t+1 refine t t
Forexample,inFigure2(f),giventheinitialoutputandthegeneratedfeedback,themodelgenerates
a re-implementation that is shorter and runs much faster than the initial implementation. The
prompt p provides examples of improving the output based on the feedback, in the form of
refine
input-output-feedback-refinedquadruples⟨x(k),y(k),fb(k),y(k)⟩.
t t t+1
Iterating SELF-REFINE SELF-REFINE alternatesbetween FEEDBACK and REFINE stepsuntila
stoppingconditionismet. Thestoppingconditionstop(fb ,t)eitherstopsataspecifiedtimestept,
t
orextractsastoppingindicator(e.g. ascalarstopscore)fromthefeedback. Inpractice,themodel
canbepromptedtogenerateastoppingindicatorinp ,andtheconditionisdeterminedper-task.
fb
Toinformthemodelaboutthepreviousiterations,weretainthehistoryofpreviousfeedbackand
outputs by appending them to the prompt. Intuitively, this allows the model to learn from past
mistakesandavoidrepeatingthem. Moreprecisely,Equation(3)isinfactinstantiatedas:
y =M(p ∥x∥y ∥fb ∥...∥y ∥fb ). (4)
t+1 refine 0 0 t t
Finally,weusethelastrefinementy
t
astheoutputofSELF-REFINE.
Algorithm1summarizes SELF-REFINE,andFigure2showsanexampleof SELF-REFINE inthe
DialogueResponseGeneration(MehriandEskenazi,2020)andCodeOptimization(Madaanetal.,
2023)tasks. AppendixSprovidesexamplesofthep ,p ,p promptsforvarioustasks. Thekey
gen fb refine
ideaisthatSELF-REFINEusesthesameunderlyingLLMtogenerate,getfeedback,andrefineits
outputsgivenitsownfeedback. Itreliesonlyonsupervisionpresentinthefew-shotexamples.
3 Evaluation
WeevaluateSELF-REFINEon7diversetasks: DialogueResponseGeneration(AppendixM; Mehri
and Eskenazi, 2020), Code Optimization (Appendix N; Madaan et al., 2023), Code Readability
Improvement(AppendixL; Purietal.,2021),MathReasoning(AppendixO; Cobbeetal.,2021),
SentimentReversal(AppendixP; Zhangetal.,2015),andweintroducetwonewtasks: Acronym
Generation(AppendixQ)andConstrainedGeneration(aharderversionofLinetal.(2020)with
20-30keywordconstraintsinsteadof3-5;AppendixR)
ExamplesforalltasksanddatasetstatisticsareprovidedinTable4(AppendixA).
3.1 InstantiatingSELF-REFINE
We instantiate SELF-REFINE following the high-level description in Section 2. The FEEDBACK-
REFINEiterationscontinueuntilthedesiredoutputqualityortask-specificcriterionisreached,uptoa
maximumof4iterations. Tomakeourevaluationconsistentacrossdifferentmodels,weimplemented
bothFEEDBACKandREFINEasfew-shotpromptsevenwithmodelsthatrespondwelltoinstructions,
suchasChatGPTandGPT-4.
BaseLLMs Ourmaingoalistoevaluatewhetherwecanimprovetheperformanceofanystrong
baseLLMsusingSELF-REFINE. Therefore,wecompareSELF-REFINEtothesamebaseLLMsbut
withoutfeedback-refineiterations. WeusedthreemainstrongbaseLLMacrossalltasks: GPT-3.5
(text-davinci-003),ChatGPT(gpt-3.5-turbo),andGPT-4(OpenAI,2023). Forcode-based
tasks,wealsoexperimentedwith CODEX (code-davinci-002). Inalltasks,either GPT-3.5 or
GPT-4 is the previous state-of-the-art.3 We used the same prompts from previous work when
3Acomparisonwithotherfew-shotandfine-tunedapproachesisprovidedinAppendixF
4
