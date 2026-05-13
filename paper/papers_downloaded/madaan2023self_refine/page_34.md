O MathReasoning
WeusetheGradeSchoolMath8k(GSM-8k)dataset(Cobbeetal.,2021)forevaluatingSELF-REFINE
onmathreasoning. Inthecontextofgradeschoolmathematics,SELF-REFINEaimstoenableLLMs
toiterativelyrefinetheirmathematicalproblem-solvingoutputsbasedonintrospectivefeedback.
FollowingGaoetal.(2022),wewritesolutionstothereasoningproblemsinPython. Considerthe
followingexamplefromthepaper,whereanerrorinthecodedemonstratesalackofunderstanding
oftheproblem:
def solution():
"""Twenty dozen cups cost $1200 less than the total cost of
half a dozen plates sold at $6000 each.
Calculate the total cost of buying each cup."""
plates = 6
plate_cost = 6000
cups = 12 * 20
cup_cost = plate_cost
result = cup_cost
return result
Byusing SELF-REFINE, wecanidentifytheerrorinthecodeandrefinethesolutionthroughan
iterativeprocessofintrospectionandfeedback:
# Let's go through the error and check step-by-step
plates = 6
plate_cost = 6000
# Let's check the other parts
cups = 12 * 20
cup_cost = plate_cost # wrong! The cost of a cup is not the same as the
cost of a plate.
(cid:44)→
# The cost of a cup is $1200 less than the total cost of half a dozen
plates sold at $6000 each.
(cid:44)→
half_dozen_plate_cost = 6 * plate_cost
cup_cost = half_dozen_plate_cost - 1200
SELF-REFINEisthusinstantiatednaturally:thegeneratorgeneratesaninitialsolution,andFEEDBACK
scansthesolutiontospoterrorsonwhichtoprovidefeedback. ThefeedbackissuppliedtoREFINEto
createanewsolution. FollowingWellecketal.(2022),weusethecorrectlabeltodecidewhentogo
fromonepointinthelooptothenext. Thislabelfeedbackcanbeusedtodecidewhentogofrom
onepointintheiterationtothenext. WeshowresultsusingSELF-REFINEinFigure14.
34
