import numpy as np
import pandas as pd
from .config import GOLD_DIR


def normalize_raw(raw_opening_balance_unified: pd.DataFrame, raw_general_ledger_unified: pd.DataFrame):
    for df in [raw_opening_balance_unified, raw_general_ledger_unified]:
        df.columns = [str(c).strip().lower() for c in df.columns]

    raw_opening_balance_unified['date'] = pd.to_datetime(raw_opening_balance_unified['date'], errors='coerce')
    raw_general_ledger_unified['date'] = pd.to_datetime(raw_general_ledger_unified['date'], errors='coerce')

    raw_opening_balance_unified['month_end'] = raw_opening_balance_unified['date']
    raw_general_ledger_unified['month_end'] = (
        raw_general_ledger_unified['date'].dt.to_period('M').dt.to_timestamp(how='end').dt.normalize()
    )

    for c in ['report', 'account', 'subaccount', 'details', 'class', 'subclass', 'subclass2']:
        if c in raw_general_ledger_unified.columns:
            raw_general_ledger_unified[f'{c}_l'] = raw_general_ledger_unified[c].astype(str).str.strip().str.lower()
        if c in raw_opening_balance_unified.columns:
            raw_opening_balance_unified[f'{c}_l'] = raw_opening_balance_unified[c].astype(str).str.strip().str.lower()

    return raw_opening_balance_unified, raw_general_ledger_unified


def build_pnl_detail_global(raw_general_ledger_unified: pd.DataFrame):
    pnl_src = raw_general_ledger_unified[raw_general_ledger_unified['report_l'] == 'profit and loss'].copy()
    rpt = (
        pnl_src.groupby(['month_end', 'class', 'subclass', 'subclass2', 'account', 'subaccount'], dropna=False, as_index=False)['amount']
        .sum()
        .rename(columns={'amount': 'value'})
    )
    check = (
        pnl_src.groupby('month_end', as_index=False)['amount'].sum().rename(columns={'amount': 'source_value'})
        .merge(rpt.groupby('month_end', as_index=False)['value'].sum().rename(columns={'value': 'detail_value'}), on='month_end', how='outer')
    )
    check['check'] = check['detail_value'] - check['source_value']
    return rpt, check


def build_bs_detail_global(raw_opening_balance_unified: pd.DataFrame):
    bs_src = raw_opening_balance_unified[raw_opening_balance_unified['report_l'] == 'balance sheet'].copy()
    rpt = (
        bs_src.groupby(['month_end', 'class', 'subclass', 'subclass2', 'account', 'subaccount'], dropna=False, as_index=False)['amount']
        .sum()
        .rename(columns={'amount': 'ending_balance'})
    )
    check = (
        bs_src.groupby('month_end', as_index=False)['amount'].sum().rename(columns={'amount': 'source_value'})
        .merge(rpt.groupby('month_end', as_index=False)['ending_balance'].sum().rename(columns={'ending_balance': 'detail_value'}), on='month_end', how='outer')
    )
    check['check'] = check['detail_value'] - check['source_value']
    return rpt, check


def build_kpis_global(rpt_pnl_detail_global: pd.DataFrame, rpt_bs_detail_global: pd.DataFrame):
    pnl = rpt_pnl_detail_global.copy()
    bs = rpt_bs_detail_global.copy()

    revenue = (
        pnl[pnl['account'].astype(str).str.lower() == 'sales']
        .groupby('month_end', as_index=False)['value'].sum()
        .rename(columns={'value': 'kpi_value'})
    )
    revenue['kpi_name'] = 'Revenue'
    revenue['kpi_group'] = 'P&L'
    revenue['kpi_format'] = 'currency'

    gross_profit = (
        pnl[pnl['account'].astype(str).str.lower().isin(['sales', 'cost of sales'])]
        .groupby('month_end', as_index=False)['value'].sum()
        .rename(columns={'value': 'kpi_value'})
    )
    gross_profit['kpi_name'] = 'Gross Profit'
    gross_profit['kpi_group'] = 'P&L'
    gross_profit['kpi_format'] = 'currency'

    current_assets = (
        bs[bs['subclass2'].astype(str).str.lower() == 'current assets']
        .groupby('month_end', as_index=False)['ending_balance'].sum()
        .rename(columns={'ending_balance': 'kpi_value'})
    )
    current_assets['kpi_name'] = 'Current Assets'
    current_assets['kpi_group'] = 'BS'
    current_assets['kpi_format'] = 'currency'

    current_liabilities = (
        bs[bs['subclass2'].astype(str).str.lower() == 'current liabilities']
        .groupby('month_end', as_index=False)['ending_balance'].sum()
        .rename(columns={'ending_balance': 'kpi_value'})
    )
    current_liabilities['kpi_name'] = 'Current Liabilities'
    current_liabilities['kpi_group'] = 'BS'
    current_liabilities['kpi_format'] = 'currency'

    rpt_kpis_global = pd.concat([
        revenue[['month_end', 'kpi_name', 'kpi_group', 'kpi_value', 'kpi_format']],
        gross_profit[['month_end', 'kpi_name', 'kpi_group', 'kpi_value', 'kpi_format']],
        current_assets[['month_end', 'kpi_name', 'kpi_group', 'kpi_value', 'kpi_format']],
        current_liabilities[['month_end', 'kpi_name', 'kpi_group', 'kpi_value', 'kpi_format']],
    ], ignore_index=True)

    return rpt_kpis_global


def save_gold_outputs(rpt_pnl_detail_global, pnl_check, rpt_bs_detail_global, bs_check, rpt_kpis_global):
    rpt_pnl_detail_global.to_csv(GOLD_DIR / 'rpt_pnl_detail_global.csv', index=False)
    pnl_check.to_csv(GOLD_DIR / 'pnl_source_check_global.csv', index=False)
    rpt_bs_detail_global.to_csv(GOLD_DIR / 'rpt_bs_detail_global.csv', index=False)
    bs_check.to_csv(GOLD_DIR / 'bs_source_check_global.csv', index=False)
    rpt_kpis_global.to_csv(GOLD_DIR / 'rpt_kpis_global.csv', index=False)
    print('✅ Capa gold generada')
