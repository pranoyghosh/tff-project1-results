# Measurement method

The corrected measure starts when the simulator delivers a market-data or
execution-report message to the application. It ends at the application's
call to `OrderEntrySession::Send`.

```text
delivery -> application work -> Send -> exchange event
    |                         |
    +--- measured interval ---+
```

This measures application response time before the simulated exchange event.
It excludes network travel and exchange processing. Each Send is linked to the
delivery that caused it. Market-data and execution-report sends are separate
groups. Deliveries with no Send are counted, but they have no delivery-to-Send
sample.

For each process run, the main corrected statistic is the median of its
market-data delivery-to-Send samples. Paired comparisons subtract the two
variants' per-run statistics. The reported 95% interval is a bootstrap interval
for the median paired difference. It describes uncertainty in the comparison.
It is not the p95 latency. P95 describes the slow end of the measured latency
samples.

The old statistic is the reported average callback latency. It includes
callbacks that send no order and work after Send. It remains in the comparisons
to show what the original evaluation measures.
