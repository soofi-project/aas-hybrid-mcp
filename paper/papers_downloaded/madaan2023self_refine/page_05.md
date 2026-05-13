GPT-3.5 ChatGPT GPT-4
Task Base +SELF-REFINE Base +SELF-REFINE Base +SELF-REFINE
SentimentReversal 8.8 30.4(↑21.6) 11.4 43.2(↑31.8) 3.8 36.2(↑32.4)
DialogueResponse 36.4 63.6(↑27.2) 40.1 59.9(↑19.8) 25.4 74.6(↑49.2)
CodeOptimization 14.8 23.0(↑8.2) 23.9 27.5(↑3.6) 27.3 36.0(↑8.7)
CodeReadability 37.4 51.3(↑13.9) 27.7 63.1(↑35.4) 27.4 56.2(↑28.8)
MathReasoning 64.1 64.1(0) 74.8 75.0(↑0.2) 92.9 93.1(↑0.2)
AcronymGeneration 41.6 56.4(↑14.8) 27.2 37.2(↑10.0) 30.4 56.0(↑25.6)
ConstrainedGeneration 28.0 37.0(↑9.0) 44.0 67.0(↑23.0) 15.0 45.0(↑30.0)
Table1: SELF-REFINEresultsonvarioustasksusingGPT-3.5,ChatGPT,andGPT-4asbaseLLM.
SELF-REFINEconsistentlyimprovesLLM.MetricsusedforthesetasksaredefinedinSection3.2.
available(suchasforCodeOptimizationandMathReasoning);otherwise,wecreatedpromptsas
detailedinAppendixS.Weusegreedydecodingwithatemperatureof0.7forallsetups.
3.2 Metrics
Wereportthreetypesofmetrics:
• Taskspecificmetric:Whenavailable,weuseautomatedmetricsfrompriorwork(MathReasoning:
%solverate;CodeOptimization: %programsoptimized;ConstrainedGen: coverage%)
• Human-pref: In Dialogue Response Generation, Code Readability Improvement, Sentiment
Reversal,andAcronymGeneration,sincenoautomatedmetricsareavailable,weperformablind
humanA/Bevaluationonasubsetoftheoutputstoselectthepreferredoutput. Additionaldetails
areprovidedinAppendixC.
• GPT-4-pref:Inadditiontohuman-pref,weuseGPT-4asaproxyforhumanpreferencefollowing
priorwork(Fuetal.,2023;Chiangetal.,2023;Gengetal.,2023;Sunetal.,2023),andfoundhigh
correlation(82%forSentimentReversal,68%forAcronymGeneration,and71%forDialogue
ResponseGeneration)withhuman-pref. ForCodeReadabilityImprovement,wepromptGPT-
4 to calculate fraction of the variables that are appropriately named given the context (e.g.,
x = []→input_buffer = []). AdditionaldetailsareprovidedinAppendixD.
3.3 Results
Table1showsourmainresults:
SELF-REFINEconsistentlyimprovesoverbasemodelsacrossallmodelsizes,andadditionally
outperforms the previous state-of-the-art across all tasks. For example, GPT-4+SELF-REFINE
improvesoverthebaseGPT-4by8.7%(absolute)inCodeOptimization,increasingoptimization
percentagefrom27.3%to36.0%. ConfidenceintervalsareprovidedinAppendixJ.Forcode-based
tasks,wefoundsimilartrendswhenusingCODEX;thoseresultsareincludedinAppendixF.
OneofthetasksinwhichweobservethehighestgainscomparedtothebasemodelsisConstrained
Generation,wherethemodelisaskedtogenerateasentencecontainingupto30givenconcepts. We
believethatthistaskbenefitssignificantlyfromSELF-REFINEbecausetherearemoreopportunities
tomisssomeoftheconceptsonthefirstattempt,andthus SELF-REFINE allowsthemodeltofix
thesemistakessubsequently. Further,thistaskhasanextremelylargenumberofreasonableoutputs,
andthusSELF-REFINEallowstobetterexplorethespaceofpossibleoutputs.
Inpreference-basedtaskssuchasDialogueResponseGeneration,SentimentReversal,andAcronym
Generation, SELF-REFINE leads to especially high gains. For example in Dialogue Response
Generation,GPT-4preferencescoreimproveby49.2%–from25.4%to74.6%. Similarly,wesee
remarkableimprovementsintheotherpreference-basedtasksacrossallmodels.
ThemodestperformancegainsinMathReasoningcanbetracedbacktotheinabilitytoaccurately
identifywhetherthereisanyerror. Inmath,errorscanbenuancedandsometimeslimitedtoasingle
line or incorrect operation. Besides, a consistent-looking reasoning chain can deceive LLMs to
5
