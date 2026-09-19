import pandas as pd
from google.cloud import bigquery
import os

def main():
    print("Iniciando lectura del archivo local...")
    # Asegúrate de tener el archivo ventas_ejemplo.csv en la misma carpeta
    df = pd.read_csv("ventas_ejemplo.csv") 

    # Limpieza básica: normalizar nombres de columnas
    df.columns = df.columns.str.lower().str.replace(' ', '_')

    print("Conectando a Google BigQuery...")
    # El cliente tomará automáticamente las credenciales de tu login anterior
    client = bigquery.Client(project="analytics-lab-sandbox")
    
    # Define el destino: proyecto.dataset.tabla
    table_id = "analytics-lab-sandbox.raw_data.tbl_ventas"

    # Configurar el trabajo para sobrescribir la tabla en cada ejecución
    job_config = bigquery.LoadJobConfig(
        write_disposition="WRITE_TRUNCATE",
    )

    print(f"Cargando {len(df)} filas a la tabla {table_id}...")
    job = client.load_table_from_dataframe(df, table_id, job_config=job_config)
    job.result() # Pausa la ejecución hasta que BigQuery confirme la carga

    print("¡Ingesta completada con éxito en la capa Raw!")

if __name__ == "__main__":
    main()