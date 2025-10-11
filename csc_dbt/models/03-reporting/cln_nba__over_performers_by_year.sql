WITH
    players AS (
        SELECT
            player_id,
            player_name,
            position,
            team_initials,
            season_year,
            awards
        FROM {{ ref("stg_nba__player_data") }}
    ),

    predicted_points AS (
        SELECT
            player_id,
            (predicted_points - points) AS points_delta
        FROM {{ ref("analytics_nba__player_points") }}
    )

SELECT
    season_year,
    team_initials,
    player_name,
    position,
    points_delta,
    awards
FROM players
INNER JOIN predicted_points USING(player_id)
QUALIFY ROW_NUMBER() OVER (PARTITION BY season_year ORDER BY points_delta DESC) = 1
ORDER BY season_year