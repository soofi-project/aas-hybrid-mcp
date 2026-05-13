A EvaluationTasks
Table4liststhetasksinourevaluation,andexamplesfromeachtask.
TaskandDescription SampleoneiterationofFEEDBACK-REFINE
SentimentReversal x: Thefoodwasfantastic...”
Rewritereviewstoreversesentiment. y : Thefoodwasdisappointing...”
t
Dataset: (Zhangetal.,2015)1000reviewpas- fb: Increasenegativesentiment
sages y : Thefoodwasutterlyterrible...”
t+1
DialogueResponseGeneration x: What’sthebestwaytocookpasta?”
Producerichconversationalresponses. y : Thebestwaytocookpastaisto...”
t
Dataset:(MehriandEskenazi,2020)372conv. fb: Makeresponserelevant,engaging,safe
y : Boilwater,addsalt,andcookpasta...”
t+1
CodeOptimization x: Nestedloopformatrixproduct
EnhancePythoncodeefficiency y : NumPydotproductfunction
t
Dataset:(Madaanetal.,2023):1000programs fb: Improvetimecomplexity
y : UseNumPy’soptimizedmatmulfunction
t+1
CodeReadabilityImprovement x: Unclearvariablenames,nocomments
RefactorPythoncodeforreadability. y : Descriptivenames,comments
t
Dataset: (Purietal.,2021)300programs∗ fb: Enhancevariablenaming;addcomments
y : Clearvariables,meaningfulcomments
t+1
MathReasoning x: Oliviahas$23,buys5bagelsat$3each”
Solvemathreasoningproblems. y : SolutioninPython
t
Dataset: (Cobbeetal.,2021)1319questions fb: Showstep-by-stepsolution
y : Solutionwithdetailedexplanation
t+1
AcronymGeneration x: RadioDetectingandRanging”
Generateacronymsforagiventitle y : RDR
t
Dataset: (AppendixQ)250acronyms fb: becontextrelevant;easypronunciation
y : RADAR”
t+1
ConstrainedGeneration x: beach,vacation,relaxation
Generatesentenceswithgivenkeywords. y : Duringourbeachvacation...
t
Dataset: (Linetal.,2020)200samples fb: Includekeywords;maintaincoherence
y :..beachvacationwasfilledwithrelaxation
t+1
Table4: AnoverviewofthetaskswhichweevaluateSELF-REFINEon,alongwiththeirassociated
datasetsandsizes. Foreverytask,wedemonstrateasingleiterationofrefinementofinputx,the
previously generated output y , the feedback generated fb , and the refinement y . Few-shot
t t t+1
promptsusedforFEEDBACKandREFINEareprovidedinAppendixS.
14
