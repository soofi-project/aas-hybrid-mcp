ConversableAgent
Agent Customization:
human_input_mode= “NEVER”
code_execution_config= False
DEFAULT_SYSTEM_MESSAGE = “You
are a helpful AI assistant… human_input_mode= “NEVER”
AutoGen I p n y t t h h o e n f c o o l d l e… o ” wing cases, suggest human_input_mode=“ALWAYS” group_chat= [ ]
Agents
AssistantAgent UserProxyAgent GroupChatManager
# This funcwill be invoked in
generate_reply
# Note: when no reply
A.register_reply(B, funcis registered, a
reply_func_A2B) list of default reply
def reply_func_A2B(msg): functions will be used.
Developer o … uput= input_from_human() User Proxy A Assistant B
Code if not ouput:
if msg includes code: 2 Initiate Conversations:
output = execute(msg) A.initiate_chat(“Plot a chart of META and
return output TESLA stock price change YTD.”, B)
The Resulting Automated Agent Chat:
Conversation-Driven
Control Flow Plot a chart of META and receive generate_reply
TESLA stock price change YTD.
receive Execute the following send
Program
code…
Execution
generate_reply Error: package yfinanceis not
generate_reply
installed
send
Conversation-Centric Sorry! Please first pip install
Computation yfinanceand then execute
…
Unified Conversation Interfaces:
• send
• receive
• generate_reply
1.2 Register a Custom Reply Func: 1.1 Define Agents:
Figure2: IllustrationofhowtouseAutoGentoprogramamulti-agentconversation. Thetopsub-
figureillustratesthebuilt-inagentsprovidedbyAutoGen,whichhaveunifiedconversationinterfaces
and can be customized. The middle sub-figure shows an example of using AutoGen to develop
a two-agent system with a custom reply function. The bottom sub-figure illustrates the resulting
automatedagentchatfromthetwo-agentsystemduringprogramexecution.
Byallowingcustomagentsthatcanconversewitheachother,conversableagentsinAutoGenserve
asausefulbuildingblock.However,todevelopapplicationswhereagentsmakemeaningfulprogress
ontasks,developersalsoneedtobeabletospecifyandmoldthesemulti-agentconversations.
2.2 ConversationProgramming
As a solution to the above problem, AutoGen utilizes conversation programming, aparadigm that
considerstwoconcepts: thefirstiscomputation–theactionsagentstaketocomputetheirresponse
in a multi-agent conversation. And the second is control flow – the sequence (or conditions) un-
der which these computations happen. As we will show in the applications section, the ability to
programthesehelpsimplementmanyflexiblemulti-agentconversationpatterns. InAutoGen,these
computations are conversation-centric. An agent takes actions relevant to the conversations it is
involvedinanditsactionsresultinmessagepassingforconsequentconversations(unlessatermina-
tionconditionissatisfied). Similarly,controlflowisconversation-driven–theparticipatingagents’
decisionsonwhichagentstosendmessagestoandtheprocedureofcomputationarefunctionsofthe
inter-agentconversation. Thisparadigmhelpsonetoreasonintuitivelyaboutacomplexworkflow
asagentactiontakingandconversationmessage-passingbetweenagents.
Figure2providesasimpleillustration. Thebottomsub-figureshowshowindividualagentsperform
theirrole-specific,conversation-centriccomputationstogenerateresponses(e.g.,viaLLMinference
calls and code execution). The task progresses through conversations displayed in the dialog box.
Themiddlesub-figuredemonstratesaconversation-basedcontrolflow. Whentheassistantreceives
amessage, theuserproxyagenttypicallysendsthehumaninputasareply. Ifthereisnoinput, it
executesanycodeintheassistant’smessageinstead.
4
ConversableAgent
Agent Customization: Unified Conversation Interfaces:
• send
human_input_mode= “NEVER” • receive
code_execution_config= False • generate_reply
DEFAULT_SYSTEM_MESSAGE = “You
are a helpful AI assistant… human_input_mode= “NEVER”
AutoGen I p n y t t h h o e n f c o o l d l e… o ” wing cases, suggest human_input_mode=“ALWAYS” group_chat= [ ]
Agents
AssistantAgent UserProxyAgent GroupChatManager
1.2 Register a Custom Reply Func: 1.1 Define Agents:
# This funcwill be invoked in
generate_reply
# Note: when no reply
A.register_reply(B, funcis registered, a
reply_func_A2B) list of default reply
def reply_func_A2B(msg): functions will be used.
Developer o … uput= input_from_human() User Proxy A Assistant B
Code if not ouput:
if msg includes code: 2 Initiate Conversations:
output = execute(msg) A.initiate_chat(“Plot a chart of META and
return output TESLA stock price change YTD.”, B)
The Resulting Automated Agent Chat:
Conversation-Driven
Control Flow Plot a chart of META and receive generate_reply
TESLA stock price change YTD.
receive Execute the following send
Program
code…
Execution
generate_reply Error: package yfinanceis not
generate_reply
installed
send
Conversation-Centric Sorry! Please first pip install
Computation yfinanceand then execute
… | ConversableAgent
Agent Customization: Unified Conversation Interfaces:
• send
human_input_mode= “NEVER” • receive
code_execution_config= False • generate_reply
DEFAULT_SYSTEM_MESSAGE = “You
are a helpful AI assistant… human_input_mode= “NEVER”
In the following cases, suggest group_chat= [ ]
python code…” human_input_mode=“ALWAYS”
AssistantAgent UserProxyAgent GroupChatManager
 | 1.2 Register a Custom Reply Func: 1.1 Define Agents:
# This funcwill be invoked in
generate_reply
# Note: when no reply
A.register_reply(B, funcis registered, a
reply_func_A2B) list of default reply
def reply_func_A2B(msg): functions will be used.
ouput= input_from_human()
… User Proxy A Assistant B
if not ouput:
if msg includes code: 2 Initiate Conversations:
output = execute(msg) A.initiate_chat(“Plot a chart of META and
return output TESLA stock price change YTD.”, B)
 | The Resulting Automated Agent Chat:
Conversation-Driven
Control Flow Plot a chart of META and receive generate_reply
TESLA stock price change YTD.
receive Execute the following send
code…
generate_reply Error: package yfinanceis not
generate_reply
installed
send
Conversation-Centric Sorry! Please first pip install
Computation yfinanceand then execute
…

human_input_mode= “NEVER”
code_execution_config= False
DEFAULT_SYSTEM_MESSAGE = “You
are a helpful AI assistant…
In the following cases, suggest
python code…” | 
 | 

