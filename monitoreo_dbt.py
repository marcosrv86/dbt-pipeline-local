import json
import os

class AnalizadorCalidadDatos:
    def __init__(self, ruta_proyecto_dbt):
        # Apuntamos a la ubicación exacta del archivo generado por dbt
        self.ruta_json = os.path.join(ruta_proyecto_dbt, "target", "run_results.json")

    def evaluar_tests_y_retornar_errores(self):
        if not os.path.exists(self.ruta_json):
            print("No se encontró el archivo run_results.json. Ejecuta 'dbt test' primero.")
            return

        print(f"Analizando resultados de calidad en: {self.ruta_json}\n")
        
        # Abrimos e interpretamos el archivo JSON
        with open(self.ruta_json, 'r', encoding='utf-8') as archivo:
            datos = json.load(archivo)

        tests_ejecutados = 0
        tests_fallidos = 0

        # Iteramos sobre la lista de resultados
        for resultado in datos.get('results', []):
            tests_ejecutados += 1
            estado = resultado.get('status')
            id_test = resultado.get('unique_id')

            if estado == 'fail' or estado == 'error':
                tests_fallidos += 1
                # Extraemos solo el nombre del test para que sea legible
                nombre_limpio = id_test.split('.')[-1]
                print(f"❌ ALERTA CRÍTICA: Falló el test '{nombre_limpio}'")
                print(f"   Detalle técnico: {resultado.get('message')}\n")

        print("-" * 40)
        if tests_fallidos == 0:
            print(f"✅ Éxito total: {tests_ejecutados} tests ejecutados sin errores.")
        else:
            print(f"⚠️ Peligro: {tests_fallidos} de {tests_ejecutados} tests fallaron.")
        return tests_fallidos
# Ejecución del módulo
if __name__ == "__main__":
    # Ajusta esta ruta si tu carpeta de dbt tiene otro nombre
    ruta_dbt = r"C:\Users\marco\laboratorio_dbt\pipeline_local" 
    monitor = AnalizadorCalidadDatos(ruta_dbt)
    monitor.evaluar_tests()