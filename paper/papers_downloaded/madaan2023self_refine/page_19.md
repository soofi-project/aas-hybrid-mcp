Method %OPT)
Purietal.(2021) HumanReferences 38.2
CODEX 13.1
GPT-3.5 14.8
OpenAIModels: OpenAI(2022,2023)
ChatGPT 22.2
GPT-4 27.3
Nijkampetal.(2022) CODEGEN-16B 1.1
SCALENE 1.4
Bergeretal.(2022) SCALENE(BEST@16) 12.6
SCALENE(BEST@32) 19.6
PIE-2B 4.4
PIE-2B(BEST@16) 21.1
PIE-2B(BEST@32) 26.3
PIE-16B 4.4
Madaanetal.(2023)
PIE-16B(BEST@16) 22.4
PIE-16B(BEST@32) 26.6
PIE-Few-shot(BEST@16) 35.2
PIE-Few-shot(BEST@32) 38.3
SELF-REFINEw/GPT-3.5 23.0
Thiswork SELF-REFINEw/ChatGPT 26.7
SELF-REFINEw/GPT-4 36.0
Table8: PerformancecomparisonofvariousmodelsonthePIEdatasetintermsofthepercentage
ofprogramsoptimized(%OPT). Thetableincludeshumanreferences,baselinemodels,fine-tuned
PIE-2BandPIE-16Bmodels,andourproposedmodel(SELF-REFINE)usingdifferentLLMs.Notably,
SELF-REFINEachievessuperiorperformancewhileusingonly4samplesatmost,significantlyfewer
thanthe16and32samplesemployedbyothermodels. Scalene, anoff-the-shelfoptimizer, uses
instructiontuningwithCodexandservesasacomparisonpoint.
19
