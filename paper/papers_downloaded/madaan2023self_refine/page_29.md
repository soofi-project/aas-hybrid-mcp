K NewTasks
ConstrainedGeneration Weintroduce“CommonGen-Hard,"amorechallengingextensionofthe
CommonGendataset(Linetal.,2020),designedtoteststate-of-the-artlanguagemodels’advanced
commonsensereasoning,contextualunderstanding,andcreativeproblem-solving. CommonGen-
Hardrequiresmodelstogeneratecoherentsentencesincorporating20-30concepts,ratherthanonly
the3-5relatedconceptsgiveninCommonGen. SELF-REFINE focusesoniterativecreationwith
introspectivefeedback,makingitsuitableforevaluatingtheeffectivenessoflanguagemodelsonthe
CommonGen-Hardtask.
Acronym Generation Acronym generation requires an iterative refinement process to create
conciseandmemorablerepresentationsofcomplextermsorphrases,involvingtradeoffsbetween
length,easeofpronunciation,andrelevance,andthusservesasanaturaltestbedforourapproach.
Wesourceadatasetof250acronyms4andmanuallypruneittoremoveoffensiveoruninformative
acronyms.
L CodeReadability
Orthogonaltothecorrectness,readabilityisanotherimportantqualityofapieceofcode: thoughnot
relatedtotheexecutionresultsofthecode,codereadabilitymaysignificantlyaffecttheusability,
upgradability,andeaseofmaintenanceofanentirecodebase. Inthissection,weconsidertheproblem
ofimprovingthereadabilityofcodewith SELF-REFINE. Weletan LLM writenaturallanguage
readabilitycritiquesforapieceofcode;thegeneratedcritiquesthenguideanotherLLMtoimprove
thecode’sreadability.
L.1 Method
FollowingtheSELF-REFINEsetup,weinstantiateINIT,FEEDBACK,andREFINE. TheINITisano-op
—wedirectlystartbycritiquingthecodewithFEEDBACKandapplyingthechangeswithREFINE.
• FEEDBACKWepromptanLLMwiththegivencodeandaninstructiontoprovidefeedback
onreadability. WegivetheLLMthefreedomtofreelychoosethetypeofenhancements
andexpressthemintheformoffreetext.
• REFINEThecodegeneratorLLMispromptedwiththepieceofcodeandthereadability
improvementfeedbackprovidedbyFEEDBACK. Inaddition,wealsosupplyaninstruction
tofixthecodeusingthefeedback. Wetakethegenerationfromthecodegeneratorasthe
productofoneiterationinthefeedbackloop.
Starting from an initial piece of code y , we first critique, c = critique(y ), and then edit the
0 1 0
code,y = editor(y ,c ). ThisisrecursivelyperformedN times,wherec = critique(y )and
1 0 1 k+1 k
y =editor(y ,c ).
k+1 k k+1
L.2 Experiments
Dataset Weuse theCodeNet (Puriet al.,2021) datasetof competitiveprogramming.5 For our
purpose, these are hard-to-read multi-line code snippets. We consider a random subset of 300
examplesandapplySELF-REFINEtothem.
Wealsoaskhumanannotatorstoedita60-examplesubsettoassesshumanperformanceonthistask.
Thehumanannotatorsareaskedtoreadthecodepieceandimproveitsreadability.
Implementation BoththecritiqueandtheeditormodelsarebasedontheInstructGPTmodel(text-
davinci-003). We consider the temperature of both T = 0.0 (greedy) and T = 0.7 (sampling)
fordecodingNaturalLanguagesuggestionfromthecritiquemodel. Wealwaysuseatemperature
T = 0.0 (greedy) when decoding Programming Language from the code editor. Due to budget
constraints,werunSELF-REFINEforN =5iterations. Theexactpromptsweusecanbefoundin
Figures22-23.
4
https://github.com/krishnakt031990/Crawl-Wiki-For-Acronyms/blob/master/AcronymsFile.csv
5https://github.com/IBM/Project_CodeNet
29
