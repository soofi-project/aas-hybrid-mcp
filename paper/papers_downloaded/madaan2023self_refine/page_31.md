StartingCode: v
0
print((int((int(eval(input()))+1)/2)))
Codev
1
print(
(int(
(int(eval(input())) + 1)
/ 2
)
)
Codev
2
num_input = eval(input())
num_input = int(num_input)
num_input += 1
num_result = int(num_input / 2)
print(num_result)
Figure 12: SELF-REFINE iterations over a piece of densely composed code. Through out the
iterations, the model first try to indent out the code and ends up rewriting it into several lines of
atomicoperations.
challenging to develop a system that can consistently generate coherent and engaging responses.
Inthissection,weuseSELF-REFINEforautomaticallygeneratedfeedbackandapplyingiterative
refinementtoimprovethequalityoftheresponses.
M.1 Modules
Wefollowthehigh-leveldescriptionoftheframeworkfromSection2,andinstantiateourframework
asfollows.
Init Thisisthefirststepinperformingthetask. Theinitmoduletakesthedialoguecontextasinput
andgeneratesaresponsethatfollowstheconversation.
Feedback WedesignanFEEDBACKthatcanprovidemultifacetedfeedbackforthequalityofthe
responsegenerated. Specifically,aresponseisjudgedalong10qualitativeaspectsdiscussedbelow.
Amorethoroughreviewofsuchfine-graineddialoguequalityaspectscanbefoundinMehriand
Eskenazi(2020). Weuse6in-contextexamplesforfeedbackgeneration. Inmanycases,thefeedback
explicitlypointsoutthereasonswhyaresponsescoreslowonsomequalitativeaspect. Weshowan
exampleinFigure13.
• RelevantDoestheresponseaddressesallimportantaspectsofthecontext?
• Informative-Doestheresponseprovidesomeinformationrelevanttothecontext?
• Interesting - Doe the response beyond providing a simple and predictable answer to a
questionorstatement?
• Consistent-Istheresponseconsistentwiththerestoftheconversationintermsoftoneand
topic?
• Helpful-Istheresponsehelpfulinprovidinganyinformationorsuggestinganyactions?
• Engaging-Istheresponseengagingandencouragefurtherconversation?
• Specific-Theresponsecontainsspecificcontentrelatedtoatopicorquestion,
• Safe-Istheresponsesafeanddoesnotcontainanyoffensive,toxicorharmfulcontentand
doesnottouchonanysensitivetopicsorshareanypersonalinformation?
• Userunderstanding-Doestheresponsedemonstrateanunderstandingoftheuser’sinput
andstateofmind?
• FluentIstheresponsefluentandeasytounderstand?
31
