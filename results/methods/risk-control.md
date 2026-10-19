# Risk status checks on a larger synthetic feed

- Sources: original `484a0a0` and status-check candidate `f6e741f`.
- Compiler: Apple Clang 21.0.0.
- Flags: `-std=c++20 -O2 -g -Wall -Wextra -Wpedantic`.
- Scenario: `durability_256.scn`, a synthetic 256-cycle feed. The compact
  result note does not retain a scenario hash, so this comparison needs a
  provenance refresh before any public release that requires hash-level
  reproducibility.
- Procedure: 5 process warm-ups and 30 randomized pairs.
- Samples: 514 market-data sends and 1,284 total sends per run.
- Behavior check: order streams and decision logs matched.
- Result: the median of per-run delivery-to-Send medians was 291 ns in both
  variants. Only 1 of 30 pairs favored status checks. Within-run p95 medians
  were 375 ns in both variants.

This test does not show a delivery-to-Send latency improvement. It does not
settle whether expected risk states should use exceptions as a design choice.
