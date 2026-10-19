# Write-ahead log sync comparison

- Compiler: Apple Clang 21.0.0.
- Flags: `-std=c++20 -O2 -g -Wall -Wextra -Wpedantic`.
- Scenario: synthetic 256-cycle feed, SHA-256
  `015528f09b46ef26f42e962001410f88e45932327605a68ce79cc0847b874e6e`.
- Procedure: 5 process warm-ups per mode and 30 randomized triplets.
- Samples: 514 market-data sends and 1,284 total sends per run. All measured
  runs had matching order and decision-log hashes.
- Modes: no durable WAL, one sync per order, and group commit at each
  `Requote` callback.

The median delivery-to-Send values were 0.125 us with no durable WAL,
34.1875 us with a sync for every order, and 18.9375 us with group commit. The
paired per-order-minus-group improvement was 15.35425 us, with bootstrap 95%
interval 15.13575 to 15.698 us. Group commit is faster than a sync per order
in this test, but it still costs more than the non-durable mode.
