B BroaderRelatedWork
Comparedtoaconcurrentwork,Reflexion(Shinnetal.,2023),ourapproachinvolvescorrection
usingfeedback,whereastheirsetupinvolvesfindingthenextbestsolutioninplanningusingReAct.
WhileReActandReflexionprovideafree-formreflectiononwhetherastepwasexecutedcorrectly
andpotentialimprovements,ourapproachismoregranularandstructured,withmulti-dimensional
feedbackandscores.Thisdistinctionallowsourmethodtooffermorepreciseandactionablefeedback,
makingitsuitableforawiderrangeofnaturallanguagegenerationtasks,includingthosethatmay
notnecessarilyinvolvestep-by-stepplanningsuchasopen-endeddialoguegeneration.
ComparisonwithWellecketal.(2022) TheclosestworktooursmaybeSelf-Correction(Welleck
etal.,2022);however,Self-CorrectionhasseveraldisadvantagescomparedtoSELF-REFINE:
1. Self-Correctiondoesnottraintheirmodeltogenerateexplicitfeedback;instead,Welleck
etal.(2022)trainedtheirmodelstorefineonly. AsweshowinSection4andTable2,having
themodelgenerateexplicitfeedbackresultsinsignificantlybetterrefinedoutputs.
2. Self-Correctiontrainsaseparaterefiner(or“corrector”)foreachtask. Incontrast,SELF-
REFINE uses instructions and few-shot prompting, and thus does not require training a
separaterefinerforeachtask.
3. Empirically, we evaluated SELF-REFINE using the same base model of GPT-3 as Self-
Correction,andwiththesamesettingsontheGSM8Kbenchmark. Self-Correctionachieved
45.9%accuracywhileSELF-REFINE(thiswork)achieved55.7%(↑9.8).
Comparisonwithnon-refinementreinforcementlearning(RL)approaches. Ratherthanhaving
anexplicitrefinementmodule,analternativewaytoincorporatefeedbackisbyoptimizingascalar
rewardfunction,e.g. withreinforcementlearning(e.g.,Stiennonetal.(2020);Luetal.(2022);Le
etal.(2022a)). Thesemethodsdifferfrom SELF-REFINE (andmoregenerally, refinement-based
approaches)inthatthemodelcannotaccessfeedbackonanintermediategeneration. Second,these
reinforcementlearningmethodsrequireupdatingthemodel’sparameters,unlikeSELF-REFINE.
SeeTable5foranadditionaldetailedcomparisonofrelatedwork.
Method PrimaryNovelty zero/fewshotimprovement multiaspectcritics NLfeedbackwither- iterativeframework
rorlocalization
RLHF(Stiennonetal.,2020) optimizeforhumanpreference trainedonfeedback single(human) (notselfgen.)
RainierRL(Liuetal.,2022) RLtogenerateknowledge trainedonendtask single(accuracy) (knowl.only)
QUARKRL(Luetal.,2022) quantizationtoeditgenerations trainedonendtask single(scalarscore) (densesignal) (traintimeiter.)
CodeRL(Leetal.,2022a) actorcriticRLforcodeim- trainedonendtask single(unittests) (densesignal)
provement
DrRepair(YasunagaandLiang,2020) Compiler feedback to itera- trainedsemisup. single(compilermsg) (notselfgen.)
tivelyrepair
PEER(Schicketal.,2022b) doc.edittrainedonwikiedits trainedonedits single(accuracy) (notselfgen.)
Selfcritique(Saundersetal.,2022a) fewshotcritiquegeneration feedbacktraining single(human) (selfgen.)
Self-correct(Wellecketal.,2022) noveltrainingofacorrector trainedonendtask single(taskspecific) (limitedsetting) (limitedsetting)
Const.AI(Baietal.,2022b) trainRL4Fonautomat(cri- critiquetraining (fixedset)
tique,revision)pair
Self-ask(Pressetal.,2022) askfollowupqueswhenin- fewshot none (none)
terimanscorrect;finalwrong
GPT3score(Fuetal.,2023) GPT can score generations fewshot single(singleutilityfn) (none)
withinstruction
Augmenter(Pengetal.,2023) factualityfeedbackfromexter- fewshot single(factuality) (selfgen.)
nalKBs
Re3(Yangetal.,2022) ∼ours: but one domain, fewshot (trainedcritics) (notselfgen.)
trainedcritics
SELF-REFINE fewshotiterativemultiaspect fewshot multiple(fewshotcritics) (selfgen.)
NLfb
Table5: Summaryofrelatedapproaches. Reinforcementlearningapproachesareshownin purple
,trainedcorrectorapproachesareshownin orange,andfew-shotcorrectorapproachesareshownin
green.
15
RLHF(Stiennonetal.,2020)
RainierRL(Liuetal.,2022)
QUARKRL(Luetal.,2022)
CodeRL(Leetal.,2022a)
DrRepair(YasunagaandLiang,2020)
PEER(Schicketal.,2022b)
Selfcritique(Saundersetal.,2022a)
Self-correct(Wellecketal.,2022)
Const.AI(Baietal.,2022b)
Self-ask(Pressetal.,2022)
GPT3score(Fuetal.,2023)
Augmenter(Pengetal.,2023)
Re3(Yangetal.,2022)
SELF-REFINE

