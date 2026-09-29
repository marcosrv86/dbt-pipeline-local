{% macro categorizar_cantidad(columna_cantidad) %}
    CASE
        WHEN {{ columna_cantidad }} >= 1000 THEN 'Volumen Alto'
        WHEN {{ columna_cantidad }} >= 500 THEN 'Volumen Medio'
        ELSE 'Volumen Estándar'
    END
{% endmacro %} 