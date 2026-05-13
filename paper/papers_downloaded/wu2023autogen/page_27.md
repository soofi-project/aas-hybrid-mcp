ManualEvaluationComparingChatGPT+CodeInterpreterandAutoGen-basedOptiGuide.
ChatGPT+CodeInterpreterisunabletoexecutecodewithprivateorcustomizeddependencies(e.g.,
Gurobi),whichmeansusersneedtohaveengineeringexpertisetomanuallyhandlemultiplesteps,
disrupting the workflow and increasing the chance for mistakes. If users lack access or expertise,
theburdenfallsonsupportingengineers,increasingtheiron-calltime.
We carried out a user study that juxtaposed OpenAI’s ChatGPT coupled with a Code Interpreter
against AutoGen-based OptiGuide. The study focused on a coffee supply chain scenario, and an
expert Python programmer with proficiency in Gurobi participated in the test. We evaluated both
systems based on 10 randomly selected questions, measuring time and accuracy. While both sys-
temsanswered8questionscorrectly,theCodeInterpreterwassignificantlyslowerthanOptiGuide
becausetheformerrequiresmoremanualintervention.Onaverage,usersneededtospend4minutes
and35secondstosolveproblemswiththeCodeInterpreter, withastandarddeviationofapproxi-
mately2.5minutes.Incontrast,OptiGuide’saverageproblem-solvingtimewasaround1.5minutes,
mostofwhichwasspentwaitingforresponsesfromtheGPT-4model. Thisindicatesa3xsaving
ontheuser’stimewithAutoGen-basedOptiGuide.
While using ChatGPT + Code Interpreter, users had to read through the code and instructions to
knowwheretopastethecodesnippets. Additionally,runningthecodeinvolvesdownloadingitand
executingitinaterminal,aprocessthatwasbothtime-consumingandpronetoerrors.Theresponse
timefromtheCodeInterpreterisalsoslower,asitgenerateslotsoftokenstoreadthecode,readthe
variablesline-by-line,performchainsofthoughtanalysis,andthenproducethefinalanswercode.
Incontrast,AutoGenintegratesmultipleagentstoreduceuserinteractionsby3-5timesonaverage
as reported in Table 4, where we evaluated our system with 2000 questions across five OptiGuide
applicationsandmeasuredhowmanypromptstheuserneedstotype.
Table4: ManualeffortsavedwithOptiGuide(W/GPT-4)whilepreservingthesamecodingperfor-
manceisshowninthedatabelow.Thedataincludeboththemeanandstandarddeviations(indicated
inparentheses).
Dataset netflow facility tsp coffee diet
SavingRatio 3.14x(0.65) 3.14x(0.64) 4.88x(1.71) 3.38x(0.86) 3.03x(0.31)
Table13and15provideadetailedcomparisonofuserexperiencewithChatGPT+CodeInterpreter
andAutoGen-basedOptiGuide. ChatGPT+CodeInterpreterisunabletoruncodewithprivatepack-
ages or customized dependencies (such as Gurobi); as a consequence, ChatGPT+Code Interpreter
requires users to have engineering expertise and to manually handle multiple steps, disrupting the
workflow and increasing the chance for mistakes. If customers lack access or expertise, the bur-
denfallsonsupportingengineers,increasingtheiron-calltime. Incontrast,theautomatedchatby
AutoGen is more streamlined and autonomous, integrating multiple agents to solve problems and
addressconcerns. Thisresultsina5xreductionininteractionandfundamentallychangestheover-
allusabilityofthesystem. Astableworkflowcanbepotentiallyreusedforotherapplicationsorto
composealargerone.
Takeaways: Theimplementationofthemulti-agentdesignwithAutoGenintheOptiGuideappli-
cation offers several advantages. It simplifies the Python implementation and fosters a mixture of
collaborativeandadversarialproblem-solvingenvironments,withtheCommanderandWriterwork-
ingtogetherwhiletheSafeguardactsasavirtualadversarialchecker. Thissetupallowsforproper
memory management, as the Commander maintains memory related to user interactions, provid-
ing context-aware decision-making. Additionally, role-playing ensures that each agent’s memory
remainsisolated,preventingshortcutsandhallucinations
27
