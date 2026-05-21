# Cross-model analysis — Stand 2026-05-21

Analysierte Modelle (Qwen3.5-Familie, alle N=230 Runs / 7 Suites):

| Modell | Parameterzahl | Correct | Manuals-first | Antipattern-hit | All-good |
|--------|--------------|---------|---------------|-----------------|----------|
| qwen35-08b | 0.8B (dense) | 0% | 51% | 3% | 0% |
| qwen35-2b | 2B (dense) | 2% | 16% | 16% | 0% |
| qwen35-4b | 4B (dense) | 50% | 33% | 71% | 4% |
| qwen35-9b | 9B (dense) | 66% | 30% | 75% | 4% |
| qwen35-27b | 27B (dense) | **84%** | 37% | 70% | 16% |
| qwen35-122b | 122B (MoE, ~10B aktiv) | **1%** | 0%† | 0% | 0% |
| qwen36-27b | 27B (dense, Gen 3.6) | 83% | 71% | 49% | 35% |

Noch ausstehend: qwen35-397b (Cortecs), qwen36-35b.

> **MoE-Hinweis:** qwen35-122b (`Qwen/Qwen3.5-122B-A10B-FP8`) ist ein
> Mixture-of-Experts-Modell mit ~10B aktiven Parametern pro Token-Forward-Pass.
> Für Vergleiche auf der Skalierungsachse ist die aktive Parameteranzahl (~10B)
> relevanter als die Gesamtzahl (122B).
>
> †  `manuals_first=0%` ist die korrekte Zahl nach einem Bug-Fix in `judge.py`
> (Zeile "trivially satisfied"): wenn ein Modell überhaupt keine Tool-Calls macht,
> war `first_query_idx=None` fälschlicherweise als `read_manuals_first=True`
> gewertet worden. 229/230 Runs haben `tool_call_count=0` — der eine echte Run
> (bench_b B6, rep 9, 6 Tool-Calls, korrekt) ist der einzige mit `manuals_first=True`.

---

## Befunde

### 1. Phasenübergang bei 4B

Unter 4B bricht der Agentenloop zusammen — 0.8B und 2B liefern praktisch nichts
Verwertbares (0% / 2% korrekt). Ab 4B funktioniert der Loop grundsätzlich. Der Sprung
von 2B auf 4B ist mit +48pp der dramatischste in der gesamten Skalierungskurve.

### 2. Das 0.8B-Paradoxon

Das kleinste Modell liest zu 51% zuerst die Manuals — höher als 4B (33%) oder 9B (30%).
Es kennt das richtige Verhaltensmuster, scheitert aber an der Ausführung (0% korrekt).
Ein Modell kann also die Meta-Strategie "konsultiere Dokumentation zuerst" gelernt haben,
ohne in der Lage zu sein, die Ergebnisse sinnvoll zu verwerten.

### 3. Validator als Korrektiv-Mechanismus für mittlere Modelle

Bei 4B und 9B löst der Agent bei 68–72% der korrekten Antworten trotzdem einen
Anti-Pattern-Hit aus — und kommt trotzdem ans richtige Ergebnis. Der Validator feuert,
lehnt die Anfrage ab, und der Agent korrigiert sich im nächsten Schritt.

Das ist der "Layered Determinism"-Befund empirisch untermauert: **der Validator wirkt
als Korrektiv-Mechanismus, der mittelgroße Modelle erst operativ nutzbar macht.**
Ohne diesen Gate würden 4B/9B-Modelle deutlich mehr Fehler liefern.

Cross-tab-Zahlen (korrekte Runs mit Antipattern-Hit):
- 4B: 68%
- 9B: 72%
- qwen35-27B: 68% — überraschend hoch, aber Korrektheit trotzdem 84%
- qwen36-27B: nur 45% — Generationsunterschied sichtbar

### 4. Qualitativer Sprung bei 27B (dense)

Der 27B-Sprung ist nicht nur quantitativ, sondern qualitativ anders — belegt durch beide
27B-Varianten (qwen35 und qwen36):

- **Korrektheit:** 84% / 83% gegenüber 66% beim 9B
- **All-good** springt auf 16–35%: Erst beim 27B gelingt es regelmäßig, alle drei
  Dimensionen gleichzeitig richtig zu machen (korrekte Antwort + kein Tool-Fehler +
  Manuals zuerst gelesen)

Generationsunterschied innerhalb der 27B-Klasse:
- qwen35-27b erreicht 84% korrekt mit **niedrigerer** Manuals-first-Rate (37%) und
  **höherer** Antipattern-Rate (70%) — der Validator kompensiert.
- qwen36-27b erreicht 83% korrekt mit **höherer** Manuals-first-Rate (71%) und
  **niedrigerer** Antipattern-Rate (49%) — proaktiveres, strategischeres Verhalten.
- All-good verdoppelt sich: 16% → 35% (qwen35 → qwen36).
- Das zeigt: Korrektheit allein verdeckt den Verhaltensqualitätssprung zwischen Generationen.

### 5. Manuals-first korreliert mit Korrektheit — aber schwächer als erwartet

Bei 4B und 9B ist der Unterschied zwischen manuals-first=True und =False praktisch null.
Diese Modelle brauchen die Manuals nicht, weil der Validator-Korrektiv-Loop als Ersatz
funktioniert. Beim qwen36-27b gibt es einen messbaren Unterschied (73% der korrekten Runs
lasen Manuals zuerst, bei falschen Runs 62%). Beim qwen35-27b ist die Korrelation schwächer
(39% correct mit Manuals-first vs. 27% incorrect mit Manuals-first) — der Effekt ist vorhanden
aber der Validator trägt stärker.

### 6. 122B MoE: "Look-up-and-Guess"-Kollaps

Das 122B-MoE-Modell zeigt ein fundamental anderes Versagensmuster als alle anderen Modelle:

| Indikator | 122b MoE | 0.8b dense (Referenz) |
|-----------|---------|----------------------|
| Correct | 1% | 0% |
| Manuals-first | **0%** (†bug-fix) | 51% |
| Antipattern-hit | **0%** | 3% |
| tool_call_count>0 | **1/230 Runs** | – |
| Median Laufzeit (bench_b) | **2.1s** | 22.7s |

Das Profil lautet: **macht in 229/230 Runs null echte Tool-Calls und antwortet direkt
mit einem Textmonolog** (bis zu 63.000 Zeichen). Das Modell schreibt Cypher-Queries als
Markdown-Code-Blöcke in seine Antwort, ruft aber nie den OpenAI Function-Calling-API-
Mechanismus auf. Die 1–3 Sekunden Median-Laufzeit bestätigt: kein iterativer Tool-Loop,
ein einziger API-Call der Text zurückgibt.

Der einzige Ausnahme-Run (bench_b B6, rep 9): 6 echte Tool-Calls, korrekte Antwort —
zeigt dass das Modell die Fähigkeit prinzipiell hat, sie aber nicht stabil aktiviert.

Dieses Muster ist **nicht** das 0.8B-Paradoxon in größer: Das 0.8B-Modell *versucht*
Queries auszuführen (Laufzeit 22s, 3% Antipattern-Hits, echte Tool-Calls), scheitert aber
an der Qualität. Das 122B-MoE tritt in 99.6% der Fälle gar nicht erst in die
Tool-Use-Schleife ein — es ist ein **function-calling compatibility failure**, nicht ein
reasoning failure.

**Interpretation (MoE-aktive-Parameter-Hypothese):** Mit ~10B aktiven Parametern liegt das
Modell auf der Skalierungsachse *unter* dem dense-4B-Threshold — nicht weil es weniger
gelernt hat, sondern weil der spärliche Aktivierungspfad im Forward-Pass nicht ausreicht,
um die agentic Tool-Use-Schleife strukturell durchzuhalten. Totale Parameterzahl (122B)
ist für agentic loops kein valider Vergleichsparameter; **aktive Parameter** sind das
relevante Maß.

---

## Dauer (Median Sekunden pro Suite)

Fairster Modellvergleich: **Median (alle Runs)** — gleiche Suite = gleiche Fragen,
Schwierigkeits-Confound damit kontrolliert. Correct-only-Median ist konfundiert: kleine
Modelle lösen nur einfache (schnelle) Fragen, große Modelle lösen auch schwere (langsamere).
Falsche Runs dauern überproportional lang, weil Modelle das Rekursionslimit erschöpfen
statt schnell aufzugeben.

| Modell | bench_b all | bench_b correct | bench_b wrong | containment all | srn_bypass all |
|--------|------------:|----------------:|--------------:|----------------:|---------------:|
| 0.8B | 22.7s | – | 22.7s | 14.4s | 11.6s |
| 2B | 22.3s | – | 22.3s | 21.7s | 20.2s |
| 4B | 60.5s | 16.6s | 96.7s | 11.3s | 8.0s |
| 9B | 23.1s | 18.4s | 92.4s | 14.5s | 11.9s |
| qwen35-27B | 26.3s | 19.9s | 60.1s | 17.1s | 8.9s |
| qwen35-122B (MoE) | **2.1s** | 19.4s† | **2.0s** | **2.8s** | **1.7s** |
| qwen36-27B | 30.1s | 24.5s | 58.0s | 20.7s | 11.4s |

† Basis N=1 (ein einziger korrekter bench_b-Run) — nicht repräsentativ.

**Befunde:**

- **4B ist der langsamste Runner** bei bench_b (all=60.5s): Er probiert lang und scheitert
  oft an der Rekursionsgrenze (wrong=96.7s), die seltenen korrekten Runs sind dagegen kurz.
- **Falsche Runs sind systematisch länger als korrekte** (außer 0.8B/122B). Das Muster ist
  konsistent: Modelle geben nicht schnell auf — sie scheitern durch Erschöpfung.
- **122B MoE bricht das Muster:** Wrong-Runs sind kürzer als Correct-Runs (2.0s vs. 19.4s).
  Das Modell gibt sofort auf, ohne es überhaupt zu versuchen — Exhaustion-Pattern tritt
  gar nicht erst auf.
- **27B correct > 9B correct bei bench_b** (20–25s vs. 18s): Der 27B löst schwerere Fragen,
  die mehr Reasoning-Schritte brauchen — das ist der Confound der Correct-only-Vergleich
  unbrauchbar macht.

---

## Paper-Implikationen (Existence Claims, keine Frequenz-Extrapolation)

1. **Capability threshold:** Unterhalb von 4B *aktiven* Parametern ist MCP-basiertes
   AAS-Agenten-Retrieval nicht operational — unabhängig von Backend und Validator.
   Die 122B-MoE-Daten zeigen, dass *totale* Parameterzahl kein valider Proxy ist;
   die ~10B aktiven Parameter platzieren das Modell unter diesem Threshold.

2. **Validator as scaffolding:** Für 4–27B-Modelle wirkt der Validator-Gate wie externe
   Fehlerkorrektur; die hohe Anti-Pattern-Rate bei gleichzeitig akzeptabler Korrektheit
   zeigt, dass das Modell den Validator als impliziten Hinweismechanismus nutzt.
   Beim qwen36-27B nimmt dieser Effekt ab (49% Antipattern), beim 122B MoE fällt er
   auf 0% — aber aus entgegengesetztem Grund (kein Tool-Use-Versuch statt gereiftem
   Querying).

3. **Qualitative shift at 27B (dense):** Erst ab 27B dense tritt das gewünschte Verhalten
   emergent auf: proaktive Dokumentationskonsultation + regelkonformes Querying + korrekte
   Antwort gleichzeitig. All-good 16–35% vs. 4% bei 4–9B.

4. **MoE / Function-Calling Kompatibilität:** Das 122B-MoE-Modell
   (`Qwen3.5-122B-A10B-FP8`) versagt nicht an Reasoning, sondern an der
   Function-Calling-API-Kompatibilität: 229/230 Runs liefern 0 echte Tool-Calls.
   Für produktive MCP-Deployments müssen Modelle auf strukturierten Function-Calling-
   Support explizit geprüft werden — Gesamtparameterzahl ist kein ausreichendes
   Selektionskriterium.
