problem involves solving a number theory issue. The correctness counts and reasons for failure
are detailed in Table 2. For the quantitative evaluation, we conduct two sets of experiments on
the MATH dataset to assess the correctness of these systems: (1) an experiment involving 120
level-5(themostchallenginglevel)problems,including20problemsfromsixcategories,excluding
geometry,and(2)anexperimentontheentiretestset,whichincludes5000problems. Weexclude
AutoGPTfromthisevaluationasitcannotaccessresultsfromcodeexecutionsanddoesnotsolve
anyproblemsinthequalitativeevaluation. OuranalysisoftheentiredatasetrevealsthatAutoGen
achieves an overall accuracy of 69.48%, while GPT-4’s accuracy stands at 55.18%. From these
evaluations, we have the following observations regarding the problem-solving success rate and
userexperienceofthesesystems:
• Problem-solving success rate: Results from the quantitative evaluations show that AutoGen can
helpachievethehighestproblem-solvingsuccessrateamongallthecomparedmethods.Thequal-
itativeevaluationselucidatecommonfailurereasonsacrossseveralalternativeapproaches. Chat-
GPT+CodeInterpreterfailstosolvethesecondproblem,andChatGPT+Pluginstrugglestosolve
both problems. AutoGPT fails on both problems due to code execution issues. The LangChain
agentalsofailsonbothproblems,producingcodethatresultsinincorrectanswersinalltrials.
• Based on the qualitative evaluation, we analyze the user experience concerning the verbosity of
theresponseandtheabilityoftheLLM-basedsystemtorunwithoutunexpectedbehaviors. Chat-
GPT+Pluginistheleastverbose,mainlybecauseWolframqueriesaremuchshorterthanPython
code. AutoGen, ChatGPT+Code Interpreter, and LangChain exhibit similar verbosity, although
LangChain is slightly more verbose due to more code execution errors. AutoGPT is the most
verbosesystemowingtopredefinedstepslikeTHOUGHTS,REASONING,andPLAN,whichit
includesinreplieseverytime.Overall,AutoGenandChatGPT+CodeInterpreteroperatesmoothly
withoutexceptions. WenotetheoccurrencesofundesiredbehaviorsfromotherLLM-basedsys-
tems that could affect user experience: AutoGPT consistently outputs code without the print’
statement and cannot correct this, requiring the user to run them manually; ChatGPT with Wol-
framAlphapluginhasthepotentialtobecomestuckinaloopthatmustbemanuallystopped;and
LangchainReActcouldexitwithaparseerror,necessitatingthepassingofa‘handle parse error’
parameter.
Expert
Assistant
Student Student
Proxy Assistant
Ask for
expert
Enable Autonomous and Human-in-the-loop
Problem Solving
Expert
Proxy
Enable Multi-User Problem Solving Via
Student and Expert
Figure 6: Examples of three settings utilized to solve math problems using AutoGen: (Gray) En-
ables a workflow where a student collaborates with an assistant agent to solve problems, either
autonomously or in a human-in-the-loop mode. (Gray + Orange) Facilitates a more sophisticated
workflowwhereintheassistant, onthefly, canengageanotherusertermed“expert”, whoisinthe
loopwiththeirownassistantagent,toaidinproblem-solvingifitsownsolutionsarenotsatisfactory.
Scenario 2: Human-in-the-loop Problem Solving. For challenging problems that these LLM
systems cannot solve autonomously, human feedback during the problem-solving process can be
20
Expert
Assistant
Student Student
Proxy Assistant
Ask for
expert
Enable Autonomous and Human-in-the-loop
Problem Solving
Expert
Proxy | Expert
Assistant
Expert
Proxy
Enable Multi-User Problem Solving Via
Student and Expert | 

