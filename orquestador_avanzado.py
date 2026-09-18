from dagster import asset, Definitions
from pipeline_poo import ExtractorCSV, TransformadorEstadistico
import pandas as pd
from extractor_erp import ExtractorERP
from cargador_bq import CargadorBigQuery

@asset
def procesar_datos_ml():
    """
    Asset que ejecuta la extracción y el perfilado estadístico 
    utilizando Programación Orientada a Objetos.
    """
    # 1. Instanciamos las clases
    extractor = ExtractorCSV("ventas_ejemplo.csv")
    transformador = TransformadorEstadistico("monto")
    
    # 2. Ejecutamos el flujo
    df_crudo = extractor.extraer()
    df_sin_anomalias = transformador.detectar_anomalias_iqr(df_crudo)
    df_perfilado = transformador.analizar_correlacion(df_sin_anomalias)
    
    # 3. Validamos para Dagster
    if df_perfilado.empty:
        raise Exception("El pipeline devolvió un DataFrame vacío.")
        
    return f"Pipeline ejecutado exitosamente. Filas procesadas: {len(df_perfilado)}"

defs = Definitions(
    assets=[procesar_datos_ml]
)
@asset
def ingesta_erp_a_bigquery():
    """Pipeline orientado a objetos para extraer de un ERP y cargar en BQ."""
    
    # 1. Instanciamos los objetos
    # Reemplaza 'tu-proyecto-id' con el ID real de tu entorno en Google Cloud
    extractor = ExtractorERP("ERP_Produccion_AR")
    cargador = CargadorBigQuery(project_id="analytics-lab-sandbox", dataset_id="raw_data")
    
    # 2. Ejecutamos los métodos
    diccionario_datos = extractor.extraer_compras()
    resultado_carga = cargador.cargar_diccionario(diccionario_datos)
    
    return resultado_carga

defs = Definitions(
    assets=[ingesta_erp_a_bigquery]
)