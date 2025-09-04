{{
    config(
        materialized='view',
        tags=['staging'],
    )
}}

WITH
    base AS (
        SELECT * FROM {{ ref("stg_nba__player_data") }} 
        WHERE team_initials = 'NYK'
    )

SELECT * FROM base