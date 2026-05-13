A4: Multi-AgentCoding
User
①User Question ⑧Final Answer
❻Log
❺
②
Questio
❸
n,
Code,
⑦
An
C
s
ommander
❹
Code
Clearance
a
R
n
e
sw
pe
e
a
r
t
in
u
g
n
t
t
h
il
e
user’s question or
timeout
Writer Safeguard
Figure 11: Our re-implementation of OptiGuide with AutoGen streamlining agents’ interactions.
The Commander receives user questions (e.g., What if we prohibit shipping from supplier 1 to
roastery2?) andcoordinateswiththeWriterandSafeguard. TheWritercraftsthecodeandinter-
pretation, the Safeguard ensures safety (e.g., not leaking information, no malicious code), and the
Commanderexecutesthecode. Ifissuesarise,theprocesscanrepeatuntilresolved. Shadedcircles
representstepsthatmayberepeatedmultipletimes.
Detailed Workflow. The workflow can be described as follows. The end user initiates the in-
teraction by posing a question, such as “What if we prohibit shipping from supplier 1 to roastery
2?”, markedby 1 totheCommanderagent. TheCommandermanagesandcoordinateswithtwo
LLM-basedassistantagents:theWriterandtheSafeguard.Apartfromdirectingtheflowofcommu-
nication,theCommanderhastheresponsibilityofhandlingmemorytiedtouserinteractions. This
capabilityenablestheCommandertocaptureandretainvaluablecontextregardingtheuser’sques-
tions and their corresponding responses. Such memory is subsequently shared across the system,
empoweringtheotheragentswithcontextfromprioruserinteractionsandensuringmoreinformed
andrelevantresponses.
In this orchestrated process, the Writer, who combines the functions of a “Coder” and an “Inter-
preter”asdefinedin(Lietal.,2023a),willcraftcodeandalsointerpretexecutionoutputlogs.Forin-
stance,duringcodewriting( 2 and 3 ),theWritermaycraftcode“model.addConstr(x[‘supplier1’,
‘roastery2’]==0,‘prohibit’)”toaddanadditionalconstrainttoanswertheuser’squestion.
Afterreceivingthecode,theCommanderwillcommunicatewiththeSafeguardtoscreenthecode
and ascertain its safety ( 4 ); once the code obtains the Safeguard’s clearance, marked by 5 , the
Commander will use external tools (e.g., Python) to execute the code and request the Writer to
interpret the execution results for the user’s question ( 6 and 7 ). For instance, the writer may
say“ifweprohibitshippingfromsupplier1toroastery2,thetotalcostwouldincreaseby10.5%.”
Bringing this intricate process full circle, the Commander furnishes the user with the concluding
answer( 8 ).
If at a point there is an exception - either a security red flag raised by Safeguard (in 5 ) or code
execution failures within Commander, the Commander redirects the issue back to the Writer with
essentialinformationinlogs( 6 ). So,theprocessfrom 3 to 6 mightberepeatedmultipletimes,
untileachuserqueryreceivesathoroughandsatisfactoryresolutionoruntilthetimeout. Thisentire
complexworkflowofmulti-agentinteractioniselegantlymanagedviaAutoGen.
ThecoreworkflowcodeforOptiGuidewasreducedfromover430linesto100linesusingAutoGen,
leadingtosignificantproductivityimprovement.Thenewagentsarecustomizable,conversable,and
canautonomouslymanagetheirchatmemories. Thisconsolidationallowsthecoderandinterpreter
rolestomergeintoasingle“Writer”agent,resultinginaclean,concise,andintuitiveimplementation
thatiseasiertomaintain.
26
 | 
 | Safeguard

