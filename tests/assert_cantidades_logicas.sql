-- Este test fallará si encuentra alguna cantidad ilógica en tu Data Mart final
SELECT
    id_documento,
    posicion,
    cantidad
FROM {{ ref('mart_compras_detalle') }}
WHERE cantidad <= 0