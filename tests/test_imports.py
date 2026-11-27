import subprocess
import sys
from pathlib import Path


def test_package_boundaries_have_no_import_side_effects(tmp_path: Path) -> None:
    result = subprocess.run(
        [
            sys.executable,
            "-c",
            "import logging; before = list(logging.getLogger().handlers); "
            "import nba_forecasting.bronze, nba_forecasting.silver, "
            "nba_forecasting.gold, nba_forecasting.ml, nba_forecasting.config, "
            "nba_forecasting.logging_config; "
            "assert list(logging.getLogger().handlers) == before",
        ],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        check=True,
    )
    assert result.stdout == ""
    assert result.stderr == ""
    assert list(tmp_path.iterdir()) == []