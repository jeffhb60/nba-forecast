"""Logging setup called explicitly by application entry points."""

import logging

from .config import Settings


def configure_logging(settings: Settings) -> None:
    """Configure stderr logging once, without replacing existing root handlers."""
    logging.basicConfig(
        level=settings.log_level,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )
