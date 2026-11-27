"""Isolate configuration tests from a developer's local environment."""

import pytest


@pytest.fixture(autouse=True)
def clean_forecast_environment(monkeypatch: pytest.MonkeyPatch) -> None:
    for key in ("NBA_FORECAST_DATA_DIR", "NBA_FORECAST_ARTIFACT_DIR", "NBA_FORECAST_LOG_LEVEL"):
        monkeypatch.delenv(key, raising=False)