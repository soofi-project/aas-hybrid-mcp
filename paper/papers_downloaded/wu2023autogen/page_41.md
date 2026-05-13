Table 17: Application A1, Scenario 1: Autonomous math problem-solving. Preliminary test with
CAMEL.Weconstructedtworoles: “MathSolver”and“PythonProgrammer”. Theresultingcode
cannotbeexecuted. Theconversationcontinues,andtherolesarenotkeenonsolvingtheproblem
andgivingananswer.
Action CAMEL
g Settaskprompt Completelysimplifyandrationalizethedenominator:
√ √
160 245
√ ×√
252 108
(cid:240) System **************Assistant sys message************* AI SystemMessage(rolename=‘Python Programmer’,
roletype=<RoleType.ASSISTANT: ‘assistant’>, metadict=‘task’: ‘Using Python programming language, write a pro-
gramthatacceptsfourintegersasinput,appliessquarerootfunctiontoeach,simplifiesandrationalizesthedenominatorofthe
√ √
fractionresultingfromthemultiplicationoftwofractions: √160 × √245,andreturnsthesimplifiedexpression.’,‘assis-
252 108
tantrole’:‘PythonProgrammer’,‘userrole’:‘MathSolver’,role=‘system’,content=‘NeverforgetyouareaPythonProgrammer
andIamaMathSolver.Neverfliproles!...)
**************AIUsersysmessage*************
SystemMessage(rolename=‘MathSolver’,roletype=<RoleType.USER:‘user’>,metadict=‘task’:‘UsingPythonprogramming
language,writeaprogramthatacceptsfourintegersasinput,appliessquarerootfunctiontoeach,simplifiesandrationalizesthe
√ √
denominatorofthefractionresultingfromthemultiplicationoftwofractions: √160 × √245,andreturnsthesimplified
252 108
expression.’,‘assistantrole’:‘PythonProgrammer’,‘userrole’:‘MathSolver’,role=‘system’,content=‘Neverforgetyouarea
MathSolverandIamaPythonProgrammer. Neverfliproles! Youwillalwaysinstructme.Weshareacommoninterestin
collaboratingtosuccessfullycompleteatask.Imusthelpyoutocompletethetask.Hereisthetask:UsingPythonprogramming
language,writeaprogramthatacceptsfourintegersasinput,appliessquarerootfunctiontoeach,simplifiesandrationalizes
√ √
thedenominatorofthefractionresultingfromthemultiplicationoftwofractions: √160 × √245,andreturnsthesimplified
252 108
expression.....)
**************Originaltaskprompt*************
√ √
Completelysimplifyandrationalizethedenominator: √160×√245
252 108
**************Specifiedtaskprompt*************
UsingPythonprogramminglanguage,writeaprogramthatacceptsfourintegersasinput,appliessquarerootfunctiontoeach,
√ √
simplifiesandrationalizesthedenominatorofthefractionresultingfromthemultiplicationoftwofractions: √160 × √245,
252 108
andreturnsthesimplifiedexpression.
**************Finaltaskprompt*************
UsingPythonprogramminglanguage,writeaprogramthataccepts...
g AIUser Instruction:Importthenecessarylibrariesforthetask.Input:None
(cid:240) AIAssistant Solution:Tosolvethistask,wewillneedthe‘math‘libraryforthesquarerootfunctionandthe‘fractions‘librarytosimplifythe
resultingfraction.Hereishowtoimporttheselibraries:
1 import math
2 from fractions import Fraction
The‘math‘libraryprovidesfunctionsthatdealwithmathematicaloperations.The‘sqrt‘function,whichwewilluseinthistask,is
partofthislibrary.
The‘fractions‘libraryprovidesfunctionsforcreatingandmanipulatingrationalnumbers.The‘Fraction‘function,whichwewill
usetosimplifytheresultingfraction,ispartofthislibrary.
Nextrequest.
g AIUser Instruction:Defineafunctionthatacceptsfourintegersasinput.Input:None
(cid:240) AIAssistant Solution:Let’sdefineafunctionnamed‘simplifyfraction‘thatacceptsfourintegersasinput. Theseintegerswillrepresentthe
numbersunderthesquarerootinthefractions.
1 def simplify_fraction(a, b, c, d):
2 pass
Inthisfunction,‘a’,‘b’,‘c’,and‘d’aretheparametersthatwillacceptthefourintegersasinput. The‘pass’statementisa
placeholderandwillbereplacedwithactualcodeinthenextsteps.
Nextrequest.
g AIUser Instruction:Insidethefunction,applythesquarerootfunctiontoeachoftheinputintegers.Input:None
(cid:240) AIAssistant Solution:Wewillusethe‘math.sqrt’functionfromthe‘math’librarytoapplythesquareroottoeachoftheinputintegers.Hereis
howtodoit:
1 def simplify_fraction(a, b, c, d):
2 sqrt_a = math.sqrt(a)
3 sqrt_b = math.sqrt(b)
4 sqrt_c = math.sqrt(c)
5 sqrt_d = math.sqrt(d)
Inthiscode,‘sqrta’,‘sqrtb’,‘sqrtc’,and‘sqrtd’arevariablesthatstorethesquarerootoftheinputintegers‘a’,‘b’,‘c’,and‘d’
respectively.
Nextrequest.
g Human Abort
41
1 import math
2 from fractions import Fraction

1 def simplify_fraction(a, b, c, d):
2 pass

1 def simplify_fraction(a, b, c, d):
2 sqrt_a = math.sqrt(a)
3 sqrt_b = math.sqrt(b)
4 sqrt_c = math.sqrt(c)
5 sqrt_d = math.sqrt(d)

