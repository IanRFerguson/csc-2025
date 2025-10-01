{{
    config(
        enabled=false
    )
}}

-- Start with a list of values we want to loop over
{% set MY_VALUES=[
    "D.C.", 
    "RICHMOND", 
    "SAN FRANCISCO", 
    "ATLANTA", 
    "MILWAUKEE", 
    "BROOKLYN"] %}

-- Loop over the values in MY_VALUES
{% for value in MY_VALUES %}
    SELECT
        /*
            We can access each value as a string, as well
            as the index associated with the value in the array.
        */
        {{ loop.index }} AS id,
        '{{ value }}' AS city

-- As long as there's another value after the current value in the array,
-- we'll union it together with the next SELECT statement.
{% if not loop.last %}
    UNION ALL
{% endif %}

{% endfor %}