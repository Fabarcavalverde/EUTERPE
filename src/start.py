from src.scrapers.billboard_scraper import BillboardTop100Scraper
from src.cleaners.top100_cleaner import BillboardTop100Cleaner
from src.scrapers.get_lyrics import run as get_lyrics_run
from src.utils.config import RAW_DATA_PATH
from src.cleaners.lyrics_text_cleaner import run as clean_lyrics_run
from src.preprocess.lyrics_tokenize import run as tokenize_run
from src.postagging.nltk_tagger import run as nltk_pos_run
from src.postagging.spacy_tagger import run as spacy_pos_run
from src.postagging.comparator import run as compare_pos_run
'''
scraper = BillboardTop100Scraper(1973, 2024)
df = scraper.run()

df = BillboardTop100Cleaner().clean(df)  # sobrescribe artist

df = get_lyrics_run(
    df,
    output_csv=RAW_DATA_PATH / "top100_songs_with_lyrics.csv",
    batch_save_every=100,
    sleep_seconds=0.2,
    timeout=15,
)

clean_lyrics_run()
tokenize_run()
'''
nltk_pos_run()
#spacy_pos_run()
