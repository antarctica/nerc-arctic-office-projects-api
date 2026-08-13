from pathlib import Path
import tomllib

_pyproject = Path(__file__).resolve().parents[1] / "pyproject.toml"

with _pyproject.open("rb") as f:
    _config = tomllib.load(f)

__version__ = _config["tool"]["poetry"]["version"]
