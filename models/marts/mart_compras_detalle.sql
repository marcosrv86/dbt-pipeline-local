{{
    config(
        materialized='incremental',
        unique_key='id_documento' 
    )
}}
WITH cabeceras AS (
    SELECT 
        id_documento,
        fecha_creacion,
        id_proveedor
    FROM {{ source('raw_data', 'raw_cabeceras_compra') }}
-- Lógica incremental: Solo se ejecuta si la tabla ya existe y no es un full-refresh
    {% if is_incremental() %}
        -- Filtramos trayendo solo los registros cuya fecha sea mayor a la última procesada
        WHERE fecha_creacion > (SELECT MAX(fecha_creacion) FROM {{ this }})
    {% endif %}
),

posiciones AS (
    SELECT 
        id_documento,
        posicion,
        material,
        cantidad
    FROM {{ source('raw_data', 'raw_posiciones_compra') }}
)

SELECT 
    -- Datos de la cabecera (se repetirán por cada posición, esto es normal en OLAP)
    c.fecha_creacion,
    c.id_proveedor,
    
    -- Datos de la posición
    p.id_documento,
    p.posicion,
    p.material,
    p.cantidad,
    
    -- Mapeo condicional simple
    CASE 
        WHEN p.cantidad > 1000 THEN 'Volumen Alto'
        ELSE 'Volumen Estándar'
    END AS categoria_volumen

FROM cabeceras c
INNER JOIN posiciones p 
    ON c.id_documento = p.id_documento