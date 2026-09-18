{% macro calcular_z_score(columna) %}
    ( {{ columna }} - AVG({{ columna }}) OVER() ) 
    / NULLIF(STDDEV({{ columna }}) OVER(), 0)
{% endmacro %}
