{{
    config(
        tags=["nba", "base"]
    )
}}

WITH
    base AS (
        SELECT 
            {{
                dbt_utils.star(
                    from=source("csc_main", "nba_player_data"),
                )
            }},
            CURRENT_TIMESTAMP() AS _transform_timestamp
        FROM {{ source('csc_main', 'nba_player_data') }}
    )

SELECT * FROM base