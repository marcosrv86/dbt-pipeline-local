{% snapshot compras_posiciones_snapshot %}

{{
    config(
      target_schema='snapshots',
      unique_key='id_documento || "-" || posicion',
      strategy='check',
      check_cols=['cantidad', 'material'],
    )
}}

SELECT * 
FROM {{ source('raw_data', 'raw_posiciones_compra') }}

{% endsnapshot %}