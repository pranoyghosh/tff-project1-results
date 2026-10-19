# Four-way source comparison

- Sources: original `484a0a0`, risk-only `f6e741f`, logging-only formatter
  overlay based on `484a0a0`, and combined `b08c4d6`.
- Compiler: Apple Clang 21.0.0.
- Flags: `-std=c++20 -O2 -g -Wall -Wextra -Wpedantic`.
- Scenario: `sweep.scn`, SHA-256
  `3f15e996714bdbef465d7f252ef059e7fc2229b3109471cdb1b6ba29d20be310`.
- Procedure: 10 process warm-ups per variant and 30 randomized quadruples.
  All 120 measured runs had matching order and decision-log hashes.
- Samples: 10 market-data sends per process.

## What the logging-only solution changes

The original `DecisionLog::Record` formats each decision with `fprintf`.
The logging-only candidate keeps the same record fields and output bytes, but
formats normal records with `std::to_chars` into a fixed-size stack buffer and
writes the completed record with one `fwrite` call. Long or otherwise
unsupported action text keeps the existing fallback path.

The call order remains:

```text
history record -> decision-log Record -> OrderEntrySession::Send
```

This removes the repeated formatted-I/O work from the successful send path
without moving the record after `Send`. Fixture outputs and measured decision
logs were compared byte for byte, and the formatter edge-case test covered
zero, negative, and extreme prices, integer limits, and the fallback path.

The old graph shows the median across run-level all-callback means. The
corrected graph shows the median across each run's market-data
delivery-to-Send medians. The logging-only corrected-metric improvement was
229 ns, with bootstrap 95% interval 228.75 to 250.25 ns. All 30 pairs favored
the formatter.

The formatter comparison changes number formatting and output-call pattern
together. It does not isolate which part caused the measured gain. Buffered
file output does not prove durable storage before Send.

The same four variants were also run on the supplied position fixture. See
[`position-scenario.md`](position-scenario.md) for that result. Its lower
candidate medians are specific to that fixture and metric.
