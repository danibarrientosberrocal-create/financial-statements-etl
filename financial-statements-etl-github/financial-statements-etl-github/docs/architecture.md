# Arquitectura del proyecto

## Resumen
El flujo toma dos archivos maestros de Google Sheets (Opening Balance y General Ledger), los descarga, normaliza y transforma en una capa analítica de reporting financiero.

## Flujo lógico
1. **Extract**
   - Acceso a Google Sheets por URL de exportación.
   - Descarga a Excel.

2. **Stage / Silver**
   - Limpieza de columnas.
   - Tipado de campos clave.
   - Validaciones de integridad.
   - Enriquecimiento con COA, Calendar y Territory.

3. **Gold / Reporting**
   - P&L mensual.
   - Balance Sheet mensual.
   - Cash Flow anual / global.
   - KPIs financieros.

4. **Export**
   - Tabla final unificada para consumo BI.

## Principios de diseño
- Reproducibilidad
- Trazabilidad
- Separación por capas
- Validación de integridad
- Preparación para consumo analítico
