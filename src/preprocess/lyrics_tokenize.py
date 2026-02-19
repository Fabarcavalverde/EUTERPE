"""
Lyrics Tokenizer (in-memory).

Recibe un DataFrame con lyrics (texto) y sobrescribe la columna `lyrics`
con lista de tokens.

Opcional:
- Guarda un parquet tokenizado si se provee `output_path`.
"""

from __future__ import annotations
from pathlib import Path
import re
import pandas as pd

from src.utils.config import PROCESSED_DATA_PATH


OUTPUT_DEFAULT = PROCESSED_DATA_PATH / "songs_with_lyrics_tokenized.parquet"

_TOKEN_RE = re.compile(r"[A-Za-zÀ-ÿ0-9_]+")


def tokenize(text: str) -> list[str] | None:
    if pd.isna(text):
        return None

    s = str(text).strip()
    if not s:
        return None

    s = s.lower()
    tokens = _TOKEN_RE.findall(s)
    return tokens if tokens else None


def run(df: pd.DataFrame, output_path: Path | None = OUTPUT_DEFAULT) -> pd.DataFrame:
    if not isinstance(df, pd.DataFrame):
        raise TypeError("run() expects a pandas DataFrame")

    if "lyrics" not in df.columns:
        raise ValueError("Column 'lyrics' not found")

    out = df.copy()
    out["lyrics"] = out["lyrics"].apply(tokenize)

    if output_path is not None:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        out.to_parquet(output_path, index=False)
        print(f"DataSet tokenizado y guardado en: {output_path}")

    return out
