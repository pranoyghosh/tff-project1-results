# Cached top of book compared with a full scan

- Source: original revision `484a0a0`; scan alternative changes only top-of-book
  maintenance and reading.
- Compiler: Apple Clang 21.0.0.
- Flags: `-std=c++20 -O2 -g -Wall -Wextra -Wpedantic`.
- Scenario: `sweep.scn`, SHA-256
  `3f15e996714bdbef465d7f252ef059e7fc2229b3109471cdb1b6ba29d20be310`.
- Procedure: 10 process warm-ups per variant, then 30 randomized paired runs.
- Behavior check: same order stream and decision log; both variants passed
  tests and fixture verification.
- Samples: each process had 10 market-data sends.
- Result: 448 ns cached versus 50,208.25 ns full scan for the median of
  per-run delivery-to-Send medians. Paired improvement was 49,729.5 ns, with
  bootstrap 95% interval 49,625 to 50,354 ns.

This supports the cached top against this full scan on this sparse ladder and
scenario. It does not compare every possible book structure. The small send
count does not support a general p95 claim.
