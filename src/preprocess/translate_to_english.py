"""
Translate non-English lyrics to English (offline/simple version).

Recibe DataFrame con columna `language`
y traduce solo los que no sean 'en'.
Devuelve DataFrame actualizado.
"""

from __future__ import annotations

import pandas as pd
from deep_translator import GoogleTranslator


def translate_text(text: str, source_lang: str) -> str | None:
    if pd.isna(text):
        return None

    try:
        return GoogleTranslator(source=source_lang, target="en").translate(text)
    except Exception:
        return None


from pathlib import Path
from src.utils.config import PROCESSED_DATA_PATH


def run(df: pd.DataFrame,
        save_snapshot: bool = True,
        output_path: Path | None = None) -> pd.DataFrame:

    if "lyrics" not in df.columns:
        raise ValueError("Column 'lyrics' not found")

    if "language" not in df.columns:
        raise ValueError("Column 'language' not found")

    out = df.copy()

    mask = (out["language"].notna()) & (out["language"] != "en")

    for idx in out[mask].index:
        text = out.at[idx, "lyrics"]
        lang = out.at[idx, "language"]

        translated = translate_text(text, lang)
        out.at[idx, "lyrics"] = translated

    out.loc[mask, "language"] = "en"

    # Guardar snapshot listo para NLP
    if save_snapshot:
        if output_path is None:
            output_path = PROCESSED_DATA_PATH / "songs_with_lyrics_deluxe.parquet"

        output_path.parent.mkdir(parents=True, exist_ok=True)
        out.to_parquet(output_path, index=False)

        print(f"Saved ready dataset to: {output_path}")

    return out
