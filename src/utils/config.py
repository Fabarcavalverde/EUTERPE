"""Configuraciones del proyecto."""

from pathlib import Path

BASE_PATH = Path(__file__).resolve().parents[2]

RAW_DATA_PATH = BASE_PATH / "data" / "raw"
RAW_DATA_PATH.mkdir(parents=True, exist_ok=True)

PROCESSED_DATA_PATH = BASE_PATH / "data" / "processed"
PROCESSED_DATA_PATH.mkdir(parents=True, exist_ok=True)

RESULTS_DATA_PATH = BASE_PATH / "data" / "results"
RESULTS_DATA_PATH.mkdir(parents=True, exist_ok=True)

#archivos

LYRICS_CLEAN_PARQUET = PROCESSED_DATA_PATH / "songs_with_lyrics_ready.parquet"

POS_COMPARISON_BY_YEAR_CSV = RESULTS_DATA_PATH /"comparacion"/ "pos_comparison_by_year.csv"

POS_SPEED_COMPARISON_CSV = RESULTS_DATA_PATH /"comparacion"/ "pos_speed_comparison.csv"
