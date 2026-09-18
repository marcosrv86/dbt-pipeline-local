import pandas as pd

class ExtractorERP:
    def __init__(self, sistema_origen):
        # Inicializamos el objeto con el nombre del sistema al que nos conectamos
        self.sistema = sistema_origen

    def extraer_compras(self):
        print(f"--- Iniciando extracción desde el sistema transaccional: {self.sistema} ---")
        
        # Simulando la extracción de una tabla de Cabeceras (Documentos de Compra)
        print("Extrayendo Cabeceras...")
        df_cabeceras = pd.DataFrame({
            'id_documento': ['4500000001', '4500000002'],
            'fecha_creacion': ['2026-09-13', '2026-09-13'],
            'id_proveedor': ['PROV-104', 'PROV-299']
        })
        
        # Simulando la extracción de una tabla de Posiciones (Detalle de Materiales)
        print("Extrayendo Posiciones...")
        df_posiciones = pd.DataFrame({
            'id_documento': ['4500000001', '4500000001', '4500000002'],
            'posicion': [10, 20, 10],
            'material': ['CHAPA_ACERO', 'TORNILLO_HEX', 'MOTOR_ELEC'],
            'cantidad': [150, 5000, 2]
        })
        
        # Devolvemos ambas tablas empaquetadas en un diccionario
        return {
            'raw_cabeceras_compra': df_cabeceras, 
            'raw_posiciones_compra': df_posiciones
        }
if __name__ == "__main__":
    # 1. Instanciamos nuestra nueva clase simulando un ERP de producción
    erp = ExtractorERP(sistema_origen="ERP_Produccion_AR")
    
    # 2. Ejecutamos el método de extracción
    lote_datos = erp.extraer_compras()
    
    # 3. Validamos la salida iterando sobre el diccionario
    for nombre_tabla, dataframe in lote_datos.items():
        print(f"\nTabla extraída: {nombre_tabla}")
        print(f"Total de registros: {len(dataframe)}")
        print(dataframe.head())