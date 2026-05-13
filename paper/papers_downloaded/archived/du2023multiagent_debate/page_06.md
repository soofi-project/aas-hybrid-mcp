Model Arithmetic(%)↑ GradeSchoolMath(%)↑ Chess(∆PS)↑
SingleAgent 67.0±4.7 77.0±4.2 91.4±10.6
SingleAgent(Reflection) 72.1±4.5 75.0±4.3 102.1±11.9
Multi-Agent(Majority) 69.0±4.6 81.0±3.9 102.2±6.2
Multi-Agent(Debate) 81.8±2.3 85.0±3.5 122.9±7.6
Table1: MultiagentDebateImprovesReasoningMulti-agentdebateimprovesthereasoningabilitiesof
languagemodels.Multi-agentresultsinthetablearerunwith3agentsandtworoundsofdebate.
Prompt: Give a bullet point biography of David S. Johnson highlighting their contributions and
achievements as a computer scientist, with each fact separated with a new line character.
Round 1
Agent 1: --He earned his bachelor's degree from Agent 2: --David S. Johnson is an American
Dartmouth Collegein 1967 and his Ph.D. from computer scientist and mathematician. ✓
MIT in 1973. ✗
--Johnson was elected to the National Academy of
--Johnson has received numerous awards for his Engineering in 2006. ✓
research and contributions to computer science,
including the ACM Turing Awardin 2013. ✗ --He has been awarded numerous honors and
awards for his contributions to computer science,
--Johnson's research interests include ✓ including the ACM SIGMOD Innovations Award
optimization, algorithms, and complexity theory. and the Knuth Prize. ✗
Round 2
Agent 1: --David S. Johnson is a computer Agent 2: --David S. Johnson is an American
scientist and mathematician. ✓ computer scientist and mathematician. ✓
--Johnson was elected to the National --He has worked at several prestigious
Academy of Engineering in 2006. ✓ universities, including Columbia University, AT&T
Bell Laboratories, and Cornell University. ✗
--He has received numerous awards for his
contributions to computer science, --Johnson is known for his work in the field of
including the ACM Turing Awardin 2013 ✗ algorithms, particularly in the areas of network
and the Knuth Prize. optimization, combinatorial optimization, and
scheduling theory. ✓
Figure7:IllustrationofGeneratingBiographies.Illustrationofgeneratingbulletbiographiesofcomputer
scientists.Forbrevity,onlythefirst3generatedbulletsareshown.
QualitativeResults. InFigure 4,5,weprovidequalitativeillustrationsofthedebateprocedure
betweenmodels. Interestingly,wefindcasesinwhichallmodelsinitiallygiveanincorrectresponse,
yettheresultofdebatestillobtainsthecorrectanswerasagentscritiqueeachothers’reasoning. Thus,
thepurposeofourdebateisn’tjusttoamplifyacorrectanswer–allmodelscaninitiallybewrong
butarriveatthecorrectanswerthroughthedebateprocess.
Compatibility with other reasoning methods. Our multiagent generation procedure operates
orthogonally approach to other prompting methods which focus on single-agent generation. In
Figure6,weillustratetheperformanceofmulti-agentdebatewithandwithoutzero-shotchain-of-
thoughtprompting[11]onGSM8K.Inbothsettings,multiagentgenerationisbeneficial.
3.2 ExtractingFactualInformationfromMultiagentDebate
Wenextevaluatetheextenttowhichmultiagentdebateimprovestheunderlyingfactualityinlanguage
models.
Tasks. Weevaluatethefactualityoflanguagemodelsinthreedifferentsettings:
• Biographies. To evaluate the factuality of language models, we introduce a novel task of
accurately generating historical biographies of people. In preliminary testing, we found that
existinglanguagemodelshadatendencytohallucinatemanyfactsonthistask. Weconstructed
ground truth bullet point biographies of 524 well-known computer scientists. We then asked
languagemodelstogeneratebulletpointbiographiesforeachperson,andevaluatedtheaccuracyat
whicheachgroundtruthbulletpointagreedwithgeneratedbullets. Wereportadditionalevaluation
detailsintheAppendix.
6
