A3: DecisionMakinginTextWorldEnvironments
ALFWorldExecutor
Action Decision
Action decision: Pick up pencil 2 from desk 2
ALFWorld Assistant
Executor
Reward & State
Observation: On the desk 2, you see an alarmclock 3,
a bowl 3, a creditcard 2, a mug 1, and a pencil 2.
Assistant GroundingAgent
ALFChat(two agents) ALFChat(three agents)
Figure9: WeuseAutoGentosolvetasksintheALFWorldbenchmark, whichcontainshousehold
tasksdescribedinnaturallanguage.Weproposetwodesigns:atwo-agentdesignwheretheassistant
agentsuggeststhenextstep, andtheExecutorexecutesactionsandprovidesfeedback. Thethree-
agentdesignaddsagroundingagentthatsuppliescommonsensefactstotheexecutorwhenneeded.
ALFWorld (Shridhar et al., 2021) is a synthetic language-based interactive decision-making task.
Itcomprisestextualenvironmentsthataimtosimulatereal-worldhouseholdscenes. Givenahigh-
levelgoal(e.g.,puttingahotappleinthefridge)andthedescriptionofthehouseholdenvironment,
theagentneedstoexploreandinteractwiththesimulatedhouseholdenvironmentthroughatextual
interface. A typical task environment contains various types of locations and could require more
than40stepstofinish,whichhighlightstheneedforagentstodecomposethegoalintosubtasksand
tacklethemonebyone,whileeffectivelyexploringtheenvironments.
DetailedWorkflow. Wefirstproposeastraightforwardtwo-agentsystemwithAutoGen,illustrated
on the left-hand side of Figure 9, to tackle tasks from this benchmark. The system consists of
an assistant agent and an executor agent. The assistant agent generates plans and makes action
decisionstosolvethetasks. TheexecutoragentistailoredspecificallyforALFWorld. Itperforms
actionsproposedbytheassistantandreportsactionexecutionresultsinthehouseholdenvironment
asfeedbacktotheassistant. Duetothestrictformatrequirementsfortheoutputformat,weusethe
BLEUmetrictoevaluatethesimilarityoftheoutputtoallvalidactionoptions. Theoptionwiththe
highestsimilaritywillbechosenastheactionforthisround.
One major challenge encompassed in ALFWorld is commonsense reasoning. The agent needs to
extract patterns from the few-shot examples provided and combine them with the agent’s general
knowledgeofhouseholdenvironmentstofullyunderstandtaskrules. Moreoftenthannot, theas-
sistanttendstoneglectsomebasicknowledgeofthehouseholdenvironment. Thankstotheeasy-to-
implement multi-agent conversational feature of AutoGen, enhancing the assistant agent’s reason-
ingabilitybyaddinganewgroundingagenttoprovidecommonsensefactsforthedecision-making
agent’sreferencebecomesstraightforward. Byscrutinizingthefailedattemptsandsummarizingthe
reasons for failure, we obtained a holistic understanding of the commonsense knowledge that the
assistantagentlacks. Then, wesetagroundingagenttoprovidethisgeneralknowledgewhenthe
taskbeginsandwhenevertheassistantoutputsthesameactionthreetimesinarow.Thisensuresthe
assistanttakesthiscommonsenseknowledgeintoconsiderationandpreventsitfromgettingstuckin
outputtingthesamecontentorconstantlyapologizing.
We compare our system’s performance with ReAct, which treats ALFWorld as a text-completion
task. ReAct (Yao et al., 2022) is a few-shot prompting technique that interleaves reasoning and
acting, allowing for greater synergy between the two and significantly improving performance on
both language and decision-making tasks. We integrate ReAct into AutoGen by modifying the
prompts in a conversational manner. Following ReAct, we employ a two-shot setting. The few-
shotpromptsareobtainedfromthecorrespondingrepository. AsshowninTable3, thetwo-agent
24
 | 

 | 

