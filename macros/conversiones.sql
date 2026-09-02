{% macro barriles_a_m3(nombre_columna) %}
    
    -- Esta función multiplica la columna de entrada por el factor de conversión
    ROUND( {{ nombre_columna }} * 0.158987, 2 )
    
{% endmacro %}