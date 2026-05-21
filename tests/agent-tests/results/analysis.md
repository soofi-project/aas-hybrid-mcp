# Cross-model analysis — Zwischenstand 2026-05-20

Analysierte Modelle (Qwen3.5-Familie, alle N=230 Runs / 7 Suites):

| Modell | Parameterzahl | Correct | Manuals-first | Antipattern-hit | All-good |
|--------|--------------|---------|---------------|-----------------|----------|
| qwen35-08b | 0.8B | 0% | 51% | 3% | 0% |
| qwen35-2b | 2B | 2% | 16% | 16% | 0% |
| qwen35-4b | 4B | 50% | 33% | 71% | 4% |
| qwen35-9b | 9B | 66% | 30% | 75% | 4% |
| qwen36-27b | 27B | 83% | 71% | 49% | 35% |

Noch ausstehend: qwen35-27b, qwen35-122b, qwen35-397b (Cortecs), qwen36-35b.

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

Cross-tab-Zahlen:
- 4B: 68% der korrekten Runs hatten trotzdem einen Anti-Pattern-Hit
- 9B: 72% der korrekten Runs hatten trotzdem einen Anti-Pattern-Hit
- 27B: nur 45% — das Modell braucht den Korrektiv-Loop seltener

### 4. Qualitativer Sprung bei 27B

Der 27B-Sprung ist nicht nur quantitativ (83% korrekt), sondern qualitativ anders:

- **Proaktive Dokumentationskonsultation:** 71% Manuals-first (vs. 30–33% bei 4B/9B)
- **Bessere Query-Qualität:** 49% Anti-Pattern-Rate vs. 71–75% bei 4B/9B
- **All-good springt von 4% auf 35%:** Erst beim 27B gelingt es regelmäßig, alle drei
  Dimensionen gleichzeitig richtig zu machen (korrekte Antwort + kein Tool-Fehler +
  Manuals zuerst gelesen)

### 5. Manuals-first korreliert mit Korrektheit nur beim 27B

Bei 4B und 9B ist der Unterschied zwischen manuals-first=True und =False praktisch null
(~30–33% in beiden Gruppen). Diese Modelle brauchen die Manuals nicht, weil der
Validator-Korrektiv-Loop als Ersatz funktioniert. Beim 27B gibt es einen messbaren
Unterschied: 73% der korrekten Runs lasen Manuals zuerst, bei falschen Runs waren es
nur 62%.

---

## Dauer (Median Sekunden pro Suite)

Fairster Modellvergleich: **Median (alle Runs)** — gleiche Suite = gleiche Fragen, Schwierigkeits-Confound damit kontrolliert. Correct-only-Median ist konfundiert: kleine Modelle lösen nur einfache (schnelle) Fragen, große Modelle lösen auch schwere (langsamere). Falsche Runs dauern überproportional lang, weil Modelle das Rekursionslimit erschöpfen statt schnell aufzugeben.

| Modell | bench_b all | bench_b correct | bench_b wrong | containment all | srn_bypass all |
|--------|------------:|----------------:|--------------:|----------------:|---------------:|
| 0.8B | 22.7s | – | 22.7s | 14.4s | 11.6s |
| 2B | 22.3s | – | 22.3s | 21.7s | 20.2s |
| 4B | 60.5s | 16.6s | 96.7s | 11.3s | 8.0s |
| 9B | 23.1s | 18.4s | 92.4s | 14.5s | 11.9s |
| 27B | 30.1s | 24.5s | 58.0s | 20.7s | 11.4s |

**Befunde:**

- **4B ist der langsamste Runner** bei bench_b (all=60.5s): Er probiert lang und scheitert oft an der Rekursionsgrenze (wrong=96.7s), die seltenen korrekten Runs sind dagegen kurz (16.6s).
- **Falsche Runs sind systematisch länger als korrekte** (außer beim 0.8B, das immer scheitert und damit keinen Unterschied zeigt). Das Muster ist konsistent: Modelle geben nicht schnell auf — sie scheitern durch Erschöpfung.
- **27B correct > 9B correct bei bench_b** (24.5s vs. 18.4s): Der 27B löst schwerere Fragen, die naturgemäß mehr Reasoning-Schritte brauchen — das ist der Confound den Correct-only-Vergleich unbrauchbar macht.
- **containment_hall4 und srn_bypass zeigen kaum Laufzeit-Unterschiede** zwischen den Modellen die überhaupt lösen können (4B/9B/27B: 8–21s) — diese Suites sind weniger rekursionsintensiv.

---

## Paper-Implikationen (Existence Claims, keine Frequenz-Extrapolation)

1. **Capability threshold:** Unterhalb von 4B ist MCP-basiertes AAS-Agenten-Retrieval
   nicht operational — unabhängig vom Backend und Validator.

2. **Validator as scaffolding:** Für 4–9B-Modelle wirkt der Validator-Gate wie externe
   Fehlerkorrektur; die hohe Anti-Pattern-Rate bei gleichzeitig akzeptabler Korrektheit
   zeigt, dass das Modell den Validator als impliziten Hinweismechanismus nutzt.

3. **Qualitative shift at 27B:** Erst ab 27B tritt das gewünschte Verhalten emergent auf:
   proaktive Dokumentationskonsultation + regelkonformes Querying + korrekte Antwort
   gleichzeitig (All-good 35%).
