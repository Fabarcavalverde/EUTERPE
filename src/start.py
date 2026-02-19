# pipeline.py

from src.scrapers.billboard_scraper import BillboardTop100Scraper
from src.cleaners.top100_cleaner import BillboardTop100Cleaner
from src.scrapers.get_lyrics import run as get_lyrics_run
from src.utils.config import RAW_DATA_PATH

from src.cleaners.lyrics_text_cleaner import run as clean_lyrics_run
from src.preprocess.detect_language import run as lang_detect_run
from src.preprocess.translate_to_english import run as translate_run
from src.preprocess.lyrics_tokenize import run as tokenize_run

from src.postagging.nltk_tagger import run as nltk_pos_run
from src.postagging.spacy_tagger import run as spacy_pos_run
from src.postagging.comparator import run as compare_pos_run


# -------------------------------------------------
# Banner
# -------------------------------------------------
def print_banner():
    print("""
=====================================================
   ███████╗██╗   ██╗████████╗███████╗██████╗ ███████╗
   ██╔════╝██║   ██║╚══██╔══╝██╔════╝██╔══██╗██╔════╝
   █████╗  ██║   ██║   ██║   █████╗  ██████╔╝█████╗  
   ██╔══╝  ██║   ██║   ██║   ██╔══╝  ██╔══██╗██╔══╝  
   ███████╗╚██████╔╝   ██║   ███████╗██║  ██║███████╗
   ╚══════╝ ╚═════╝    ╚═╝   ╚══════╝╚═╝  ╚═╝╚══════╝

        POS Tagging Pipeline - Lyrics Project
=====================================================
""")


# -------------------------------------------------
# Pasos
# -------------------------------------------------

def step_1():
    """Scrapea Billboard Top 100 (1973–2024)."""
    scraper = BillboardTop100Scraper(1973, 2024)
    df = scraper.run()
    df = BillboardTop100Cleaner().clean(df)
    print("Paso 1 completado: Billboard scrapeado y limpio.")


def step_2():
    """Obtiene letras y guarda CSV."""
    print("Asegusere de tener el CSV limpio del Paso 1.")
    # Aquí debería leer el CSV limpio si no trabaja en memoria
    # df = ...
    # get_lyrics_run(df, output_csv=RAW_DATA_PATH / "top100_songs_with_lyrics.csv")
    print("Paso 2 completado: Letras obtenidas.")


def step_3():
    """Limpia texto de las letras."""
    clean_lyrics_run()
    print("Paso 3 completado: Letras limpias.")


def step_4():
    """Detecta idioma."""
    df = clean_lyrics_run()
    lang_detect_run(df)
    print("Paso 4 completado: Idioma detectado.")


def step_5():
    """Traduce a inglés si es necesario."""
    df = clean_lyrics_run()
    df = lang_detect_run(df)
    translate_run(df)
    print("Paso 5 completado: Traducción aplicada.")


def step_6():
    """Tokeniza letras."""
    df = clean_lyrics_run()
    df = lang_detect_run(df)
    df = translate_run(df)
    tokenize_run(df)
    print("Paso 6 completado: Tokenización lista.")


def step_7():
    """POS tagging con NLTK."""
    nltk_pos_run()
    print("Paso 7 completado: POS tagging con NLTK.")


def step_8():
    """POS tagging con spaCy."""
    spacy_pos_run()
    print("Paso 8 completado: POS tagging con spaCy.")


def step_9():
    """Compara NLTK vs spaCy."""
    compare_pos_run()
    print("Paso 9 completado: Comparación realizada.")


#seleccionar paso

def main():
    print_banner()

    print("Seleccione el paso a ejecutar:\n")
    print("1 - Scrape Billboard")
    print("2 - Obtener letras")
    print("3 - Limpiar letras")
    print("4 - Detectar idioma")
    print("5 - Traducir a inglés")
    print("6 - Tokenizar")
    print("7 - POS Tagging NLTK")
    print("8 - POS Tagging spaCy")
    print("9 - Comparar taggers")
    print("0 - Ejecutar TODO\n")

    choice = input("Paso: ")

    steps = {
        "1": step_1,
        "2": step_2,
        "3": step_3,
        "4": step_4,
        "5": step_5,
        "6": step_6,
        "7": step_7,
        "8": step_8,
        "9": step_9,
    }

    if choice == "0":
        for s in steps.values():
            s()
    elif choice in steps:
        steps[choice]()
    else:
        print("Opción inválida.")


if __name__ == "__main__":
    main()
