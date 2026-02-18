"""
NLTK POS Tagger.

Lee tokens desde Parquet (processed) y genera POS tags con NLTK.
Guarda resultado en data/results.
"""

from __future__ import annotations
from pathlib import Path

import pandas as pd
import nltk

from src.utils.config import PROCESSED_DATA_PATH, RESULTS_DATA_PATH


INPUT_FILE = PROCESSED_DATA_PATH / "songs_with_lyrics_tokenized.parquet"
OUTPUT_FILE = RESULTS_DATA_PATH / "pos_nltk.parquet"


def tag_tokens(tokens):
    """
    Recibe tokens (list/np.array/arrow list) y devuelve lista de tuplas (token, tag)
    o None si no hay tokens.
    """
    if tokens is None:
        return None

    # NaN (por si acaso)
    if isinstance(tokens, float) and pd.isna(tokens):
        return None

    # Lista vacía / array vacío / etc.
    if hasattr(tokens, "__len__") and len(tokens) == 0:
        return None

    # Convertir explícitamente a lista
    tokens = list(tokens)

    return nltk.pos_tag(tokens)


def run(input_path: Path = INPUT_FILE, output_path: Path = OUTPUT_FILE) -> pd.DataFrame:
    """
    Lee el parquet tokenizado, aplica POS tagging con NLTK y guarda un parquet en results.
    """
    # Si no los tienes descargados, descomenta (solo una vez):
    # nltk.download("punkt")
    # nltk.download("averaged_perceptron_tagger")

    df = pd.read_parquet(input_path)

    required = {"year", "rank", "artist", "song", "lyrics"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing columns: {sorted(missing)}")

    out = df.copy()
    out["pos_nltk"] = out["lyrics"].apply(tag_tokens)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    out.to_parquet(output_path, index=False)

    print(f"Saved NLTK POS to: {output_path}")
    print(f"Rows with POS: {out['pos_nltk'].notna().sum()} / {len(out)}")

    return out


if __name__ == "__main__":
    run()
