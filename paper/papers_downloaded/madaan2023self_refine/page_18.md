F Comparisonof SELF-REFINE withState-of-the-artofFew-ShotLearning
ModelsandFine-TunedBaselines
Inthissection,wepresentacomprehensivecomparisonoftheperformanceofSELF-REFINEwith
other few-shot models and fine-tuned baselines across a range of tasks, including mathematical
reasoningandprogrammingtasks. Tables8and7displaytheperformanceofthesemodelsonthe
PIEdatasetandGSMtasks,respectively. Ouranalysisdemonstratestheeffectivenessofdifferent
modelarchitecturesandtrainingtechniquesintacklingcomplexproblems.
Method SolveRate
Cobbeetal.(2021) OpenAI6B 20.0
Weietal.(2022) CoTw/CODEX 65.6
PaLw/CODEX 72.0
PaLw/GPT-3 52.0
Gaoetal.(2022)
PaLw/GPT-3.5 56.8
PaLw/ChatGPT 74.2
PaLw/GPT-4 93.3
Self-Correctw/GPT-3 45.9
Wellecketal.(2022)
Self-Correct(fine-tuned) 24.3
SELF-REFINEw/GPT-3 55.7
SELF-REFINEw/GPT-3.5 62.4
Thiswork
SELF-REFINEw/ChatGPT 75.1
SELF-REFINEw/GPT-4 94.5
Table7: Performancecomparisonofmodelsonmathreasoning(MathReasoning).
18
