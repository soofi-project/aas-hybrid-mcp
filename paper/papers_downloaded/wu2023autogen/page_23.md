Task description
who carried the usaflag in opening ceremony?
(a) W/O Interactive Retrieval (b) W/ Interactive Retrieval
Assistant: You’re a retrieve augmented chatbot. You answer user’s Assistant: You’re a retrieve augmented chatbot. You answer user’s
questions based on your own knowledge and the context provided by questions based on your own knowledge and the context provided by
the user. If you can’t answer the question with or without the the user. If you can’t answer the question with or without the
current context, you should reply ‘sorry, I don’t know’. You must current context, you should reply exactly ‘UPDATE CONTEXT’. You
give as short an answer as possible. must give as short an answer as possible.
User’s question is:who carried the usaflag in opening ceremony User’s question is: who carried the usaflag in opening ceremony
Context is: < P > On January 17 , 1899 , under ... The Astros Context is: < P > On January 17 , 1899 , under ... The Astros
beat the Yankees that night , 2 -1 . < /P > beat the Yankees that night , 2 -1 . < /P >
UserProxy: Sorry, I cannot find any information about who carried UserProxy: Sorry, I cannot find any information about who carried
the USA flag in the opening ceremony. Sorry, I don’t know. the USA flag in the opening ceremony. UPDATE CONTEXT.
Assistant: You’re a retrieve augmented chatbot. You answer user’s
questions based on your own knowledge and the context provided by
the user. If you can’t answer the question with or without the
current context, you should reply exactly ‘UPDATE CONTEXT’. You
must give as short an answer as possible.
User’s question is: who carried the usaflag in opening ceremony
Context is: < T able > ... Erin Hamlin ... < /T d >
UserProxy: Erin Hamlin carried the USA flag in the opening
ceremony.
Figure8: Retrieval-augmentedChatwithout(W/O)andwith(W/)interactiveretrieval.
requiredinformationforaresponse. Asaresult,theLLMassistant(GPT-3.5-turbo)replies“Sorry,
IcannotfindanyinformationaboutwhocarriedtheUSAflagintheopeningceremony. UPDATE
CONTEXT.”WiththeuniqueandinnovativeabilitytoupdatecontextinRetrieval-AugmentedChat,
theuserproxyagentautomaticallyupdatesthecontextandforwardsittotheassistantagentagain.
Followingthisprocess,theagentisabletogeneratethecorrectanswertothequestion.
Inaddition,weconductanexperimentusingthesamepromptasillustratedin(Adlakhaetal.,2023)
toinvestigatetheadvantagesofAutoGenW/Ointeractiveretrieval. TheF1scoreandRecallforthe
first500questionsare23.40%and62.60%,respectively,aligningcloselywiththeresultsreported
inFigure4b. Consequently,weassertthatAutoGenW/OinteractiveretrievaloutperformsDPRdue
to differences in the retrievers employed. Specifically, we utilize a straightforward vector search
retrieverwiththeall-MiniLM-L6-v2modelforembeddings.
Furthermore, we analyze the number of LLM calls in experiments involving both AutoGen and
AutoGenW/Ointeractiveretrieval,revealingthatapproximately19.4%ofquestionsintheNatural
Questionsdatasettriggeran“UpdateContext”operation,resultinginadditionalLLMcalls.
Scenario2:CodeGenerationLeveragingLatestAPIsfromtheCodebase.Inthiscase,theques-
tionis“HowcanIuseFLAMLtoperformaclassificationtaskanduseSparkforparalleltraining?
Trainfor30secondsandforcecanceljobsifthetimelimitisreached.”. FLAML(v1)(Wangetal.,
2021) is an open-source Python library designed for efficient AutoML and tuning. It was open-
sourced in December 2020, and is included in the training data of GPT-4. However, the question
necessitatestheuseofSpark-relatedAPIs,whichwereaddedinDecember2022andarenotencom-
passedintheGPT-4trainingdata. Consequently,theoriginalGPT-4modelisunabletogeneratethe
correctcode,duetoitslackofknowledgeregardingSpark-relatedAPIs. Instead,iterroneouslycre-
atesanon-existentparameter,spark,andsetsittoTrue’. Nevertheless,withRetrieval-Augmented
Chat,weprovidethelatestreferencedocumentsascontext. Then,GPT-4generatesthecorrectcode
blocksbysettinguse sparkandforce canceltoTrue’.
23
Context is: < P > On January 17 , 1899 , under ... The Astros
beat the Yankees that night , 2 -1 . < /P >

 | Erin Hamlin carried the USA flag in the opening
ceremony. | 

