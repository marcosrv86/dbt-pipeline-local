{% macro convertir_barriles_a_m3(nombre_columna) %}
    
    ROUND(({{ nombre_columna }} * 0.158987), 2)

{% endmacro %}