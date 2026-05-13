SELF-REFINE 3377..22 3355..66 2277..22 ChatGPT
SELF-REFINE 3333..33 5511..11 1155..55 MULTI
0 10 20 30 40 50 60 70 80 90 100
PreferenceratesforSentimentReversal
SELF-REFINE 4433..22 4455..44 1111..44 ChatGPT
SELF-REFINE 4400..0055 5533..8822 66..11 MULTI
0 10 20 30 40 50 60 70 80 90 100
PreferenceratesforAcronymGeneration
Figure6: Preferencefortheoutputsgeneratedbyourmethod(SELF-REFINE),themultiple-sample
baseline(MULTI),andties(ties).
GPT-3.5 ChatGPT GPT-4
Task Base +SELF-REFINE Base +SELF-REFINE Base +SELF-REFINE
MathReasoning 64.1 64.1(0) 74.8 75.0(↑0.2) 92.9 93.1(↑0.2)
MathReasoning(Oracle) 64.06 68.9(↑4.8) 74.8 76.2(↑1.4) 92.9 93.8(↑0.7)
Table9: SELF-REFINEresultsonMathReasoningusingGPT-3.5,ChatGPT,andGPT-4asbase
LLMwithOraclefeedback.
H AdditionalAnalysis
H.1 UsingOracleFeedback
WeexperimentedwithOracleFeedbackfollowingWellecketal.(2022).Thismethodusescorrectness
informationtoguidemodelrefinement,onlyprogressingtoREFINEstageifthecurrentansweris
incorrect. ThisadjustmentnotablyenhancedperformanceintheMathReasoningtask,withGPT-3
improvingby4.8%andGPT-4by0.7%Table9. Thisindicatesthepotentialofexternalsignalsto
optimizemodelperformanceinparticulartasks.
Iteration Acronym Pronunciation Pron. (5) Spell. (5) Rel. (5) Pos. Con. (5) Total(25)
1 USTACCSF us-tacks-eff 1 1 5 3 11
2 TACC-SIM tacks-sim 4 4 5 3 17
3 TACCSF tacks-eff 1 2 5 3 12
4 TACC-SIMF tack-simf 4 4 5 3 17
Table10: Acronymgenerationresultsacrossiterations,showcasinghowimprovementsincertainas-
pects(e.g.,pronunciationandspelling)canbeaccompaniedbylossesinothers,leadingtofluctuating
overallperformanceinmulti-aspectfeedbacktaskslikeAcronymGeneration.
Non-monotonicincreaseinoutputqualityforacronymgeneration Fortaskswithmulti-aspect
feedback like Acronym Generation, the output quality can fluctuate during the iterative process,
improvingononeaspectwhilelosingoutonanother(Table10). Toaddressthis,SELF-REFINE’s
feedbackgeneratesexplicitnumericalscorestocapturethedifferentaspectsofoutputquality. This
allowsforamorebalancedevaluationofoutputsandtheselectionofthemostappropriateone. The
algorithm selects the best output based on the maximum score across all iterations, as described
in Algorithm 1 (line 8). A similar selection is possible for other tasks like Math Reasoning and
SentimentReversal,whileweobservethatoutputqualityincreasesmonotonicallywithiterations.
22
 |  |  |  | 
3377..22 |  | 3355..66 | 2277..22 | 
 |  |  |  | 
3333..33 | 5511..11 |  |  | 1155..55
 |  |  |  | 

 |  |  |  | 
4433..22 |  | 4455..44 | 1111..44 | 
 |  |  |  | 
4400..0055 | 5533..8822 |  |  | 66..11
 |  |  |  | 

