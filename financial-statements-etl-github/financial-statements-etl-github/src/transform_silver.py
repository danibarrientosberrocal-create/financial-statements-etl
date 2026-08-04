import re
import pandas as pd
from .config import SILVER_DIR


def clean_column_name(col: str) -> str:
    col = str(col).strip().lower()
    col = col.replace(' ', '_')
    col = re.sub(r'[^a-z0-9_]+', '_', col)
    col = re.sub(r'_+', '_', col).strip('_')
    return col


def stage_clean(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df = df.dropna(how='all').dropna(axis=1, how='all')
    df.columns = [clean_column_name(c) for c in df.columns]
    return df.reset_index(drop=True)


def build_silver(ob_path: str, gl_path: str):
    opening_balance_book = pd.read_excel(ob_path, sheet_name=None, header=0, engine='openpyxl')
    gl_book = pd.read_excel(gl_path, sheet_name=None, header=0, engine='openpyxl')

    tb_df = stage_clean(opening_balance_book['TB'])
    coa_ob_df = stage_clean(opening_balance_book['COA'])
    calendar_ob_df = stage_clean(opening_balance_book['Calendar'])
    territory_ob_df = stage_clean(opening_balance_book['Territory'])

    gl_df = stage_clean(gl_book['GL'])
    cashflow_st_df = stage_clean(gl_book['CashFlow_St'])
    soce_st_df = stage_clean(gl_book['SoCE_St'])

    # Tipado base
    for df in [tb_df, gl_df]:
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
        df['territory_key'] = pd.to_numeric(df['territory_key'], errors='coerce')
        df['account_key'] = pd.to_numeric(df['account_key'], errors='coerce')
        df['amount'] = pd.to_numeric(df['amount'], errors='coerce')

    coa_ob_df['account_key'] = pd.to_numeric(coa_ob_df['account_key'], errors='coerce')
    territory_ob_df['territory_key'] = pd.to_numeric(territory_ob_df['territory_key'], errors='coerce')

    dim_coa_master = coa_ob_df.drop_duplicates(subset=['account_key']).reset_index(drop=True)

    raw_opening_balance_unified = (
        tb_df
        .merge(dim_coa_master, on='account_key', how='left')
        .merge(calendar_ob_df, on='date', how='left')
        .merge(territory_ob_df, on='territory_key', how='left')
    )
    raw_opening_balance_unified['source_workbook'] = 'opening_balance'
    raw_opening_balance_unified['source_sheet'] = 'TB'

    raw_general_ledger_unified = (
        gl_df
        .merge(dim_coa_master, on='account_key', how='left')
        .merge(calendar_ob_df, on='date', how='left')
        .merge(territory_ob_df, on='territory_key', how='left')
    )
    raw_general_ledger_unified['source_workbook'] = 'gl'
    raw_general_ledger_unified['source_sheet'] = 'GL'

    raw_opening_balance_unified.to_csv(SILVER_DIR / 'raw_opening_balance_unified.csv', index=False)
    raw_general_ledger_unified.to_csv(SILVER_DIR / 'raw_general_ledger_unified.csv', index=False)
    cashflow_st_df.to_csv(SILVER_DIR / 'raw_cashflow_mapping.csv', index=False)
    soce_st_df.to_csv(SILVER_DIR / 'raw_soce_mapping.csv', index=False)

    print('✅ Capa silver generada')
    return raw_opening_balance_unified, raw_general_ledger_unified
