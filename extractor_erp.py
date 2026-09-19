import pandas as pd
import logging

# Configuramos el formato básico del log
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ExtractorERP:
    def __init__(self, sistema_origen):
        self.sistema = sistema_origen

    def extraer_compras(self):
        logging.info(f"Conectando al ERP transaccional: {self.sistema}")
        
        try:
            # Simulamos un error de red forzando una división por cero o un error de lectura
            # Descomenta la siguiente línea para probar la caída:
            # error_forzado = 1 / 0 
            
            df_cabeceras = pd.DataFrame({'id_documento': ['45001'],'fecha_creacion': ['2026-09-17'], 'id_proveedor': ['PROV-1']})
            df_posiciones = pd.DataFrame({
    'id_documento': ['45001'], 
    'posicion': [10],               # <--- Faltaba esta
    'material': ['CHAPA_ACERO'],    # <--- Y faltaba esta
    'cantidad': [500]
})
            
            logging.info("Extracción de cabeceras y posiciones exitosa.")
            return {'raw_cabeceras_compra': df_cabeceras, 'raw_posiciones_compra': df_posiciones}
            
        except Exception as e:
            logging.error(f"Fallo crítico al extraer datos del ERP: {str(e)}")
            # Levantamos el error para que Dagster lo intercepte y marque el nodo en rojo
            raise