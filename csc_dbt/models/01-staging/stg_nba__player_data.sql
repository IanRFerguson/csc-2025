{{
    config(
        tags=["staging"],
    )
}}

WITH
    base AS (
        SELECT
        
            CAST(Rk AS INT64) AS rank,
            Player AS player_name,
            Age AS age,
            Pos AS position,
            G AS games_played,
            GS AS games_started,
            MP AS minutes_played,
            FG AS field_goals,
            FGA AS field_goals_attempted,
            `FG%` AS field_goal_percentage,
            `3P` AS three_point_field_goals,
            `3PA` AS three_point_field_goals_attempted,
            `3P%` AS three_point_field_goal_percentage,
            `2P` AS two_point_field_goals,
            `2PA` AS two_point_field_goals_attempted,
            `2P%` AS two_point_field_goal_percentage,
            `eFG%` AS effective_field_goal_percentage,
            FT AS free_throws,
            FTA AS free_throws_attempted,
            `FT%` AS free_throw_percentage,
            ORB AS offensive_rebounds,
            DRB AS defensive_rebounds,
            TRB AS total_rebounds,
            AST AS assists,
            STL AS steals,
            BLK AS blocks,
            TOV AS turnovers,
            PF AS personal_fouls,
            PTS AS points,
            Awards AS awards,
            year AS season_year,
            team_initials AS team_initials,
            etl_load_date,
            _transform_timestamp

        FROM {{ ref('base_nba__player_data') }}
    ),

    additional_fields AS (
        SELECT
            *,
            {{
                dbt_utils.generate_surrogate_key(
                    [
                        'player_name',
                        'season_year',
                        'team_initials'
                    ]
                )
            }} AS player_id
        FROM base
    )

SELECT 
    * 
FROM additional_fields
WHERE player_name != 'Team Totals'