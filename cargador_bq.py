from google.cloud import bigquery

class CargadorBigQuery:
    def __init__(self, project_id, dataset_id):
        self.project_id = project_id
        self.dataset_id = dataset_id
        # Inicializamos el cliente una sola vez al instanciar la clase
        self.client = bigquery.Client(project=self.project_id)

    def cargar_diccionario(self, diccionario_dfs):
        print(f"--- Iniciando proceso de carga hacia {self.dataset_id} ---")
        
        # Iteramos sobre el diccionario dinámicamente
        for nombre_tabla, df in diccionario_dfs.items():
            table_id = f"{self.project_id}.{self.dataset_id}.{nombre_tabla}"
            
            # Configuración para sobreescribir la tabla si ya existe
            job_config = bigquery.LoadJobConfig(
                write_disposition="WRITE_TRUNCATE",
            )
            
            print(f"Subiendo {len(df)} filas a la tabla: {nombre_tabla}...")
            job = self.client.load_table_from_dataframe(df, table_id, job_config=job_config)
            job.result() # Esperamos a que termine el trabajo
            
            print(f"✓ {nombre_tabla} cargada exitosamente.")
            
        return "Carga masiva completada"