import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

PROJECT_DIR = Path(os.getenv('PROJECT_DIR', '.')).resolve()
RAW_DIR = PROJECT_DIR / 'data' / 'raw'
SILVER_DIR = PROJECT_DIR / 'data' / 'silver'
GOLD_DIR = PROJECT_DIR / 'data' / 'gold'
EXPORT_DIR = PROJECT_DIR / 'data' / 'exports'

OPENING_BALANCE_ID = os.getenv('OPENING_BALANCE_ID', '')
GL_ID = os.getenv('GL_ID', '')

for p in [RAW_DIR, SILVER_DIR, GOLD_DIR, EXPORT_DIR]:
    p.mkdir(parents=True, exist_ok=True)
