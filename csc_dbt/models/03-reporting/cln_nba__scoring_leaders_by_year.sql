WITH
    scorers AS (
        SELECT
            player_id,
            player_name,
            season_year AS year,
            team_initials,
            points,
            RANK() OVER (PARTITION BY team_initials, season_year ORDER BY points DESC) AS rank_by_team_and_year
        FROM {{ ref("stg_nba__player_data") }}
    )

SELECT
    * EXCEPT(rank_by_team_and_year)
FROM scorers
WHERE rank_by_team_and_year = 1
ORDER BY year, team_initials