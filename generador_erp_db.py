import sqlite3
import pandas as pd
from datetime import datetime, timedelta
import random

class ERPDatabaseBuilder:
    def __init__(self, db_name="erp_transaccional.db"):
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()

    def construir_esquema(self):
        # Creamos la tabla de Cabeceras (simulando SAP EKKO)
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS cabeceras_compra (
                id_documento TEXT PRIMARY KEY,
                fecha_creacion DATE,
                id_proveedor TEXT,
                estado_liberacion TEXT
            )
        ''')
        
        # Creamos la tabla de Posiciones (simulando SAP EKPO)
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS posiciones_compra (
                id_documento TEXT,
                posicion INTEGER,
                material TEXT,
                cantidad INTEGER,
                precio_unitario REAL,
                FOREIGN KEY(id_documento) REFERENCES cabeceras_compra(id_documento)
            )
        ''')
        self.conn.commit()
        print("Tablas relacionales creadas con éxito.")

    def inyectar_datos_masivos(self, cantidad_documentos=100):
        # Generación de datos complejos y aleatorios
        materiales = ['CHAPA_ACERO', 'TORNILLO_10MM', 'MOTOR_ELECTRICO', 'CABLE_COBRE']
        proveedores = ['PROV-1', 'PROV-2', 'PROV-3']
        
        for i in range(cantidad_documentos):
            id_doc = f"4500{i:03d}"
            # Fechas aleatorias de los últimos 30 días
            fecha = (datetime.now() - timedelta(days=random.randint(0, 30))).strftime('%Y-%m-%d')
            prov = random.choice(proveedores)
            estado = random.choice(['LIBERADO', 'BLOQUEADO'])
            
            self.cursor.execute(
                "INSERT INTO cabeceras_compra VALUES (?, ?, ?, ?)", 
                (id_doc, fecha, prov, estado)
            )
            
            # Cada documento tendrá entre 1 y 3 posiciones
            for pos in range(1, random.randint(2, 4)):
                mat = random.choice(materiales)
                cant = random.randint(10, 1500)
                precio = round(random.uniform(5.5, 150.0), 2)
                
                self.cursor.execute(
                    "INSERT INTO posiciones_compra VALUES (?, ?, ?, ?, ?)", 
                    (id_doc, pos * 10, mat, cant, precio)
                )
                
        self.conn.commit()
        print(f"Se inyectaron {cantidad_documentos} documentos con sus posiciones.")

    def cerrar_conexion(self):
        self.conn.close()

# Ejecución de la clase
if __name__ == "__main__":
    db = ERPDatabaseBuilder()
    db.construir_esquema()
    db.inyectar_datos_masivos(50) # Inyectamos 50 documentos de prueba
    db.cerrar_conexion()