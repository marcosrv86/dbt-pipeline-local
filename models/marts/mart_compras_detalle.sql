{{
    config(
        materialized='incremental',
        unique_key='id_transaccion_sk',
        partition_by={
            "field": "fecha_creacion",
            "data_type": "date",
            "granularity": "day"
        }
    )
}}

WITH cabeceras AS (
    SELECT * FROM {{ source('raw_data', 'raw_cabeceras_compra') }}
),

posiciones AS (
    SELECT * FROM {{ source('raw_data', 'raw_posiciones_compra') }}
)

SELECT 
    {{ dbt_utils.generate_surrogate_key(['c.id_documento', 'p.posicion']) }} AS id_transaccion_sk,
    c.id_documento,
    CAST(c.fecha_creacion AS DATE) AS fecha_creacion, -- Aseguramos que sea tipo DATE para la partición
    c.id_proveedor,
    p.posicion,
    p.material,
    p.cantidad,
    -- Aquí llamamos a nuestra función Jinja:
    {{ categorizar_cantidad('p.cantidad') }} AS categoria_volumen

FROM cabeceras c
JOIN posiciones p ON c.id_documento = p.id_documento

{% if is_incremental() %}
    WHERE CAST(c.fecha_creacion AS DATE) >= (SELECT max(fecha_creacion) FROM {{ this }})
{% endif %}