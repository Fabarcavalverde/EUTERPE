"""
Billboard Year-End Hot 100 Scraper.

Este módulo descarga las tablas anuales del ranking Billboard Year-End Hot 100
desde Wikipedia, extrae ranking, canción y artista, y devuelve un DataFrame
(con opción de exportar si algún día lo necesitas, pero el flujo principal es in-memory).
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd


class BillboardTop100Scraper:
    """
    Descarga y procesa el Billboard Year-End Hot 100 desde Wikipedia
    para un rango de años determinado.
    """

    def __init__(self, start_year: int = 1973, end_year: int = 2024):
        self.start_year = start_year
        self.end_year = end_year

        self.base_url = "https://en.wikipedia.org/wiki/Billboard_Year-End_Hot_100_singles_of_"
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

        self.songs = {}
        self.singers = {}
        self.ranks = {}

    def fetch_data(self) -> None:
        """
        Ejecuta el scraping para cada año y almacena los resultados
        en los diccionarios internos.
        """
        for year in range(self.start_year, self.end_year + 1):
            names = []
            singer_names = []
            year_ranks = []

            url = f"{self.base_url}{year}"
            r = requests.get(url, headers=self.headers, timeout=20)

            if r.status_code != 200:
                print(f"[WARN] {year} status={r.status_code} url={url}")
                self.songs[year] = names
                self.singers[year] = singer_names
                self.ranks[year] = year_ranks
                continue

            soup = BeautifulSoup(r.text, "html.parser")
            tables = soup.find_all("table", class_="wikitable")

            if not tables:
                print(f"[WARN] {year} no wikitable found.")
                self.songs[year] = names
                self.singers[year] = singer_names
                self.ranks[year] = year_ranks
                continue

            # Elegir la tabla más probable (rank + artist(s))
            target = None
            for t in tables:
                header = t.get_text(" ", strip=True).lower()
                if "rank" in header and ("artist" in header or "artists" in header):
                    target = t
                    break
            if target is None:
                target = tables[0]

            for row in target.find_all("tr"):
                cols = row.find_all("td")
                if not cols:
                    continue

                # Rank (usualmente col 0)
                try:
                    rank = int(cols[0].get_text(strip=True))
                except Exception:
                    continue

                # Preferir columnas: más estable que links
                # Estructura típica: Rank | Song | Artist(s)
                song = None
                singer = None

                if len(cols) >= 3:
                    song = cols[1].get_text(" ", strip=True).strip()
                    singer = cols[2].get_text(" ", strip=True).strip()

                    # Wikipedia suele poner las canciones entre comillas
                    song = song.strip('"').strip("“").strip("”").strip()
                else:
                    # Fallback: lógica basada en links (por si cambia la tabla)
                    links = row.find_all("a")
                    if not links:
                        continue

                    if len(links) >= 2:
                        song = links[0].get_text(strip=True)
                        singer = links[1].get_text(strip=True)
                    else:
                        song = links[0].get_text(strip=True)
                        singer = None

                if song:
                    names.append(song)
                    singer_names.append(singer)
                    year_ranks.append(rank)

            self.songs[year] = names
            self.singers[year] = singer_names
            self.ranks[year] = year_ranks

    def build_dataframe(self) -> pd.DataFrame:
        """
        Construye un DataFrame consolidado con columnas:
        year, rank, song, artist.
        """
        data = []
        for year in range(self.start_year, self.end_year + 1):
            songs = self.songs.get(year, [])
            for i in range(len(songs)):
                data.append({
                    "year": year,
                    "rank": self.ranks.get(year, [None] * len(songs))[i],
                    "song": self.songs.get(year, [None] * len(songs))[i],
                    "artist": self.singers.get(year, [None] * len(songs))[i],
                })
        return pd.DataFrame(data)

    def run(self) -> pd.DataFrame:
        """
        Ejecuta scraping + construcción del DataFrame y lo devuelve (in-memory).
        """
        self.fetch_data()
        return self.build_dataframe()

