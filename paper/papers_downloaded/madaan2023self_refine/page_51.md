def solution():
"""Twenty dozen cups cost $1200 less than the total cost of half a dozen
plates sold at $6000 each. Calculate the total cost of buying each
(cid:44)→
cup."""
(cid:44)→
plates = 6
plate_cost = 6000
cups = 12 * 20
cup_cost = plate_cost
result = cup_cost
return result
# There is an error in the code above because of lack of understanding of the
question. What is the error? To find the error, go through semantically
(cid:44)→
complete blocks of the code, and check if everything looks good.
(cid:44)→
# Let us go through the error and check step-by-step
plates = 6
plate_cost = 6000
# looks good
# Let's check the other parts
cups = 12 * 20
cup_cost = plate_cost
# wrong! The cost of a cup is not the same as the cost of a plate. The cost of a
cup is $1200 less than the total cost of half a dozen plates sold at $6000
(cid:44)→
each. So we need to calculate the cost of a cup first (total cost of half a
(cid:44)→
dozen plates sold at $6000 each - $1200) and use that.
(cid:44)→
Okay! Here is the rewrite:
def solution():
"""Twenty dozen cups cost $1200 less than the total cost of half a dozen
plates sold at $6000 each. Calculate the total cost of buying each
(cid:44)→
cup."""
(cid:44)→
plates = 6
plate_cost = 6000
cups = 12 * 20
total_cup_cost = (plate_cost * plates) - 1200
cost_per_cup = total_cup_cost / cups
return cost_per_cup
Figure32: REFINEpromptforMathReasoning
51
 |  | 
 | def solution():
"""Twenty dozen cups cost $1200 less than the total cost of half a dozen
plates sold at $6000 each. Calculate the total cost of buying each
(cid:44)→
cup."""
(cid:44)→
plates = 6
plate_cost = 6000
cups = 12 * 20
cup_cost = plate_cost
result = cup_cost
return result
# There is an error in the code above because of lack of understanding of the
question. What is the error? To find the error, go through semantically
(cid:44)→
complete blocks of the code, and check if everything looks good.
(cid:44)→
# Let us go through the error and check step-by-step
plates = 6
plate_cost = 6000
# looks good
# Let's check the other parts
cups = 12 * 20
cup_cost = plate_cost
# wrong! The cost of a cup is not the same as the cost of a plate. The cost of a
cup is $1200 less than the total cost of half a dozen plates sold at $6000
(cid:44)→
each. So we need to calculate the cost of a cup first (total cost of half a
(cid:44)→
dozen plates sold at $6000 each - $1200) and use that.
(cid:44)→
Okay! Here is the rewrite:
def solution():
"""Twenty dozen cups cost $1200 less than the total cost of half a dozen
plates sold at $6000 each. Calculate the total cost of buying each
(cid:44)→
cup."""
(cid:44)→
plates = 6
plate_cost = 6000
cups = 12 * 20
total_cup_cost = (plate_cost * plates) - 1200
cost_per_cup = total_cup_cost / cups
return cost_per_cup | 
 |  | 

