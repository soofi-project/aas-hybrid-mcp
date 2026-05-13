Student Assistant Assistant Retrieval-augmented Retrieval-augmented
User Proxy Assistant
Ask
expert ALFWorld
Executor
Assistant
Expert Grounding
Agent
A1. Math Problem Solving A2. Retrieval-augmented Chat A3. ALF Chat
Commander Chess Board
Manager
Broadcast Speak
Human/AI Chess Human/AI Chess
Writer Safeguard Player A Player B
A4. Multi-agent Coding A5. Dynamic Group Chat A6. Conversational Chess
Figure 3: Six examples of diverse applications built using AutoGen. Their conversation patterns
showAutoGen’sflexibilityandpower.
A1: MathProblemSolving
Mathematics is a foundational discipline and the promise of leveraging LLMs to assist with math
problemsolvingopensupanewplethoraofapplicationsandavenuesforexploration,includingper-
sonalizedAItutoring,AIresearchassistance,etc. ThissectiondemonstrateshowAutoGencanhelp
developLLMapplicationsformathproblemsolving,showcasingstrongperformanceandflexibility
insupportingvariousproblem-solvingparadigms.
(Scenario1)Weareabletobuildasystemforautonomousmathproblemsolvingbydirectlyreusing
two built-in agents from AutoGen. We evaluate our system and several alternative approaches,
including open-source methods such as Multi-Agent Debate (Liang et al., 2023), LangChain Re-
Act(LangChain,2023),vanillaGPT-4,andcommercialproductsChatGPT+CodeInterpreter,and
ChatGPT+Plugin(WolframAlpha),ontheMATH(Hendrycksetal.,2021)datasetandsummarize
theresultsinFigure4a. Weperformevaluationsover120randomlyselectedlevel-5problemsand
ontheentire5 testdatasetfromMATH.Theresultsshowthatthebuilt-inagentsfromAutoGenal-
readyyieldbetterperformanceoutoftheboxcomparedtothealternativeapproaches,evenincluding
thecommercialones. (Scenario2)Wealsoshowcaseahuman-in-the-loopproblem-solvingprocess
with the help of AutoGen. To incorporate human feedback with AutoGen, one only needs to set
human input mode=‘ALWAYS’ in the UserProxyAgent of the system in scenario 1. We demon-
stratethatthissystemcaneffectivelyincorporatehumaninputstosolvechallengingproblemsthat
cannot be solved without humans. (Scenario 3) We further demonstrate a novel scenario where
multiplehumanuserscanparticipateintheconversationsduringtheproblem-solvingprocess. Our
experimentsandcasestudiesforthesescenariosshowthatAutoGenenablesbetterperformanceor
newexperiencecomparedtoothersolutionsweexperimentedwith. Duetothepagelimit,detailsof
theevaluation,includingcasestudiesinthreescenariosareinAppendixD.
A2: Retrieval-AugmentedCodeGenerationandQuestionAnswering
Retrievalaugmentationhasemergedasapracticalandeffectiveapproachformitigatingtheintrinsic
limitationsofLLMsbyincorporatingexternaldocuments. Inthissection, weemployAutoGento
build a Retrieval-Augmented Generation (RAG) system (Lewis et al., 2020; Parvez et al., 2021)
namedRetrieval-augmentedChat. Thesystemconsistsoftwoagents: aRetrieval-augmentedUser
Proxy agent and a Retrieval-augmented Assistant agent, both of which are extended from built-in
agents from AutoGen. The Retrieval-augmented User Proxy includes a vector database (Chroma,
5WedidnotevaluateChatGPTonthewholedatasetsinceitrequiressubstantialmanualeffortandisre-
stricted by its hourly message-number limitation. Multi-agent debate and LangChain ReAct were also not
evaluatedsincetheyunderperformedvanillaGPT-4onthesmallertestset.
6






