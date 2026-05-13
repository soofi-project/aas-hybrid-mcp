J StatisticalConfidenceIntervals
GPT-3.5 ChatGPT GPT-4
Task Base +SELF-REFINE Base +SELF-REFINE Base +SELF-REFINE
SentimentReversal 8.8±2.05 30.4±3.61∗ 11.4±2.34 43.2±3.98∗ 3.8±1.28 36.2±3.82∗
DialogueResponse 36.4±6.14 63.6±6.62∗ 40.1±6.33 59.9±6.67∗ 25.4±5.36 74.6±6.22∗
CodeOptimization 14.8±2.66 23.0±3.25∗ 23.9±3.30 27.5±3.49 27.3±3.48 36.0±3.81∗
CodeReadability 37.4±6.86 51.3±7.39 27.7±6.13 63.1±7.40∗ 27.4±6.10 56.2±7.45∗
MathReasoning 64.1±3.47 64.1±3.47 74.8±3.20 75.0±3.20 92.9±2.05 93.1±2.03
AcronymGen. 41.6±7.72 56.4±8.15 27.2±6.60 37.2±7.46 30.4±6.92 56.0±8.15∗
ConstrainedGen. 28.0±7.38 37.0±8.26 44.0±8.72 67.0±9.00∗ 15.0±5.38 45.0±8.77∗
Table13: SELF-REFINEresultsfromtable1withWilsonconfidenceinterval(at95%confidence
interval) and statistical significance. On various tasks using GPT-3.5, ChatGPT, and GPT-4 as
baseLLM,SELF-REFINEconsistentlyimprovesLLM.Metricsusedforthesetasksaredefinedin
Section3.2asfollows: MathReasoningusesthesolverate;CodeOptimizationusesthepercentage
ofprogramsoptimized;andSentimentReversal,DialogueResponseandAcronymGenuseaGPT-
4-basedpreferenceevaluation, whichmeasuresthepercentageoftimesoutputsfromthebaseor
enhancedmodelswereselected,withtherestcategorizedasatie. ConstrainedGenusesthecoverage
percentage. GainsoverBase,thatarestatisticallysignificantbasedontheseconfidenceintervalsare
marked*
Table13showsresultsfromTable1withWilsonconfidenceinterval(Brownetal.,2001)(atα=
99%confidenceinterval)andstatisticalsignificance. Gainsthatarestatisticalsignificancebasedon
theseconfidenceintervalsaremarkedwithanasterisk. WefindthatnearlyallofGPT-4gainsare
statisticallysignificant,ChatGPTgainsaresignificantfor4outof7datasets,andGPT-3.5gainsare
significantfor3outof7datasets.
28
