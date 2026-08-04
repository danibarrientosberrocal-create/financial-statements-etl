import requests
from pathlib import Path
from .config import RAW_DIR, OPENING_BALANCE_ID, GL_ID


def _download_file(url: str, output_path: Path) -> None:
    response = requests.get(url, timeout=60)
    response.raise_for_status()
    output_path.write_bytes(response.content)
    print(f'✅ Guardado: {output_path}')


def run_extract() -> tuple[Path, Path]:
    if not OPENING_BALANCE_ID or not GL_ID:
        raise ValueError('Faltan OPENING_BALANCE_ID y/o GL_ID en el fichero .env')

    ob_url = f'https://docs.google.com/spreadsheets/d/{OPENING_BALANCE_ID}/export?format=xlsx'
    gl_url = f'https://docs.google.com/spreadsheets/d/{GL_ID}/export?format=xlsx'

    ob_path = RAW_DIR / 'opening_balance_workbook.xlsx'
    gl_path = RAW_DIR / 'gl_workbook.xlsx'

    _download_file(ob_url, ob_path)
    _download_file(gl_url, gl_path)

    return ob_path, gl_path
