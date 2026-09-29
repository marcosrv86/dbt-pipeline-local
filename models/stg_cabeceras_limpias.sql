WITH origen AS (
    SELECT * FROM {{ source('raw_data', 'raw_cabeceras_compra') }}
)

SELECT 
    id_documento,
    fecha_creacion,
    -- Llamamos a la macro y le pasamos una lista con las columnas a limpiar
    {{ limpiar_columnas_texto(['id_proveedor', 'estado_liberacion']) }}

FROM origen