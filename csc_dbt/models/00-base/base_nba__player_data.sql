WITH
    base AS (
        SELECT 
            *,
            CURRENT_TIMESTAMP() AS _transform_timestamp
        FROM {{ source('csc_main', 'nba_player_data') }}
    )

SELECT * FROM base