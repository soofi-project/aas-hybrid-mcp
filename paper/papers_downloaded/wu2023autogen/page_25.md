Task description
You are in the middle of a room. Looking quickly around you, you see a bed 1, a desk 2, a desk 1, a safe 1, a drawer 2, a drawer1, a
shelf 3, a shelf 2, and a shelf 1.
Your task is to: look at bowl under the desklamp.
(a) Two agents (b) Three agents
Assistant(to Executor): THOUGHT [First, I need to find a bowl. A Assistant(to Executor): THOUGHT [First, I need to find a bowl. A
bowl is more likely to appear in desk (1-2), drawer (1-2), shelf bowl is more likely to appear in desk (1-2), drawer (1-2), shelf
(1-3), bed (1). Then I need to find and use a desklamp.] ACTION (1-3), bed (1). Then I need to find and use a desklamp.] ACTION
[go to desk 1] [go to desk 1]
(Assistant finds the desklampat desk 1, then goes to desk 2.) (Assistant finds the desklampat desk 1, then goes to desk 2.)
Executor(to Assistant): On the desk 2, you see a bowl 1, and a (Assistant falls into the same loop as (a))
cd 3... GroundingAgent(to Executor): You must find and take the object
Assistant(to Executor): THOUGHT [Now I find a bowl (1). I need before you can examine it. You must go to where the target
to use the desklampto look at the bowl. I'll go to the desklamp object is before you can use it.
now.] ACTION [go to desk 1] Executor(to Assistant): You turn on the desklamp1. Hint: You must
Executor(to Assistant):On the desk 1, you see a desklamp1, a find and take the object before you can examine it.
pencil 2... Assistant(to Executor): THOUGHT [I need to find and take the
Assistant: ACTION [use desklamp1] bowl (1) before I can examine it. Let me find the bowl first.]
Executor(to Assistant): You turn on the desklamp1. ACTION [go to desk 2]
Assistant(to Executor):THOUGHT [Now that the desklampis turned Executor(to Assistant): On the desk 2, you see a bowl 1, a cd
on, I can use it to look at the bowl (1) that I found earlier.] 3...
ACTION [look at bowl 1 under the desklamp1] Assistant(to Executor): ACTION [take bowl 1 from desk 2]
Executor(to Assistant): You turn on the desklamp1. Executor(to Assistant): You pick up bowl 1 from desk 2.
(Assistant falls into an infinite loop turning on desklamp.) Assistant(to Executor):ACTION [go to desk 1]
Executor(to Assistant): Task failed. Reply TERMINATE. Assistant(to Executor):ACTION[use desklamp1]
Assistant(to Executor): TERMINATE Executor(to Assistant): Task success. Reply TERMINATE.
Assistant(to Executor): TERMINATE
Figure 10: Comparison of results from two designs: (a) Two-agent design which consists of an
assistant and an executor, (b) Three-agent design which adds a grounding agent that serves as a
knowledge source. For simplicity, we omit the in-context examples and part of the exploration
trajectory,andonlyshowpartscontributingtothefailure/successoftheattempt.
Method Pick Clean Heat Cool Look Pick2 All
ReAct(avg) 63 52 48 71 61 24 54
ALFChat(2agents)(avg) 61 58 57 67 50 19 54
ALFChat(3agents)(avg) 79 64 70 76 78 41 69
ReAct(bestof3) 75 62 61 81 78 35 66
ALFChat(2agents)(bestof3) 71 61 65 76 67 35 63
AFLChat(3agents)(bestof3) 92 74 78 86 83 41 77
Table 3: Comparisons between ReAct and the two variants of ALFChat on the ALFWorld bench-
mark. Foreachtask,wereportthesuccessrateoutof3attempts. Successratedenotesthenumber
oftaskssuccessfullycompletedbytheagentdividedbythetotalnumberoftasks. Theresultsshow
thataddingagroundingagentsignificantlyimprovesthetasksuccessrateinALFChat.
design matches the performance of ReAct, while the three-agent design significantly outperforms
ReAct. Wesurmisethattheperformancediscrepancyiscausedbytheinherentdifferencebetween
dialogue-completionandtext-completiontasks. Ontheotherhand, introducingagroundingagent
asaknowledgesourceremarkablyadvancesperformanceonalltypesoftasks.
Case study. Figure 10 exemplifies how a three-agent design eliminates one root cause for failure
cases. Mostofthetasksinvolvetakinganobjectandthenperformingaspecificactionwithit(e.g.,
finding a vase and placing it on a cupboard). Without a grounding agent, the assistant frequently
conflates finding an object with taking it, as illustrated in Figure 10a). This leads to most of the
failurecasesin’pick’and’look’typetasks.Withtheintroductionofagroundingagent,theassistant
canbreakoutofthisloopandsuccessfullycompletethetask
Takeaways. We introduced a grounding agent to serve as an external commonsense knowledge
source,whichsignificantlyenhancedtheassistant’sabilitytomakeinformeddecisions. Thisproves
that providing necessary commonsense facts to the decision-making agent can assist it in making
more informed decisions, thus effectively boosting the task success rate. AutoGen brings both
simplicityandmodularitywhenaddingthegroundingagent.
25
 | THOUGHT [Now I find a bowl (1). I need
to use the desklampto look at the bowl. I'll go to the desklamp | 

 | THOUGHT [I need to find and take the
bowl (1) before I can examine it. Let me find the bowl first.] | 

 | THOUGHT [Now that the desklampis turned
on, I can use it to look at the bowl (1) that I found earlier.] | 

Pick Clean Heat Cool Look Pick2
63 52 48 71 61 24
61 58 57 67 50 19
79 64 70 76 78 41
75 62 61 81 78 35
71 61 65 76 67 35
92 74 78 86 83 41

