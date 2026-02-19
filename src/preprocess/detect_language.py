"""
Language Detection (offline using langdetect).

Recibe DataFrame limpio y devuelve DataFrame
con columna `language` agregada.
"""

from __future__ import annotations

import pandas as pd
from langdetect import detect, DetectorFactory

# Hace el resultado determinístico
DetectorFactory.seed = 42


def detect_language(text: str) -> str | None:
    if pd.isna(text):
        return None

    text = str(text).strip()


    if len(text) < 50:
        return None

    try:
        return detect(text)
    except:
        return None


def run(df: pd.DataFrame) -> pd.DataFrame:
    """
    Agrega columna `language` al DataFrame.

    Parameters
    ----------
    df : pd.DataFrame
        Debe contener columna `lyrics`.

    Returns
    -------
    pd.DataFrame
    """

    if "lyrics" not in df.columns:
        raise ValueError("Column 'lyrics' not found")

    out = df.copy()
    out["language"] = out["lyrics"].apply(detect_language)

    return out
