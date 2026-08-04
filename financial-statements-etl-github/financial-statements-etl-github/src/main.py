from .extract_google_sheets import run_extract
from .transform_silver import build_silver
from .build_reporting import normalize_raw, build_pnl_detail_global, build_bs_detail_global, build_kpis_global, save_gold_outputs
from .export_reporting import export_unified_reporting


def main():
    ob_path, gl_path = run_extract()
    raw_opening_balance_unified, raw_general_ledger_unified = build_silver(ob_path, gl_path)
    raw_opening_balance_unified, raw_general_ledger_unified = normalize_raw(
        raw_opening_balance_unified,
        raw_general_ledger_unified,
    )
    rpt_pnl_detail_global, pnl_check = build_pnl_detail_global(raw_general_ledger_unified)
    rpt_bs_detail_global, bs_check = build_bs_detail_global(raw_opening_balance_unified)
    rpt_kpis_global = build_kpis_global(rpt_pnl_detail_global, rpt_bs_detail_global)
    save_gold_outputs(rpt_pnl_detail_global, pnl_check, rpt_bs_detail_global, bs_check, rpt_kpis_global)
    export_unified_reporting()


if __name__ == '__main__':
    main()
