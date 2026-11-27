from dataclasses import FrozenInstanceError
from pathlib import Path

import pytest

from nba_forecasting.config import Settings


def test_defaults() -> None:
    settings = Settings.from_env()
    assert settings.data_dir == Path("data")
    assert settings.artifact_dir == Path("artifacts")
    assert settings.log_level == "INFO"
    assert settings.bronze_dir == Path("data/bronze")
    assert settings.silver_db == Path("data/silver/nba.duckdb")
    assert settings.gold_dir == Path("data/gold")


def test_environment_overrides(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    data = tmp_path / "custom data"
    artifacts = tmp_path / "models"
    monkeypatch.setenv("NBA_FORECAST_DATA_DIR", str(data))
    monkeypatch.setenv("NBA_FORECAST_ARTIFACT_DIR", str(artifacts))
    monkeypatch.setenv("NBA_FORECAST_LOG_LEVEL", " debug ")
    settings = Settings.from_env()
    assert settings.bronze_dir == data / "bronze"
    assert settings.silver_db == data / "silver" / "nba.duckdb"
    assert settings.gold_dir == data / "gold"
    assert settings.artifact_dir == artifacts
    assert settings.log_level == "DEBUG"
    assert not data.exists()
    assert not artifacts.exists()


@pytest.mark.parametrize("value", ["VERBOSE", "", "10"])
def test_invalid_log_level(monkeypatch: pytest.MonkeyPatch, value: str) -> None:
    monkeypatch.setenv("NBA_FORECAST_LOG_LEVEL", value)
    with pytest.raises(ValueError, match="Unsupported log level"):
        Settings.from_env()


@pytest.mark.parametrize("key", ["NBA_FORECAST_DATA_DIR", "NBA_FORECAST_ARTIFACT_DIR"])
def test_empty_paths(monkeypatch: pytest.MonkeyPatch, key: str) -> None:
    monkeypatch.setenv(key, "  ")
    with pytest.raises(ValueError, match=key):
        Settings.from_env()


def test_settings_are_immutable() -> None:
    settings = Settings()
    with pytest.raises(FrozenInstanceError):
        settings.log_level = "DEBUG"


def test_configuration_does_not_create_default_paths(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    monkeypatch.chdir(tmp_path)
    Settings.from_env()
    assert list(tmp_path.iterdir()) == []
