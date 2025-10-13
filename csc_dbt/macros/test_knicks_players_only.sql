{% test knicks_players_only(model, target_column="team_initials")  %}
    SELECT
        *
    FROM {{ model }}
    WHERE {{ target_column }} != 'NYK'
{% endtest %}