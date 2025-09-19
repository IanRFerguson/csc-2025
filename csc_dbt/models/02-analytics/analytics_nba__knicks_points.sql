WITH
    knicks_players AS (
        SELECT 
            {{
                dbt_utils.star(
                    from=ref("stg_nba__knicks_players"),
                )
            }}
        FROM {{ ref('stg_nba__knicks_players') }}
    ),

    predicted_points AS (
        SELECT
            player_id,
            predicted_points
        FROM {{ ref("analytics_nba__player_points") }}
    ),

    staging AS (
        SELECT
            kp.player_id,
            kp.player_name,
            kp.season_year AS year,
            kp.points,
            pp.predicted_points
        FROM knicks_players AS kp
        LEFT JOIN predicted_points AS pp USING(player_id)
    )

SELECT
    player_id,
    player_name,
    year,
    points,
    predicted_points,
    CASE
        WHEN points > predicted_points THEN 'PLUS'
        WHEN points < predicted_points THEN 'MINUS'
        ELSE 'MEETS'
    END AS performance_vs_prediction
FROM staging
