{{ config(materialized='view') }}

SELECT 
    id_lote AS id_pozo,
    fecha_cosecha AS fecha_medicion,
    toneladas_netas AS barriles_extraidos,
    hectareas_sembradas AS horas_operacion,
    -- Calculamos la tasa de extracción (flow rate)
    (toneladas_netas / hectareas_sembradas) AS barriles_por_hora
FROM 
    {{ source('sistema_origen', 'cosecha_2026') }}