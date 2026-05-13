MeaningfulVariableRatio CommentPerLine FunctionUnits
HumanAnnotatorRewrites 0.653 0.24 0.70
SELF-REFINE(T=0.0) 0.628 0.12 1.41
SELF-REFINE(T=0.7) 0.700 0.25 1.33
Table14: Humanv.s. SELF-REFINEperformanceon60-examplesubset. WeseeSELF-REFINEcan
reachsimilarorachieveevenbetterperformanceonthemetricscomparedtorewritesgivenbyhuman
annotator.
EvaluationMethods Weconsiderafewautomaticheuristic-basedevaluationmetrics,
• MeaningfulVariableNames: Inordertounderstandtheflowofaprogram,havingsemanti-
callymeaningfulvariablenamescanoffermuchusefulinformation. Wecomputetheratio
ofmeaningfulvariables,thenumberofdistinctvariableswithmeaningfulnamestothetotal
numberofdistinctvariables. Weautomatetheprocessofextractingdistinctvariablesand
themeaningfulsubsetofvariablesusingafew-shotpromptedlanguagemodel.
• Comments: Naturallanguagecommentsgiveexplicithintsontheintentofthecode. We
computetheaveragenumberofcommentpiecespercodeline.
• FunctionUnits: Longfunctionsarehardtoparse. Seasonedprogrammerswilloftenrefactor
andmodularizecodeintosmallerfunctionalunits.
Result Foreachautomaticevaluationmetric,theratioofmeaningfulvariable,ofcomment,and
thenumberoffunctionunits,wecomputeforeachiterationaveragedacrossalltestexamplesand
plotforeach SELF-REFINE iterationinFigure11(a), Figure11(b)andFigure11(c)respectively.
ThetwocurveseachcorrespondtocritiquewithtemperatureT =0.0andT =0.7. Theiteration0
numberismeasuredfromtheoriginalinputcodepiecefromCodeNet. Weobservetheaverageofall
threemetricsgrowsacrossiterationoffeedbackloops. Adiversegenerationofahighertemperature
in the critique leads to more edits to improve the meaningfulness of variable names and to add
comments. Thegreedycritique,ontheotherhand,providesmoresuggestionsonrefactoringthecode
formodularization. Figure12providesanexampleofcode-readabilityimprovingoveriterations.
InTable14,wemeasurehumanperformanceonallthreemetricsandcomparewithSELF-REFINE
lastiterationoutput. AtT =0.7,SELF-REFINEproducesmoremeaningvariables,morefunction
units and slightly more comments compared to the human annotators on average. At T = 0.0,
SELF-REFINEproduceslessmeaningfulvariables,lesscommentsperlinebutevenmorefunction
units.
0.8
0.6
0.4
0.2
0
0 1 2 3 4 5
Iteration
y
0.3
T=0.0
T=0.7
0.2
0.1
0
0 1 2 3 4 5
Iteration
(a)Meaningfulvariableratioacross
differentSELF-REFINEiterations.
y
T=0.0 4
T=0.7
3
2
1
0
0 1 2 3 4 5
Iteration
(b) Comment per line ratio across
differentSELF-REFINEiterations.
y
T=0.0
T=0.7
(c)Numberoffunctionunitsacross
differentSELF-REFINEiterations.
Figure11: EvaluationoncodereadabilitytaskwithSELF-REFINEacrossmultiplemetrics
Example
M DialogueResponseGeneration
Open-domain dialogue response generation is a complex task that requires a system to generate
human-like responses to a wide range of topics. Due to the open-ended nature of the task, it is
30
MeaningfulVariableRatio | CommentPerLine
0.653
0.628
0.700 | 0.24
0.12
0.25

