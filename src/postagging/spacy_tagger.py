"""
spaCy POS Tagger.

Lee tokens desde Parquet (processed) y genera POS tags con spaCy.
Guarda resultado en data/results.
"""

from __future__ import annotations
from pathlib import Path
import pandas as pd

from src.utils.config import PROCESSED_DATA_PATH, RESULTS_DATA_PATH


INPUT_FILE = PROCESSED_DATA_PATH / "songs_with_lyrics_tokenized.parquet"
OUTPUT_FILE = RESULTS_DATA_PATH / "pos_spacy.parquet"


def run(
    input_path: Path = INPUT_FILE,
    output_path: Path = OUTPUT_FILE,
    spacy_model: str = "en_core_web_sm",
    batch_size: int = 128
) -> pd.DataFrame:
    import spacy  # lazy import

    df = pd.read_parquet(input_path)

    required = {"year", "rank", "artist", "song", "lyrics"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing columns: {sorted(missing)}")

    nlp = spacy.load(spacy_model, disable=["ner", "parser", "lemmatizer"])
    # usamos tagger/attribute_ruler si aplica
    # Nota: spaCy POS opera sobre texto, no tokens sueltos, así que unimos tokens con espacio.

    texts = df["lyrics"].apply(lambda t: "" if t is None else " ".join(t)).tolist()

    pos_spacy = []
    for doc in nlp.pipe(texts, batch_size=batch_size):
        if not doc.text.strip():
            pos_spacy.append(None)
        else:
            pos_spacy.append([(token.text, token.pos_) for token in doc])

    out = df.copy()
    out["pos_spacy"] = pos_spacy

    output_path.parent.mkdir(parents=True, exist_ok=True)
    out.to_parquet(output_path, index=False)
    print(f"Saved spaCy POS to: {output_path}")

    return out


if __name__ == "__main__":
    run()
