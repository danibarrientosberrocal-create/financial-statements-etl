import pandas as pd
from .config import GOLD_DIR, EXPORT_DIR


def export_unified_reporting():
    pnl = pd.read_csv(GOLD_DIR / 'rpt_pnl_detail_global.csv')
    bs = pd.read_csv(GOLD_DIR / 'rpt_bs_detail_global.csv')
    kpis = pd.read_csv(GOLD_DIR / 'rpt_kpis_global.csv')

    pnl['statement'] = 'P&L'
    pnl['metric_name'] = 'value'
    pnl['metric_value'] = pnl['value']

    bs['statement'] = 'BS'
    bs['metric_name'] = 'ending_balance'
    bs['metric_value'] = bs['ending_balance']

    kpis['statement'] = 'KPI'
    kpis['section'] = 'KPI'
    kpis['subsection'] = kpis['kpi_name']
    kpis['class'] = 'KPI'
    kpis['subclass'] = kpis['kpi_group']
    kpis['subclass2'] = 'KPI'
    kpis['account'] = 'KPI'
    kpis['subaccount'] = 'KPI'
    kpis['line_item'] = kpis['kpi_name']
    kpis['metric_name'] = kpis['kpi_name']
    kpis['metric_value'] = kpis['kpi_value']
    kpis['sort_order'] = None
    kpis['notes'] = kpis['kpi_format']

    pnl_fact = pnl.assign(section=pnl.get('class', ''), subsection=pnl.get('subclass', ''), line_item=pnl.get('subaccount', pnl.get('account', '')), sort_order=None, notes='')[['month_end', 'statement', 'section', 'subsection', 'class', 'subclass', 'subclass2', 'account', 'subaccount', 'line_item', 'metric_name', 'metric_value', 'sort_order', 'notes']]
    bs_fact = bs.assign(section=bs.get('class', ''), subsection=bs.get('subclass', ''), line_item=bs.get('subaccount', bs.get('account', '')), sort_order=None, notes='')[['month_end', 'statement', 'section', 'subsection', 'class', 'subclass', 'subclass2', 'account', 'subaccount', 'line_item', 'metric_name', 'metric_value', 'sort_order', 'notes']]
    kpi_fact = kpis[['month_end', 'statement', 'section', 'subsection', 'class', 'subclass', 'subclass2', 'account', 'subaccount', 'line_item', 'metric_name', 'metric_value', 'sort_order', 'notes']]

    fact = pd.concat([pnl_fact, bs_fact, kpi_fact], ignore_index=True)
    fact['year'] = pd.to_datetime(fact['month_end'], errors='coerce').dt.year
    fact['month_num'] = pd.to_datetime(fact['month_end'], errors='coerce').dt.month

    final_cols = ['month_end', 'year', 'month_num', 'statement', 'section', 'subsection', 'class', 'subclass', 'subclass2', 'account', 'subaccount', 'line_item', 'metric_name', 'metric_value', 'sort_order', 'notes']
    fact = fact[final_cols].sort_values(['month_end', 'statement', 'sort_order', 'account', 'subaccount'], na_position='last').reset_index(drop=True)

    fact.to_csv(EXPORT_DIR / 'fact_financials_looker_global.csv', index=False)
    with pd.ExcelWriter(EXPORT_DIR / 'financials_looker_global.xlsx', engine='openpyxl') as writer:
        fact.to_excel(writer, sheet_name='fact_financials', index=False)
        pnl.to_excel(writer, sheet_name='pnl_detail_global', index=False)
        bs.to_excel(writer, sheet_name='bs_detail_global', index=False)
        kpis.to_excel(writer, sheet_name='kpis_global', index=False)

    print('✅ Export final generado')
