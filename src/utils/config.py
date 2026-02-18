"""Configuraciones del proyecto."""

from pathlib import Path

# config.py está en src/utils
# parents[2] sube: utils → src → euterpe (root)
BASE_PATH = Path(__file__).resolve().parents[2]

RAW_DATA_PATH = BASE_PATH / "data" / "raw"
RAW_DATA_PATH.mkdir(parents=True, exist_ok=True)
PROCESSED_DATA_PATH = BASE_PATH / "data" / "processed"
PROCESSED_DATA_PATH.mkdir(parents=True, exist_ok=True)

RESULTS_DATA_PATH= BASE_PATH / "data" / "results"
RESULTS_DATA_PATH.mkdir(parents=True, exist_ok=True)