WITH calculo_estadistico AS (
    SELECT 
        id_venta,
        fecha,
        producto,
        monto,
        -- Invocamos la macro de Jinja compilando el SQL dinámico
        {{ calcular_z_score('monto') }} AS z_score_monto
    FROM {{ source('raw_data', 'tbl_ventas') }}
)

SELECT 
    *,
    -- Aplicamos la regla del umbral de Machine Learning
    CASE 
        WHEN z_score_monto > 3 OR z_score_monto < -3 THEN 'Anomalía Detectada'
        ELSE 'Normal'
    END AS flag_outlier
FROM calculo_estadistico