A6: ConversationalChess
Chess Board
Human/AI Chess Player A Human/AI Chess Player B
Validate
move Validate
move
Developing my knightto a
good square.Your move.
Challenging your pawn in
the center. Your move.
Figure 14: A6: Conversational Chess: Our conversational chess application can support various
scenarios, as each player can be an LLM-empowered AI, a human, or a hybrid of the two. Here,
theboardagentmaintainstherulesofthegameandsupportstheplayerswithinformationaboutthe
board. Playersandtheboardagentallusenaturallanguageforcommunication.
InConversationalChess,eachplayerisaAutoGenagentandcanbepoweredeitherbyahumanoran
AI.Athirdparty,knownastheboardagent,isdesignedtoprovideplayerswithinformationaboutthe
boardandensurethatplayers’movesadheretolegalchessmoves.Figure14illustratesthescenarios
supportedbyConversationalChess:AI/humanvs.AI/human,anddemonstrateshowplayersandthe
boardagentinteract. Thissetupfosterssocialinteractionandallowsplayerstoexpresstheirmoves
creatively,employingjokes,memereferences,andcharacter-playing,therebymakingchessgames
moreentertainingforbothplayersandobservers(Figure15providesanexampleofconversational
chess).
Torealizethesescenarios,weconstructedaplayeragentwithLLMandhumanasback-endoptions.
Whenhumaninputisenabled,beforesendingtheinputtotheboardagent,itfirstpromptsthehuman
playertoinputthemessagethatcontainsthemovealongwithanythingelsetheplayerwantstosay
(such as a witty comment). If human input is skipped or disabled, LLM is used to generate the
message. The board agent is implemented with a custom reply function, which employs an LLM
to parse the natural language input into a legal move in a structured format (e.g., UCI), and then
pushesthemovetotheboard. Ifthemoveisnotlegitimate,theboardagentwillreplywithanerror.
Subsequently, the player agent needs to resend a message to the board agent until a legal move is
made. Oncethemoveissuccessfullypushed,theplayeragentsendsthemessagetotheopponent.
AsshowninFigure15,theconversationbetweenAIplayerscanbenaturalandentertaining. When
theplayeragentusesLLMtogenerateamessage, itutilizestheboardstateandtheerrormessage
from the board agent. This helps reduce the chance of hallucinating an invalid move. The chat
between one player agent and the board agent is invisible to the other player agent, which helps
keepthemessagesusedinchatcompletionwell-managed.
There are two notable benefits of using AutoGen to implement Conversational Chess. Firstly, the
agentdesigninAutoGenfacilitatesthenaturalcreationofobjectsandtheirinteractionsneededin
our chess game. This makes development easy and intuitive. For example, the isolation of chat
messagessimplifiestheprocessofmakingaproperLLMchatcompletioninferencecall. Secondly,
AutoGengreatlysimplifiestheimplementationofagentbehaviorsusingcomposition. Specifically,
weutilizedtheregister replymethodsupportedbyAutoGenagentstoinstantiateplayeragents
andaboardagentwithcustomreplyfunctions. Concentratingtheextensionworkneededatasingle
point (the reply function) simplifies the reasoning processes, and development and maintenance
effort.
30
