import subprocess
from dagster import asset, Definitions
from extractor_erp import ExtractorERP
from cargador_bq import CargadorBigQuery

@asset
def ingesta_erp_a_bigquery():
    # ... (Tu código actual de instanciar ExtractorERP y CargadorBigQuery queda exactamente igual) ...
    extractor = ExtractorERP("ERP_Produccion_AR")
    cargador = CargadorBigQuery(project_id="analytics-lab-sandbox", dataset_id="raw_data")
    diccionario_datos = extractor.extraer_compras()
    resultado_carga = cargador.cargar_diccionario(diccionario_datos)
    return resultado_carga

# ---> PEGA AQUÍ TU NUEVO BLOQUE, REEMPLAZANDO EL ANTERIOR <---
@asset(deps=[ingesta_erp_a_bigquery])
def transformar_y_testear_erp():
    """Ejecuta el modelo incremental y luego pasa los tests de calidad."""
    
    # 1. Ejecutar el modelo
    subprocess.run(["dbt", "run", "--select", "mart_compras_detalle"], check=True)
    
    # 2. Ejecutar los tests (Dagster fallará si algún test no pasa)
    resultado_tests = subprocess.run(["dbt", "test", "--select", "mart_compras_detalle"], capture_output=True, text=True)
    
    if resultado_tests.returncode != 0:
        raise Exception(f"Fallo en Data Quality.\nLog: {resultado_tests.stdout}")
        
    return "Modelo materializado y validado con éxito (0 nulos, 0 valores no aceptados)"

# ---> IMPORTANTE: ACTUALIZA EL NOMBRE EN LAS DEFINICIONES AL FINAL <---
defs = Definitions(
    assets=[ingesta_erp_a_bigquery, transformar_y_testear_erp]
)