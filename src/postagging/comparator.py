"""
Comparador NLTK vs spaCy
- Penn Treebank → Universal (NLTK)
- Universal POS (spaCy)
- Comparación por año
- Comparación de velocidad
"""

import time
from collections import Counter

import pandas as pd
import nltk
import spacy
from nltk import word_tokenize, pos_tag
from nltk.tag.mapping import map_tag

# IMPORTAR RUTAS DEL PROYECTO


from src.utils.config import (
    LYRICS_CLEAN_PARQUET,
    POS_COMPARISON_BY_YEAR_CSV,
    POS_SPEED_COMPARISON_CSV,
)

TEXT_COL = "lyrics"
YEAR_COL = "year"
MAX_ROWS = 3000


# FUNCIONES

def nltk_universal(text: str) -> Counter:
    tokens = word_tokenize(text)
    tagged = pos_tag(tokens)  # Penn Treebank
    universal = [map_tag("en-ptb", "universal", tag) for _, tag in tagged]
    return Counter(universal)


def spacy_universal(nlp, text: str) -> Counter:
    doc = nlp(text)
    return Counter([token.pos_ for token in doc if not token.is_space])


def normalize(counter: Counter) -> dict:
    total = sum(counter.values())
    return {k: v / total for k, v in counter.items()} if total > 0 else {}



# RUN PRINCIPAL (importable)


def run():

    # Descargar recursos NLTK si no están
    nltk.download("punkt", quiet=True)
    nltk.download("averaged_perceptron_tagger", quiet=True)
    nltk.download("universal_tagset", quiet=True)

    # Leer parquet desde config
    df = pd.read_parquet(LYRICS_CLEAN_PARQUET)
    df = df[[YEAR_COL, TEXT_COL]].dropna()

    if MAX_ROWS:
        df = df.head(MAX_ROWS)

    # spaCy sin parser/ner (más rápido)
    nlp = spacy.load("en_core_web_sm", disable=["parser", "ner"])

    nltk_year_pos = {}
    spacy_year_pos = {}

    total_tokens_nltk = 0
    total_tokens_spacy = 0


    # NLTK


    start = time.perf_counter()

    for year, group in df.groupby(YEAR_COL):
        counter = Counter()
        for text in group[TEXT_COL]:
            c = nltk_universal(text)
            counter.update(c)
            total_tokens_nltk += sum(c.values())
        nltk_year_pos[year] = normalize(counter)

    nltk_time = time.perf_counter() - start
    nltk_speed = total_tokens_nltk / nltk_time if nltk_time > 0 else 0


    # spaCy


    start = time.perf_counter()

    for year, group in df.groupby(YEAR_COL):
        counter = Counter()
        for text in group[TEXT_COL]:
            c = spacy_universal(nlp, text)
            counter.update(c)
            total_tokens_spacy += sum(c.values())
        spacy_year_pos[year] = normalize(counter)

    spacy_time = time.perf_counter() - start
    spacy_speed = total_tokens_spacy / spacy_time if spacy_time > 0 else 0


    # Guardar comparación POS


    all_pos = set()
    for d in nltk_year_pos.values():
        all_pos.update(d.keys())
    for d in spacy_year_pos.values():
        all_pos.update(d.keys())

    results = []

    for year in sorted(df[YEAR_COL].unique()):
        for pos in all_pos:
            nltk_freq = nltk_year_pos.get(year, {}).get(pos, 0)
            spacy_freq = spacy_year_pos.get(year, {}).get(pos, 0)

            results.append({
                "year": year,
                "pos": pos,
                "nltk_freq": nltk_freq,
                "spacy_freq": spacy_freq,
                "abs_diff": abs(nltk_freq - spacy_freq)
            })

    pos_df = pd.DataFrame(results)
    pos_df.to_csv(POS_COMPARISON_BY_YEAR_CSV, index=False)


    # Guardar comparación de velocidad


    speed_df = pd.DataFrame([
        {
            "model": "NLTK (Penn -> Universal)",
            "time_seconds": nltk_time,
            "tokens": total_tokens_nltk,
            "tokens_per_second": nltk_speed
        },
        {
            "model": "spaCy (Universal)",
            "time_seconds": spacy_time,
            "tokens": total_tokens_spacy,
            "tokens_per_second": spacy_speed
        }
    ])

    speed_df.to_csv(POS_SPEED_COMPARISON_CSV, index=False)

    print("Comparacion del POst Taggin guardada en:", POS_COMPARISON_BY_YEAR_CSV)
    print("Comparacion de la velocidad guardada en:", POS_SPEED_COMPARISON_CSV)



if __name__ == "__main__":
    run()
