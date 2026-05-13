A7: OnlineDecisionMakingforBrowserinteractions
Action decision: Next action to perform on a web page Action decision = “Click the button
with xpath ’//button[id =
Action Decision ‘subbtn’]’“
Executor Assistant Environment State =
“<div id="wrap" data-wob_ref="2" data-wob_eps="e0">
<div id="query">Click button ONE, then click button
TWO.</div>
<div id="area" data-wob_ref="3" data-wob_eps="e0">
<button id="subbtn" style="position:absolute;
left:50px; top:74px" data-wob_ref="4" data-
wob_eps="e0">ONE</button>
<button id="subbtn2" style="position:absolute;
left:98px; top:167px" data-wob_ref="5" data-
wob_eps="e0">TWO</button>
Reward & State </div>
</div>“
Environment State: HTML code for current web pages
Reward = ”0” (Ongoing)
Reward: Success/Fail/Ongoing
Figure17: WeuseAutoGentobuildMiniWobChat, whichsolvestasksintheMiniWob++bench-
mark. MiniWobChatconsistsoftwoagents: anassistantagentandanexecutoragent. Theassistant
agentsuggestsactionstomanipulatethebrowserwhiletheexecutorexecutesthesuggestedactions
andreturnsrewards/feedback.Theassistantagentrecordsthefeedbackandcontinuesuntilthefeed-
backindicatestasksuccessorfailure.
In practice, many applications require the presence of agents capable of interacting with environ-
mentsandmakingdecisionsinanonlinecontext,suchasingameplaying(Mnihetal.,2013;Vinyals
et al., 2017), web interactions (Liu et al., 2018; Shi et al., 2017), and robot manipulations (Shen
et al., 2021). With the multi-agent conversational framework in AutoGen, it becomes easy to de-
compose the automatic agent-environment interactions and the development of a decision-making
agent by constructing an executor agent responsible for handling the interaction with the environ-
ment, thereby delegating the decision-making part to other agents. Such a decomposition allows
developerstoreusethedecision-makingagentfornewtaskswithminimaleffortratherthanbuild-
ingaspecializeddecision-makingagentforeverynewenvironment.
Workflow. We demonstrate how to use AutoGen to build a working system for handling such
scenarios with the MiniWoB++ benchmark (Shi et al., 2017). MiniWoB++ comprises browser in-
teraction tasks that involve utilizing mouse and keyboard actions to interact with browsers. The
ultimateobjectiveofeachtaskistocompletethetasksdescribedconciselyinnaturallanguage,such
as“expandthewebsectionbelowandclickthesubmitbutton.”Solvingthesetaskstypicallyrequires
asequenceofwebmanipulationactionsratherthanasingleaction,andmakingactiondecisionsat
eachtimesteprequiresaccesstothewebstatus(intheformofHTMLcode)online.Fortheexample
above,clickingthesubmitbuttonrequirescheckingthewebstatusafterexpandingthewebsection.
Wedesignedastraightforwardtwo-agentsystemnamedMiniWobChatusingAutoGen,asshownin
Figure17. Theassistantagentisaninstanceofthebuilt-inAssistantAgentandisresponsiblefor
makingactiondecisionsforthegiventask. Thesecondagent, theexecutoragent, isacustomized
UserProxyAgent,whichisresponsibleforinteractingwiththebenchmarkbyexecutingtheactions
suggestedbytheAssistantAgentandreturningfeedback.
To assess the performance of the developed working system, we compare it with RCI (Kim et al.,
2023),arecentsolutionfortheMiniWoB++benchmarkthatemploysasetofself-critiquingprompts
and has achieved state-of-the-art performance. In our evaluation, we use all available tasks in the
official RCI code, with varying degrees of difficulty, to conduct a comprehensive analysis against
MiniWobChat. Figure 18 illustrates that MiniWobChat achieves competitive performance in this
evaluation8. Specifically, among the 49 available tasks, MiniWobChat achieves a success rate of
52.8%, which is only 3.6% lower than RCI, a method specifically designed for the MiniWob++
benchmark.Itisworthnotingthatinmosttasks,thedifferencebetweenthetwomethodsismirrored
asshowninFigure18. Ifweconsider0.1asasuccessratetoleranceforeachtask,i.e.,twomethods
that differ within 0.1 are considered to have the same performance, both methods outperform the
8WereporttheresultsofRCIbyrunningitsofficialcodewithdefaultsettings.
32
Action decision: Next action to perform on a web page Action decision = “Click the button
with xpath ’//button[id =
Action Decision ‘subbtn’]’“
Executor Assistant Environment State =
“<div id="wrap" data-wob_ref="2" data-wob_eps="e0">
<div id="query">Click button ONE, then click button
TWO.</div>
<div id="area" data-wob_ref="3" data-wob_eps="e0">
<button id="subbtn" style="position:absolute;
left:50px; top:74px" data-wob_ref="4" data-
wob_eps="e0">ONE</button>
<button id="subbtn2" style="position:absolute;
left:98px; top:167px" data-wob_ref="5" data-
wob_eps="e0">TWO</button>
Reward & State </div>
</div>“
Environment State: HTML code for current web pages
Reward = ”0” (Ongoing)
Reward: Success/Fail/Ongoing | 

