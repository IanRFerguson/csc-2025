{{
    config(
        materialized='incremental',
        unique_key='player_id',
        incremental_strategy="merge",
    )
}}

WITH
    source_data AS (
        SELECT
            {{
                dbt_utils.star(
                    from=ref("stg_nba__player_data")
                )
            }}
        FROM {{ ref("stg_nba__player_data") }} AS source
        
        /* 
        When a full refresh is running, we'll only pull
        in data from the source table that is newer
        than the most recent record in the target table.
        */
        {% if is_incremental() %}
        WHERE source._transform_timestamp > (
            SELECT 
                MAX(target._transform_timestamp) 
            FROM {{ this }} AS target
        )
        {% endif %}
    )

SELECT * FROM source_data