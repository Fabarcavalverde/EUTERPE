"""
Top 100 Cleaner.

Recibe un DataFrame (output del BillboardTop100Scraper)
y sobrescribe la columna `artist` dejando únicamente
el primer artista cuando hay colaboraciones.

Este DataFrame luego se usa directamente para el scraper de lyrics.
"""

import re
import pandas as pd


class BillboardTop100Cleaner:
    _COLLAB_SPLIT = re.compile(
        r"""
        \s+(?:featuring\b|feat\.?\b|ft\.?\b|with\b)\s+ |
        \s+and\s+ |
        \s+&\s+ |
        \s+vs\.?\s+ |
        \s+\+\s+ |
        \s+\/\s+ |
        ,\s+
        """,
        re.IGNORECASE | re.VERBOSE
    )

    _PARENS = re.compile(r"[\(\[].*?[\)\]]")

    def _extract_primary_artist(self, artist: str) -> str:

        if artist is None or (isinstance(artist, float) and pd.isna(artist)):
            return artist

        artist = str(artist).strip()

        # Normalizar caracteres
        artist = (
            artist.replace("’", "'")
                  .replace("–", "-")
                  .replace("—", "-")
                  .replace("×", " × ")
        )

        # Quitar texto en paréntesis/corchetes
        artist = self._PARENS.sub("", artist).strip()

        # Separar colaboraciones
        parts = [
            p.strip()
            for p in self._COLLAB_SPLIT.split(artist)
            if p and p.strip()
        ]

        return parts[0] if parts else artist

    def clean(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Sobrescribe la columna `artist` con el artista limpio.
        """

        if "artist" not in df.columns:
            raise ValueError("Column 'artist' not found")

        df = df.copy()
        df["artist"] = df["artist"].apply(self._extract_primary_artist)

        return df
