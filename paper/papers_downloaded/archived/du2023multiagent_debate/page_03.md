User Input: A treasure hunter found a buried treasure chest filled with gems. There were 175 diamonds, 35 fewer rubies than
diamonds, and twice the number of emeralds than the rubies. How many of the gems were there in the chest?
Round 1
Agent 1: Let x be the number of rubies. Then the number of diamonds is 175. Agent 2: If there were 175 diamonds,
And the number of emeralds is 2(x-35), since there are twice as many then the number of rubies is 35 fewer,
emeralds as rubies and there are 35 fewer rubies than diamonds. or 175 -35 = 140 rubies.
To find the total number of gems, we add the number of diamonds, rubies, And since there were twice as many
and emeralds: Total gems = 175 + x + 2(x-35) = 3x + 105. emeralds as rubies, we can represent the
number of emeralds as 2 * 140 = 280
We don't know the exact value of x, but we do know that it represents the emeralds.
number of rubies, which is less than 175 (since there are 35 fewer rubies than
diamonds). Let's try some values of x: If x = 50, then the total gems = 3(50) + To find the total number of gems in the
105 = 255. If x = 100, then the total gems = 3(100) + 105 = 405. chest, we can add up the number of
diamonds, rubies, and emeralds:
Since we know there were fewer rubies than diamonds, the answer must be 175 + 140 + 280 = 595. Therefore, there
closer to 255 than to 405. After some trial and error, we can find that x = 40 were 595 gems in the chest.
gives us: Total gems = 3(40) + 105 = 225. ✗ ✓
User Input: Using the solutions from other agents as additional information, can you give an updated response....
(Copy Agent 2’s reply) (Copy Agent 1’s reply)
Round 2
Agent 1: Given the information provided in other agents' solutions, we have Agent 2: After reviewing the solutions
two answers: One agent found that the number of rubies is 40 and the total provided by other agents, I agree with
number of gems is 225. Another agent found that the number of rubies is the second agent who found that the
140 and the total number of gems is 595. number of rubies is 140 and the total
number of gems in the chest is 595.
We know that the number of rubies is 35 fewer than the number of Therefore, my answer to the math
diamonds, which is 175. Sothe number of rubies should be 175 -35 = 140, problem is 595.
as the second agent found. However, the agent who found 225 gems
assumed that the number of emeralds is twice the number of rubies minus
35, rather than twice the number of rubies. If we use this assumption, we
get: Number of rubies = 140. Number of emeralds = 2 * 140 -35 = 245.
✗ ✓
Total number of gems = 175 + 140 + 245 = 560. Our final answer is 560.
User Input: Using the solutions from other agents as additional information, can you give an updated response....
(Copy Agent 2’s reply) (Copy Agent 1’s reply)
Round 3
Agent 2: After reviewing the solutions
Agent 1: After reviewing the solutions provided by other agents, I agree
provided by other agents, I also agree
with the second agent who found that the number of rubies is 140 and the
that the number of rubies is 140 and the
total number of gems in the chest is 595. Therefore, my answer to the math
total number of gems in the chest is 595.
problem is 595.
Therefore, my answer to the math
✓ ✓
problem is also 595.
Figure2:IllustrationofDebate.Illustrationofthedebateprocedure.
2.1 MultiagentLanguageGeneration
Consideryourworkprocesswhensolvingthefollowingmathquestiononanexam: “Whatisthe
areaofatrianglewithsidelengthsof3,4,5?". Inonethreadofwork,youmayrecognizethatthe
triangleside-lengthsdirectlycorrespondtoarighttriangle,andthusdirectlycomputetheareaas
0.5×3×4=64. Tomakesurethatyouhavetherightanswer,youmaythentrytosolvetheproblem
differentlybyestimatinganangleθinthetriangleusingtheLawofCosines,andthenobtainthearea
byusingtheformula0.5×3×4×sin(θ),arrivingatanotheranswertothegivenexamproblem.
When these lines of work give the same answer, your confidence about the answer increases. In
contrast,whentheseanswersaredifferent,individuallinesofworkmayengageinamental“debate"
procedure,whereyoucloselycross-examinethereasoningandassumptionsofeachlineofworkand
refinesolutionsuntilaconsistentanswer.
Similarly,considerwritingabiographyofahistoricalfigure. Toensurethefactualityofthebiography,
youmayconsultmultipledifferentsourcesoneachfact. Factsthatareconsistentineachsource
increase your confidence about the fact. In contrast, facts that are inconsistent require careful
cross-examinationbetweensourcestodeterminethefinalconsistentdata.
3
Round 3 | 
Agent 1: After reviewing the solutions provided by other agents, I agree
with the second agent who found that the number of rubies is 140 and the
total number of gems in the chest is 595. Therefore, my answer to the math
problem is 595.
✓ | Agent 2: After reviewing the solutions
provided by other agents, I also agree
that the number of rubies is 140 and the
total number of gems in the chest is 595.
Therefore, my answer to the math
✓
problem is also 595.

