"""
Lyrics Text Cleaner.

Lee desde RAW_DATA_PATH,
limpia texto de lyrics y guarda en PROCESSED_DATA_PATH.
"""

import re
import pandas as pd
from src.utils.config import RAW_DATA_PATH, PROCESSED_DATA_PATH


INPUT_CSV = RAW_DATA_PATH / "top100_songs_with_lyrics.csv"
OUTPUT_CSV = PROCESSED_DATA_PATH / "songs_with_lyrics_clean.csv"


def clean_lyrics(text: str) -> str | None:

    if pd.isna(text):
        return None

    text = str(text)

    # Eliminar encabezado tipo "Paroles de la chanson ..."
    text = re.sub(
        r"^Paroles de la chanson.*?\n?",
        "",
        text,
        flags=re.IGNORECASE
    )

    # Eliminar contenido entre [], (), {}
    text = re.sub(r"\[.*?\]", " ", text)
    text = re.sub(r"\(.*?\)", " ", text)
    text = re.sub(r"\{.*?\}", " ", text)

    # Convertir saltos de línea en espacio
    text = re.sub(r"\s+", " ", text)

    # Eliminar caracteres especiales (mantener letras con acentos, números y espacio)
    text = re.sub(r"[^a-zA-ZÀ-ÿ0-9\s]", "", text)

    # Normalizar espacios
    text = re.sub(r"\s+", " ", text).strip()

    return text


def run() -> pd.DataFrame:

    df = pd.read_csv(INPUT_CSV, encoding="utf-8")

    df["lyrics"] = (
        df["lyrics"]
        .astype("string")
        .fillna(pd.NA)
        .apply(clean_lyrics)
    )

    df = df[["year", "rank", "artist", "song", "lyrics"]]

    OUTPUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUTPUT_CSV, index=False, encoding="utf-8")

    print(f"Cleaned file saved to: {OUTPUT_CSV}")
    print(f"Non-null lyrics: {df['lyrics'].notna().sum()}")

    return df


if __name__ == "__main__":
    run()
