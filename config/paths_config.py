import os

# Data ingestion
RAW_DIR = "artifacts/raw"
CONFIG_PATH = "config/config.yaml"

# Data processing
PROCESSED_DIR = "artifacts/processed"
ANIMELIST_CSV = "artifacts/raw/animelist.csv"
ANIME_CSV = "artifacts/raw/anime.csv"
ANIME_SYNOPSIS_CSV = "artifacts/raw/anime_with_synopsis.csv"

RATING_DF = os.path.join(PROCESSED_DIR, "rating_df.csv")
ANIME_DF = os.path.join(PROCESSED_DIR, "anime_df.csv")
SYNOPSIS_DF = os.path.join(PROCESSED_DIR, "synopsis_df.csv")

USER2USER_ENCODED = os.path.join(PROCESSED_DIR, "user2user_encoded.pkl")
USER2USER_DECODED = os.path.join(PROCESSED_DIR, "user2user_decoded.pkl")

ANIME2ANIME_ENCODED = os.path.join(PROCESSED_DIR, "anim2anime_encoded.pkl")
ANIME2ANIME_DECODED = os.path.join(PROCESSED_DIR, "anim2anime_decoded.pkl")
