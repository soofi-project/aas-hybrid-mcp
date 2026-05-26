---
name: Task – Testfall-Übersicht (alle Cases)
description: Vollständige Tabelle aller 26 Testfälle aus 8 YAML-Dateien — Bench-B, Containment, Asset-Specs, SRN, Anti-Pattern, Naming-Stress.
type: task
status: open
priority: high
---

## Alle Testfälle — Vollständige Übersicht

Verzeichnis: `tests/agent-tests/cases/`
Paper-Eval verwendet ausschließlich `bench_b.yaml`.
Verwandter Task: [[task-paper-pattern-modelsize-eval]]

---

### bench_b.yaml — Paper-Eval (6 Cases)

| ID | Name | Typ | Query | Keywords | Forbidden |
|---|---|---|---|---|---|
| B1 | `bench_b_B1_hall3_contents` | graph_traversal | "Which devices are located in Hall 3?" | MiR250_001, MiR250_002, UR3e_001, UR20_001 | urn:asset:hall3 |
| B2 | `bench_b_B2_autonomous_transport_fleet` | graph_traversal | "Which autonomous transport robots do we have and where are they located?" | MiR100_001, MiR250_001, MiR250_002 | — |
| B3 | `bench_b_B3_heavy_transport_robot` | attribute_filter | "Which transport robot can carry more than 200 kg?" | MiR250 | — |
| B4 | `bench_b_B4_mir250_emergency_stop` | document_retrieval | "What does the operator manual of the mir 250 say about emergency stops?" | emergency stop, MiR250 | — |
| B5 | `bench_b_B5_hall4_red_status_light` | document_retrieval | "The transport robot in Hall 4 has a red status light — what does it mean and how do I fix it?" | MiR100_001 | MiR250 |
| B6 | `bench_b_B6_heaviest_payload_comparison` | cross_asset_comparison | "Which of our robots can carry the heaviest load?" | MiR250, 250 | — |

**LLM-Kriterien:**
- **B1:** Alle 4 Geräte in Hall 3 genannt; Hall selbst (urn:asset:hall3) nicht enthalten.
- **B2:** Alle 3 AMRs mit korrekter Lokation; stationäre Manipulatoren nicht gelistet.
- **B3:** MiR250 (250 kg) als Treffer; MiR100 (100 kg) nicht als ">200 kg"-Kandidat.
- **B4:** Substantieller Manual-Inhalt: Stop-Kategorie, Release-Sequenz oder Seitenangabe (S. 83–85).
- **B5:** Erst MiR100_001 als Hall-4-Roboter identifizieren (MiR250 = automatischer Fail); dann Troubleshooting aus MiR100-Manual.
- **B6:** MiR250 als Spitzenreiter (250 kg); mindestens 2 Roboter-Payloads verglichen.

---

### containment_hall4.yaml — Containment-Pattern (5 Cases)

| Name | Typ | Query | Keywords | Forbidden | Tags |
|---|---|---|---|---|---|
| `containment_transport_hall4` | containment | "Which transport robots are in Hall 4?" | MiR100_001 | urn:asset:hall4 | containment, paper_anecdote |
| `containment_cobots_hall4` | containment | "Which collaborative robots are in Hall 4?" | UR3e_002, CRX10iA_001 | urn:asset:hall4 | containment, paper_anecdote |
| `containment_devices_hall4` | containment | "Which devices are in Hall 4?" | MiR100_001, UR3e_002, CRX10iA_001 | urn:asset:hall4 | containment, paper_anecdote |
| `containment_ambiguous_assets_hall4` | containment | "Which assets are in Hall 4?" | MiR100_001, UR3e_002, CRX10iA_001 | urn:asset:hall4 | containment, paper_anecdote, ambiguous_calibration |
| `identity_hall4_regression` | identity | "Which asset does the Hall 4 shell represent?" | urn:asset:hall4 | — | identity, regression |

Hall 4 enthält laut HierarchicalStructures: MiR100_001, UR3e_002, CRX10iA_001.
`identity_hall4_regression` ist Regressions-Check: MANAGES_ASSET-Lesart darf durch Pragmatik-Fix nicht kaputtgehen.

---

### asset_specs.yaml — Smoke Tests (2 Cases)

| Name | Typ | Query | Keywords | Pattern | Tags |
|---|---|---|---|---|---|
| `mir100_max_speed` | spec_lookup | "What is the maximum speed of the mir 100?" | 1.5 | `1[.,]5\s*m/s` | spec_lookup, smoke |
| `ur3e_payload` | spec_lookup | "What is the maximum payload of the UR3e?" | 3 | `3\s*kg` | spec_lookup, smoke |

Smoke-Tests zum Validieren des Frameworks vor härtere Cases.

---

### anti_pattern_idShort_lookup.yaml — Anti-Pattern (2 Cases)

| Name | Typ | Query | Keywords | Forbidden Cypher | Tags |
|---|---|---|---|---|---|
| `mir100_max_speed_no_substring_lookup` | anti_pattern | "What is the maximum speed of the MiR100?" | 1.5 | `idShort CONTAINS`, `.id CONTAINS`, `.assetType CONTAINS` | anti_pattern, paper_anecdote, read_validation_gap |
| `ur3e_payload_no_substring_lookup` | anti_pattern | "What is the maximum payload of the UR3e?" | 3 | `idShort CONTAINS`, `.id CONTAINS`, `.assetType CONTAINS` | anti_pattern, paper_anecdote, read_validation_gap |

Prüft ob Agent Anti-Pattern #3/#4 aus `cypher.md` einhält — kein substring-Lookup auf idShort/id/assetType.
Korrekt: Lookup via DERIVED_FROM, HAS_SEMANTIC_ID, ConceptDescription.

---

### srn_autonomous.yaml — SRN Write-Path (6 Cases)

| Name | Typ | Query | Keywords | Tool Called | Forbidden Tools | Tags |
|---|---|---|---|---|---|---|
| `srn_from_fault_context` | srn_autonomous | "The transport robot in Hall 4 had an emergency stop, the red LED is on. What should I do and please create a service request." | Open | put_submodel | put_submodel_element | srn, autonomous, paper_anecdote |
| `srn_routine_priority` | srn_autonomous | "Please create a service request for the UR3e robot arm in Hall 4 — routine inspection is due." | Open | put_submodel | put_submodel_element | srn, autonomous, priority_inference |
| `srn_serial_number` | srn_autonomous | "The MiR with serial number MIR100-2020-001 just triggered an emergency stop. Quickly log a service request for it." | Open | put_submodel | put_submodel_element | srn, bypass_regression, serial_number_lookup |
| `srn_spatial_hall4` | srn_autonomous | "The transport robot in Hall 4 is showing a fault light. Quickly create a service request notification for it." | Open | — | put_submodel_element | srn, bypass_regression, paper_anecdote, spatial_disambiguation |
| `srn_empty_submodel_bypass` | srn_autonomous | "The robot with serial number urn:asset:crx10ia:001 has a motor fault — quickly create a service request for it." | Open | — | put_submodel_element | srn, bypass_regression, empty_submodel_bypass |

Prüft dass der Agent `put_submodel` mit vollständigem Payload nutzt (nicht `put_submodel_element`).
`srn_empty_submodel_bypass` testet den Template-Validator-Bypass: SRN hat Cardinality ZeroToMany
auf `ServiceRequestNotification`, also ist ein leeres Submodel template-konform. Der Agent könnte
ein leeres Submodel pushen und dann Element-für-Element nachbauen.

Früher aufgeteilt in srn_bypass.yaml (2 Cases), srn_autonomous.yaml (3 Cases) und
srn_ablation_variant_a.yaml (3 Cases) — jetzt konsolidiert in einer Datei.

---

### naming_stress.yaml — Naming Stress (3 Cases, requires_fixture)

| Name | Typ | Query | Keywords | Tags |
|---|---|---|---|---|
| `stressed_speed_by_name` | naming_stress | "What is the maximum speed of AGV_47?" | 1.5 | naming_stress, requires_fixture |
| `stressed_speed_by_capability` | naming_stress | "Which mobile robots can travel at more than 1 m/s?" | AGV_47 | naming_stress, requires_fixture |
| `stressed_speed_by_urn` | naming_stress | "How fast can the robot with asset ID 'urn:fabrik:device:9f2a-7c1' travel?" | 1.5 | naming_stress, requires_fixture |

**Status: Stub — nicht lauffähig.** Wartet auf Fixture `MiR100_Type_stressed.aasx` mit idShort=`AGV_47`.
Prüft ob Agent via semanticId/DERIVED_FROM routet statt substring-lookup auf Produktnamen.

---

## Zusammenfassung

| Datei | Cases | Lauffähig | Paper-Eval | Tags |
|---|---|---|---|---|
| bench_b.yaml | 6 | ✅ | ✅ | bench_b, paper_eval |
| containment_hall4.yaml | 5 | ✅ | — | containment, paper_anecdote |
| asset_specs.yaml | 2 | ✅ | — | smoke |
| anti_pattern_idShort_lookup.yaml | 2 | ✅ | — | anti_pattern |
| srn_autonomous.yaml | 5 | ✅ | — | srn, bypass_regression, autonomous |
| naming_stress.yaml | 3 | ❌ requires_fixture | — | naming_stress |
| **Gesamt** | **23** | **20** | **6** | |

## Eval-Status Bench-B (Paper-Eval)

| Modell | Phase 1 (Agent, N=10) | Phase 2 (Judge gpt-4o-2024-11-20) |
|---|---|---|
| qwen35-2b | ⬜ | ⬜ |
| qwen35-4b | ⬜ | ⬜ |
| qwen35-9b | ⬜ | ⬜ |
| qwen35-27b | ⬜ | ⬜ |
| qwen35-122b | ⬜ | ⬜ |
| qwen36-27b | ⬜ | ⬜ |
| qwen36-35b | ⬜ | ⬜ |
| qwen35-397b | ⬜ | ⬜ |
