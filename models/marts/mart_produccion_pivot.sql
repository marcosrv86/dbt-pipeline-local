SELECT
  id_pozo,
  
  -- La macro pivot escanea la tabla fct_produccion_pozos, encuentra todas las 
  -- provincias únicas y construye las columnas dinámicamente sumando los barriles.
  {{ dbt_utils.pivot(
      'provincia',
      dbt_utils.get_column_values(ref('fct_produccion_pozos'), 'provincia'),
      then_value='total_barriles'
  ) }}

FROM {{ ref('fct_produccion_pozos') }}
GROUP BY id_pozo