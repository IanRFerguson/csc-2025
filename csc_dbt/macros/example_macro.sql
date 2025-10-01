


{% macro example_macro(message="Hello Stranger", column_name="salutation") %}
    '{{ message }}' AS {{ column_name }}
{% endmacro %}


