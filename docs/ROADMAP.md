# Roadmap

Work in small, reviewable phases. Each phase must include tests, documentation and
an explicit handoff with executed checks and outstanding issues. Future phases are
proposals; none is implemented by the initial foundation.

| Phase | Deliverable | Exit criteria |
| --- | --- | --- |
| 0 | Repository foundation (0.1.0) | Installable package, config/logging tests, docs, lint and CI configuration; report validation limits |
| 1 | Bronze ingestion | Source contracts, archived JSON with metadata, fixture-based tests, retry/idempotency behavior, reproducible backfill |
| 2 | Silver validation | DuckDB schema, key and status rules, deterministic transforms, replay and invalid-data tests |
| 3 | Gold datasets | Pregame cutoff policy, feature/label contracts, versioned Parquet manifests, temporal leakage tests |
| 4 | Evaluation harness | Chronological splits, rolling backtests, separate tuning/calibration/test windows, baseline metrics |
| 5 | Classification | Independent classifier and calibration; held-out probability evaluation and versioned artifacts |
| 6 | Regression | Independent signed-margin model and prediction intervals; held-out error/coverage evaluation and versioned artifacts |
| 7 | Prediction | Reproducible pregame inference, feature parity, versioned outputs, tests against training contracts |
| 8 | Monitoring | Outcome joins, data quality and drift metrics, calibration and interval coverage tracking, documented alert policy |

## Next task: Bronze design and ingestion

Before writing ingestion code, inspect the repository and confirm NBA data source,
season scope (regular season, playoffs or both), historical coverage, source usage
constraints, and treatment of postponed or canceled games. Define the response
archive and metadata contracts, then implement the smallest end-to-end fixture-based
slice. Add `nba_api` or another client only when the chosen source requires it.
No live requests are necessary for unit tests. Keep raw data out of Git.

## Later considerations

Add DuckDB when Silver work begins, and Parquet tooling when Gold begins. Choose
model libraries and exact dependency locking as evaluation and modeling requirements
become concrete. Define deployment, UI and automation only after prediction contracts
are stable. Do not promise dates or accuracy targets before measuring the baseline.
