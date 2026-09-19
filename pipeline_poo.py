import pandas as pd
import numpy as np

class ExtractorCSV:
    def __init__(self, ruta_archivo):
        # El constructor guarda la ruta cuando instanciamos la clase
        self.ruta_archivo = ruta_archivo

    def extraer(self):
        print(f"Iniciando extracción desde: {self.ruta_archivo}")
        df = pd.read_csv(self.ruta_archivo)
        # Limpieza básica estandarizada
        df.columns = df.columns.str.lower().str.replace(' ', '_')
        return df

class TransformadorEstadistico:
    def __init__(self, columna_objetivo):
        self.columna = columna_objetivo

    def detectar_anomalias_iqr(self, df):
        print(f"Calculando dispersión IQR para la columna: {self.columna}...")
        
        # Calcular los cuartiles usando Pandas
        q1 = df[self.columna].quantile(0.25)
        q3 = df[self.columna].quantile(0.75)
        iqr = q3 - q1
        
        # Definir los límites matemáticos
        limite_inferior = q1 - 1.5 * iqr
        limite_superior = q3 + 1.5 * iqr
        
        # Crear una bandera (flag) booleana
        df['es_anomalia_iqr'] = (df[self.columna] < limite_inferior) | (df[self.columna] > limite_superior)
        
        print(f"Límites calculados -> Inferior: {limite_inferior}, Superior: {limite_superior}")
        return df    

    # Agrega este método dentro de la clase TransformadorEstadistico
    def analizar_correlacion(self, df):
        print("\n--- Generando Matriz de Correlación (Pearson) ---")
        # Filtramos solo las columnas numéricas para evitar errores
        df_numerico = df.select_dtypes(include=['float64', 'int64'])
        
        # Calculamos la matriz
        matriz_corr = df_numerico.corr()
        
        # Extraemos solo cómo se relacionan las demás variables con nuestra columna objetivo
        if self.columna in matriz_corr.columns:
            correlacion_objetivo = matriz_corr[self.columna].sort_values(ascending=False)
            print(f"Correlación con '{self.columna}':\n{correlacion_objetivo}")
        else:
            print(f"La columna {self.columna} no es numérica o no existe.")
            
        return df # Devolvemos el df intacto para seguir el pipeline
if __name__ == "__main__":
    # 1. Instanciamos los objetos
    extractor = ExtractorCSV("ventas_ejemplo.csv")
    transformador = TransformadorEstadistico("monto")
    
    # 2. Ejecutamos el flujo
    datos_crudos = extractor.extraer()
    datos_procesados = transformador.detectar_anomalias_iqr(datos_crudos)
    
    # 3. Validamos el resultado
    print("\nMuestra de los datos procesados:")
    print(datos_procesados[['id_venta', 'monto', 'es_anomalia_iqr']].head())    