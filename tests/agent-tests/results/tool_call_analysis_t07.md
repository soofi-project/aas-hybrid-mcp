# Tool-Call Analysis — Cross-Model Comparison

Records: 1800 | Grouped by: model

## Summary

| Model | N | Pass% | AP-hit% | Self-corr% | Schema-1st | Manual-1st | All-3-1st | Manual>AP | NoMan>AP | Avg TC |
|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| qwen35-122b | 200 | 68% | 74% | 97% | 16% | 16% | 2% | 10% | 72% | 13.1 |
| qwen35-27b | 200 | 71% | 63% | 98% | 1% | 15% | 1% | 12% | 86% | 12.7 |
| qwen35-2b | 200 | 38% | 13% | 96% | 2% | 4% | 0% | 12% | 38% | 40.9 |
| qwen35-35b | 200 | 64% | 62% | 98% | 42% | 3% | 0% | 5% | 89% | 18.1 |
| qwen35-397b | 200 | 70% | 62% | 95% | 12% | 44% | 4% | 50% | 41% | 11.8 |
| qwen35-4b | 200 | 50% | 76% | 97% | 25% | 2% | 1% | 1% | 56% | 19.8 |
| qwen35-9b | 200 | 50% | 76% | 95% | 19% | 4% | 0% | 3% | 49% | 20.3 |
| qwen36-27b | 200 | 64% | 48% | 97% | 24% | 49% | 21% | 32% | 54% | 15.4 |
| qwen36-35b | 200 | 64% | 39% | 97% | 8% | 39% | 5% | 22% | 51% | 17.0 |

## Failure Mode Breakdown

| Model | Pass | Viol+Pass | Viol+Fail | Clean Fail | No Tools |
|---|--:|--:|--:|--:|--:|
| qwen35-122b | 68% | 46% | 28% | 4% | 0% |
| qwen35-27b | 71% | 38% | 25% | 4% | 0% |
| qwen35-2b | 38% | 4% | 10% | 52% | 1% |
| qwen35-35b | 64% | 36% | 26% | 11% | 0% |
| qwen35-397b | 70% | 40% | 22% | 8% | 0% |
| qwen35-4b | 50% | 40% | 36% | 14% | 0% |
| qwen35-9b | 50% | 36% | 40% | 10% | 0% |
| qwen36-27b | 64% | 26% | 22% | 14% | 0% |
| qwen36-35b | 64% | 22% | 17% | 20% | 0% |

## Manual vs. Anti-Pattern Compliance

Manual>AP = read manual *before* first violation, still violated.
NoMan>AP = never read manual, committed violation.
Manual>OK = read manual at some point, no violations.

| Model | N | Manual>AP | NoMan>AP | Manual>OK |
|---|--:|--:|--:|--:|
| qwen35-122b | 200 | 15 | 107 | 16 |
| qwen35-27b | 200 | 15 | 108 | 15 |
| qwen35-2b | 200 | 3 | 10 | 39 |
| qwen35-35b | 200 | 6 | 110 | 8 |
| qwen35-397b | 200 | 63 | 51 | 26 |
| qwen35-4b | 200 | 2 | 84 | 5 |
| qwen35-9b | 200 | 5 | 74 | 3 |
| qwen36-27b | 200 | 30 | 51 | 76 |
| qwen36-35b | 200 | 17 | 40 | 69 |
