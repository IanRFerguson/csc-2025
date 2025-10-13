{% macro datetime_to_date(value) %}
    DATE({{ value }})
{% endmacro %}


