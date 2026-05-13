50
40
35
32
30
20
10
10
5
3
0
0
C o n c e
pt
o ns e ns
e
O v er
all
m
m
o
C
oitaRgninniW
Direct
SELF-REFINE
Figure15: AcomparisonofSELF-REFINEanddirectgenerationwithGPT-3.5onCommonGen-
Hard.
andviceversa. Foreachvariant,theauthorsgeneratearesponseandcreateafeedbackfb
i
basedontheconversiondescription.
• DialogueResponseGenerationWesamplesixexamplesas⟨x ,y ⟩forthefew-shotprompt
i i
fortheBaseLLM.Foreachoutputy ,theauthorscreatearesponse,evaluateitbasedona
i
rubrictogeneratefb ,andproduceanimprovedversiony .
i i+1
• AcronymGenerationWeprovidetheBaseLLMwithatotalof15(title,acronym)examples.
Then,foronetitle(x )wegenerateanacronym(y )usingChatGPT.Theauthorsthenscore
i i
theacronymsbasedona5-pointrubrictocreatethecorrespondingfb ,andwriteimproved
i
versionsoftheacronymtocreatey
i+1
.3suchexamplesareusedforREFINEandFEEDBACK.
• CodeOptimizationWeusetheslow(x )andfast(y )versionsofprogramsreleasedby
i i
Madaanetal.(2023)forBaseLLM.Weusetheirprovidedexplanations(Madaanetal.,
2023)forFEEDBACKandREFINE.
• MathReasoningThepromptsfortheBaseLLMaresourcedfromPaL(Gaoetal.,2022)as
⟨x
i
,y
i
⟩.WeselecttwoexamplesfromthetrainingsetonwhichCODEXfailswhenprompted
withPaL-styledprompts,andmanuallywritethecorrectsolution(y )andreasoning(fb )
i+1 i
forREFINEandFEEDBACK.
• Constrained Generation We provide ten examples to the Base LLM as ⟨x ,y ⟩. We
i i
samplesixexamplesfromthetrainingsetofConstrainedGenerationandcreatevariants
with missing concepts or incoherent outputs. The missing concepts and the reason for
incoherenceformfb.
• TODO:Addrelevantinformationfortheremainingtask.
38
Direct
SELF-REFINE |  |  |  |  |  |  |  | 
35
32 |  |  |  |  |  |  |  | 
 |  |  |  |  |  |  |  | 
 |  |  |  |  |  |  |  | 
 |  |  |  |  |  |  |  | 
 |  |  | 10 |  |  |  |  | 
3 |  |  | 5 |  |  | 0 |  | 
 |  |  |  |  |  |  |  | 
 |  |  |  |  |  |  |  | 

