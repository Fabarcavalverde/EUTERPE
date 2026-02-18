"""
POS Comparator.

Compara NLTK vs spaCy:
- Distribución de tags
- Coincidencia token-a-token (cuando el texto coincide)

Guarda un CSV resumen en data/results.
"""

from __future__ import annotations
from pathlib import Path
from collections import Counter
import pandas as pd

from src.utils.config import RESULTS_DATA_PATH


NLTK_FILE = RESULTS_DATA_PATH / "pos_nltk.parquet"
SPACY_FILE = RESULTS_DATA_PATH / "pos_spacy.parquet"
OUT_SUMMARY = RESULTS_DATA_PATH / "pos_compare_summary.csv"


def _flatten(tagged):
    if tagged is None or (isinstance(tagged, float) and pd.isna(tagged)):
        return []
    return tagged


def run(
    nltk_path: Path = NLTK_FILE,
    spacy_path: Path = SPACY_FILE,
    out_path: Path = OUT_SUMMARY
) -> pd.DataFrame:

    df_n = pd.read_parquet(nltk_path)
    df_s = pd.read_parquet(spacy_path)

    keys = ["year", "rank", "artist", "song"]
    df = df_n[keys + ["pos_nltk"]].merge(df_s[keys + ["pos_spacy"]], on=keys, how="inner")

    # Distribución de tags
    nltk_tags = Counter()
    spacy_tags = Counter()

    matches = 0
    total_compared = 0

    for row in df.itertuples(index=False):
        n = _flatten(row.pos_nltk)
        s = _flatten(row.pos_spacy)

        nltk_tags.update([tag for _, tag in n])
        spacy_tags.update([tag for _, tag in s])

        # comparación token-a-token solo si hay misma longitud
        if len(n) == len(s) and len(n) > 0:
            for (tok_n, tag_n), (tok_s, tag_s) in zip(n, s):
                if tok_n == tok_s:
                    total_compared += 1
                    if tag_n == tag_s:
                        matches += 1

    agreement = (matches / total_compared) if total_compared else 0.0

    summary = pd.DataFrame([
        {"metric": "rows_compared", "value": len(df)},
        {"metric": "token_tag_agreement_exact_token_match", "value": agreement},
        {"metric": "nltk_unique_tags", "value": len(nltk_tags)},
        {"metric": "spacy_unique_tags", "value": len(spacy_tags)},
    ])

    out_path.parent.mkdir(parents=True, exist_ok=True)
    summary.to_csv(out_path, index=False, encoding="utf-8")
    print(f"Saved summary to: {out_path}")

    return summary


if __name__ == "__main__":
    run()

