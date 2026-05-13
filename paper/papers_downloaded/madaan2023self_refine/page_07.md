11.3
C.Opt.
10 C.Gen.
Task y0 y1 y2 y3
6.4 S.Rev.
5
CodeOpt. 22.0 27.0 27.9 28.8 5
3
SentimentRev. 33.9 34.9 36.1 36.8
ConstrainedGen. 29.0 40.3 46.7 49.7 1 0.9 1.2 0.9 0.7
0
∆(y →y ) ∆(y →y ) ∆(y →y )
0 1 1 2 2 3
Figure4: Left: Iteration-wisescoreimprovements. Earlyiterationssignificantlyimproveoutput
quality,andscoresgenerallykeepimprovingwithmoreiterations.Right: SELF-REFINEPerformance
improvementswithiterations. Mostgains(∆)areintheinitialiterationsforbothCodeOpt. andSenti-
mentReversal. ThenumbersareaveragedoverChatGPT,GPT-3.5,andGPT-4. Taskabbreviations:
C.Opt. (CodeOptimiz.),S.Rev. (SentimentReversal),C.Gen. (ConstrainedGeneration).
# Slower code
def solve(amount):
# Faster code
best_price = (amount + 199) // 200 *
def solve(amount):
380
(cid:44)→ coins = [200, 300]
# First loop
prices = [380, 550]
for a in range(amount // 200 + 1):
dp = [float('inf')] * (amount + 1)
# ... 4 nested loops ...
dp[0] = 0
for c1 in range(amount // 1500 +
for i in range(len(coins)):
1):
(cid:44)→ for j in range(coins[i], amount+1):
if a*200 + b*300 == amount:
dp[j] = min(dp[j], dp[j -
price = a*380 + b*550
coins[i]] + prices[i])
if price < best_price: (cid:44)→
return dp[amount]
best_price = price
return best_price
Figure5: ComparisonofcodegeneratedbyMadaanetal.(2023)(left)andtheoutputafterapplying
SELF-REFINE(right). Theinitialcodebythebaseline,whichisnearlyidenticaltotheslowerinput
program,failstoimprovetheefficiencyandmerelyaltersthelogicforreadinginput. SELF-REFINE
firstgeneratesfeedbackthatdiagnoses thatThiscodeisslowbecauseitisusingsixnestedloopsto
iteratethroughallpossiblecombinationsofcoinstopaytheamount,andsuggeststhatamoreefficient
approachwouldbe.... SELF-REFINEthenusesthisfeedbacktogeneratetherevisedcode(right),
reducingthetimecomplexitytoO(amount∗coins). ThefullexampleisprovidedinAppendixH
Canwejustgeneratemultipleoutputsinsteadofrefining? DoesSELF-REFINEimprovebecause
oftheiterativerefinement,orjustbecauseitgeneratesmoreoutputs? WecompareSELF-REFINEwith
ChatGPT,whenChatGPTgeneratesk =4samples(butwithoutfeedbackandrefinement). Then,
wecomparetheperformanceofSELF-REFINEagainstthesekinitialoutputsina1vs. kevaluation.
Inotherwords,weassesswhetherSELF-REFINEcanoutperformallkinitialoutputs. Theresults
ofthisexperimentareillustratedinFigure6(AppendixH).Despitetheincreaseddifficultyofthe
1vs. ksetting,theoutputsofSELF-REFINEarestillpreferredbyhumansoverallkinitialoutputs.
Thisshowstheimportanceofrefinementaccordingtofeedbackoverthealternativeofjustgenerating
multipleinitialoutputs.
DoesSELF-REFINEworkwithweakermodels? TheexperimentsinSection3.3wereperformed
withsomeofthestrongestavailablemodels;doesSELF-REFINEworkwithsmallerorweakermodels
aswell? Toinvestigatethis,weinstantiatedSELF-REFINEwithVicuna-13B(Chiangetal.,2023),a
7
 |  | 1.3 |  |  |  |  |  | C. | Opt. | 
 |  |  |  |  |  |  |  |  |  | 
 |  |  | 6. |  |  | C.
4 S. |  | C.
S. | Gen.
Rev. | 
 |  |  |  |  |  |  |  |  |  | 
 |  |  | 1 0.9 |  |  |  | 3
1.2 0.9 |  | 0.7 | 
 |  |  |  |  |  |  |  |  |  | 
 |  |  |  |  |  |  |  |  |  | 
 |  |  |  |  |  |  |  |  |  | 

 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | This | code | is | slow |  | be | causei | tis | us | ing | sixn | ested | loopst |  |  | o
i | ter | ate | through |  | all | pos |  | si | ble | com | bi | na | tions | of | coinst |  | opay | the |  | amount, |  |  |  |  |  |  | more | ef | fi | cient | 
ap |  | proach |  | would |  | be | .. |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | 

