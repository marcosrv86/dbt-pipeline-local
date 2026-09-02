SELECT 
    1 as id_cliente, 
    'Cliente A' as nombre,
    CURRENT_TIMESTAMP() as fecha_creacion
UNION ALL
SELECT 2, 'Cliente B', CURRENT_TIMESTAMP()