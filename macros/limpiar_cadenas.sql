{% macro limpiar_columnas_texto(lista_columnas) %}
    
    {% for columna in lista_columnas %}
        TRIM(UPPER({{ columna }})) AS {{ columna }}_limpio
        
        {# Agregamos una coma si no es el último elemento de la lista #}
        {% if not loop.last %}
            ,
        {% endif %}
    {% endfor %}

{% endmacro %}