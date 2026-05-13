A5: DynamicGroupChat
Manager
Alice User Proxy Bob
1. Select a Speaker
Response
Alice User Proxy Bob
Bob Manager
3. Broadcast
2. Ask the Speaker to Respond
Figure12: A5: DynamicGroupChat: OverviewofhowAutoGenenablesdynamicgroupchatsto
solve tasks. The Manager agent, which is an instance of the GroupChatManager class, performs
thefollowingthreesteps–selectasinglespeaker(inthiscaseBob),askthespeakertorespond,and
broadcasttheselectedspeaker’smessagetoallotheragents
To validate the necessity of multi-agent dynamic group chat and the effectiveness of the role-play
speaker selection policy, we conducted a pilot study comparing a four-agent dynamic group chat
systemwithtwopossiblealternativesacross12manuallycraftedcomplextasks. Anexampletaskis
“HowmuchmoneywouldIearnifIbought200$AAPLstocksatthelowestpriceinthelast30days
andsoldthematthehighestprice? Savetheresultsintoafile.”Thefour-agentgroupchatsystem
comprised the following group members: a user proxy to take human inputs, an engineer to write
codeandfixbugs,acritictoreviewcodeandprovidefeedback,andacodeexecutorforexecuting
code. Oneofthepossiblealternativesisatwo-agentsysteminvolvinganLLM-basedassistantand
a user proxy agent, and another alternative is a group chat system with the same group members
butatask-basedspeakerselectionpolicy. Inthetask-basedspeakerselectionpolicy,wesimplyap-
pend role information, chat history, and the next speaker’s task into a single prompt. Through the
pilotstudy,weobservedthatcomparedwithatask-styleprompt,utilizingarole-playpromptindy-
namicspeakerselectionoftenleadstomoreeffectiveconsiderationofbothconversationcontextand
rolealignmentduringtheprocessofgeneratingthesubsequentspeaker,andconsequentlyahigher
successrateasreportedinTable5, fewerLLMcallsandfewerterminationfailures, asreportedin
Table6.
Table5: Numberofsuccessesonthe12tasks(higherthebetter).
Model TwoAgent GroupChat GroupChatwithatask-basedspeakerselectionpolicy
GPT-3.5-turbo 8 9 7
GPT-4 9 11 8
Table6: Average#LLMcallsandnumberofterminationfailuresonthe12tasks(lowerthebetter).
Model TwoAgent GroupChat GroupChatwithatask-basedspeakerselectionpolicy
GPT-3.5-turbo 9.9,9 5.3,0 4,0
GPT-4 6.8,3 4.5,0 4,0
28
