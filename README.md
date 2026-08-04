# Financial Statements ETL from General Ledger

## 1) Problema de negocio
En muchas organizaciones, la información financiera está dispersa entre distintas fuentes operativas y no siempre existe un modelo reproducible para transformar movimientos contables en reportes de gestión. En este proyecto se parte de **dos bases de datos alojadas en Google Drive / Google Sheets** que funcionan como origen maestro:

- **Opening Balance**: saldos iniciales y dimensiones base.
- **General Ledger**: movimientos contables, catálogo de cuentas, calendario, territorios y mappings financieros.

El reto consiste en construir un pipeline analítico que:

1. Descargue y consolide ambas fuentes.
2. Estandarice y limpie la información.
3. Construya tablas analíticas para reporting.
4. Genere automáticamente:
   - **P&L (Profit & Loss)**
   - **BS (Balance Sheet)**
   - **CF (Cash Flow)**
   - **KPIs financieros**
5. Exporte un dataset final listo para consumo en BI / reporting (por ejemplo, Looker Studio, Power BI o Excel).

---

## 2) Objetivo del proyecto
Diseñar un repositorio reproducible en GitHub que convierta datos financieros crudos en una **capa de reporting confiable**, con validaciones y exportaciones finales.

---

## 3) Arquitectura funcional

```text
Google Drive / Google Sheets
        |
        v
   data/raw      <- descarga de workbooks fuente
        |
        v
   data/silver   <- tablas limpias, tipadas y unificadas
        |
        v
   data/gold     <- P&L, BS, CF, KPIs y checks
        |
        v
 data/exports    <- fact table final para reporting / BI
```

### Capas
- **Raw**: copia fiel de las fuentes descargadas.
- **Silver**: limpieza, tipado, joins y estandarización.
- **Gold**: reporting financiero y KPIs.
- **Exports**: tabla final unificada para dashboards o reportes externos.

---

## 4) Fuentes de datos consideradas
### Workbook 1: Opening Balance
Hojas esperadas:
- `TB`
- `COA`
- `Territory`
- `Calendar`

### Workbook 2: General Ledger
Hojas esperadas:
- `GL`
- `COA`
- `Calendar`
- `Territory`
- `CashFlow_St`
- `SoCE_St`

---

## 5) Transformaciones principales
### A. Ingesta
- Montaje de Google Drive.
- Descarga de ambos workbooks desde Google Sheets a formato `.xlsx`.
- Inventario de hojas, filas y columnas.

### B. Preparación (Silver)
- Limpieza de nombres de columnas.
- Conversión de tipos (`date`, `territory_key`, `account_key`, `amount`).
- Construcción de un **COA maestro**.
- Validaciones de integridad:
  - cuentas del GL presentes en COA
  - territorios válidos
  - fechas incluidas en calendario
- Construcción de tablas unificadas:
  - `raw_opening_balance_unified`
  - `raw_general_ledger_unified`

### C. Reporting (Gold)
Se construyen las siguientes tablas:
- `rpt_pnl_detail_global`
- `rpt_bs_detail_global`
- `rpt_cashflow_detail_global`
- `rpt_kpis_global`

Además se generan checks técnicos:
- conciliación P&L origen vs detalle
- conciliación BS origen vs detalle
- validaciones por componentes del Cash Flow
- bridge final de caja
- nulos y conteos de KPIs

### D. Export
Se genera una tabla final unificada:
- `fact_financials_looker_global`

Esta tabla permite explotar un único modelo para reportes y dashboards.

---

## 6) KPIs generados
El pipeline contempla, entre otros:
- Revenue
- Gross Profit
- Gross Margin %
- PBT
- Cash Balance
- Current Assets
- Current Liabilities
- Working Capital
- Current Ratio
- Operating Cash Flow
- Investing Cash Flow
- Financing Cash Flow
- Net Cash Flow

---

## 7) Estructura del repositorio
```text
financial-statements-etl-github/
├── README.md
├── requirements.txt
├── .gitignore
├── .env.example
├── src/
│   ├── config.py
│   ├── extract_google_sheets.py
│   ├── transform_silver.py
│   ├── build_reporting.py
│   ├── export_reporting.py
│   └── main.py
├── docs/
│   └── architecture.md
├── data/
│   ├── raw/
│   ├── silver/
│   ├── gold/
│   └── exports/
└── tests/
```

---

## 8) Cómo ejecutar
### 1. Clonar repo
```bash
git clone <TU_REPO_GITHUB>
cd financial-statements-etl-github
```

### 2. Crear entorno
```bash
python -m venv .venv
source .venv/bin/activate   # Linux / Mac
# .venv\Scripts\activate    # Windows
pip install -r requirements.txt
```

### 3. Configurar variables
Copia `.env.example` a `.env` y completa:
- rutas locales
- IDs de Google Sheets

### 4. Ejecutar pipeline
```bash
python -m src.main
```

---

## 9) Valor del proyecto
Este proyecto demuestra capacidad para:
- Diseñar pipelines ETL financieros.
- Estructurar datos para reporting ejecutivo.
- Aplicar checks de control financiero.
- Construir datasets finales para BI.
- Documentar un proyecto analítico de forma profesional para GitHub / portfolio.

---

## 10) Posibles mejoras futuras
- Parametrización por país / territorio.
- Automatización con GitHub Actions.
- Testing unitario ampliado.
- Persistencia en base de datos SQL.
- Dashboard en Power BI o Looker Studio conectado al export final.
- Dockerización del proyecto.

---

## 11) Autor
Proyecto preparado como caso de portfolio de analítica financiera y reporting automatizado.
