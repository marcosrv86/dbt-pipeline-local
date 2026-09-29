import pandas as pd
import logging
import sqlite3
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
            conexion = sqlite3.connect("erp_transaccional.db")

            # 2. Ecribes tu consulta SQL
            consulta = "SELECT * FROM cabeceras_compra"

            # 3. Lees los datos directamente a un DataFrame de Pandas
            df_cabeceras = pd.read_sql_query(consulta, conexion)


            #df_cabeceras = pd.DataFrame({'id_documento': ['45001'],'fecha_creacion': ['2026-09-17'], 'id_proveedor': ['PROV-1']})
            #df_posiciones = pd.DataFrame({'id_documento': ['45001'], 'posicion': [10],               # <--- Faltaba esta 'material': ['CHAPA_ACERO'],    # <--- Y faltaba esta 'cantidad': [800]})
            consulta2 = "SELECT * FROM posiciones_compra" 
            df_posiciones = pd.read_sql_query(consulta2, conexion)
           



            logging.info("Extracción de cabeceras y posiciones exitosa.")
            return {'raw_cabeceras_compra': df_cabeceras, 'raw_posiciones_compra': df_posiciones}
            
        except Exception as e:
            logging.error(f"Fallo crítico al extraer datos del ERP: {str(e)}")
            # Levantamos el error para que Dagster lo intercepte y marque el nodo en rojo
            raise
        finally:
        # El bloque finally se ejecuta SIEMPRE (haya éxito o haya error)
         if 'conexion' in locals():
            conexion.close()
            logging.info("Conexión a la base de datos cerrada de forma segura.")