otheronthesamenumberoftasks. Forillustrationpurposes,weprovideacaseanalysisinTable7
onfourtypicaltasks.
Additionally,wealsoexploredthefeasibilityofusingAuto-GPTforhandlingthesametasks. Auto-
GPT faces challenges in handling tasks that involve complex rules due to its limited extensibility.
Itprovidesaninterfaceforsettingtaskgoalsusingnaturallanguage. However,whendealingwith
the MiniWob++ benchmark, accurately instructing Auto-GPT to follow the instructions for using
MiniWob++proveschallenging. Thereisnoclearpathtoextenditinthemannerofthetwo-agent
chatfacilitatedbyAutoGen.
Takeaways: Forthisapplication,AutoGenstoodoutasamoreuser-friendlyoption,offeringmod-
ularityandprogrammability:Itstreamlinedtheprocesswithautonomousconversationsbetweenthe
assistantandexecutor,andprovidedreadilyavailablesolutionsforagent-environmentinteractions.
Thebuilt-inAssistantAgentwasdirectlyreusableandexhibitedstrongperformancewithoutcus-
tomization.Moreover,thedecouplingoftheexecutionandassistantagentensuresthatmodifications
toonecomponentdonotadverselyimpacttheother. Thisconveniencesimplifiesmaintenanceand
futureupdates.
1.0
0.5
0.0
click-b c u l t c i t c h o k o n c - c o c l - i l s s h c ic e e c k e k q l - - c i l - c u c i k c s h k e b h t e - n o e b c c x c u k e e k t b s b t c o o - o l l x n i a x c e c r e k l s g i s - - c e c - t k s r h - a o e c c n f c o t l s i k l c f l b a e k o p - r c x s o e ib l s l l a e c c p l - l i 2 s i c c i k b k - - l c e d c o i l a i l c o l k o r - g d - c i 2 a l c i l c l o i k c g c - k c l l i - i l n c m ic k k k e -o - n s c p u c l t i r c i o o k c l n - c l l - i s l c l i h i c k s a k t -t d - a s e b h s - a c 2 p li - c e h k a - r t m c d a c li b a l c i i - c k l 2 - k - i t n - a t c b e e c b l o m i l s c i x t c k - a c - k 2 - f o i - t o l w - u e r in s n w i e d t b t m a g - o s r e a x d h t i - - a l f n - o p i l n r - e t w b u o a r x e k rd - m n -n l e a e - l t n i n e u l- t t n r i e e n k t r r e b - - t p r o e - a x d x s a t s - t d w e y o e n r n a d t m e e n r i f - c t o t e e c r u x - g t t s i r m - f l i t o o d e e g c - x c u i t n o s - - o 2 - u t r e s d x e in t r- a n l p o t a o e g v p s in i e u g - a p a s u r i t s c m e e h s s - p r o - t o e r l c c e e n i i - a e a g a l l i - l - n g m m e e e e b d d s r i a o i a a c - - a i s a l o l l- m m t u e e e s d r e m ia -s in p a in l ner
e
etar
sseccus
RCI MiniWobChat
Figure18: ComparisonsbetweenRCI(state-of-the-artpriorwork)andMiniWobChatontheMini-
Wob++ benchmark are elucidated herein. We utilize all available tasks in the official RCI code,
eachwithvaryingdegreesofdifficulty,toconductcomprehensivecomparisons. Foreachtask,the
successrateacrosstendifferentinstancesisreported. TheresultsrevealthatMiniWobChatattainsa
performancecomparabletothatofRCI.Whenasuccessratetoleranceof0.1isconsideredforeach
task,bothmethodsoutperformeachotheronanequalnumberoftasks.
Table7: CasesanalysisonfourtypicaltasksfromMiniWob++.
Correctness Mainfailurereason
AutoGen:10/10 N/A.
click-dialog
RCI:10/10 N/A.
AutoGen:5/10 AssistantAgentprovidesactionswithinfeasible
click-checkboxes-large
characters.
RCI:0/10 RCIperformsactionsthatareoutofitsplan.
AutoGen:2/10 AssistantAgentprovideactionswithredundantcontent
count-shape
thatcannotconverttoactionsinthebenchmark.
RCI:0/10 RCIprovidesawrongplaninmostcases.
AutoGen:0/10 AssistantAgentreturnactionsoutofitsplan.
use-spinner
RCI:1/10 RCIprovidesawrongplaninmostcases.
33
Correctness
toGen:10/10
RCI:10/10
toGen:5/10
RCI:0/10
toGen:2/10
RCI:0/10
toGen:0/10
RCI:1/10

