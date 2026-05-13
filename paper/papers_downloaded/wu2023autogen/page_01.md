AutoGen: Enabling Next-Gen LLM
Applications via Multi-Agent Conversation
QingyunWu†,GaganBansal∗,JieyuZhang±,YiranWu†,BeibinLi∗
ErkangZhu∗,LiJiang∗,XiaoyunZhang∗,ShaokunZhang†,JialeLiu∓
AhmedAwadallah∗,RyenW.White∗,DougBurger∗,ChiWang∗1
∗MicrosoftResearch,†PennsylvaniaStateUniversity
±UniversityofWashington,∓XidianUniversity
Conversable agent Plot a chart of Output:
META and TESLA
stock price change
YTD. $
Execute the
following code… Month
Multi-Agent Conversations Error package No, please plot %
yfinanceis not change!
installed
Got it! Here is the
… … … … p S ip o r i r n y s ! t a P l l l e a y s f e in a fi n r c s e t revised code …
and then execute Output:
the code
… … … … Installing… %
Joint chat Hierarchical chat
Month
Agent Customization Flexible Conversation Patterns Example Agent Chat
Figure1: AutoGenenablesdiverseLLM-basedapplicationsusingmulti-agentconversations. (Left)
AutoGenagentsareconversable,customizable,andcanbebasedonLLMs,tools,humans,oreven
a combination of them. (Top-middle) Agents can converse to solve tasks. (Right) They can form
a chat, potentially with humans in the loop. (Bottom-middle) The framework supports flexible
conversationpatterns.
Abstract
AutoGen2 isanopen-sourceframeworkthatallowsdeveloperstobuildLLMap-
plications via multiple agents that can converse with each other to accomplish
tasks. AutoGen agents are customizable, conversable, and can operate in vari-
ous modes that employ combinations of LLMs, human inputs, and tools. Using
AutoGen, developers can also flexibly define agent interaction behaviors. Both
naturallanguageandcomputercodecanbeusedtoprogramflexibleconversation
patterns for different applications. AutoGen serves as a generic framework for
building diverse applications of various complexities and LLM capacities. Em-
pirical studies demonstrate the effectiveness of the framework in many example
applications, with domains ranging from mathematics, coding, question answer-
ing,operationsresearch,onlinedecision-making,entertainment,etc.
1Correspondingauthor.Email:auto-gen@outlook.com
2https://github.com/microsoft/autogen
3202
tcO
3
]IA.sc[
2v55180.8032:viXra
Conversable agent |  | Plot a chart of
META and TESLA
stock price change
YTD.
Execute the
following code…
Error package
yfinanceis not
installed
Sorry! Please first
pip install yfinance
and then execute
the code
Installing…
 | Multi-Agent Conversations | 
 | … … … …
… … … …
Joint chat Hierarchical chat | 


…


…

