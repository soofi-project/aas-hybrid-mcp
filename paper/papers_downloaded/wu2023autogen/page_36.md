Table 11: Application A1, Scenario 1: Autonomous math problem-solving. AutoGPT on the first
qualitativeexample. Weabortasthecodeneverprintstheresult,andthesystemdoesnotrectifyit
after2turns. AutoGPTismuchmoreverbosecomparedtootherframeworks. Wehaveshortened
someunnecessarycontent.
Action AutoGPT
System Welcomeback!WouldyoulikemetoreturntobeingMathSolverGPT?Askinguserviakeyboard...Continuewiththelastsettings?
Name:MathSolverGPT
Role:anintelligentmath-solvingAIthatassistsstudents,professionals,...
Goals:[’Providestep-by-stepsolutionstomathproblems,ensuringclarityandunderstandingfortheuser...
Continue(y/n):
g Human y
System MathSolverGPThasbeencreatedwiththefollowingdetails:Name:MathSolverGPT
Role:anintelligentmath-solvingAIthatassistsstudents,professionals,andenthusiastsinsolvingawiderangeofmathproblems,frombasic
arithmetictoadvancedcalculusandbeyond.
Goals:-Providestep-by-stepsolutionstomathproblems,ensuringclarityandunderstandingfortheuser.-Offerexplanationsandinsights
intotheunderlyingconceptsandprinciplesbehindthesolutions,fosteringadeeperunderstandingofmathematics.-Handleavarietyofmath
problemtypes,includingalgebra,geometry,trigonometry,calculus,andmore....
(cid:240) MATHSOLVERGPTTHOUGHTS:Withoutaspecifictaskorquestion,it’sdifficulttodetermineexactlyonecommandtouse.Theuserhasn’t
providedanycontextorproblemtosolve.
REASONING:Theuser’srequestistoovague.Theyhaven’tspecifiedwhattheywantmetodoorwhatproblemtheywantmetosolve.
PLAN:-Asktheuserformoreinformationoraspecifictask.
CRITICISM:Ishouldhaveaskedtheuserformoreinformationoraspecifictaskinthefirstplace.
SPEAK:Couldyoupleaseprovidemoreinformationorspecifyatask?
NEXTACTION:COMMAND=ARGUMENTS={}
System Enter‘y’toauthorisecommand,‘y-N’torunNcontinuouscommands,‘n’toexitprogram,orenterfeedbackforMathSolverGPT...Asking
userviakeyboard...
g Human Completelysimplifyandrationalizethedenominator: √ √
160 245
√ ×√
252 108
(cid:240) MATHSOLVERGPTTHOUGHTS:Tosolvethisproblem,Ineedtosimplifyandrationalizethedenominatorofthegivenexpression.This
involvessimplifyingthesquarerootsandthenmultiplyingthefractions. IcanusePython’smathlibrarytocalculatethesquarerootsand
performthemultiplication.
REASONING:Theprobleminvolvessimplifyingsquarerootsandmultiplyingfractions.Python’smathlibraryprovidesfunctionsforthese
operations.
PLAN:-WriteaPythonscripttocalculatethesquarerootsandmultiplythefractions.-Executethescripttogetthesimplifiedexpression.
CRITICISM:IneedtoensurethatIcorrectlycalculatethesquarerootsandperformthemultiplication.Ishouldalsomakesuretorationalize
thedenominator,astheproblemspecifies.
SPEAK:Let’ssimplifyandrationalizethedenominatorofthegivenexpression.
NEXTACTION:COMMAND=executepythoncodeARGUMENTS=
1 {’code’: ’import math\n\n# Calculate the square roots\nsqrt_160 = math.sqrt
(160)\nsqrt_252 = math.sqrt(252)\nsqrt_245 = math.sqrt(245)\nsqrt_108 =
math.sqrt(108)\n\n# Multiply the fractions\nresult = (sqrt_160 / sqrt_252
) * (sqrt_245 / sqrt_108)\n\n# Simplify the result\nsimplified_result =
math.simplify(result)\n\nsimplified_result’, ’name’: ’simplify_expression
’}
g Human y
System -=-=-=-=-=-=-=COMMANDAUTHORISEDBYUSER-=-=-=-=-=-=-=
Executingpythonfile’/app/autogpt/workspa...
SYSTEM:Commandexecutepythoncodereturned:Error:Traceback(mostrecentcalllast):File“...”,line13,in¡module¿simplifiedresult
=math.simplify(result)AttributeError:module’math’hasnoattribute’simplify’
(cid:240) MATHSOLVERGPTTHOUGHTS:Theerrormessageindicatesthatthe‘math’moduleinPythondoesnothavea‘simplify’function.Ineed
tousethe‘sympy’libraryinstead,whichprovidesafunctionforsimplifyingexpressions.
REASONING:The‘math’moduleinPythondoesnotprovideafunctionforsimplifyingexpressions.The‘sympy’library,ontheotherhand,
doesprovidesuchafunction.
PLAN:-RewritethePythonscripttousethe‘sympy’libraryinsteadofthe‘math’module.-Executethescripttogetthesimplifiedexpression.
CRITICISM:Ishouldhaveknownthatthe‘math’moduledoesnotprovideafunctionforsimplifyingexpressions. Ishouldhaveusedthe
‘sympy’libraryfromthestart.SPEAK:Let’stryagainusingthe‘sympy’librarytosimplifytheexpression.
NEXTACTION:COMMAND=executepythoncodeARGUMENTS=
1 {’code’: ’import sympy as sp\n\n# Calculate the square roots\nsqrt_160 = sp.
sqrt(160)\nsqrt_252 = sp.sqrt(252)\nsqrt_245 = sp.sqrt(245)\nsqrt_108 =
sp.sqrt(108)\n\n# Multiply the fractions\nresult = (sqrt_160 / sqrt_252)
* (sqrt_245 / sqrt_108)\n\n# Simplify the result\nsimplified_result = sp.
simplify(result)\n\nsimplified_result’, ’name’: ’simplify_expression’}
g Human y
System SYSTEM:Commandexecutepythoncodereturned:
(cid:240) MATHSOLVERGPTTHOUGHTS:Thecommandexecutiondidn’treturnanyoutput,whichisunusual.Itseemstheremightbeanissuewith
theexecutionofthePythoncode.Ineedtodebugthis.
REASONING:ThePythoncodeexecutionshouldhavereturnedaresult.Theabsenceofaresultsuggeststhattheremightbeanissuewiththe
codeoritsexecution.
PLAN:-ReviewthePythoncodetoidentifyanypotentialissues.-Ifnecessary,modifythecodeandexecuteitagain.CRITICISM:Ishould
haveensuredthatthePythoncodewascorrectandwouldproducearesultbeforeexecutingit.SPEAK:Itseemstherewasanissuewiththe
executionofthePythoncode.Let’stryagain.
NEXTACTION:COMMAND=executepythoncodeARGUMENTS=...(Exactsamecodeaslast)
System SYSTEM:Commandexecutepythoncodereturned:
(cid:240) MATHSOLVERGPTTHOUGHTS:ThePythoncodeexec3ut6ionstillisn’treturninganyoutput.It’spossiblethattheissuelieswiththecalcu-
lationofthesquareroots...
g Human control+C(Aborted)
1 {’code’: ’import math\n\n# Calculate the square roots\nsqrt_160 = math.sqrt
(160)\nsqrt_252 = math.sqrt(252)\nsqrt_245 = math.sqrt(245)\nsqrt_108 =
math.sqrt(108)\n\n# Multiply the fractions\nresult = (sqrt_160 / sqrt_252
) * (sqrt_245 / sqrt_108)\n\n# Simplify the result\nsimplified_result =
math.simplify(result)\n\nsimplified_result’, ’name’: ’simplify_expression
’}

1 {’code’: ’import sympy as sp\n\n# Calculate the square roots\nsqrt_160 = sp.
sqrt(160)\nsqrt_252 = sp.sqrt(252)\nsqrt_245 = sp.sqrt(245)\nsqrt_108 =
sp.sqrt(108)\n\n# Multiply the fractions\nresult = (sqrt_160 / sqrt_252)
* (sqrt_245 / sqrt_108)\n\n# Simplify the result\nsimplified_result = sp.
simplify(result)\n\nsimplified_result’, ’name’: ’simplify_expression’}

