# Tech for Finance: Assignment 1 performance results

This repository is a copy of selected performance graphs and
aggregate results.

## Results

- [Corrected delivery-to-Send measurement window](figures/metric-window.svg)
- [Old callback metric](figures/old-metric-fourway.svg)
- [Corrected delivery-to-Send metric](figures/delivery-to-send-fourway.svg)
- [Position fixture: corrected metric](figures/position-delivery-to-send.svg)
- [Cached top-of-book comparison](figures/top-of-book.svg)
- [Risk control on the larger feed](figures/risk-control-large.svg)
- [Decision-log formatting](figures/log-formatting.svg)
- [WAL sync comparison](figures/group-commit.svg)
- [Execution-report delivery-to-Send samples](results/summaries/execution-report-summary.csv)

The charts use the compact values in [`results/summaries/chart-data.csv`](results/summaries/chart-data.csv).
Run `python3 scripts/render_charts.py` to rebuild them. The script uses only
the Python standard library.

## Main findings and limits

- The cached top of book was faster than a full ladder scan in this test.
- Faster decision-log formatting lowered delivery-to-Send time in the small
  test. That test had only ten market-data sends per run.
- On the position fixture, all three candidate variants had a lower median
  delivery-to-Send time than baseline. See the [position scenario method note](results/methods/position-scenario.md).
- Group commit reduced the latency cost of synchronized WAL writes compared
  with a sync for each order. This was an operating-system sync test. It did
  not test physical power-loss durability.

These results apply to the listed source versions, compiler, machine, and
scenarios. They do not show live-market or network latency. Read the method
notes before using a chart as evidence.

## Execution-report delivery-to-Send samples

The corrected analyzer also measured sends caused by execution reports. In
`sweep.scn`, each run had 13 report deliveries. Twelve caused no send. One
caused a send. The files below include all 30 run-level samples for each
source and compiler, plus a summary with quartiles and the median.

| Environment | Original median | Status-check median |
|---|---:|---:|
| macOS Apple Clang 17 | 854 ns | 666.5 ns |
| Docker GCC 12 | 416 ns | 417 ns |
| Docker Clang 21 | 375 ns | 416 ns |

These early runs were not a dedicated randomized paired test for the
execution-report path. Treat these medians as descriptive. They do not support
a general claim that status checks improve execution-report delivery-to-Send
latency. The per-run values are in
[`execution-report-per-run.csv`](results/summaries/execution-report-per-run.csv);
the grouped values are in
[`execution-report-summary.csv`](results/summaries/execution-report-summary.csv).

These are reproducible, workload-specific simulator measurements, not
live-market or end-to-end network benchmarks. The supplied fixtures provide
behavior coverage; `sweep.scn` is the detailed reference comparison,
`position.scn` is a higher-send supporting workload, and `durability_256.scn`
is a synthetic durability/risk workload.

## Four-way experiment across the supplied fixtures

Each fixture comparison used four variants: original, risk-only, logging-only,
and both changes. Each fixture had 10 warm-up runs per variant, followed by 30
randomized quadruples. Each quadruple had one measured run for each variant,
for 120 measured runs per fixture. The main result below is corrected
market-data delivery-to-Send median latency compared with the original.

- **Risk-only:** replace expected-risk exception control flow with status checks.
- **Logging-only:** use the faster decision-log formatting change.
- **Combined:** apply both changes.
- **Original:** use the unmodified baseline.

| Fixture | Market-data sends per run | Result versus original |
|---|---:|---|
| `basic` | 14 | Logging-only and combined improved corrected median latency |
| `empty_side` | 6 | Logging-only improved corrected median latency |
| `gap` | 4 | Risk-only and combined improved; logging-only was uncertain |
| `loss` | 21 | Risk-only, logging-only, and combined improved corrected median latency |
| `position` | 30 | All candidates improved; combined was best |
| `quiet` | 2 | Too few sends for a strong latency conclusion |
| `sweep` | 11 | Logging-only and combined improved; risk-only was uncertain |

Here, “improved” describes the corrected median result. It does not mean that
every latency statistic improved. The small fixtures, especially `quiet`, have
few sends per run and give weak evidence about tail latency. The [position fixture graph](figures/position-delivery-to-send.svg)
shows its four variant medians. See the [four-way method note](results/methods/hill-climb.md)
for the `sweep` setup and limits.

## Layout

```text
figures/                 SVG charts
results/summaries/       Small aggregate CSV files
results/methods/         Measurement method and limits for each comparison
scripts/                 Script to rebuild the charts
provenance/              Artifact source list
```
