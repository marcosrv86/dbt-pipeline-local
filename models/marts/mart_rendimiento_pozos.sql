{{ config(materialized='table') }}

WITH staging AS (
    SELECT * FROM {{ ref('stg_extraccion_diaria') }}
),

resumen_pozos AS (
    SELECT
        id_pozo,
        SUM(volumen_petroleo_m3) AS total_petroleo_m3,
        SUM(volumen_agua_m3) AS total_agua_m3,
        AVG(presion_psi) AS presion_promedio,
        COUNT(fecha_extraccion) AS dias_con_extraccion
    FROM staging
    GROUP BY 
        id_pozo
)

SELECT * FROM resumen_pozos