"""Public API for JAM Asset Manager."""

from .core import BaseConfig, JamConfig

__all__ = ["BaseConfig", "JamConfig", "run"]
__version__ = "0.1.0"


def run(config=None):
    """Launch JAM inside Maya with an optional injected configuration."""
    from .application import run as launch

    return launch(config=config)
