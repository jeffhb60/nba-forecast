# NBA Forecasting

A Python platform for forecasting NBA games. The platform is a
modular monolith with a Medallion data architecture and two independent forecasting
objectives. No license is granted by this repository until its owner selects one.

**Status:** 0.1.0 — foundation only. No API requests, data ingestion, database schemas,
feature pipelines, trained models, predictions, or monitoring are implemented yet.

## Objectives

- **Classification:** calibrated probability that the home team wins a completed game.
- **Regression:** signed final margin (home points minus away points), with prediction
  intervals. Positive values favor the home team; negative values favor the away team.

## Architecture

```text
NBA API (planned)
    -> Bronze: immutable raw JSON
    -> Silver: validated relational DuckDB
    -> Gold: point-in-time features, versioned Parquet
    -> ML: independent classification and regression workflows
```

See [Architecture](docs/ARCHITECTURE.md), [Roadmap](docs/ROADMAP.md), and
[Changelog](CHANGELOG.md)

## Requirements and setup

Python 3.11 or newer; Python 3.12 is recommended for development. Git is recommended.
Run the commands from the repository root. The package uses a `src/` layout; install
it in editable mode rather than modifying `PYTHONPATH`.

### Windows / PowerShell

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -e ".[dev]"
.\.venv\Scripts\python.exe -m pytest
.\.venv\Scripts\python.exe -m ruff check .
.\.venv\Scripts\python.exe -m ruff format --check .
```

Activation is optional: using the interpreter directly avoids PowerShell execution
policy issues. If desired, activate with `.\.venv\Scripts\Activate.ps1`.
In PyCharm, open the repository root, select `.venv\Scripts\python.exe` as the
project interpreter, and set the working directory to the repository root. Use pytest
as the test runner.

### Linux

```bash
python3.12 -m venv .venv
.venv/bin/python -m pip install --upgrade pip
.venv/bin/python -m pip install -e '.[dev]'
.venv/bin/python -m pytest
.venv/bin/python -m ruff check .
.venv/bin/python -m ruff format --check .
```

Use `python3.11` instead if appropriate. With the environment activated, the above
commands can use `python -m ...` directly.

## Configuration

Settings are read explicitly via `Settings.from_env()` in future entry points.
Paths are relative to the process working directory unless absolute; `~` is expanded
for environment-provided paths. Settings do not create files or directories.

| Environment variable | Default | Purpose |
| --- | --- | --- |
| `NBA_FORECAST_DATA_DIR` | `data` | Parent of Bronze, Silver, and Gold |
| `NBA_FORECAST_ARTIFACT_DIR` | `artifacts` | Future model/evaluation output |
| `NBA_FORECAST_LOG_LEVEL` | `INFO` | DEBUG, INFO, WARNING, ERROR, CRITICAL |

For example, in PowerShell:

```powershell
$env:NBA_FORECAST_DATA_DIR = 'D:\nba-data'
$env:NBA_FORECAST_LOG_LEVEL = 'DEBUG'
```

On Linux: `export NBA_FORECAST_DATA_DIR=/path/to/nba-data`.
No dotenv loader is installed; configure variables in the shell or IDE.
The application will use standard Python logging; explicit setup sends logs to
stderr and does not override existing root handlers. Modules use named loggers.
Do not log credentials or sensitive environment values.

## Development workflow

`pyproject.toml` is the sole dependency declaration. Runtime dependencies are empty
for now. Dev extras install pytest and Ruff with bounded compatible ranges.
These ranges are not an exact lock; when data and ML dependencies arrive, introduce
a reproducible lock strategy before publishing trained models. Do not treat an
unlocked install as bit-for-bit reproducible.

Use `python -m ruff check . --fix` for safe lint fixes and `python -m ruff format .`
for formatting; review changes. Run tests and both Ruff checks before handing off.
CI is configured to run these checks on Windows and Linux with Python 3.11/3.12.

Use semantic versioning and Conventional Commits (e.g. `feat(bronze): archive raw responses`).
Do not commit or push without authorization. Data, generated artifacts, credentials,
and local IDE settings must stay outside version control. Do not add a license without
repository-owner approval.

## Foundation verification

The initial editable installation succeeded on Linux with Python 3.12 using
preinstalled setuptools and no dependency downloads. All 13 tests passed with
pytest 9.0.2. Ruff could not be installed from the available package source, so
lint and format checks remain unverified. The Windows/Linux GitHub Actions
workflow is configured but has not been run.