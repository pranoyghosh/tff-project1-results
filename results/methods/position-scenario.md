# Four-way comparison on the position fixture

This is the supplied `position.scn` fixture. Its SHA-256 is
`a889f5f5500b298c3bccd3a5f25f5a009c0311d7c6354e9cc5eaefff8c2728ca`.

- Sources: original `484a0a0`, risk-only `f6e741f`, logging-only formatter
  overlay based on `484a0a0`, and combined `b08c4d6`.
- Compiler: Apple Clang 21.0.0.
- Flags: `-std=c++20 -O2 -g -Wall -Wextra -Wpedantic`.
- Procedure: 10 randomized process warm-ups per variant and 30 randomized
  measured quadruples.
- Samples: 30 market-data sends per process.
- Behavior check: the factorial experiment required matching order and
  decision-log hashes for each measured comparison. All seven supplied
  fixtures passed verification for all four variants.

The graph shows the median of each run's market-data delivery-to-Send medians:

| Variant | Median latency |
|---|---:|
| Original | 395.5 ns |
| Risk only | 375.0 ns |
| Logging only | 167.0 ns |
| Combined | 145.5 ns |

All three candidate medians were lower than baseline. The paired median
improvements and bootstrap 95% intervals were:

| Comparison | Improvement | 95% interval | Pairs favoring candidate |
|---|---:|---:|---:|
| Baseline to risk only | 41.0 ns | 20.5 to 41.75 ns | 23 of 30 |
| Baseline to logging only | 228.5 ns | 208.5 to 229.5 ns | 30 of 30 |
| Baseline to combined | 249.75 ns | 229.5 to 250.5 ns | 30 of 30 |

This supports lower median delivery-to-Send time for these variants on this
fixture. It does not mean that every latency statistic improved. For example,
the p95 comparison for risk-only includes zero, and the combined p95 did not
show a clear change from baseline. Do not generalize this fixture result to
other workloads.
