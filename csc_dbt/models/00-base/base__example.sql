{{
    config(
        enabled=false
    )
}}

SELECT
    1 AS id,
    'Intro to dbt' AS session_name,
    'Learning a lot about dbt' AS current_status,

    -- Run the macro with default values
    {{ example_macro() }},

    -- Pass in values to override the defaults
    {{ 
        example_macro(
            message="Goodbye Friend", 
            column_name="happy_trails"
        ) 
    }}