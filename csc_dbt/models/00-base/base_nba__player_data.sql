{{
    config(
        tags=["nba", "base"],
        cluster_by=["team_initials"],
        materialized='table',
        partition_by={
            "field": "_transform_timestamp",
            "data_type": "timestamp",
            "granularity": "day"
        }
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