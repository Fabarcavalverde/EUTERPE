"""
Lyrics Fetcher (lyrics.ovh).

Este módulo obtiene lyrics usando https://api.lyrics.ovh/v1/{artist}/{title}.
Ahora expone una función `run(df, ...)` que recibe un DataFrame (ya limpio)
y devuelve el DataFrame con la columna `lyrics`.

Opcionalmente puede escribir a CSV (checkpoint + final).
"""

import time
from pathlib import Path
from urllib.parse import quote
import csv

import pandas as pd
import requests
from requests.adapters import HTTPAdapter, Retry


def build_session() -> requests.Session:
    s = requests.Session()
    retries = Retry(
        total=6,
        connect=6,
        read=6,
        status=6,
        backoff_factor=1.0,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET"],
        raise_on_status=False,
    )
    adapter = HTTPAdapter(max_retries=retries, pool_connections=20, pool_maxsize=20)
    s.mount("https://", adapter)
    s.mount("http://", adapter)
    return s


def get_lyrics(session: requests.Session, artist: str, title: str, timeout: int = 15) -> str | None:
    url = f"https://api.lyrics.ovh/v1/{quote(artist)}/{quote(title)}"
    r = session.get(url, timeout=timeout)

    if r.status_code == 200:
        return r.json().get("lyrics")

    if r.status_code == 404:
        return None

    r.raise_for_status()


def clean_quotes(series: pd.Series) -> pd.Series:
    # Ojo: si series trae NaN, astype(str) lo vuelve "nan", por eso normalizamos después.
    s = (
        series.astype(str)
        .str.replace('"', "", regex=False)
        .str.replace("'", "", regex=False)
        .str.strip()
    )
    return s.replace({"nan": pd.NA})


def _prepare_df(df: pd.DataFrame) -> pd.DataFrame:
    required = {"year", "rank", "artist", "song"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    out = df.copy()
    out["song"] = clean_quotes(out["song"])
    out["artist"] = clean_quotes(out["artist"])

    if "lyrics" not in out.columns:
        out["lyrics"] = pd.NA

    return out


def _resume_from_output(df: pd.DataFrame, output_csv: Path) -> pd.DataFrame:
    if not output_csv.exists():
        return df

    done = pd.read_csv(output_csv, encoding="utf-8")
    if "lyrics" not in done.columns:
        done["lyrics"] = pd.NA

    keys = ["year", "rank", "artist", "song"]
    done = done[keys + ["lyrics"]].drop_duplicates(keys)

    merged = df.merge(done, on=keys, how="left", suffixes=("", "_done"))
    if "lyrics_done" in merged.columns:
        merged["lyrics"] = merged["lyrics"].combine_first(merged["lyrics_done"])
        merged.drop(columns=["lyrics_done"], inplace=True)

    print(f"Resuming: {merged['lyrics'].notna().sum()} rows already have lyrics.")
    return merged


def run(
    df: pd.DataFrame,
    output_csv: Path | None = None,
    batch_save_every: int = 100,
    sleep_seconds: float = 0.2,
    timeout: int = 15,
) -> pd.DataFrame:
    """
    Recibe DataFrame (idealmente ya con artist limpio) y devuelve el DataFrame con lyrics.
    Si `output_csv` se provee, hace checkpoints y guarda al final.

    Parameters
    ----------
    df : pd.DataFrame
        Debe incluir columnas: year, rank, artist, song.
    output_csv : Path | None
        Si no es None, guarda checkpoints y resultado final en esa ruta.
    batch_save_every : int
        Cada cuántas filas nuevas con intento de lyrics se guarda checkpoint.
    sleep_seconds : float
        Pausa entre requests para evitar rate limiting.
    timeout : int
        Timeout por request.

    Returns
    -------
    pd.DataFrame
    """
    out = _prepare_df(df)

    if output_csv is not None:
        out = _resume_from_output(out, output_csv)

    session = build_session()
    total = len(out)
    processed_since_save = 0

    for idx, row in out.iterrows():
        if pd.notna(row.get("lyrics")):
            continue

        artist = row["artist"]
        song = row["song"]

        try:
            lyrics = get_lyrics(session, artist, song, timeout=timeout)
        except (requests.Timeout, requests.ConnectionError):
            lyrics = None
        except requests.HTTPError:
            lyrics = None

        out.at[idx, "lyrics"] = lyrics
        processed_since_save += 1

        if sleep_seconds:
            time.sleep(sleep_seconds)

        if output_csv is not None and processed_since_save >= batch_save_every:
            out.to_csv(
                output_csv,
                index=False,
                encoding="utf-8",
                quoting=csv.QUOTE_ALL,
                escapechar="\\",
                lineterminator="\n",
            )
            print(f"Saved checkpoint ({out['lyrics'].notna().sum()} filled / {total} total)")
            processed_since_save = 0

    if output_csv is not None:
        out.to_csv(
            output_csv,
            index=False,
            encoding="utf-8",
            quoting=csv.QUOTE_ALL,
            escapechar="\\",
            lineterminator="\n",
        )
        print(f"Done. Saved: {output_csv}")

    return out
