A2: Retrieval-AugmentedCodeGenerationandQuestionAnswering
1. Question and Contexts
2. Satisfied Answers or `Update Context`
3. Terminate,feedbacks or `Update Context`
4. Satisfied Answers or Terminate
Retrieval-augmented Retrieval-augmented
User Proxy Assistant
Figure7: OverviewofRetrieval-augmentedChatwhichinvolvestwoagents,includingaRetrieval-
augmented User Proxy and a Retrieval-augmented Assistant. Given a set of documents, the
Retrieval-augmentedUserProxyfirstautomaticallyprocessesdocuments—splits,chunks,andstores
them in a vector database. Then for a given user input, it retrieves relevant chunks as context and
sendsittotheRetrieval-augmentedAssistant, whichusesLLMtogeneratecodeortexttoanswer
questions. Agentsconverseuntiltheyfindasatisfactoryanswer.
Detailed Workflow. The workflow of Retrieval-Augmented Chat is illustrated in Figure 7. To
use Retrieval-augmented Chat, one needs to initialize two agents including Retrieval-augmented
User Proxy and Retrieval-augmented Assistant. Initializing the Retrieval-Augmented User Proxy
necessitatesspecifyingapathtothedocumentcollection. Subsequently, theRetrieval-Augmented
User Proxy can download the documents, segment them into chunks of a specific size, compute
embeddings,andstoretheminavectordatabase. Onceachatisinitiated,theagentscollaboratively
engageincodegenerationorquestion-answeringadheringtotheproceduresoutlinedbelow:
1. TheRetrieval-AugmentedUserProxyretrievesdocumentchunksbasedontheembeddingsimi-
larity,andsendsthemalongwiththequestiontotheRetrieval-AugmentedAssistant.
2. TheRetrieval-AugmentedAssistantemploysanLLMtogeneratecodeortextasanswersbased
onthequestionandcontextprovided. IftheLLMisunabletoproduceasatisfactoryresponse,it
isinstructedtoreplywith“UpdateContext”totheRetrieval-AugmentedUserProxy.
3. Ifaresponseincludescodeblocks,theRetrieval-AugmentedUserProxyexecutesthecodeand
sendstheoutputasfeedback. Iftherearenocodeblocksorinstructionstoupdatethecontext,it
terminates the conversation. Otherwise, it updates the context and forwards the question along
withthenewcontexttotheRetrieval-AugmentedAssistant. Notethatifhumaninputsolicitation
is enabled, individuals can proactively send any feedback, including Update Context”, to the
Retrieval-AugmentedAssistant.
4. IftheRetrieval-AugmentedAssistantreceives“UpdateContext”,itrequeststhenextmostsimilar
chunks of documents as new context from the Retrieval-Augmented User Proxy. Otherwise, it
generatesnewcodeortextbasedonthefeedbackandchathistory. IftheLLMfailstogenerate
an answer, it replies with “Update Context” again. This process can be repeated several times.
Theconversationterminatesifnomoredocumentsareavailableforthecontext.
We utilize Retrieval-Augmented Chat in two scenarios. The first scenario aids in generating code
basedonagivencodebase. WhileLLMspossessstrongcodingabilities,theyareunabletoutilize
packagesorAPIsthatarenotincludedintheirtrainingdata,e.g.,privatecodebases,orhavetrouble
using trained ones that are frequently updated post-training. Hence, Retrieval-Augmented Code
Generation is considered to be highly valuable. The second scenario involves question-answering
on the Natural Questions dataset (Kwiatkowski et al., 2019), enabling us to obtain comparative
evaluationmetricsfortheperformanceofoursystem.
Scenario 1: Evaluation on Natural Questions QA dataset. In this case, we evaluate the
Retrieval-Augmented Chat’s end-to-end question-answering performance using the Natural Ques-
tionsdataset(Kwiatkowskietal.,2019). Wecollected5,332non-redundantcontextdocumentsand
6,775queriesfromHuggingFace. First,wecreateadocumentcollectionbasedontheentirecontext
corpusandstoreitinthevectordatabase. Then,weutilizeRetrieval-AugmentedChattoanswerthe
questions. Anexample(Figure8)fromtheNQdatasetshowcasestheadvantagesoftheinteractive
retrieval feature: “who carried the usa flag in opening ceremony”. When attempting to answer
thisquestion,thecontextwiththehighestsimilaritytothequestionembeddingdoesnotcontainthe
22
