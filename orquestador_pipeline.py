import subprocess
import sys  # Importa sys para obtener la ruta exacta de Python
from dagster import asset, Definitions

@asset
def extraer_datos_csv():
    """Ejecuta el script de Python externo para la ingesta."""
    # Reemplaza "python" por sys.executable
    resultado = subprocess.run([sys.executable, "ingesta.py"], capture_output=True, text=True)
    
    if resultado.returncode != 0:
        raise Exception(f"Fallo en la ingesta: {resultado.stderr}")
    
    return "Ingesta completada con éxito"

# ... el resto de tus assets (ejecutar_modelos_dbt, etc.) se mantienen exactamente igual
@asset(deps=[extraer_datos_csv])
def ejecutar_modelos_dbt():
    """Ejecuta el comando dbt run apuntando a tu mart."""
    # Ejecuta dbt apuntando a tu entorno de VS Code
    resultado = subprocess.run(
        ["dbt", "run", "--select", "mart_rendimiento_pozos"], 
        capture_output=True, 
        text=True
    )
    
    if resultado.returncode != 0:
        raise Exception(f"Fallo en dbt: {resultado.stderr}")
    
    return "Modelos de dbt materializados correctamente"

defs = Definitions(
    assets=[extraer_datos_csv, ejecutar_modelos_dbt]
)