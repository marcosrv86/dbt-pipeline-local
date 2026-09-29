import subprocess
from dagster import asset, Definitions, AssetSelection, define_asset_job, ScheduleDefinition
from extractor_erp import ExtractorERP
from cargador_bq import CargadorBigQuery
from monitoreo_dbt import AnalizadorCalidadDatos

# ... (Tus @asset ingesta_erp_a_bigquery y transformar_y_testear_erp quedan exactamente igual) ...

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

@asset(deps=[transformar_y_testear_erp])
def auditoria_calidad_dbt():
    # Instanciamos la clase apuntando a tu proyecto
    ruta_proyecto = r"C:\Users\marco\laboratorio_dbt\pipeline_local" 
    monitor = AnalizadorCalidadDatos(ruta_proyecto)
    
    # Modificamos tu método para que devuelva la cantidad de fallos
    fallos = monitor.evaluar_tests_y_retornar_errores() 
    
    if fallos > 0:
        # El Circuit Breaker salta: abortamos el proceso en Dagster
        raise ValueError(f"CRÍTICO: Se detectaron {fallos} errores de calidad. Pipeline detenido.")
        
    return "Auditoría superada. Datos listos para consumo."


# ---> IMPORTANTE: ACTUALIZA EL NOMBRE EN LAS DEFINICIONES AL FINAL <---

# Definimos el Job que selecciona todos los assets del proyecto
pipeline_diario_job = define_asset_job(
    name="job_elt_compras_diario",
    selection=AssetSelection.all()
)

# Definimos el Schedule usando notación cron
programacion_diaria = ScheduleDefinition(
    job=pipeline_diario_job,
    cron_schedule="0 6 * * *", # 6:00 AM todos los días
    execution_timezone="America/Argentina/Buenos_Aires" 
)
defs = Definitions(
    assets=[ingesta_erp_a_bigquery, transformar_y_testear_erp,auditoria_calidad_dbt],
    jobs=[pipeline_diario_job],
    schedules=[programacion_diaria]
)