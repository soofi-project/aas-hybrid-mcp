D GPT-4Evaluation
InlightoftheimpressiveachievementsofGPT-4inassessingandprovidingreasoningforcomplex
tasks,weleverageitsabilitiesforevaluationinSELF-REFINE. Theapproachinvolvespresenting
taskstoGPT-4inastructuredmanner,promotingthemodel’sdeliberationonthetaskandgenerating
arationaleforitsdecision. ThismethodologyisdemonstratedinListings1to3:
Listing1PromptforGPT-4evaluationofSentimentReversal.
f"""Which review is aligned with the sentiment {target_sentiment}?
Review A: {review_a}
Review B: {review_b}.
Pick your answer from ['Review A', 'Review B', 'both', 'neither']. Generate a
short explanation for your choice first. Then, generate 'The more aligned
(cid:44)→
review is A' or 'The more aligned review is B' or 'The more aligned review is
(cid:44)→
both' or 'The more aligned review is neither'.
(cid:44)→
Format: <explanation> <answer> STOP
Listing2PromptforGPT-4evaluationofAcronymGeneration.
f"""Title: {title}
Acronym A: {acronym_a}
Acronym B: {acronym_b}
Pick the better acronym for the given title. The acronyms should be compared based
on the following criteria:
(cid:44)→
* Ease of pronunciation.
* Ease of spelling.
* Relation to title.
* Positive connotation.
Generate your answer in the following format:
<Short explanation>. The better acronym is A OR The better acronym is B OR The
acronyms are equally good OR Neither acronym is good. STOP.
(cid:44)→
Listing3PromptforGPT-4evaluationofDialogueResponseGeneration.
f"""Which response is better given this context: {context}?
Response A: {response_a}
Response B: {response_b}.
Pick your answer from ['Response A', 'Response B', 'both', 'neither']. Generate a
short explanation for your choice first. Then, generate 'The better response
(cid:44)→
is A' or 'The better response is B' or 'The better response is both' or 'The
(cid:44)→
better response is neither'.
(cid:44)→
Format: <explanation> <answer> STOP
E ModelKey
Weuseterminologyhere: https://platform.openai.com/docs/models/gpt-3-5
17
