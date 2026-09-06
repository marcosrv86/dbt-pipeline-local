{{ config(materialized='view') }}

WITH source AS (
    SELECT * FROM {{ source('sistema_origen_raw', 'fct_extraccion_diaria') }}
),

renamed AS (
    SELECT
        id_pozo,
        -- Aseguramos el casteo correcto de fechas
        CAST(fecha_extraccion AS DATE) AS fecha_extraccion,
        volumen_petroleo_m3,
        volumen_agua_m3,
        presion_psi,
        bomba_activa,
        estado_operativo
    FROM source
)

SELECT * FROM renamed