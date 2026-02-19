import pandas as pd
from functools import lru_cache
from pathlib import Path
import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parents[1]
PARQUET_PATH = PROJECT_ROOT / "data" / "results" / "pos_spacy.parquet"

@lru_cache(maxsize=1)
def load_df():
    df = pd.read_parquet(PARQUET_PATH, columns=["year", "language", "pos_spacy"])
    df = df.dropna(subset=["year", "pos_spacy"])
    df["year"] = df["year"].astype(int)
    return df

def add_decade(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["decade"] = (df["year"] // 10) * 10
    return df

def explode_tokens(df: pd.DataFrame) -> pd.DataFrame:
    """
    Convierte pos_spacy (np.ndarray de np.ndarray) a tabla token-level.
    """
    out = []

    for year, language, seq in df[["year", "language", "pos_spacy"]].itertuples(index=False):
        if not isinstance(seq, np.ndarray):
            continue

        for it in seq:
            if isinstance(it, np.ndarray) and it.size >= 2:
                token = it[0]
                pos = it[1]
                if pos is not None:
                    out.append((year, token, pos))

    return pd.DataFrame(out, columns=["year", "token", "pos"])
