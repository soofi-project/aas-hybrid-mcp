# **The Berkeley Function Calling Leaderboard (BFCL): From Tool Use to Agentic Evaluation of Large ...

Source: bfcl2024.pdf


---

### Page 1

**The Berkeley Function Calling Leaderboard (BFCL): From Tool Use to Agentic Evaluation of Large Language Models** 

## correctness, and effectiveness in function invocation. 

Evaluating LLMs’ function-invocation capabilities poses unique challenges because deterministic validation typically requires executing the corresponding functions which complicates large-scale evaluation. BFCL overcomes this by introducing a novel validation strategy that obviates the need for function execution. Drawing inspiration from programming language literature, we employ Abstract Syntax Tree (AST) sub-string matching as a proxy for actual function execution, thereby facilitating scalable evaluations. To validate this approach, we utilize a subset of our dataset to evaluate models using the earlier mentioned execution approach and observe a strong correlation between BFCL’s execution and AST metrics. 

As models increasingly incorporate function calling capability, our phased release lets us compare if BFCL’s single-turn dataset has possibly leaked into the training data of the latest models. To investigate this, through CharNLL as a measure, we compare LLMs’ familiarity with the single-turn dataset against that of the crowd-sourced dataset which was released six months apart. 

In summary, this work makes the following contributions: 

1. BFCL is a diverse dataset of 5 _,_ 551 question-functionanswer pairs across multiple programming languages, including Python, Java, JavaScript, REST APIs, and SQL. This diversity ensures a comprehensive assessment of LLMs’ function-calling ability across a range of domains and use cases. 

2. A novel application of Abstract Syntax Trees (AST) based sub-string matching to serve as a proxy for function execution and enabling scalable, deterministic validation of function calls. 

3. The first inclusion of community-contributed, realworld user queries and functions in function-calling evaluations, providing a more accurate representation of practical complexities and use cases. 

## **2. Related Work** 

**Language Models Using Tools.** Function calling (Schick et al., 2023) extends the capabilities of LLMs beyond its own knowledge base by enabling them to interact with external tools and APIs. Unlike structured output (Zhong & Chen, 2021), function calling allows LLMs to perform tasks requiring real-time data or external computation (Attouche et al., 2024). Models like GPT-4 (OpenAI, 2024) have demonstrated early ability to generate structured JSON for function invocation, prompting research into leveraging API calls as functions. More recent models have natively integrated function calling, empowering them to interact 

**==> picture [235 x 235] intentionally omitted <==**

Figure 1: This chart visualizes the diverse categories within BFCL. The inner ring represents the four major sections, the middle ring specifies their respective evaluation methods, and the outer ring highlights each category. Numbers indicate the total number of datapoints in each category. 

with external systems for knowledge retrieval (Sasaki et al., 2024) and real-time interaction. Furthermore, advancements like the LLMCompiler (Kim et al., 2024) optimize this process through parallel function execution, improving both efficiency and accuracy. This integration of function calling represents a crucial step towards more capable and versatile LLMs and subsequently unlocks broad agentic behaviors. 

**Benchmark for Function Calling.** Quite a few benchmarks have been proposed to test LLM’s ability to perform function calling, in this work, we focus on those designed to evaluate a model’s native function-calling capabilities, rather than methods that rely on prompt-based or code-generation approaches (e.g., Nexus Raven (team, 2023) uses a promptbased protocol, and AppWorld (Trivedi et al., 2024) emphasis code generation capability). Among benchmarks that do evaluate native function calling, many such as App Blend (Basu et al., 2024) and API Bench (Patil et al., 2024) focus solely on single-turn interactions. Although TinyAgent (Erdogan et al., 2024) addresses nested function calls, it does so by using placeholder variables instead of letting the model see the actual execution output of earlier calls; in effect, it still operates under a single-turn framework. 

For benchmarks that truly cover multi-turn interactions, most are constrained by a narrow domain scope or a limited set of functions. TauBench (Yao et al., 2024), for example, supports only 28 functions spanning two domains (airline and retail), and RestBench (Song et al., 2023) offers scenarios solely within the TMDB and Spotify domains. The

### Page 2

**The Berkeley Function Calling Leaderboard (BFCL): From Tool Use to Agentic Evaluation of Large Language Models** 

narrow coverage ( _<_ 150 entries) is more prone to overfitting and does not sufficiently reflect the breadth of realworld function-calling scenarios. Furthermore, benchmarks like ToolSandBox (Lu et al., 2024) and TauBench (Yao et al., 2024) rely on LLMs to simulate user queries. Despite careful attempt to control the user simulator’s behavior, LLM-based users remain prone to hallucination and instruction-following errors, which confound evaluation. 

Other works, such as ToolBench (Qin et al., 2023), depend solely on Rapid APIs that are subject to high variance in performance, making reproducibility a challenge. While the subsequent StableToolBench (Guo et al., 2025) version mitigates this by caching or simulating API responses, it continues to rely on LLM-based evaluators for determining response solvability, thus risking model-induced biases and undermining objectivity (e.g., GPT-family models tending to favor responses from their own model (Panickssery et al., 2024)). Similar issues exist in T-Eval (Chen et al., 2024), which also depends on LLM-based evaluation. 

Lastly, current benchmarks uniformly employ LLM-curated user queries, limiting their ability to accurately reflect genuine user interactions. 

Our benchmark directly addresses these shortcomings by incorporating deterministic evaluation metrics, an extensive and diverse set of robust multi-turn interactions, and a unique multilingual dataset derived from real-world, usercontributed queries that have more than 15 languages represented in user queries, including Chinese, French, Japanese, and Korean, etc. Additionally, on top of Python and REST (which are commonly covered in existing benchmarks), we also have entries in Java and JavaScript for more diverse programming languages. 

Collectively, these enhancements enable a more comprehensive, fair, and reproducible assessment of LLM function calling, setting our benchmark apart from existing efforts. 

**Impact:** Since it’s preview, BFCL has become the defacto evaluation for function calling used by all leading labs developing large language models (MetaAI, 2024; Team, 2025; Cohere, 2025). The leaderboard is constantly evolving and is in it’s current iteration (v4). This paper collapses the timeline and condenses all the learnings 

## **3. Berkeley Function Calling Leaderboard** 

BFCL employs a structured data curation pipeline to construct our benchmarking dataset across different categories. The pipeline follows five stages: **data collection** sources functions from online repositories, APIs, and user queries; **data pre-processing** extracts and structures key function attributes; **data generation** standardizes functions and user queries into a schema that can be presented to the 

**==> picture [235 x 105] intentionally omitted <==**

Figure 2: Examples of single-turn function-calling scenarios to illustrate multiple, parallel, and irrelevance entry types outlined in Section 3.1. 

LLMs; **data transformation** augments data with incomplete queries, and **data validation** ensures consistency and correctness through comprehensive unit-tests. 

## **3.1. Single-turn Dataset** 

We classify single turn function-calling scenarios into five types based on the number of available tools and their invocation patterns. **Simple** involves one tool with a single invocation, whereas **Multiple** includes several tools each invoked once. **Parallel** scenarios feature multiple invocations of a single tool, and **Parallel Multiple** combines multiple tools with multiple invocations. **Irrelevance** refers to cases where tools are available but not invoked. Detailed definitions are provided in Appendix C. 

We evaluate function calling through two methods: ASTbased substring matching and executable tests. For ASTbased evaluation, we curate functions in Python, Java, and JavaScript from popular GitHub repositories, filtering out trivial ones. For executable tests, we include (1) Python functions covering mathematical and physical computations, and (2) API-wrapped functions emulating real-world services (e.g., currency exchange and geocoding). Functions are standardized into a schema to avoid inconsistent documentation and ensure fair model comparisons. We further increase complexity by generating multiple and parallel calls, adding distractor functions, and testing robustness with missing parameters. See Appendix E for details. 

## **3.2. Crowd-sourced Dataset** 

The crowd-sourced dataset contains 64,517 real single-turn user queries collected between 2024-02-26 and 2024-04-01, representing genuine function-call interactions from users. We remove duplicates via ROUGE-L and embedding based similarity, and exclude queries from public sets to avoid contamination. Human experts minimally edit queries for clarity and adherence to our function schema, preserving their original semantics. See Appendix E.2 for details. This dataset has the same dataset structure and categories as Section 3.1.

### Page 3

**The Berkeley Function Calling Leaderboard (BFCL): From Tool Use to Agentic Evaluation of Large Language Models** 

## **3.3. Multi-turn Dataset** 

**Multi-turn** covers an entire conversation between the user and the assistant. Each conversation includes multiple **turns** —a new user message—and each turn may involve one or more **steps** —individual interactions between the assistant and a tool or environment. 

Our multi-turn dataset evaluates the LLMs’s ability to handle queries that evolve over multiple turns. It is divided into four categories: **Base** category covers the basic multi-turn user queries asking everyday tasks and providing all necessary information. **Missing Parameters** tests the model’s ability to recognize when critical parameter information is missing from the user request and cannot be inferred from the system. **Missing Functions** tests the model to identify when no available function can fulfill the user request. **Long Context** challenges the model’s ability to maintain accuracy in multi-turn long context queries or function call results. Detailed definitions are provided in Appendix D. 

To construct the dataset, we developed a custom API codebase across diverse domains like vehicle control, ensuring full transparency of API state and design. **Data generation** involves task generation of multi-turn queries that describe real-world tasks, along with specified initial API state configurations and function documents. Human annotators label ground truth trajectories from the generated multi-turn queries. **Data validation** includes question completeness, initial state verification, and function call sequence alignment with human-labeled ground truth. Detailed data generation and validation processes are outlined in Appendix E.3. 

## **3.4. Agentic Dataset** 

The Agentic dataset is divided into three categories. We describe them in detail below. They share similar data curation pipeline as the single-turn dataset in Section 3.1. 

## 3.4.1. WEB SEARCH DATASET 

For this category, the LLM has two tools: a DuckDuckGo search function that retrieves webpage titles, snippets, and URLs, and a fetch function that extracts full webpage content. To ensure fairness across models with varying knowledge cutoffs, questions focus on recent but stable information, such as the 2024 TIME Person of the Year, rather than constantly changing data like stock prices. 

## 3.4.2. MEMORY DATASET 

Our memory dataset spans **five distinct domains** , each chosen to reflect a practical, real-world use case for LLMs— _college advising, customer support, medical assistant_ , etc. Within every domain, the model is first given a concise _setting prompt_ (e.g., “You are an academic advisor helping a sophomore plan their coursework”) and then 

participates in a sequence of consecutive conversations that gradually reveal user-specific facts. After each domain-level dialogue block, we record a _memory snapshot_ . Evaluation queries are issued with an _empty chat history_ but access to the stored snapshot, probing whether the model can accurately retrieve, add, overwrite, or delete information that was mentioned minutes (short-term) or many turns (long-term) earlier. This design lets us measure how well the model maintains and updates memory across both topic boundaries and temporal gaps, mirroring real deployment scenarios where sustained, personalized assistance is critical. 

## 3.4.3. SQL DATASET 

Each question in the SQL category can be succinctly translated into an SQL query. Traditional text-to-SQL tasks typically involve prompting language models to generate a valid SQL query, then evaluating the result via exact string matching or by querying a predefined database. In BFCL, however, we adopt a more structured approach by supplying the LLM with a JSON-based schema that defines fundamental SQL operations (e.g., SELECT, INSERT, UPDATE, DELETE). Each operation includes detailed structured parameters needed for a complete SQL query (e.g., WHERE, LIMIT, JOIN). This schema allows for a deterministic translation of function calls into SQL queries and supports nested or more complex queries through the composition of multiple function calls. 

## **4. Evaluation Methodology** 

BFCL employs tailored evaluation protocols for each dataset category. The **Single-Turn** category use both _AST-substring matching_ (Section 4.1) and _execution-response matching_ (Section 4.2), whereas the **Crowd-Sourced** category relies solely on the AST matcher. The **Multi-Turn** category combines a _state-based_ and a _response-based_ checker (Section 4.4), and the **Agentic** category is evaluated with a strict _exact-match_ criterion (Section 4.5). 

We later quantify the agreement among the AST substringmatching and execution-response matching metrics (Section 4.3) to validate the reliability of the AST approach, highlight differences in inference strategies for prompt-only versus function-calling models (Section 5.1), and, finally, leverage perplexity ratios on the single-turn and crowdsourced settings to detect potential data contamination in the BFCL single-turn corpus. 

## **4.1. AST Substring Matching** 

Evaluating function calls by direct execution can be challenging due to the limited availability of executable functions and the laborious process of manual implementation, which curtails the diversity of functions available for testing.

### Page 4

**The Berkeley Function Calling Leaderboard (BFCL): From Tool Use to Agentic Evaluation of Large Language Models** 

**==> picture [219 x 128] intentionally omitted <==**

Figure 3: The Abstract Syntax Tree (AST) based evaluation (AST Summary) are strongly correlated with the evaluation by executing the functions (Exec Summary) validating AST as a reliable off-line evaluation methodology. 

To address this, we introduce an Abstract Syntax Tree (AST) substring matching approach that preserves alignment with execution-based evaluation without actual execution. 

We restrict the model’s output to Python-callable function calls using prompt-based instructions, then extract function names and parameters through Python’s ast module. Instead of requiring exact parameter matches, we verify that each parameter belongs to a predefined set of valid values. A function call is correct if the function name matches exactly and if all parameter values fall within their respective possible answers. For details on the AST matching rules, please refer to Appendix H. 

## **4.2. Execution Response Matching** 

Execution response matching involves validating function calls by executing them and comparing the results against expected outcomes. There are three ways we compare the response. For functions that output deterministic results, we check for exact-match of the response. For functions whose outputs are time sensitive, we execute the ground truth function call and the model’s output function call simultaneously and match the results, accounting for real-time value fluctuations. For nested lists or dictionaries, we perform structure matching, which only checks the length of the list and the presence of the dictionary key. 

## **4.3. AST Matching Performance** 

By comparing the scores and relative rankings on the BFCL single-turn dataset, evaluated using AST and Execution in Figure 3, we observe a strong correlation between AST scores and execution-based performance. This suggests that AST matching serves as a reliable indicator of model effectiveness in real-world scenarios. 

## **4.4. State & Response Based Evaluation** 

For multi-turn tasks, we employ two checks after each turn: **state-based** and **response-based** . An entry is correct only 

if it passes both checks in all turns. 

State-Based Evaluation compares the system’s final state after each turn (i.e., after all function calls) with the groundtruth state. Multiple sequences of function calls can achieve the same result, but the final state must match the labeled outcome. This approach captures modifications to the system (e.g., creating files or removing stocks from a watchlist). 

Response-Based Evaluation verifies that the model follows the necessary sequence of function calls (the _minimal viable execution result path_ ) to produce the requested output. This is critical for read-only requests (e.g., retrieving stock prices), where we want to ensure the model calls the appropriate functions rather than guessing the result. 

While state-based evaluation is a powerful technique, it cannot detect whether non-state-changing functions (e.g., get ~~z~~ ipcode ~~b~~ y ~~c~~ ity or estimate ~~d~~ istance) were actually invoked. We need response-based checks to confirm the model is reasoning through the task reliably (e.g., calling get ~~z~~ ipcode ~~b~~ y ~~c~~ ity(City ~~N~~ ame) before get ~~w~~ eather ~~b~~ y ~~z~~ ipcode(City ~~Z~~ ipcode)). By combining both types of evaluation, BFCL provides deeper insight into the model’s correctness and decisionmaking process. 

## **4.5. Exact-Match Evaluation** 

During evaluation, the model is given explicit formatting instructions through the system prompt detailed in Appendix J. We evaluate only the dedicated answer field with a strict exact-match criterion. Focusing on this individual field prevents spurious positives that would occur if the reference phrase appeared incidentally inside a longer, unclear sentence. For example, consider a yes/no question: a reply such as “I am not sure because no relevant information was found” contains the token “no,” but the model has not actually committed to the negative answer. By isolating the answer field, such cases are not erroneously marked as correct responses. 

Before matching, both candidate and reference answers are normalized—converted to lowercase and stripped of punctuation—using the same procedure as in our AST-based evaluation. A prediction is deemed correct if and only if the normalized strings are identical. 

## **5. Results and Analysis** 

## **5.1. Accuracy** 

Table 1 presents the evaluation results of various LLMs on BFCL. While the top-performing models excel in singleturn, crowd-sourced, and hallucination-related metrics, there remains significant room for improvement in multi-turn and agentic tasks, particularly in memory management.

### Page 5

**The Berkeley Function Calling Leaderboard (BFCL): From Tool Use to Agentic Evaluation of Large Language Models** 

Table 1: Evaluating different LLMs on BFCL. The categories are defined in Section 4 

|Model<br>Overall Acc|Singl|e Turn|Crowd Sourced|Hallucination Measure|Multi Turn|Agentic|
|---|---|---|---|---|---|---|
||AST|Execute|AST|Irrelevance<br>Relevance|Base<br>Miss Func<br>Miss Param<br>Long Context|Web Search<br>Memory<br>SQL|
||Simple<br>Multiple<br>Parallel<br>Parallel Multiple|Simple<br>Multiple<br>Parallel<br>Parallel Multiple|Simple<br>Multiple<br>Parallel<br>Parallel Multiple||||
|gpt-4o-2024-11-20 (Prompt)<br>**66.4**<br>gpt-4o-2024-11-20 (FC)<br>65.8<br>GPT-4-turbo-2024-04-09 (FC)<br>60.9<br>GPT-4o-mini-2024-07-18 (FC)<br>60.6<br>o1-2024-12-17 (Prompt)<br>59.1<br>Qwen2.5-72B-Instruct (Prompt)<br>57.0<br>Gemini-2.0-Flash-Exp (Prompt)<br>56.8<br>ToolACE-2-8B (FC)<br>56.6<br>Amazon-Nova-Pro-v1:0 (FC)<br>56.6<br>Qwen2.5-32B-Instruct (FC)<br>55.6<br>Gemini-2.0-Flash-Exp (FC)<br>55.5<br>BitAgent-8B<br>55.0<br>GPT-4o-mini-2024-07-18 (Prompt)<br>54.5<br>Claude-3.5-Sonnet-20241022 (FC)<br>53.8<br>o1-mini-2024-09-12 (Prompt)<br>53.5<br>o1-2024-12-17 (FC)<br>52.8<br>claude-3.5-haiku-20241022 (FC)<br>52.3<br>Qwen2.5-32B-Instruct (Prompt)<br>52.1<br>Amazon-Nova-Lite-v1:0 (FC)<br>52.1<br>GPT-4-turbo-2024-04-09 (Prompt)<br>51.4<br>Llama-3.1-70B-Instruct (Prompt)<br>50.4<br>Llama-3.3-70B-Instruct (Prompt)<br>50.4<br>Claude-3.5-Sonnet-20241022 (Prompt)<br>49.4<br>Qwen2.5-14B-Instruct (FC)<br>49.2<br>Hammer2.1-7b (FC)<br>48.6<br>Qwen2.5-14B-Instruct (Prompt)<br>47.8<br>claude-3.5-haiku-20241022 (Prompt)<br>46.6<br>Command-R-Plus (FC)<br>46.5<br>Command R7B (FC)<br>46.4<br>ToolACE-8B (FC)<br>45.6<br>Haha-7B<br>45.2<br>Hammer2.1-3b (FC)<br>45.0<br>Qwen2.5-7B-Instruct (FC)<br>44.7<br>xLAM-8x7b-r (FC)<br>44.2<br>Amazon-Nova-Lite-v1:0 (FC)<br>43.7<br>xLAM-7b-r (FC)<br>43.0<br>GoGoAgent<br>42.9<br>Qwen2.5-7B-Instruct (Prompt)<br>42.7<br>Llama-3.3-70B-Instruct (Prompt)<br>42.4<br>Gemma-3-12b-it (Prompt)<br>41.4<br>Hammer2.1-1.5b (FC)<br>41.3<br>Ministral-8B-Instruct-2410 (FC)<br>40.9<br>MiniCPM3-4B-FC (FC)<br>39.9<br>Amazon-Nova-Micro-v1:0 (FC)<br>39.8<br>Llama-3.1-8B-Instruct (Prompt)<br>39.6<br>Granite-20b-FunctionCalling (FC)<br>39.4<br>Qwen2.5-3B-Instruct (FC)<br>38.7<br>Falcon3-10B-Instruct (FC)<br>37.1<br>Qwen2.5-1.5B-Instruct (FC)<br>36.6<br>Qwen2.5-3B-Instruct (Prompt)<br>35.7<br>Llama-3.2-3B-Instruct (Prompt)<br>35.6<br>Falcon3-7B-Instruct (FC)<br>35.4<br>Qwen2.5-1.5B-Instruct (Prompt)<br>35.3<br>DBRX-Instruct (Prompt)<br>35.0<br>Hammer2.1-0.5b (FC)<br>34.0<br>Bielik-11B-v2.3-Instruct (Prompt)<br>32.5<br>GLM-4-9b-Chat (FC)<br>30.1<br>xLAM-7b-fc-r (FC)<br>30.0<br>MiniCPM3-4B (Prompt)<br>29.2<br>Gemma-3-4b-it (Prompt)<br>28.9<br>Meta-Llama-3-8B-Instruct (Prompt)<br>27.3<br>Qwen2.5-0.5B-Instruct (FC)<br>27.1<br>Falcon3-3B-Instruct (FC)<br>22.7<br>Qwen2-1.5B-Instruct (Prompt)<br>22.0<br>Qwen2.5-0.5B-Instruct (Prompt)<br>21.0<br>Llama-3.1-8B-Instruct (FC)<br>21.0<br>Llama-3.1-70B-Instruct (FC)<br>20.8<br>xLAM-1b-fc-r (FC)<br>18.7<br>Llama-3.2-1B-Instruct (Prompt)<br>15.4<br>Falcon3-1B-Instruct (FC)<br>13.1<br>Gemma-3-1b-it (Prompt)<br>12.5|79.4<br>95.5<br>94.0<br>83.5<br>77.2<br>93.5<br>93.0<br>86.0<br>70.4<br>91.0<br>90.0<br>87.5<br>74.8<br>92.0<br>90.0<br>84.0<br>72.7<br>93.5<br>91.5<br>85.0<br>80.2<br>**97.5**<br>93.5<br>92.0<br>76.8<br>95.5<br>**95.0**<br>**92.5**<br>75.3<br>92.5<br>92.5<br>90.0<br>68.8<br>92.5<br>92.0<br>84.5<br>72.8<br>94.0<br>93.5<br>88.5<br>68.4<br>89.5<br>92.0<br>90.5<br>76.2<br>95.0<br>94.0<br>82.5<br>80.1<br>90.5<br>89.5<br>87.0<br>78.8<br>94.5<br>3.5<br>5.0<br>71.2<br>89.0<br>83.5<br>72.0<br>67.9<br>93.0<br>0.0<br>0.0<br>68.0<br>92.0<br>2.5<br>0.0<br>70.2<br>94.5<br>90.5<br>88.0<br>69.8<br>94.0<br>84.0<br>66.0<br>**82.5**<br>95.5<br>93.5<br>92.0<br>77.9<br>96.0<br>94.5<br>91.5<br>74.8<br>94.5<br>84.0<br>87.0<br>81.4<br>92.0<br>70.5<br>46.0<br>69.7<br>95.0<br>88.0<br>89.0<br>78.1<br>95.0<br>93.5<br>88.0<br>73.2<br>92.5<br>92.0<br>85.0<br>76.2<br>93.0<br>84.0<br>79.5<br>72.1<br>89.5<br>82.5<br>64.0<br>68.2<br>91.5<br>85.5<br>81.5<br>76.7<br>93.5<br>90.5<br>89.5<br>78.1<br>95.5<br>89.5<br>81.0<br>81.4<br>95.0<br>89.5<br>81.5<br>71.8<br>95.0<br>90.0<br>86.0<br>73.6<br>90.0<br>69.0<br>38.0<br>69.8<br>94.0<br>84.0<br>66.0<br>74.2<br>95.5<br>81.0<br>73.5<br>75.4<br>93.0<br>92.0<br>84.5<br>75.3<br>94.5<br>91.5<br>84.5<br>74.8<br>94.5<br>84.0<br>87.0<br>77.3<br>95.0<br>90.0<br>73.0<br>74.7<br>92.0<br>84.5<br>80.0<br>71.8<br>91.5<br>84.5<br>87.5<br>69.8<br>91.5<br>82.5<br>79.5<br>63.5<br>88.0<br>77.5<br>55.5<br>72.8<br>93.5<br>87.0<br>83.5<br>72.8<br>91.5<br>84.0<br>81.5<br>73.3<br>92.0<br>73.5<br>76.5<br>70.5<br>93.5<br>87.5<br>87.0<br>72.4<br>87.0<br>81.5<br>75.5<br>74.2<br>90.5<br>79.5<br>79.0<br>73.8<br>92.0<br>80.5<br>76.0<br>64.8<br>89.5<br>86.5<br>88.5<br>71.0<br>86.0<br>70.0<br>66.5<br>73.5<br>92.0<br>42.5<br>37.0<br>68.0<br>83.0<br>71.5<br>54.0<br>71.2<br>93.5<br>46.0<br>49.5<br>65.2<br>81.5<br>0.0<br>0.0<br>76.8<br>93.5<br>77.0<br>41.0<br>63.5<br>72.5<br>65.5<br>62.0<br>64.3<br>91.5<br>56.5<br>41.0<br>62.7<br>82.5<br>48.0<br>50.0<br>61.2<br>78.0<br>60.0<br>50.0<br>58.0<br>69.0<br>61.0<br>25.0<br>51.2<br>79.0<br>46.5<br>40.5<br>58.2<br>68.0<br>53.5<br>33.0<br>55.8<br>54.0<br>48.5<br>34.5<br>49.2<br>24.5<br>12.5<br>15.0<br>71.7<br>86.0<br>5.0<br>2.0<br>29.2<br>33.5<br>36.0<br>15.0<br>3.6<br>6.0<br>17.5<br>9.0<br>43.5<br>38.5<br>2.0<br>2.0|**100.0**<br>94.0<br>86.0<br>77.5<br>88.3<br>92.0<br>**94.0**<br>82.5<br>87.4<br>90.0<br>86.0<br>77.5<br>83.3<br>92.0<br>84.0<br>75.0<br>58.6<br>92.0<br>86.0<br>82.5<br>99.3<br>94.0<br>90.0<br>**87.5**<br>63.6<br>92.0<br>84.0<br>80.0<br>95.4<br>92.0<br>86.0<br>75.0<br>97.1<br>84.0<br>84.0<br>77.5<br>97.6<br>88.0<br>84.0<br>77.5<br>61.9<br>88.0<br>80.0<br>80.0<br>98.6<br>94.0<br>88.0<br>77.5<br>62.9<br>96.0<br>82.0<br>82.5<br>97.6<br>90.0<br>4.0<br>0.0<br>89.3<br>86.0<br>78.0<br>77.5<br>60.6<br>94.0<br>0.0<br>0.0<br>87.9<br>90.0<br>24.0<br>0.0<br>96.6<br>90.0<br>90.0<br>82.5<br>92.0<br>84.0<br>80.0<br>65.0<br>99.3<br>96.0<br>80.0<br>82.5<br>94.0<br>**98.0**<br>86.0<br>82.5<br>95.7<br>**98.0**<br>84.0<br>85.0<br>**100.0**<br>92.0<br>68.0<br>60.0<br>90.4<br>92.0<br>72.0<br>85.0<br>86.4<br>92.0<br>86.0<br>77.5<br>92.4<br>90.0<br>88.0<br>85.0<br>97.9<br>90.0<br>76.0<br>75.0<br>90.9<br>90.0<br>84.0<br>60.0<br>87.1<br>92.0<br>82.0<br>75.0<br>97.4<br>94.0<br>88.0<br>77.5<br>80.4<br>96.0<br>88.0<br>80.0<br>82.9<br>92.0<br>84.0<br>77.5<br>95.4<br>94.0<br>84.0<br>77.5<br>89.2<br>90.0<br>72.0<br>45.0<br>92.0<br>84.0<br>80.0<br>65.0<br>74.0<br>96.0<br>82.0<br>67.5<br>95.4<br>96.0<br>88.0<br>80.0<br>92.1<br>90.0<br>86.0<br>85.0<br>95.7<br>98.0<br>84.0<br>85.0<br>84.7<br>94.0<br>80.0<br>72.5<br>86.6<br>90.0<br>82.0<br>75.0<br>71.3<br>86.0<br>86.0<br>75.0<br>89.3<br>90.0<br>86.0<br>85.0<br>80.4<br>76.0<br>68.0<br>52.5<br>83.7<br>96.0<br>88.0<br>77.5<br>84.9<br>92.0<br>86.0<br>82.5<br>86.9<br>90.0<br>66.0<br>70.0<br>97.1<br>92.0<br>92.0<br>82.5<br>88.0<br>90.0<br>78.0<br>72.5<br>80.9<br>86.0<br>80.0<br>80.0<br>87.3<br>92.0<br>78.0<br>77.5<br>89.0<br>94.0<br>86.0<br>77.5<br>80.4<br>94.0<br>88.0<br>80.0<br>90.1<br>88.0<br>46.0<br>52.5<br>68.4<br>84.0<br>82.0<br>47.5<br>76.6<br>90.0<br>44.0<br>50.0<br>94.0<br>90.0<br>0.0<br>0.0<br>84.5<br>92.0<br>56.0<br>10.0<br>40.4<br>34.0<br>48.0<br>80.0<br>68.1<br>80.0<br>30.0<br>12.5<br>77.7<br>86.0<br>42.0<br>60.0<br>51.2<br>88.0<br>52.0<br>52.5<br>54.6<br>46.0<br>20.0<br>10.0<br>46.6<br>76.0<br>52.0<br>35.0<br>63.1<br>70.0<br>62.0<br>52.5<br>58.7<br>58.0<br>54.0<br>30.0<br>53.0<br>36.0<br>30.0<br>7.5<br>77.8<br>90.0<br>4.0<br>0.0<br>34.1<br>28.0<br>34.0<br>5.0<br>9.4<br>4.0<br>18.0<br>15.0<br>34.0<br>44.0<br>4.0<br>0.0|84.9<br>79.8<br>87.5<br>75.0<br>81.4<br>78.8<br>87.5<br>75.0<br>83.7<br>78.6<br>81.2<br>70.8<br>78.7<br>76.2<br>87.5<br>70.8<br>82.9<br>76.5<br>81.2<br>75.0<br>85.3<br>82.1<br>62.5<br>75.0<br>85.7<br>79.3<br>81.2<br>**87.5**<br>70.9<br>79.0<br>81.2<br>54.2<br>80.2<br>77.5<br>81.2<br>58.3<br>80.2<br>80.1<br>43.8<br>62.5<br>74.8<br>70.7<br>81.2<br>70.8<br>77.9<br>77.4<br>87.5<br>70.8<br>81.4<br>76.7<br>93.8<br>79.2<br>84.1<br>82.0<br>25.0<br>20.8<br>72.9<br>71.6<br>75.0<br>75.0<br>81.8<br>79.0<br>0.0<br>0.0<br>82.9<br>78.3<br>18.8<br>0.0<br>83.0<br>78.5<br>62.5<br>58.3<br>72.9<br>70.1<br>75.0<br>66.7<br>**88.0**<br>**84.1**<br>**100.0**<br>79.2<br>78.3<br>76.2<br>87.5<br>66.7<br>81.8<br>77.1<br>93.8<br>66.7<br>86.8<br>80.1<br>81.2<br>45.8<br>77.1<br>75.0<br>75.0<br>70.8<br>76.7<br>77.4<br>81.2<br>70.8<br>74.4<br>75.8<br>62.5<br>66.7<br>84.9<br>75.0<br>87.5<br>54.2<br>70.5<br>58.8<br>62.5<br>45.8<br>63.2<br>58.7<br>56.2<br>62.5<br>73.3<br>76.7<br>81.2<br>70.8<br>78.3<br>77.6<br>75.0<br>70.8<br>73.3<br>73.3<br>62.5<br>66.7<br>75.6<br>75.6<br>68.8<br>66.7<br>74.8<br>79.3<br>43.8<br>58.3<br>72.9<br>70.1<br>75.0<br>66.7<br>72.1<br>74.9<br>50.0<br>62.5<br>72.9<br>75.4<br>68.8<br>66.7<br>76.7<br>74.9<br>62.5<br>70.8<br>81.8<br>77.1<br>93.8<br>66.7<br>84.9<br>70.8<br>87.5<br>62.5<br>71.3<br>69.8<br>50.0<br>62.5<br>75.6<br>72.3<br>62.5<br>62.5<br>74.8<br>63.9<br>43.8<br>62.5<br>65.9<br>64.2<br>62.5<br>45.8<br>74.0<br>73.3<br>56.2<br>54.2<br>68.2<br>56.3<br>43.8<br>58.3<br>74.0<br>72.1<br>62.5<br>45.8<br>76.4<br>76.2<br>50.0<br>41.7<br>74.0<br>66.1<br>50.0<br>45.8<br>69.8<br>66.5<br>56.2<br>62.5<br>64.0<br>64.9<br>12.5<br>45.8<br>74.0<br>66.5<br>75.0<br>62.5<br>70.5<br>59.3<br>56.2<br>41.7<br>78.3<br>73.0<br>75.0<br>41.7<br>60.1<br>58.0<br>50.0<br>45.8<br>72.9<br>69.3<br>43.8<br>54.2<br>72.5<br>64.4<br>0.0<br>0.0<br>78.7<br>58.0<br>31.2<br>25.0<br>46.5<br>34.8<br>43.8<br>41.7<br>72.9<br>62.8<br>37.5<br>29.2<br>61.2<br>61.4<br>37.5<br>33.3<br>56.2<br>41.3<br>56.2<br>20.8<br>55.4<br>56.3<br>31.2<br>37.5<br>48.8<br>40.3<br>12.5<br>25.0<br>53.9<br>34.8<br>56.2<br>16.7<br>51.9<br>49.0<br>37.5<br>41.7<br>52.3<br>52.6<br>31.2<br>25.0<br>64.0<br>53.4<br>6.2<br>0.0<br>31.4<br>7.6<br>12.5<br>4.2<br>4.7<br>2.4<br>0.0<br>12.5<br>31.0<br>10.5<br>0.0<br>0.0|83.8<br>83.3<br>83.1<br>83.3<br>83.8<br>72.2<br>74.7<br>83.3<br>87.8<br>72.2<br>72.8<br>**100.0**<br>86.4<br>77.8<br>90.1<br>72.2<br>71.0<br>77.8<br>81.9<br>64.7<br>**91.5**<br>55.6<br>82.4<br>83.3<br>80.7<br>83.3<br>74.0<br>77.8<br>89.6<br>61.1<br>82.0<br>72.2<br>63.7<br>83.3<br>73.8<br>100.0<br>76.4<br>66.7<br>35.6<br>**100.0**<br>54.8<br>**100.0**<br>48.7<br>**100.0**<br>64.4<br>77.8<br>77.7<br>55.6<br>78.6<br>82.3<br>77.1<br>77.8<br>65.8<br>77.8<br>53.2<br>72.2<br>81.0<br>55.6<br>87.9<br>83.3<br>80.7<br>83.3<br>81.9<br>82.3<br>69.1<br>77.8<br>67.2<br>94.4<br>76.4<br>66.7<br>77.1<br>94.4<br>83.1<br>77.8<br>65.2<br>88.9<br>48.7<br>100.0<br>61.1<br>88.9<br>79.3<br>77.8<br>55.3<br>70.6<br>72.2<br>72.2<br>74.2<br>72.2<br>48.8<br>77.8<br>74.8<br>88.9<br>64.3<br>88.9<br>31.9<br>94.4<br>62.7<br>94.4<br>54.2<br>88.9<br>51.7<br>88.9<br>33.7<br>88.9<br>63.0<br>83.3<br>40.5<br>94.4<br>73.9<br>77.8<br>40.6<br>77.8<br>79.7<br>66.7<br>45.0<br>77.8<br>74.4<br>50.0<br>48.1<br>77.8<br>18.6<br>77.8<br>46.2<br>88.9<br>34.5<br>77.8<br>21.2<br>94.4<br>16.4<br>94.4<br>4.9<br>94.4<br>44.8<br>**100.0**<br>6.7<br>100.0<br>59.7<br>38.9<br>87.2<br>0.0<br>30.9<br>50.0|59.0<br>**41.0**<br>35.5<br>55.0<br>**62.5**<br>6.0<br>37.5<br>**58.0**<br>54.0<br>13.5<br>35.5<br>49.5<br>47.5<br>19.5<br>29.0<br>40.5<br>50.5<br>0.5<br>**48.5**<br>44.5<br>24.5<br>20.0<br>15.5<br>12.0<br>28.0<br>3.0<br>19.0<br>21.5<br>48.5<br>29.0<br>28.0<br>42.0<br>37.5<br>19.0<br>22.0<br>26.0<br>29.5<br>25.5<br>20.5<br>13.5<br>31.0<br>0.5<br>22.5<br>27.0<br>48.0<br>40.0<br>26.5<br>39.5<br>33.0<br>12.0<br>17.0<br>26.0<br>55.0<br>19.0<br>42.5<br>47.5<br>40.5<br>5.0<br>34.5<br>33.0<br>52.5<br>38.0<br>30.5<br>43.0<br>54.5<br>26.5<br>35.0<br>44.0<br>25.0<br>20.0<br>15.0<br>11.0<br>27.5<br>5.5<br>17.5<br>19.0<br>42.5<br>25.0<br>20.5<br>33.0<br>16.5<br>13.0<br>10.5<br>10.0<br>9.0<br>8.0<br>4.5<br>6.0<br>9.0<br>5.5<br>5.0<br>10.5<br>19.5<br>17.0<br>16.5<br>10.5<br>35.5<br>25.5<br>19.0<br>14.0<br>19.0<br>11.5<br>12.0<br>6.5<br>16.0<br>0.5<br>8.0<br>14.5<br>16.5<br>10.0<br>9.0<br>17.0<br>6.5<br>1.5<br>6.5<br>5.5<br>7.5<br>11.5<br>5.0<br>7.0<br>13.0<br>10.0<br>11.5<br>7.0<br>27.5<br>17.5<br>14.5<br>10.0<br>13.5<br>14.5<br>11.0<br>7.0<br>26.0<br>13.0<br>11.5<br>11.5<br>27.5<br>5.5<br>17.5<br>19.0<br>16.5<br>8.5<br>7.5<br>7.5<br>1.5<br>2.0<br>0.5<br>0.0<br>9.5<br>8.5<br>7.0<br>5.5<br>9.0<br>8.0<br>4.5<br>6.0<br>8.0<br>3.5<br>2.5<br>4.5<br>14.5<br>12.5<br>9.0<br>6.0<br>21.5<br>8.5<br>10.0<br>5.5<br>5.0<br>1.0<br>3.0<br>1.5<br>24.5<br>5.5<br>14.0<br>20.5<br>13.0<br>10.0<br>7.5<br>8.0<br>6.0<br>1.5<br>4.5<br>1.5<br>8.5<br>6.0<br>4.5<br>5.0<br>6.0<br>5.0<br>4.5<br>4.5<br>4.0<br>1.5<br>3.0<br>1.5<br>5.5<br>3.5<br>2.0<br>2.5<br>8.5<br>2.5<br>4.5<br>5.5<br>3.5<br>3.5<br>3.5<br>3.0<br>1.5<br>2.5<br>0.5<br>0.0<br>0.0<br>0.0<br>0.0<br>0.0<br>4.0<br>0.5<br>3.0<br>1.5<br>7.0<br>0.5<br>3.0<br>4.5<br>3.5<br>4.0<br>2.5<br>4.0<br>0.0<br>0.0<br>0.0<br>0.0<br>3.0<br>3.5<br>1.0<br>0.5<br>0.0<br>0.0<br>0.5<br>0.0<br>1.5<br>0.0<br>1.0<br>0.5<br>1.0<br>2.0<br>1.0<br>1.0<br>0.5<br>0.5<br>0.0<br>1.0<br>0.5<br>1.0<br>0.0<br>0.5<br>0.0<br>0.0<br>0.0<br>0.0<br>5.0<br>7.5<br>5.0<br>4.0<br>7.0<br>4.0<br>4.5<br>4.0<br>0.5<br>0.0<br>0.0<br>0.0<br>0.0<br>0.0<br>0.0<br>0.0<br>0.0<br>0.0<br>0.0<br>0.0<br>0.0<br>0.0<br>0.0<br>0.0|64.0<br>6.0<br>78.0<br>82.0<br>0.0<br>81.0<br>66.0<br>4.0<br>50.0<br>78.0<br>6.0<br>66.0<br>5.0<br>**12.0**<br>**91.0**<br>54.0<br>8.0<br>70.0<br>73.0<br>0.0<br>53.0<br>25.0<br>2.0<br>37.0<br>76.0<br>0.0<br>51.0<br>53.0<br>4.0<br>45.0<br>70.0<br>6.0<br>45.0<br>22.0<br>0.0<br>29.0<br>43.0<br>0.0<br>63.0<br>74.0<br>4.0<br>60.0<br>7.0<br>0.0<br>70.0<br>48.0<br>**12.0**<br>83.0<br>**83.0**<br>6.0<br>59.0<br>46.0<br>0.0<br>42.0<br>62.0<br>0.0<br>58.0<br>27.0<br>0.0<br>54.0<br>56.0<br>0.0<br>61.0<br>78.0<br>0.0<br>64.0<br>68.0<br>0.0<br>60.0<br>30.0<br>0.0<br>30.0<br>14.0<br>0.0<br>13.0<br>28.0<br>0.0<br>26.0<br>0.0<br>2.0<br>68.0<br>69.0<br>0.0<br>45.0<br>69.0<br>0.0<br>18.0<br>9.0<br>0.0<br>13.0<br>20.0<br>0.0<br>8.0<br>2.0<br>0.0<br>6.0<br>12.0<br>0.0<br>14.0<br>23.0<br>0.0<br>34.0<br>10.0<br>0.0<br>9.0<br>14.0<br>0.0<br>9.0<br>10.0<br>0.0<br>14.0<br>14.0<br>0.0<br>15.0<br>36.0<br>2.0<br>8.0<br>25.0<br>0.0<br>13.0<br>0.0<br>0.0<br>2.0<br>13.0<br>0.0<br>12.0<br>6.0<br>0.0<br>8.0<br>10.0<br>0.0<br>5.0<br>8.0<br>0.0<br>9.0<br>0.0<br>0.0<br>29.0<br>3.0<br>0.0<br>5.0<br>12.0<br>0.0<br>8.0<br>0.0<br>0.0<br>1.0<br>0.0<br>0.0<br>4.0<br>0.0<br>0.0<br>5.0<br>8.0<br>0.0<br>6.0<br>0.0<br>0.0<br>3.0<br>9.0<br>6.0<br>36.0<br>0.0<br>0.0<br>1.0<br>6.0<br>0.0<br>10.0<br>3.0<br>0.0<br>8.0<br>2.0<br>0.0<br>5.0<br>0.0<br>0.0<br>3.0<br>0.0<br>0.0<br>6.0<br>2.0<br>0.0<br>7.0<br>0.0<br>0.0<br>0.0<br>0.0<br>0.0<br>3.0<br>0.0<br>0.0<br>0.0<br>0.0<br>0.0<br>0.0<br>4.0<br>0.0<br>0.0<br>5.0<br>0.0<br>0.0<br>0.0<br>0.0<br>0.0<br>0.0<br>0.0<br>0.0<br>0.0<br>0.0<br>0.0<br>0.0<br>0.0<br>1.0|



Models that support native function-calling (FC), such as GPT-4, Gemini-1.5-Pro, Claude-3.5-Sonnet, can run BFCL directly by supplying all function definitions in their tools input field. In contrast, most models lack built-in functioncalling capabilities. For these models, we use a promptbased workaround: we guide them to produce structured function calls through the system prompt (detailed in Appendix A), placing the function definitions in the system prompt rather than in a dedicated tools field. Throughout this paper, we refer to models that have their native function-calling feature enabled as “FC models” (or operating in “FC mode”), and those for which we rely on system prompts to trigger function calls as “prompting models” (or in “prompting mode”). 

If a model supports both FC and prompting modes, we find that the FC mode outputs tend to be structured responses that lower parsing errors. However, these structural constraints of the FC mode can limit the flexibility of a model in complex function calling scenarios. We therefore see more capable models often performing better in the prompting mode. For instance, Claude cannot execute parallel 

function calls in FC mode, whereas it can in prompting mode. In addition, when handling other programming languages (e.g., Java or JavaScript), models in prompting mode often outperforms FC mode. 

Prompting models exhibit on average three times more decoding issues than FC models (412.93 vs. 182.5 out of 4,251 total entries), aligning with the observation that structured FC-mode outputs are easier to parse. However, among successfully decoded responses in the _multiple_ functioncall category, FC models show more incorrect function-call counts on average (77.5 vs. 21). A similar trend appears in the _parallel multiple_ category, indicating that prompting models are generally more flexible in complex scenarios. 

## **5.2. Dataset Composition Difference** 

We construct the data generation pipeline for single-turn based on our understanding of the composition of real-life function-calling scenarios from our experiences building a function-calling LLM, and from function-calling documentations (OpenAI, 2025b) and community forums (OpenAI, 2025a). At that time, there were no formal crowd-sourced

### Page 6

**The Berkeley Function Calling Leaderboard (BFCL): From Tool Use to Agentic Evaluation of Large Language Models** 

datasets. After we collected the crowd-sourced part of this dataset, we found that there are quite a few differences between the single turn and the crowd-sourced. 

In crowd-sourced, there are significantly more scenarios on multiple and much less parallel function calling scenarios. This observation reflects how most users interact with function calling: high demand for the feature of having to intelligently choose between functions and lower demand for making parallel function calls in a single turn. 

Crowd-sourced dataset also differ from single turn in that they contain multi-lingual user prompts, multi-lingual function docs, as well as user prompts that contains lots of redundant information, etc. As an example of the rich diversity we observed in our dataset, we even include a classification function triggered through function calling. 

On average, each entry in crowd-sourced contains 3 function choices, with the maximum one having 37 function choices. Each function has an average of 4 parameters, with the maximum one having 28 parameters. Here are some statistics and distributions. 

## **5.3. Parallel Function Call Ability** 

When a question requires multiple function calls (whether to the same function or different ones), the model can issue them all at once in a single turn, or sequentially across multiple turns. For tasks that have no interdependencies among calls, issuing parallel function calls in a single turn significantly reduces latency. For instance, checking the stock prices of 20 different stocks simultaneously is far more efficient than making 20 separate requests. 

We observe notable shifts in the evlolution of models’ abilities to generate parallel function calls. Early models (e.g., the Claude Sonnet) lacked any function call capability. Later iterations introduced partial support for parallel calls—albeit with suboptimal performance. Interestingly, with the release of flagship versions such as o1-2024-12-17-FC and claude-3-5-sonnet-20241022-FC, the parallel function call feature appears to have regressed or even removed! We hypothesize that this is because although parallel calls can be more efficient for non-interdependent tasks, they may adversely affect accuracy when function calls are chained. In many real-world scenarios, each subsequent call relies on information returned by the previous one. As a result, generating calls one at a time—waiting for each execution’s result—might ultimately be both faster and more accurate for these use cases. 

## **5.4. Multi Turn Error Analysis** 

We analyze the errors made by models in two ways: The first is through a deterministic algorithmic approach for classifying the different ways a model’s results don’t align 

with our ground truth answers. The second is an LLM-as-aJudge approach to better understand the root-causes behind the the errors. 

## 5.4.1. DETERMINISTIC ERROR ANALYSIS 

We classify the errors shown by our benchmarked models into 5 categories: Empty Turn Response Error, Instance State Mismatch, Execution Response Mismatch, Force Termination, and API Error. An **Empty Response Error** refers to when a model does not make any function call for one or more turns in the conversation. An **Instance State Mismatch** refers to a discrepancy between the model’s internal representation of the API state and the expected ground truth state. An **Execution Response Mismatch** error occurs when the responses generated by the model for a specific turn do not include all the expected responses defined in the ground truth for that turn. The **Force Termination** error occurs when the model’s processing is abruptly stopped during inference. This happens in cases when the model uses many steps within a turn in an attempt to answer the user’s question leading to termination of its efforts. Lastly, the **API Error** simply groups all the cases the model’s provided API endpoint failed to run on an entry in the dataset due to it being down or the token length of our questions going over the maximum allowable input token length. 

**==> picture [235 x 118] intentionally omitted <==**

Figure 4: Error distribution across models on the BFCL MultiTurn Dataset showing the counts of different error types: Empty Response Error, Execution Response Mismatch, Force Terminated, Instance State Mismatch, and API Error. The total number of entries in the dataset is 800. 

## 5.4.2. LLM-AS-A-JUDGE ERROR ANALYSIS 

In addition to the mechanical error analysis, we employed LLMs-as-judges to classify and analyze the root causes of failures in multi-turn interactions. We utilized a few-shot structured prompting method to query the LLMs about error cases. The prompts included detailed multi-turn conversation logs, initial configurations, and user queries. The judges were tasked with explaining and categorizing failures into predefined types: 1) **Failed to Understand Environment State** : Errors stemming from inaccurate assumptions or hallucinated environment states. 2) **Failed to Understand User’s Request** : Misinterpretation of user request specifi-

### Page 7

**The Berkeley Function Calling Leaderboard (BFCL): From Tool Use to Agentic Evaluation of Large Language Models** 

**==> picture [235 x 176] intentionally omitted <==**

Figure 5: The bar chart shows the frequency of three error types—failed to understand environment state, failed to understand function documentation, and failed to understand the user’s request—across various AI models. Error types are color-coded, illustrating differences in model performance. 

cations. 3) **Failed to Understand Function Documentation** : Errors due to misinterpretation or misuse of provided function documentation. Full judge prompt template is in Appendix F 

The most prevalent failure mode across models was **Failed to Understand Environment State** as can be seen in Figure 5. These errors occurred when the model either hallucinated or assumed incorrect environment state information, including attempting actions in incorrect directories or failing to execute necessary steps due to premature termination of actions due to state misalignment. **Failed to Understand User’s Request** was the second most frequent error type. These failures typically arose when the model misinterpreted user intent, such as returning unsorted data instead of sorted content or failing to execute requested multi-step operations in the correct sequence user requested. 

## **5.5. Measuring Data Contamination using crowd-sourced** 

Traditional benchmarks inadvertently compromise if a model’s training data overlaps with the evaluation set, leading to artificially low perplexity and Negative log likelihood on those benchmarks. By comparing language modeling metrics between crowd-sourced and single-turn, we can diagnose possible data contamination or overfitting. In particular, an abnormally low perplexity or character-level negative log-likelihood (char-NLL) on the static single-turn benchmark, coupled with a significant performance drop on crowd-sourced, would signal that the model may have memorized the former. On the other hand, consistent performance across single-turn and crowd-sourced suggests genuine generalization rather than training exposure to the test answers 

Table 2: While all models display consistently high perplexity in single-turn dataset then its crowd-sourced counterpart, the relative difference entails the model’s familiarity to the single-turn which is open to be trained on as evaluation entries. 

|**Model**|**PPL (single-turn)**|**PPL (crowd-sourced)**|
|---|---|---|
|Llama2-7B|3.47|2.56|
|Openfunctions-v2|3.09|2.49|
|CodeLlama-7B|3.45|2.49|
|Meta-Llama-3 8B|3.58|2.63|
|Mistral-7B|4.39|2.92|
|Functionary-7B|3.81|2.73|
|Salesforce xLAM-7B|3.67|5.09|



Table 3: Character-level negative log-likelihood (Char-NLL) metric provides insights similar to those from Table 2. As the outputs of the function calls are structured, Char-NLL effectively captures model uncertainty and predictive performance at the token level across both single-turn and crowd-sourced settings. Lower values indicate better modeling of structured output. 

|**Model**|**Char-NLL (single-turn)**|**Char-NLL (crowd-sourced)**|
|---|---|---|
|Llama2-7B|0.344|0.264|
|Openfunctions-v2|0.295|0.239|
|CodeLlama-7B|0.342|0.256|
|Meta-Llama-3 8B|0.322|0.245|
|Mistral-7B|0.404|0.295|
|Functionary-7B|0.337|0.254|
|Salesforce xLAM-7B|0.340|0.427|



Tables 2 and 3 present the perplexity and char-NLL metrics, respectively, for several open-source models on the original single-turn benchmark versus the novel crowd-sourced dataset (wherein lower values signify superior predictive performance). It is observed that the majority of models achieve comparable or improved performance, i.e., lower perplexity and char-NLL on the crowd-sourced data relative to single-turn. For instance, Llama 2-7B (Touvron et al., 2023) exhibits a perplexity of 3.47 on single-turn compared to 2.56 on crowd-sourced, and a char-NLL of 0.344 versus 0.264. Similarly, Openfunctions-v2 and CodeLlama-7B also demonstrate slightly enhanced performance on the crowdsourced queries. This trend implies that these models did not derive an unfair advantage from memorization on the original benchmark. This finding supports the inference that their strong benchmark scores are attributable to genuine capability rather than exposure to test solutions. In contrast, Salesforce xLAM-7B (Zhang et al., 2024) shows an increase in perplexity from 3.67 to 5.09(char-NLL from 0.340 to 0.427) on crowd-sourced, representing a notable performance degradation. 

These performance decrements underscore the utility of the crowd-sourced dataset as a ”stress test” for models: any model that has primarily memorized benchmark solutions or was overly tuned to the static test distribution is likely to be exposed through a significant score regression on the new dataset. In the instances of xLAM, the crowd-sourced evaluation reveals vulnerabilities that the original static test masked. It is noteworthy that both are specialized or smaller-

### Page 8

**The Berkeley Function Calling Leaderboard (BFCL): From Tool Use to Agentic Evaluation of Large Language Models** 

scale models, which may have been exposed to limited data variety; consequently, when confronted with genuinely novel queries, their performance markedly declines. 

Overall, the perplexity and char-NLL metrics across singleturn and crowd-sourced present a coherent pattern. Figure 6, and 7 visualize these results, plotting each model’s performance on single-turn against its performance on crowdsourced. The majority of data points are situated near the diagonal, signifying comparable proficiency on both datasets. In contrast, the outlier models deviate sharply upward, indicating higher perplexity/NLL on crowd-sourced. This analysis substantiates the practical value of the BFCL Live methodology. By incorporating a real-world test set, a more robust indicator of contamination or overfitting is obtained. Models cannot rely on memorized answers for crowd-sourced queries; thus, any substantial discrepancy in metrics serves as an immediate flag for potential evaluation inflation. In summary, these comparative metrics confirm that top-performing models maintain strong generalization on fresh data, whereas models exhibiting any indication of contamination or poor robustness are clearly identified by the performance gap between their single-turn and crowd-sourced scores. 

**==> picture [235 x 176] intentionally omitted <==**

Figure 6: Character-level NLL on single-turn dataset. 

## **5.6. Memory Management Category Analysis** 

Current models struggle with memory tasks; even the benchmark leader, _openai o1-2024-12-17 (FC)_ , reaches only 12% accuracy. We observe models demonstrate faulty behaviors in memory management and organization. For instance, when preserving the fact that “the user is a fourth-year male CS major,” some models save as one key (user profile), others split it (major, year, gender). Splitting quickly exhausts key space, demands frequent merges, and complicates retrieval. 

Models often hallucinate during key retrieval. Because the key–value store requires exact matches, models should first call list ~~k~~ eys to view existing keys before retrieving 

**==> picture [235 x 176] intentionally omitted <==**

Figure 7: Character-level NLL on crowd-sourced dataset. 

information. While some models handle this correctly, most skip listing the keys and instead attempt to guess a key when calling retrieve, leading to mismatches and errors. Even worse, many models give up after a single failure, mistakenly concluding that the information is unavailable rather than attempting to look up valid keys. 

## **6. Conclusion** 

The Berkeley Function Calling Leaderboard (BFCL) establishes a new standard for evaluating large language models’ (LLMs) ability to invoke and manage external tools and APIs. By introducing a comprehensive benchmark that spans single-turn, crowd-sourced, multi-turn, and agentic scenarios, BFCL provides a robust and scalable framework for assessing the function-calling capabilities critical to agentic AI systems. Its use of Abstract Syntax Tree (AST) based evaluation ensures reproducibility and avoids the scalability limitations of execution-based methods. The inclusion of real-world, multilingual user queries further enhances the benchmark’s practical relevance. 

Our analysis reveals that while many LLMs perform well on simple single-turn tasks, they often falter in more complex agentic and memory-intensive scenarios. This underscores the gap between current LLM performance and the demands of real-world, long-horizon reasoning tasks. Moreover, our comparative evaluations with crowd-sourced data expose potential overfitting in static benchmarks and highlight BFCL’s role in stress-testing generalization. 

As function-calling becomes a foundational capability for LLM-powered applications, BFCL serves as an essential tool for the community. We hope this benchmark not only drives advancements in LLM architectures and training but also promotes transparent and reproducible evaluation practices in the development of functionally robust AI agents.

### Page 9

**The Berkeley Function Calling Leaderboard (BFCL): From Tool Use to Agentic Evaluation of Large Language Models** 

## **Impact Statement** 

The introduction of the Berkeley Function Calling Leaderboard (BFCL) represents a significant advancement in the evaluation and benchmarking of large language models (LLMs) for function-calling capabilities. Function calling is an increasingly critical skill for LLMs, enabling them to integrate seamlessly with external systems, perform complex tasks, and reason effectively in stateful, multi-turn interactions. Despite its importance, existing benchmarks inadequately capture the diversity, complexity, and real-world applicability of function-calling scenarios. 

BFCL addresses these challenges by presenting a multifaceted benchmark that evaluates LLMs across single-turn, multi-turn, crowd-sourced, and agentic datasets. By leveraging innovative techniques such as Abstract Syntax Tree (AST) substring matching for scalable and deterministic evaluation, and incorporating real-world user-contributed data, BFCL sets a new standard for evaluating LLMs’ capabilities. 

This benchmark has the potential to significantly shape the development of next-generation LLMs by providing researchers and practitioners with a comprehensive tool to assess and improve function-calling performance. Moreover, it paves the way for more robust, adaptable, and ethically-aligned LLM deployments in diverse domains such as healthcare, finance, and education. 

Ultimately, BFCL contributes to the broader goal of making LLMs more effective, and reliable in real-world applications, fostering innovation and ensuring responsible AI use. 

## **References** 

- Attouche, L., Baazizi, M.-A., Colazzo, D., Ghelli, G., Sartiani, C., and Scherzinger, S. Validation of modern json schema: Formalization and complexity. _Proceedings of the ACM on Programming Languages_ , 8(POPL):1451– 1481, 2024. 

- Basu, K., Abdelaziz, I., Chaudhury, S., Dan, S., Crouse, M., Munawar, A., Kumaravel, S., Muthusamy, V., Kapanipathi, P., and Lastras, L. A. Api-blend: A comprehensive corpora for training and benchmarking api llms, 2024. URL https://arxiv.org/abs/2402.15491. 

- Chen, Z., Du, W., Zhang, W., Liu, K., Liu, J., Zheng, M., Zhuo, J., Zhang, S., Lin, D., Chen, K., and Zhao, F. T- eval: Evaluating the tool utilization capability of large language models step by step, 2024. URL https:// arxiv.org/abs/2312.14033. 

- Cohere, T. Command a: An enterprise-ready large language model, 2025. URL https://arxiv.org/ abs/2504.00698. 

- Erdogan, L. E., Lee, N., Jha, S., Kim, S., Tabrizi, R., Moon, S., Hooper, C., Anumanchipalli, G., Keutzer, K., and Gholami, A. Tinyagent: Function calling at the edge, 2024. URL https://arxiv.org/abs/2409.00608. 

- Gao, D., Wang, H., Li, Y., Sun, X., Qian, Y., Ding, B., and Zhou, J. Text-to-sql empowered by large language models: A benchmark evaluation. _Proc. VLDB Endow._ , 17(5):1132–1145, January 2024. ISSN 21508097. doi: 10.14778/3641204.3641221. URL https: //doi.org/10.14778/3641204.3641221. 

- Ge, T., Chan, X., Wang, X., Yu, D., Mi, H., and Yu, D. Scaling synthetic data creation with 1,000,000,000 personas, 2024. URL https://arxiv.org/abs/ 2406.20094. 

- Guo, Z., Cheng, S., Wang, H., Liang, S., Qin, Y., Li, P., Liu, Z., Sun, M., and Liu, Y. Stabletoolbench: Towards stable large-scale benchmarking on tool learning of large language models, 2024. 

- Guo, Z., Cheng, S., Wang, H., Liang, S., Qin, Y., Li, P., Liu, Z., Sun, M., and Liu, Y. Stabletoolbench: Towards stable large-scale benchmarking on tool learning of large language models, 2025. URL https://arxiv.org/ abs/2403.07714. 

- Huang, S., Zhong, W., Lu, J., Zhu, Q., Gao, J., Liu, W., Hou, Y., Zeng, X., Wang, Y., Shang, L., Jiang, X., Xu, R., and Liu, Q. Planning, creation, usage: Benchmarking LLMs for comprehensive tool utilization in realworld complex scenarios. In Ku, L.-W., Martins, A., and Srikumar, V. (eds.), _Findings of the Association for Computational Linguistics: ACL 2024_ , pp. 4363– 4400, Bangkok, Thailand, August 2024. Association for Computational Linguistics. doi: 10.18653/v1/2024. findings-acl.259. URL https://aclanthology. org/2024.findings-acl.259/. 

- Kim, S., Moon, S., Tabrizi, R., Lee, N., Mahoney, M. W., Keutzer, K., and Gholami, A. An LLM compiler for parallel function calling. In _Forty-first International Conference on Machine Learning_ , 2024. URL https: //openreview.net/forum?id=uQ2FUoFjnF. 

- Lin, C.-Y. ROUGE: A package for automatic evaluation of summaries. In _Text Summarization Branches Out_ , pp. 74–81, Barcelona, Spain, July 2004. Association for Computational Linguistics. URL https: //aclanthology.org/W04-1013/. 

- Lu, J., Holleis, T., Zhang, Y., Aumayer, B., Nan, F., Bai, F., Ma, S., Ma, S., Li, M., Yin, G., Wang, Z., and Pang, R. Toolsandbox: A stateful, conversational, interactive evaluation benchmark for llm tool use capabilities, 2024. URL https://arxiv.org/abs/2408.04682.

### Page 10

**The Berkeley Function Calling Leaderboard (BFCL): From Tool Use to Agentic Evaluation of Large Language Models** 

- Marten, R., Vu, T., Cheng-Jie Ji, C., Sharma, K., Dimakis, A., and Sathiamoorthy, M. Curator, January 2025. 

- MetaAI. The llama 3 herd of models, 2024. URL https: //arxiv.org/abs/2407.21783. 

- OpenAI. Gpt-4 technical report, 2024. URL https:// arxiv.org/abs/2303.08774. 

- OpenAI. Openai community forum, 2025a. URL https: //community.openai.com. Community of developers building AI-powered applications. 

- OpenAI. Function calling, 2025b. URL https: //platform.openai.com/docs/guides/ function-calling. Documentation for integrating OpenAI models with custom code and external services. 

- Packer, C., Wooders, S., Lin, K., Fang, V., Patil, S. G., Stoica, I., and Gonzalez, J. E. Memgpt: Towards llms as operating systems, 2024. URL https://arxiv. org/abs/2310.08560. 

- Panickssery, A., Bowman, S. R., and Feng, S. Llm evaluators recognize and favor their own generations, 2024. URL https://arxiv.org/abs/2404.13076. 

- Patil, S. G., Zhang, T., Wang, X., and Gonzalez, J. E. Gorilla: Large language model connected with massive apis. In _The Thirty-eighth Annual Conference on Neural Information Processing Systems_ , 2024. URL https: //openreview.net/forum?id=tBRNC6YemY. 

- Qin, Y., Liang, S., Ye, Y., Zhu, K., Yan, L., Lu, Y., Lin, Y., Cong, X., Tang, X., Qian, B., Zhao, S., Hong, L., Tian, R., Xie, R., Zhou, J., Gerstein, M., Li, D., Liu, Z., and Sun, M. Toolllm: Facilitating large language models to master 16000+ real-world apis, 2023. URL https://arxiv.org/abs/2307.16789. 

- Sasaki, M., Watanabe, N., and Komanaka, T. Enhancing contextual understanding of mistral llm with external knowledge bases. 2024. 

- Schick, T., Dwivedi-Yu, J., Dessi, R., Raileanu, R., Lomeli, M., Hambro, E., Zettlemoyer, L., Cancedda, N., and Scialom, T. Toolformer: Language models can teach themselves to use tools. In _Thirty-seventh Conference on Neural Information Processing Systems_ , 2023. URL https://openreview.net/forum? id=Yacmpz84TH. 

- Song, Y., Xiong, W., Zhu, D., Wu, W., Qian, H., Song, M., Huang, H., Li, C., Wang, K., Yao, R., Tian, Y., and Li, S. Restgpt: Connecting large language models with real-world restful apis, 2023. URL https://arxiv. org/abs/2306.06624. 

- Srinivasan, V. K., Dong, Z., Zhu, B., Yu, B., Mao, H., Mosk-Aoyama, D., Keutzer, K., Jiao, J., and Zhang, J. Nexusraven: a commercially-permissive language model for function calling. In _NeurIPS 2023 Workshop on Instruction Tuning and Instruction Following_ , 2023. URL https://openreview.net/forum? id=Md6RUrGz67. 

- team, N. Nexusraven-v2: Surpassing gpt-4 for zero-shot function calling, 2023. URL https://nexusflow. ai/blogs/ravenv2. 

- Team, Q. Qwen3 technical report, 2025. URL https: //arxiv.org/abs/2505.09388. 

- Touvron, H., Martin, L., Stone, K., Albert, P., Almahairi, A., Babaei, Y., Bashlykov, N., Batra, S., Bhargava, P., Bhosale, S., Bikel, D., Blecher, L., Ferrer, C. C., Chen, M., Cucurull, G., Esiobu, D., Fernandes, J., Fu, J., Fu, W., Fuller, B., Gao, C., Goswami, V., Goyal, N., Hartshorn, A., Hosseini, S., Hou, R., Inan, H., Kardas, M., Kerkez, V., Khabsa, M., Kloumann, I., Korenev, A., Koura, P. S., Lachaux, M.-A., Lavril, T., Lee, J., Liskovich, D., Lu, Y., Mao, Y., Martinet, X., Mihaylov, T., Mishra, P., Molybog, I., Nie, Y., Poulton, A., Reizenstein, J., Rungta, R., Saladi, K., Schelten, A., Silva, R., Smith, E. M., Subramanian, R., Tan, X. E., Tang, B., Taylor, R., Williams, A., Kuan, J. X., Xu, P., Yan, Z., Zarov, I., Zhang, Y., Fan, A., Kambadur, M., Narang, S., Rodriguez, A., Stojnic, R., Edunov, S., and Scialom, T. Llama 2: Open foundation and fine-tuned chat models, 2023. URL https://arxiv.org/abs/2307.09288. 

- Trivedi, H., Khot, T., Hartmann, M., Manku, R., Dong, V., Li, E., Gupta, S., Sabharwal, A., and Balasubramanian, N. Appworld: A controllable world of apps and people for benchmarking interactive coding agents, 2024. URL https://arxiv.org/abs/2407.18901. 

- Vu, T., Iyyer, M., Wang, X., Constant, N., Wei, J., Wei, J., Tar, C., Sung, Y.-H., Zhou, D., Le, Q., and Luong, T. Freshllms: Refreshing large language models with search engine augmentation, 2023. URL https://arxiv. org/abs/2310.03214. 

- Yao, S., Chen, H., Yang, J., and Narasimhan, K. Webshop: Towards scalable real-world web interaction with grounded language agents. In Koyejo, S., Mohamed, S., Agarwal, A., Belgrave, D., Cho, K., and Oh, A. (eds.), _Advances in Neural Information Processing Systems_ , volume 35, pp. 20744–20757. Curran Associates, Inc., 2022. 

- Yao, S., Shinn, N., Razavi, P., and Narasimhan, K. _τ_ -bench: A benchmark for tool-agent-user interaction in real-world domains, 2024. URL https://arxiv.org/abs/ 2406.12045.

### Page 11

**The Berkeley Function Calling Leaderboard (BFCL): From Tool Use to Agentic Evaluation of Large Language Models** 

- Zhang, J., Lan, T., Zhu, M., Liu, Z., Hoang, T., Kokane, S., Yao, W., Tan, J., Prabhakar, A., Chen, H., Liu, Z., Feng, Y., Awalgaonkar, T., Murthy, R., Hu, E., Chen, Z., Xu, R., Niebles, J. C., Heinecke, S., Wang, H., Savarese, S., and Xiong, C. xlam: A family of large action models to empower ai agent systems, 2024. URL https:// arxiv.org/abs/2409.03215. 

- Zhong, Z. and Chen, D. A frustratingly easy approach for entity and relation extraction. In Toutanova, K., Rumshisky, A., Zettlemoyer, L., Hakkani-Tur, D., Beltagy, I., Bethard, S., Cotterell, R., Chakraborty, T., and Zhou, Y. (eds.), _Proceedings of the 2021 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies_ , pp. 50–61, Online, June 2021. Association for Computational Linguistics. doi: 10.18653/v1/2021.naacl-main.5. URL https: //aclanthology.org/2021.naacl-main.5/.

### Page 12

**The Berkeley Function Calling Leaderboard (BFCL): From Tool Use to Agentic Evaluation of Large Language Models** 

## **A. System Prompt for Prompting Models** 

To enable prompting models to execute function-calling actions, we use the following universal system prompt, where the _{_ functions _}_ placeholder is replaced with the function documentation(s): 

_”””_ 

- _You are an e x p e r t in composing f u n c t i o n s . You are given a q u e s t i o n and a s e t of p o s s i b l e f u n c t i o n s . Based on the question , you w i l l need to make one or more f u n c t i o n / t o o l c a l l s to achieve the purpose ._ 

- _I f none of the f u n c t i o n s can be used , p o i n t i t out . I f the given q u e s t i o n l a c k s the parameters r e qu i re d by the f u n c t i o n , also p o i n t i t out ._ 

- _You should only r e t u r n the f u n c t i o n c a l l s in your response ._ 

- _I f you decide to invoke any of the f u n c t i o n ( s ) , you MUST put i t in the format of [ func name1 ( params name1=params value1 , params name2=params value2 . . . ) , func name2 ( params ) ]_ 

- _You SHOULD NOT i n c l u d e any other t e x t in the response ._ 

- _At each turn , you should t r y your b e s t to complete the t a s k s r e q u e s t e d by the user w i t h i n the c u r r e n t turn . Continue to output f u n c t i o n s to c a l l u n t i l you have f u l f i l l e d the user ’ s r e q u e s t to the b e s t of your a b i l i t y . Once you have no more f u n c t i o n s to c all , the system w i l l c o ns i de r the c u r r e n t turn complete and proceed to the next turn or t a s k ._ 

_Here i s a l i s t of f u n c t i o n s in JSON format t h a t you can invoke . \ n{ f u n c t i o n s }\ n ”””_ 

## **B. Data Augmentation on Function Documents** 

_Parallel Functions Category_ : We created an additional user query that invoked the same function but with a different set of parameter values. This allowed us to expand the dataset by having multiple questions that invoked the same function, each with different input parameters. For example: 

Parallel Functions Augmentation query1 + [ _{_ ’name’: ’func1’, ’description’: ’order takeout’ _}_ ] -> ans1 query2 (which contains query1) + [ _{_ ’name’: ’func1’, ’description’: ’order takeout’ _}_ ] -> [ans1, ans2] 

The key transformation here is introducing query2 and generating ans2 based on a different set of parameter values. 

_Multiple Functions Category_ : In this category, we combined several function documents from different base entries to introduce distractor functions. However, the user query remained unmodified. These distractor functions were meant to test whether the model could accurately select the relevant function and not be misled by additional, unrelated function docs. GPT was used to ensure that none of the distractors could be alternative solutions to the function call. For example: 

Multiple Functions Augmentation query + [ _{_ ’name’: ’func1’, ’description’: ’order takeout’ _}_ ] -> ans1 query + [ _{_ ’name’: ’func1’, ’description’: ’order takeout’ _}_ , _{_ ’name’: ’func2’, ’description’: ’get weather’ _}_ ] -> [ans1] 

Here, the distractor func2 is added to test the model’s ability to focus on func1 and avoid being distracted by irrelevant functions. 

_Multiple Parallel Functions Category_ : We combined multiple user queries and function documents from different base

### Page 13

**The Berkeley Function Calling Leaderboard (BFCL): From Tool Use to Agentic Evaluation of Large Language Models** 

entries, ensuring that more function docs were combined than user queries. This transformation tested the model’s ability to handle multiple function calls and filter out unused functions. Some of the functions remained unused in the process, creating a more complex multi-query scenario. For example: 

## Multiple Parallel Functions Augmentation 

query1 + [func1] -> ans1 query1 + query2 + [func1, func2, func3] -> [ans1, ans2] 

The transformation here introduced query2 and added func2 and func3 while testing how the model handles the multiple function calls. 

_Function Parameter Removal_ : Based on the base entry, we asked GPT to remove one or more pieces of parameter information from the user prompt, while keeping the function document unchanged. In this case, the model was expected to either ask a follow-up question to clarify the missing information or return an error message instead of making a function call (which would be considered a hallucination). This will be used in the irrelevance category. For example: 

## Function Parameter Removal Augmentation 

query1 + [func1] -> ans1 query1’ (missing parameter info) + [func1] -> [No Function Call, Model asks for clarification.] 

The key transformation involved removing the necessary parameter info in query1’ and testing whether the model responded with a clarification or error message. 

_Function Removal_ : In this case, we removed one or more invoked functions from the function list in the augmented multiple parallel entries (from the previous step). The model was expected to either ask for more information on the missing function or produce an error indicating the absence of a relevant function for the query. This will be used in the irrelevance category. For example: 

## Function Removal Augmentation 

query1 + query2 + [func1, func2, func3] -> [ans1, ans2] query1 + query2 + [func1, func3] -> [No Function Call, Model asks for clarification.] 

The transformation involved removing func2 from the list and verifying whether the model recognized its absence, producing the appropriate error message. 

## **C. Single Turn Dataset Formal Definition** 

## **C.1. Dataset Structure** 

Each entry in the dataset consists of a user query, a list of candidate functions, and a corresponding expected model output: 

- **AST-based functions** : Each entry is represented as: 

**==> picture [315 x 26] intentionally omitted <==**

**==> picture [13 x 9] intentionally omitted <==**

- **Executable functions** : Each entry follows: 

**==> picture [378 x 28] intentionally omitted <==**

### Page 14

**The Berkeley Function Calling Leaderboard (BFCL): From Tool Use to Agentic Evaluation of Large Language Models** 

## **C.2. Dataset Categories** 

We categorize function-calling scenarios based on the number of available tools and the type of invocation: 

- **Simple (** _S_ **)** : Single available tool, single function invocation. 

**==> picture [281 x 13] intentionally omitted <==**

- **Multiple (** _M_ **)** : Multiple available tools, single function invocation. 

**==> picture [281 x 13] intentionally omitted <==**

**==> picture [477 x 170] intentionally omitted <==**

## **D. Multi-turn Dataset Formal Definition** 

## **D.1. Multi-turn Dataset Structure** 

**Dataset Structure** Each dataset entry consists of a multi-turn user query sequence and a corresponding ground truth function trajectory: 

**==> picture [439 x 26] intentionally omitted <==**

## **D.2. Dataset Categories** 

The dataset is divided into four categories: 

- **Base (** _B_ **)** : Standard multi-turn tasks where each turn has at least one expected function call. 

**==> picture [258 x 11] intentionally omitted <==**

- **Missing Parameters (** _MP_ **)** : One turn contains an underspecified query, and the expected assistant response is a natural language follow-up. 

- _∃i_ s.t. _τi_ = _∅, qi_ +1 resolves missing parameters _._ (11) 

- • **Missing Functions (** _MF_ **)** : One turn requests a function that is unavailable, prompting the assistant to respond with a clarification request. 

|||_∃i_s.t. _τi_ =_∅,_|_qi_+1provides missing function information_._|(12)|
|---|---|---|---|---|
|•|**Long Context (**_LC_**)**:|User queries and assistant responses in each turn contain a high number of tokens.|||
||||_∀i,_<br>_|qi|_+_|τi| ≫_1|(13)|

### Page 15

**The Berkeley Function Calling Leaderboard (BFCL): From Tool Use to Agentic Evaluation of Large Language Models** 

## **E. Data Generation Pipeline Implementation Details** 

## **E.1. Single-turn Dataset** 

**Data Collection** For the single-turn tasks, we divide the data collection into two categories based on their evaluation method: **AST** categories that use Abstract Syntax Tree, and **Execute** categories that evaluate by execution. The evaluation methodology is discussed in 4.1 and 4.2. _AST_ : We collect functions from popular GitHub repositories (top 100 starred) in Python, Java, and JavaScript. These functions are well-documented, making them ideal candidates for our downstream tasks. We exclude trivial functions such as ~~i~~ nit ~~, e~~ q , and functions with fewer than two parameters (excluding the self parameter) to ensure complexity and relevance. 

_Execute_ : The category is divided into two sub-categories based on the backend type. 1) **Pure Python Functions** : We manually constructed functions inspired by common math and physics calculations. These are purely executable Python functions that don’t rely on external APIs. 2) **Python Functions Wrapped APIs** : This sub-category includes functions that invoke API calls from popular public API providers such as ExchangeRate API, OMDb API, and Geocoding API. We focused on GET requests, as they are the most common in real-world scenarios. These functions demonstrate the model’s ability to generate executable REST API calls through complex function documentation, using requests.get() along with the API’s hardcoded URL and a description of the function’s purpose and parameters. 

**Data Preprocessing** We pre-process them to extract useful context for downstream data generation tasks. _AST_ : We extract function names, descriptions, parameter names, types, and default values directly from signatures and docstrings. 

_Execute_ : For executable functions, we use Python’s requests.get() as function document template. The schemas included base URLs, query parameters, path parameters, and body parameters. 

**Data Generation** We transform the extracted function information, such as docstrings from python functions and API documentation from ExchangeRate, into well-formatted function documents. This transformation ensures consistent formatting, including proper descriptions of parameters, types, and default values, making them compatible with our downstream evaluation pipeline. Once the function documentation was generated, realistic user questions were created based on these documents and their use in the original codebase or API context. 

**Data Transformation** To introduce complexity and mimic diverse real-world function-calling scenarios, we expand the dataset through various transformations detailed in B. These transformations included augmenting the entries to simulate different function calling patterns, such as parallel and multiple, and introducing scenarios with queries having incomplete or missing information to test the model’s behavior. 

**Data Validation** We ensure 1) function documentations adhered to the BFCL format, including all required function schema fields. 2) The function parameters are precisely defined and correctly categorized. 3) User prompts were relevant, clear, and properly aligned with the corresponding function documentation. We’ve instructed three human experts 

## **E.2. Crowd-sourced Dataset** 

**Data Collection** For the crowd-sourced dataset, 64,517 real-world user queries are collected between 2024-02-26 and 2024-04-01 via our hosted model endpoint. 

**Data Preprocessing** To preprocess the collected data: 

_Deduplication_ : We applied the ROUGE-L (Lin, 2004) score and OpenAI’s text-embedding models to remove duplicate queries and function docs. 

_Exclusion of Public Datasets_ : We filtered out any queries from public test sets such as those from Nexus Function Calling Leaderboard to prevent contamination. 

_Data Parsing_ : The valid function documentation was then parsed into a JSON format compatible with the BFCL evaluation pipeline.

### Page 16

**The Berkeley Function Calling Leaderboard (BFCL): From Tool Use to Agentic Evaluation of Large Language Models** 

**Data Generation** The expert-curated dataset doesn’t have a data generation phase, because all entries are authenticate user-contributed data. The result from the pre-processing phase go directly into the transformation phase. **Data Transformation** _Minimum Edit Transformation_ : Using the minimum edit principle, human annotators applied necessary corrections to improve clarity, precision, and consistency without changing the core content of the function docs or user prompts. 

**Data Validation** In addition to all the data validation step used in the single-turn section, we also make sure that 1) The transformed function doc and prompt preserve their original semantic meaning. 2) Any sensitive information in user prompts was replaced with placeholders to maintain privacy, and ambiguous content was clarified. 

## **E.3. Multi-turn Dataset** 

**Data Collection** The multi-turn dataset began with the creation of a custom API codebase that spanned eight domains, including Vehicle Control, Trading Bots, Travel Booking, File System, Messaging, Twitter, Ticket Booking, and Math. Each API was designed to simulate real-world multi-turn function calls. 

**Data Preprocessing** We constructed a graph of function dependencies, where each function represented a node, and edges mapped output dependencies. This setup allowed us to model realistic multi-turn interactions across different APIs and domains. 

**Data Generation** The data generation process for multi-turn interactions involved: 

- **Task Generation** : We prompt GPT-4o-0806a to invoke a series of function calls and then derive a natural langugage query that requires the function trajectories. The questions vary in tone and style to simulate different user personas and interaction scenarios. 

- Precisely, we adopted the dataset from Persona Hub (Ge et al., 2024) to generate a diverse evaluation dataset with different personas ranging from people with different occupations, age groups, etc. For example, a persona can look like: 

High school physics teachers Science historians Elderly hermits Each persona would have a unique style to phrase the request. 

- **Function Lists** : For each task, we provided a list of available functions from both primary and companion APIs. 

- **Initial Configurations** : We set up initial states (e.g., pre-authenticated sessions) to avoid unnecessary interactions and focus on meaningful multi-turn tasks. 

- **Human-labeled Ground Truth** : Expert human labelers reviewed and labeled each data point with ground truth for each multi-turn interaction. 

**Data Transformation** During data transformation, we scaled the dataset by sampling execution paths through the graph. Additionally, incomplete tasks were fixed by introducing additional configurations and function calls to maintain coherence. 

**Data Validation** Validation in multi-turn interactions involved: 

- **Question Validation** : Ensuring that the questions were specific and complete. 

- **Ground Truth Validation** : Verifying that the multi-turn function call sequences matched the ground truth. 

- **Initial Configuration Validation** : Ensuring that the initial configurations were complete and relevant to the multi-turn tasks. 

- **Function List Validation** : Checking that all necessary functions were included in the task’s function list. 

- **API Code Validation** : Using unit tests and format checkers to ensure that the API code was consistent and complied with the required standards.

### Page 17

**The Berkeley Function Calling Leaderboard (BFCL): From Tool Use to Agentic Evaluation of Large Language Models** 

## **F. LLM Judge BFCL Error Analyzer Implementation Details** 

We use GPT-4o-08-06 as a judge, using bespoke curator (Marten et al., 2025) for structured synthetic data generation. The judge prompt is formatted as follows, 

_”””_ 

_### ** Error A n a l y s i s Prompt **_ 

_**[Role :] ** You are an ** error a n a l y s i s e x p e r t ** tasked with i d e n t i f y i n g and c l a s s i f y i n g f a i l u r e s in the AI a s s i s t a n t ’ s responses . Your goal i s to determine i f and where the a s s i s t a n t f a i l e d , c a t e g o r i z i n g the root cause as one of the f o l l o w i n g : −** Failed to Understand Function Documentation ** −** Failed to Understand User ’ s Request ** −** Failed to Understand Environment S t a t e ** −**No_ 

_**[I n s t r u c t i o n s][:] ** C a r e f u l l y analyze the provided **[multi −turn] c o n v e r s a t i o n ** to i d e n t i f y any f a i l u r e s and t h e i r u n d e r l y i n g causes ._ 

_−−−_ 

_### ** I n i t i a l C o n f i g u r a t i o n and User Queries ** −** I n i t i a l C o n f i g u r a t i o n :** { i n i t i a l c o n f i g } −** Related Function Documentations :** { f u n c t i o n d o c u m e n t a t i o n } −** L i s t of User Queries :** { u s e r q u e r i e s }_ 

_−−−_ 

_### ** Evaluation Process ** Use the f o l l o w i n g g u i d e l i n e s to c r i t i c a l l y e v a l u a t e the multi −turn responses : 1. **[Compare] the model ’ s f u n c t i o n c a l l t r a c e s ** with the ground t r u t h f u n c t i o n c a l l t r a c e s to i d e n t i f y any d i s c r e p a n c i e s in API usage . 2. **[Compare] the end s t a t e ** with the ground t r u t h s t a t e to determine i f the model achieved the c o r r e c t outcome . 3. **[Pay] a t t e n t i o n to any m e c h a n i s t i c e r r o r s ** r ep o rt e d by the s t a t e checker , as t h e s e i n d i c a t e v a l i d a t i o n f a i l u r e s ._ 

_−−−_ 

_### ** Entry ID : { e n t r y i d }** #### **Turn−by−Turn Breakdown ** { turns breakdown }_ 

_−−−_ 

_### ** S t a t e Checker R e s u l t s ** { s t a t e c h e c k e r r e s u l t s }_

### Page 18

**The Berkeley Function Calling Leaderboard (BFCL): From Tool Use to Agentic Evaluation of Large Language Models** 

_−−−_ 

_### ** F a i l u r e C a t e g o r i z a t i o n ** A f a i l u r e occurs **[ONLY] ** i f : −The environment ’ s ** f i n a l s t a t e ** d i f f e r s from the **[ground] t r u t h s t a t e ** , OR −The a s s i s t a n t **[f a i l e d] to produce the minimum r eq u ir e d t r a j e c t o r y **. **[E x p l o r a t i o n] Steps ** −The a s s i s t a n t may take e x p l o r a t i o n steps , which may r e s u l t in e x e c u t i o n e r r o r s . −**Do not p e n a l i z e ** the a s s i s t a n t f o r e x p l o r a t i o n s t e p s . −** Only mark** the c r i t i c a l s t e p t h a t leads to the f a i l u r e . I f the **[s t a t e] checker r e p o r t s an error ** , a f a i l u r e **[d e f i n i t e l y ] **[occurred][.] I f the **[s t a t e] checker r e p o r t s ”None ”** , check i f the model f a i l e d to produce the **[minimum] r eq u ir e d t r a j e c t o r y **._ 

_−−−_ 

_### ** Example Failu re Analyses ** #### ** Example 1** **[Context :] ** Fuel tank has 5 g a l l o n s of gas i n i t i a l l y . Max c a p a c i t y i s 50 g a l l o n s . **[User :] ** *[F i l l] the f u e l tank u n t i l we are able to reach R i v e r m i s t . Oil c o s t s money so I j u s t need to reach there , I don ’ t need a f u l l tank .* **[A s s i s t a n t] Response :** ‘ f i l l F u e l T a n k ( fuel amount =50) ‘ **[Ground][Truth :] ** ‘ d i s p l a y C a r S t a t u s ( ’ f u e l ’) , f i l l F u e l T a n k ( fuelAmount =44) ‘_ 

_**[F a i l u r e] A n a l y s i s :** −** F a i l u r e Type :** * Failed to Understand Environment S t a t e * −** D e s c r i p t i o n :** The model f i l l e d the tank to maximum c a p a c i t y without checking the c u r r e n t f u e l l e v e l f i r s t . ID :** ‘0 ‘_ 

_−−−_ 

_#### ** Example 2** **[Context :] ** User has a t r a d i n g account with $10 ,000 balance . **[User :] ** *[I] want to buy some Apple stock , but f i r s t t e l l me i t s c u r r e n t p r i c e and make sure I can a f f o r d at l e a s t 5 shares . * **[A s s i s t a n t] Response :** ‘ e x e c u t e t r a d e ( symbol =’AAPL ’ , q u a n t i t y =5, o r d e r t y p e =’ market ’ , s i d e =’buy ’) ‘ **[Ground][Truth :] ** ‘ g e t s t o c k p r i c e ( symbol =’AAPL ’) ‘_ 

_**[F a i l u r e] A n a l y s i s :** −** F a i l u r e Type :** * Failed to Understand User ’ s Request * −** D e s c r i p t i o n :** The model executed a trade immediately when the user only r e q u e s t e d p r i c e i n f o r m a t i o n and a f f o r d a b i l i t y check . ID :** ‘0 ‘_ 

_−−−_ 

_### ** Final Task ** Now , i d e n t i f y the f a i l u r e s using the above c a t e g o r i z a t i o n . **[Only] i d e n t i f y ONE root cause of the f a i l u r e .**_

### Page 19

**The Berkeley Function Calling Leaderboard (BFCL): From Tool Use to Agentic Evaluation of Large Language Models** 

_I f t h e r e i s **[NO][f a i l u r e ] ** in ANY turn , **[r e p o r t] e x a c t l y ONE e n t r y ** with : −** F a i l u r e Type :** ‘No Failure ‘ −** D e s c r i p t i o n :** ‘No Failure Occurs ‘ −** Root Cause :** ‘No Failure Occurs ‘ ID :** ‘−1‘_ 

_### ** Your Failure A n a l y s i s :** ”””_ 

## **G. Function Calling Model Performance over time** 

PLease refer to Figure 7. 

**==> picture [389 x 234] intentionally omitted <==**

Figure 8: Models from 2023 and early 2024 struggled with reliable function calling at scale. As model sizes grew and function calling became a post-training objective, their capabilities improved significantly. 

## **H. BFCL AST Substring Matching** 

## **Parallel Tool Calls** 

By definition, _parallel_ tool calls execute simultaneously; therefore, their order is irrelevant. If strict sequencing _is_ required, the model must emit one function call at a time and wait for its completion before producing the next. 

Given a predicted sequence _A_ = [ _a_ 1 _, a_ 2 _, . . . , am_ ] and a ground-truth sequence _B_ = [ _b_ 1 _, b_ 2 _, . . . , bn_ ], 

- we do **not** require positional alignment; 

- any predicted call _ai_ may match any ground-truth call _bj_ . 

The evaluation follows an _all-or-nothing_ rule: if even a single ground-truth call is unmatched, the entire prediction fails. This ensures the model identifies _all_ required calls, regardless of order.

### Page 20

**The Berkeley Function Calling Leaderboard (BFCL): From Tool Use to Agentic Evaluation of Large Language Models** 

**==> picture [487 x 252] intentionally omitted <==**

Figure 9: BFCL AST Substring Matching procedure. The model response is parsed to extract function information in the systematic manner outlined above. 

## **Parameter Values** 

## INTEGER VS. FLOAT 

- **Python only** : an int may be supplied where a float is expected (Python auto-converts). 

- **Java & JavaScript** : when documentation specifies a float, the model must output a literal float (e.g. 5.0); an int such as 5 is incorrect. 

- Supplying a float for an int parameter is invalid in _all_ languages. 

## LIST AND TUPLE 

- Order matters: [1,2,3] = [2,3,1]. For order-agnostic questions, all permutations of the correct answer are enumerated. 

- Type matching is recursive for nested structures; outer and inner element types must satisfy the specification. 

## STRING 

- Comparison is case-insensitive. 

- All strings are standardized before checking: 

   - whitespace removed, 

   - punctuation ,./-_*ˆ (note: and ˆ) stripped. 

- **Examples** 

Possible dates: ["20th June", "2023-06-20", "06/20/2023", "Jun.20, 2023"] Possible locations: ["New York City", "NYC"] 

## DICTIONARY ( D ICT) 

- Key presence and value correctness are checked. 

- Key order is ignored (dictionaries are inherently unordered).

### Page 21

**The Berkeley Function Calling Leaderboard (BFCL): From Tool Use to Agentic Evaluation of Large Language Models** 

- LIST OF DICTIONARIES 

- The _list_ order of dictionaries matters. 

- Within each dictionary, key order does _not_ matter. 

## **Cross-Language Notes** 

For Java and JavaScript, strings representing code constructs are converted to Python equivalents using Tree-Sitters before evaluation. During conversion, parameter types are also validated (e.g. a Java long must end with L). 

## **I. Function Parameters Distribution** 

**==> picture [239 x 239] intentionally omitted <==**

**==> picture [239 x 239] intentionally omitted <==**

Figure 10: Distribution of functions (left) and function parameters (right) in BFCL dataset between single-turn and crowd-sourced categories. The histograms reveal that the crowd-sourced data entries have broader range and higher mean in both functions and parameters count compared to single-turn scenarios. It’s worth noting that in crowd-sourced, we have entries with 37 functions and functions with 21 parameters, where that max number for single-turn is only 3.36 and 3.69, respectively. 

## **J. Format Instruction Prompt for Agentic Task** 

This is the additional system prompt that models would receive on agentic dataset entries: 

_”””_ 

- _For your f i n a l answer to the user , you must respond in t h i s format : { ’ answer ’: A s h o r t and p r e c i s e answer to the question , ’ c o n t e x t ’: A b r i e f e x p l a n a t i o n of how you a r r i v e d at t h i s answer or why i t i s c o r r e c t } . I f you do not know the answer , respond with { ’ answer ’: ’ I do not know ’ , ’ c o n t e x t ’: ’ I do not know ’ } . I f you t h i n k the q u e s t i o n cannot be pr o pe r ly answered , response with { ’_ 

- _answer ’: ’ I cannot answer t h i s q u e s t i o n ’ , ’ c o n t e x t ’: A s h o r t reason e x p l a i n i n g why t h i s q u e s t i o n cannot be answered } ._ 

- _”””_

### Page 22

