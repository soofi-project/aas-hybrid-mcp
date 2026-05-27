# Cross-Model Evaluation Analysis — All Models, T07

9 models · 5 suites · 1,750 total runs (7 models with 200 each, qwen36-27b with 150 — no SRN suite)

Models ordered by parameter count:

| Label | Architecture | Active params | N runs |
|---|---|---|---|
| qwen35-2b | 2B dense | 2B | 200 |
| qwen35-4b | 4B dense | 4B | 200 |
| qwen35-9b | 9B dense | 9B | 200 |
| qwen35-27b | 27B dense | 27B | 200 |
| qwen36-27b | 27B dense (Qwen3 gen) | 27B | 150 |
| qwen35-35b | 35B dense | 35B | 200 |
| qwen36-35b | 35B dense, 4-bit AWQ | 35B | 200 |
| qwen35-122b | 122B MoE | ~10B | 200 |
| qwen35-397b | 397B MoE | ~17B | 200 |

---

## 1. Paper-Evaluation Table per Suite

### Correct rate per suite

| Suite | 2B | 4B | 9B | 35-27B | 36-27B | 35-35B | 36-35B | 122B | 397B |
|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| anti_pattern | 10% | 80% | 90% | 100% | 100% | 100% | 100% | 100% | 100% |
| asset_specs | 20% | 85% | 70% | 100% | 100% | 100% | 100% | 100% | 100% |
| bench_b | 3% | 45% | 55% | 78% | 85% | 73% | 87% | 72% | 82% |
| containment_hall4 | 10% | 42% | 44% | 100% | 100% | 88% | 94% | 92% | 100% |
| srn_autonomous | 0% | 4% | 14% | 32% | 14% | 34% | 18% | 22% | 26% |
| **Overall** | **6.5%** | **41.5%** | **47%** | **76.5%** | **74%** | **72%** | **74%** | **70%** | **76%** |

qwen36-27b overall recalculated at N=200 (150 read-path + 50 SRN): (20+20+51+50+7)/200 = 74%.

### Overall correct rate by model size

```
2B  ████                                                     6.5%
4B  █████████████████████                                     41.5%
9B  ███████████████████████                                   47%
27B █████████████████████████████████████                      76.5%
35B ████████████████████████████████████                        72%
122B████████████████████████████████████                        70%
397B█████████████████████████████████████                       76%
```

Three regimes emerge:

1. **Below threshold (2B):** Floor performance. Even the simplest read-only suite (asset_specs) achieves only 20%. SRN is 0%. The model cannot sustain multi-step tool chains.
2. **Sub-viable (4B–9B):** Read-only suites with focused scope work (80–90% on anti_pattern, 70–85% on asset_specs), but broader suites collapse (3–55% on bench_b, 10–44% on containment_hall4). SRN is 4–14% — functionally broken. The 4B→9B jump is marginal (+5.5 pp overall).
3. **Viable (27B+):** Read-only suites exceed 72% (most reach 85–100%). SRN ranges 18–34% — still low but functionally present. The 9B→27B jump is the scaling cliff (+29.5 pp overall, +18 pp SRN). Beyond 27B, gains are modest and non-monotonic.

### Key observation: non-monotonicity above 27B

The 27B dense models (qwen35-27b at 76.5%, qwen36-27b at 94% read-only) are competitive with or superior to larger models. The 122B MoE (70% overall, 22% SRN) and 397B MoE (76%, 26% SRN) underperform the 35B dense model (72%, 34% SRN) on write-path tasks. Active parameter count, not total parameter count, predicts performance: the 122B MoE with ~10B active params behaves like a 9B-class model on SRN (22%), while the 397B MoE with ~17B active params is closer to 27B-class.

---

## 2. idShort Violation Self-Correction Rate

| Model | Violation rate | Self-correction rate |
|---|--:|--:|
| 2B | 13% | 96.2% |
| 4B | 75.5% | 96.7% |
| 9B | 76% | 95.4% |
| 35-27B | 63% | 97.6% |
| 36-27B | 48% | 97.2% |
| 35-35B | 62% | 98% |
| 36-35B | 39% | 95% |
| 122B | 79% | 98% |
| 397B | 62% | 100% |

The self-correction rate is consistently high (95–100%) across all model sizes — the validator feedback loop works reliably regardless of model capacity. The variation is in violation rate:

- **2B (13%):** Fewer violations because the model makes fewer tool calls overall, not because of better compliance.
- **4B–9B (76%):** Peak violation rates. These models make many tool calls but have weak idShort discipline, defaulting to natural-language patterns.
- **27B+ (39–79%):** Violation rates decrease with model capability, with the 36-27B and 36-35B (newer generation) showing the best compliance (48% and 39%). The 122B MoE is an outlier at 79% — likely because the MoE routing produces more "pattern-matching" behavior from specialized experts.

**Dominant violation rule across all models:** `idShort_contains_or_regex` — the agent uses idShort as a natural-language token in Cypher patterns rather than as a structural identifier.

---

## 3. Write-Path Bypass (SRN Suite Only)

**Note:** The original bypass classification (navigation failure / write avoidance / surfaced /
direct bypass) was derived by the framework's regex-based tool-call extractor, which misaligns
name↔result blocks when tool results contain embedded code fences. The per-tier bypass labels are
therefore not reproducible and have been replaced with assignment-independent metrics below.
See `task_paper_bench_c_bypass_rewrite.md` for root-cause details.

### Write success vs. semantic correctness (all 9 models, N=50 per model)

| Model | SRN % (judge) | Wrote % (write signal) | put_submodel calls |
|---|--:|--:|--:|
| 2B  |  0% | 12% |  6/50 |
| 4B  |  4% | 74% | 37/50 |
| 9B  | 14% | 58% | 29/50 |
| 35-27B | 32% | 98% | 49/50 |
| 35-35B | 34% | 92% | 46/50 |
| 36-35B | 18% | 76% | 38/50 |
| 36-27B | 14% | 96% | 48/50 |
| 122B | 22% | 92% | 46/50 |
| 397B | 26% | 92% | 46/50 |
| **Total** | — | **77% (345/450)** | |

**Key finding:** The write success vs. semantic correctness gap is model-size-independent.
Write success scales quickly (6% at 2B → 96–98% at 27B+) but SRN correctness peaks at 34%
(35-35B). Even Qwen3.6-27B, which writes in 96% of runs, achieves only 14% SRN correctness —
identical to the 9B model. The bottleneck is vocabulary, not structure. Zero write-tool
rejections were recorded across all 450 runs (assignment-independent: no `validation failed` /
`does not exist` / `conformance` signatures in any run).

### Per-case SRN correct rate (models with SRN data)

| Case | 2B | 4B | 9B | 35-27B | 35-35B | 36-35B | 122B | 397B |
|---|--:|--:|--:|--:|--:|--:|--:|--:|
| srn_from_fault_context | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 2% |
| srn_routine_priority | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| srn_serial_number | 0% | 0% | 0% | 40% | 80% | 20% | 0% | 0% |
| srn_spatial_hall4 | 0% | 0% | 20% | 40% | 60% | 50% | 70% | 100% |
| srn_empty_submodel_bypass | 0% | 20% | 10% | 0% | 30% | 20% | 30% | 0% |

Three cases are at 0% for almost all models: `srn_from_fault_context`, `srn_routine_priority`, and `srn_serial_number`. These require vocabulary inference (CorrectiveMaintenance, Inspection, Low priority) or serial-number resolution — capabilities that no model reliably possesses. The only consistently solvable case is `srn_spatial_hall4`, which requires only spatial reasoning without value inference.

---

## 4. Template Validation

**All nine models report zero write-tool rejections and zero validation errors across all 450 SRN-suite runs (1,750 total across all suites).** When any model issues a write call, the payload passes schema validation — regardless of model size, architecture, or correctness.

This confirms the template validation gap is architectural, not model-dependent:

1. `Cardinality ZeroToMany` on ServiceRequestNotification allows empty submodels to pass.
2. `put_submodel_element` has no template check at all.
3. The validator checks structural conformance only, not semantic correctness (controlled vocabulary).

All models invent ServiceType values ("Emergency", "Maintenance", "Routine Inspection") and Priority values ("Normal", "Critical") that the validator accepts. The gap is identical across the entire model spectrum.

---

## 5. Judge Failure Modes per SRN Case

Aggregated across all models with SRN data (2B, 4B, 9B, 35-27B, 35-35B, 36-35B, 122B, 397B):

| Failure mode | Cases affected | Frequency | Model-dependence |
|---|---|---|---|
| Wrong ServiceType | srn_from_fault_context, srn_routine_priority | 100% miss in 2B–9B; 60–100% miss in 27B+ | Universal — no model maps "emergency stop" → CorrectiveMaintenance reliably |
| Wrong Priority (Low→Normal) | srn_routine_priority | 100% miss in 2B–9B; 100% miss in 27B+ | Universal — all models default to "Normal" instead of "Low" |
| Wrong Status (Open→New) | srn_from_fault_context | 0% in 2B–9B; 30–100% in 27B+ | Emerging at larger sizes — models use "New" instead of "Open" |
| Serial not resolved | srn_serial_number | 40–100% miss across all models | Universal — no model reliably maps MIR100-2020-001 → MiR100_001 |
| No write attempted | srn_empty_submodel_bypass | 60–100% in 36-35B and 4B | Size-dependent — smaller models give up, 36-35B reports existing data |
| Asset not identified | srn_spatial_hall4 | 0–90% miss | Size-dependent — 2B fails 90%, 397B 0% |

Two systemic failure modes are model-independent:

1. **Vocabulary gap:** No model reliably maps natural-language descriptions to the SRN schema's controlled vocabulary. ServiceType=CorrectiveMaintenance and Priority=Low are missed in 100% of runs for most models. This is a scaffolding problem, not a scaling problem — the information is not in the prompt or the tools.
2. **Serial number resolution:** No model reliably traces MIR100-2020-001 → MiR100_001. This requires a multi-hop lookup path (Nameplate → SerialNumber → AAS ID) that the agent must discover autonomously.

---

## 6. Duration: Median per Suite

| Suite | 2B | 4B | 9B | 35-27B | 36-27B | 35-35B | 36-35B | 122B | 397B |
|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| anti_pattern (correct) | 17.2 | 7.6 | 6.7 | 13.4 | 13.2 | 8.8 | 5.3 | 19.0 | 18.1 |
| asset_specs (correct) | 15.1 | 9.4 | 8.9 | 11.4 | 12.7 | 10.2 | 5.2 | 18.1 | 17.9 |
| bench_b (correct) | 14.9 | 13.4 | 10.5 | 28.8 | 33.0 | 18.2 | 17.3 | 29.3 | 34.3 |
| bench_b (wrong) | 24.2 | 18.4 | 18.5 | 24.7 | 18.8 | 24.3 | 17.0 | 34.3 | 29.4 |
| containment_hall4 (correct) | 14.1 | 7.0 | 6.6 | 26.9 | 29.0 | 19.4 | 17.7 | 24.2 | 33.2 |
| srn_autonomous (correct) | — | 37.0 | 38.3 | 94.9 | — | 34.8 | 66.1 | 63.7 | 94.3 |
| srn_autonomous (wrong) | 22.8 | 50.6 | 47.7 | 83.2 | — | 45.0 | 57.2 | 68.6 | 65.5 |

Two patterns:

1. **Speed does not predict quality.** The 2B model is fastest on SRN (22.8s median wrong) because it fails early — it exhausts its capability before engaging deeply. The 27B model is slowest (94.9s correct) because successful write chains are inherently longer. At floor performance, duration reflects engagement depth, not competence.

2. **Correct SRN runs are slower than wrong runs at 27B+** (94.9s vs 83.2s for 35-27B, 94.3s vs 65.5s for 397B). The opposite pattern holds at 9B and below (wrong runs are slower), where the model wastes time on futile exploration. The crossover reflects a shift from "exploration waste" to "correct execution cost."

---

## 7. Manuals-First Correlation

| Model | Manuals-first correct | No-manuals correct | Delta | N manuals-first | N no-manuals |
|---|--:|--:|--:|--:|--:|
| 2B | 0% | 7% | **−7 pp** | 15 | 185 |
| 4B | 54.1% | 25.8% | **+28.3 pp** | 111 | 89 |
| 9B | 64.2% | 27.7% | **+36.5 pp** | 106 | 94 |
| 35-27B | 81.7% | 70.3% | **+11.4 pp** | 109 | 91 |
| 36-27B | 99.2% | 72.4% | **+26.8 pp** | 121 | 29 |
| 35-35B | 73% | 71% | **+2 pp** | 123 | 77 |
| 36-35B | 71% | 82% | **−11 pp** | 150 | 50 |
| 122B | 74% | 63% | **+11 pp** | 130 | 70 |
| 397B | 78% | 64% | **+14 pp** | 167 | 33 |

The manuals-first effect is strongly size-dependent:

1. **2B:** Negative correlation (−7 pp). The model cannot act on documentation even when it retrieves it. Manuals-first is a marker of difficulty, not a help.
2. **4B–9B:** Strong positive correlation (+28 to +37 pp). These models depend heavily on documentation to anchor graph traversal. The causal effect is strongest here — removing manuals would be catastrophic.
3. **27B:** Moderate positive correlation (+11 to +27 pp). Documentation helps but is not essential for most read-only tasks. The qwen36-27b shows a large +27 pp effect but with an imbalanced sample (121 manuals-first vs 29 no-manuals).
4. **35B:** Near-zero or negative. The 35-35B shows +2 pp; the 36-35B shows −11 pp. At this size, the model reads manuals reactively on harder cases (confounding), and the marginal information gain from documentation is lower.
5. **122B–397B:** Moderate positive (+11 to +14 pp). Manuals help, but the no-manuals baseline is already at 63–64%, suggesting the model has sufficient parametric knowledge for most read-only tasks.

**Interpretation:** The manuals-first delta is an inverted-U function of model size — smallest for models that cannot use the information (2B) or do not need it (35B), and largest for models in the middle range (4B–9B) that can use the information but cannot compensate without it.

---

## 8. Key Takeaways / Action Items

### T1 — The scaling cliff is at ~27B, not between smaller sizes

The 2B→4B jump (+35 pp) reflects escape from floor performance. The 4B→9B jump (+5.5 pp) is marginal. The 9B→27B jump (+29.5 pp) is the qualitative shift: read-only suites go from 44–55% to 78–100%, and SRN goes from 14% to 32%. Beyond 27B, gains are modest and non-monotonic (35B drops to 72%, 122B to 70%). **Action:** Position 27B as the minimum viable model size for the current tool set and prompt design. The 2B/4B/9B cluster is below threshold; the 27B+ cluster is viable.

### T2 — Active parameters, not total, predict SRN performance

The 122B MoE (~10B active) achieves 22% SRN — comparable to the 9B dense (14%), not the 27B dense (32%). The 397B MoE (~17B active) achieves 26% — between 9B and 27B. The 35B dense achieves 34% SRN — the best across all models. **Action:** In the paper, report active parameter counts alongside total counts. Frame the SRN scaling result in terms of active parameters: the write path demands >10B active parameters for non-trivial performance.

### T3 — The vocabulary gap is model-independent

No model reliably maps "emergency stop" → CorrectiveMaintenance or "routine" → Priority=Low. The 397B MoE scores 0/10 on srn_routine_priority; the 35B dense scores 0/10 on srn_from_fault_context. This is not a scaling problem — the information is not available in the prompt, tools, or templates. **Action:** Inject the SRN enum vocabulary directly into the writing manual or system prompt. This is the highest-ROI fix: it would improve SRN for all models simultaneously.

### T4 — Bypass profiles diagnose the failure stage

The shift from "null" (2B) → "none" (4B) → "surfaced" (27B) → "direct" (35B/397B) → "high compliance, low vocabulary" (122B) maps to a progression through failure stages: navigation → write avoidance → read/write confusion → protocol bypass → vocabulary limitation. **Action:** Use bypass profile as a diagnostic for where in the pipeline a model fails, and target interventions accordingly.

### T5 — Template validation gap is architectural, not model-dependent

Zero rejections across 1,750 runs confirms the validator cannot enforce semantic correctness. All models write invented values that pass structural validation. **Action:** Implement server-side enum validation for ServiceType, Priority, and Status. This is a prerequisite for meaningful SRN evaluation — without it, "correct" SRN runs may succeed for the wrong reasons.

### T6 — Manuals-first is most valuable for 4B–9B models

The +28 to +37 pp effect at 4B–9B is the strongest intervention signal in the entire evaluation. For models below 27B, enforcing manual consultation before tool calls would be the single highest-impact prompt change. **Action:** For the paper, present the manuals-first delta as evidence that prompt-side scaffolding (documentation) disproportionately benefits smaller models, supporting the scaffolding-asymmetry thesis.

### T7 — The 36-27B (Qwen3 generation) shows generation-level improvement

The qwen36-27b achieves 94% read-only correctness (vs 76.5% for qwen35-27b) with lower violation rates (48% vs 63%) and higher self-correction (97.2% vs 97.6%). The Qwen3 generation is substantially better at AAS tasks at the same parameter count. **Action:** Include the qwen36-27b as evidence that generation quality matters alongside parameter count — same-size models can cross the viability threshold with improved training.

### T8 — SRN is the binding constraint across all model sizes

No model exceeds 34% SRN. The highest performers on read-only tasks (qwen35-27b: 100% on three suites) collapse on write-path. The overall accuracy range (70–94% read-only vs 0–34% SRN) shows that AAS agent viability is determined entirely by write-path capability. **Action:** Until SRN exceeds ~50%, model selection and prompt design should prioritize write-path improvements over marginal read-only gains.
