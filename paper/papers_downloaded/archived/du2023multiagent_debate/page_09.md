Question: Carla is downloading a 200 GB file. Normally she can download 2 GB/minute, but 40% of the way through
the download, Windows forces a restart to install updates, which takes 20 minutes. Then Carla has torestart the
download from the beginning. How load does it take to download the file?
Round 1
ChatGPT: Before the restart, Carla was able to download Bard: Carla is downloading a 200 GB file at a speed
40% of the file, which is 0.4 * 200 GB = 80 GB. At a rate of 2 GB/minute. This means that it will take her 200 /
of 2 GB/minute, it would take her: time = 80 GB ÷2 2 = 100 minutes to download the file.
GB/minute = 40 minutes.
However, Windows forces a restart to install updates,
Because of the restart, Carla had to start over. This means which takes 20 minutes. This means that Carla will
she had to download the entire 200 GB file. The time it have to restart the download from the beginning.
takes to download the remaining 120 GB is: time = 120 GB Since Carla has already downloaded 40% of the file,
÷2 GB/minute = 60 minutes. she only needs to download 200 -40 = 160 GB. At a
speed of 2 GB/minute, it will take Carla 160 / 2 = 80
But Carla also had to wait 20 minutes for the Windows minutes to download the file.
update to install, so the total time it took to download the
file is: total time = 40 minutes + 60 minutes + 20 minutes = Adding the time for the Windows restart, it will take
120 minutes. ✗ Carla 80 + 20 = 100 minutesto download the file. ✗
Round 2
ChatGPT: Based on the calculations provided by the other agent, the correct answer is: Before the restart, Carla was
able to download 40% of the file, which is 0.4 * 200 GB = 80 GB. At a rate of 2 GB/minute, it would take her: time =
80 GB ÷2 GB/minute = 40 minutes
However, because of the restart, Carla had to start over. This means she had to download the entire 200 GB file. The
time it takes to download the entire 200 GB file is: time = 200 GB ÷2 GB/minute = 100 minutes
And since Carla had to wait 20 minutes for the Windows update to install, the total time it took to download the file is:
total time = 40 minutes + 100 minutes + 20 minutes = 160 minutes. ✓
Figure11:DebateBetweenchatGPTandBardIllustrationofdebatebetweendifferentmodels.
theimpactofusingtwodifferentlanguagemodels,whereweaskchatGPTandBard [23]language
modelstodebatewitheachotheronasetof20GSM8Kmathproblems. Inthisset,wefindthat
multi-agentdebateimprovestheperformanceofbothagents,withBardsolving11problems,chatGPT
solving14problems,andjointmulti-agentdebatesolving17problems. Wequalitativelyillustrate
adebatebetweenagentsinFigure11. Whilebothagentsinitiallyprovideincorrectanswerstothe
problem,chatGPTisabletoutilizetheincorrectresponsegivenbyBardtogeneratethefinalcorrect
answer.
4 RelatedWork
Reasoning and Factuality in Language Models. A wide range of work has explored how to
enablereasoningandfactualityinlanguagemodels. Toimprovereasoning,approacheshavereliedon
promptingtechniquessuchasscratchpads [20],verification [3],chain-of-thoughtdemonstrations [30,
11,25],andintermediateself-reflection [26,18]andfinetuning[13,24,31]. Toimprovefactuality,
approacheshavereliedontrainingtechniquessuchasRLHF [33,16,2],pruningtruthfuldatasets[12],
externalknowledgeretrieval[7]andtraining-freemethodsbasedofflikelihoodestimation [10].
Ourworkprovidesanalternativewaytoobtainreasoningandfactualityinlanguagemodelsusing
multiagentdebates,whichonlyrequiresblack-boxaccesstoalanguagegenerator. Priorworkalso
hasexploredhowtotakethemajorityvoteacrossdifferentmodels [15,3,29,28]whileinthiswork,
weusethepowerofalanguagemodeltocombinedifferentanswers. Mostsimilartoourwork,Irving
etal.[9]alsoproposesadebateproceduretoverifytheaccuracyandsafetyofpowerfulAIagents. In
contrasttoourapproach,intheirwork,agentsareaskedtoalternativelyprovideproofofainput,and
humansaretaskedwithassessingthesedebatesanddeterminingsafety.
CompositionalGeneration. Ourworkisalsorelatedtoexistingworksthatfocusontextgeneration
bycombiningdifferentmodels [4,17,32,1,5].Mostsimilartoourwork,[14,32]proposetocombine
multipledifferentlargepretrainedmodelstogetherformultimodalreasoning. Incontrast,inourwork,
weaimtousecommunicationbetweendifferentlanguagemodelstoenablemoreeffectivereasoning
andfactualityinlanguagemodels.
9
