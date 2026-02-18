"""
Lyrics Tokenizer (Parquet Version).

Este módulo forma parte del pipeline de preprocesamiento NLP.

Lee el dataset limpio de lyrics desde PROCESSED_DATA_PATH,
tokeniza el texto y sobrescribe la columna `lyrics`
con una lista real de tokens.

El resultado se guarda en formato Parquet para permitir
almacenamiento eficiente de listas y compatibilidad
con etapas posteriores.

Pipeline stage:
    RAW → CLEAN → TOKENIZED

Input:
    processed/songs_with_lyrics_clean.csv

Output:
    processed/songs_with_lyrics_tokenized.parquet

Requiere:
    pip install pyarrow
"""

from __future__ import annotations

import re
import pandas as pd
from src.utils.config import PROCESSED_DATA_PATH


INPUT_FILE = PROCESSED_DATA_PATH / "songs_with_lyrics_clean.csv"
OUTPUT_FILE = PROCESSED_DATA_PATH / "songs_with_lyrics_tokenized.parquet"

# Regex de tokenización:
# - Letras (incluye acentos)
# - Números
# - Underscore (por robustez)
_TOKEN_RE = re.compile(r"[A-Za-zÀ-ÿ0-9_]+")


def tokenize(text: str) -> list[str] | None:
    """
    Convierte un string en lista de tokens.

    Parameters
    ----------
    text : str

    Returns
    -------
    list[str] | None
    """

    if pd.isna(text):
        return None

    s = str(text).strip()
    if not s:
        return None

    # Lowercase recomendado para NLP tradicional
    s = s.lower()

    tokens = _TOKEN_RE.findall(s)

    return tokens if tokens else None


def run(
    input_path=INPUT_FILE,
    output_path=OUTPUT_FILE
) -> pd.DataFrame:
    """
    Ejecuta el proceso de tokenización.

    Parameters
    ----------
    input_path : Path
        Ruta del CSV limpio.
    output_path : Path
        Ruta de salida en formato Parquet.

    Returns
    -------
    pd.DataFrame
        DataFrame tokenizado.
    """

    df = pd.read_csv(input_path, encoding="utf-8")

    required = {"year", "rank", "artist", "song", "lyrics"}
    missing = required - set(df.columns)

    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    df["lyrics"] = df["lyrics"].apply(tokenize)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(output_path, index=False)

    print(f"Tokenized dataset saved to: {output_path}")
    print(f"Rows with tokens: {df['lyrics'].notna().sum()}")

    return df


if __name__ == "__main__":
    run()
