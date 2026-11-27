"""Explicit, environment-based configuration with no import-time side effects."""

import os
from dataclasses import dataclass
from pathlib import Path

_LOG_LEVELS = frozenset({"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"})


@dataclass(frozen=True, slots=True)
class Settings:
    """Local runtime settings; relative paths are resolved against the working directory."""

    data_dir: Path = Path("data")
    artifact_dir: Path = Path("artifacts")
    log_level: str = "INFO"

    def __post_init__(self) -> None:
        if self.log_level not in _LOG_LEVELS:
            raise ValueError(f"Unsupported log level: {self.log_level!r}")

    @classmethod
    def from_env(cls) -> "Settings":
        """Read settings at the application boundary, not on module import."""
        return cls(
            data_dir=_path_from_env("NBA_FORECAST_DATA_DIR", "data"),
            artifact_dir=_path_from_env("NBA_FORECAST_ARTIFACT_DIR", "artifacts"),
            log_level=os.environ.get("NBA_FORECAST_LOG_LEVEL", "INFO").strip().upper(),
        )

    @property
    def bronze_dir(self) -> Path:
        return self.data_dir / "bronze"

    @property
    def silver_db(self) -> Path:
        return self.data_dir / "silver" / "nba.duckdb"

    @property
    def gold_dir(self) -> Path:
        return self.data_dir / "gold"


def _path_from_env(name: str, default: str) -> Path:
    value = os.environ.get(name, default)
    if not value.strip():
        raise ValueError(f"{name} must not be empty")
    return Path(value).expanduser()
