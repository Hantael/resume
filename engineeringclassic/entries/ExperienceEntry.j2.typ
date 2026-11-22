{% set date_parts = entry.date_and_location_column.splitlines()|map('trim')|reject('equalto', '')|list %}
{% set inline_date = date_parts|join(' ')|replace('(  ', '(')|replace('( ', '(')|replace('  )', ')')|replace(' )', ')') %}
{% set main_lines = entry.main_column.splitlines() %}
#regular-entry(
  [
    {{ main_lines[0]|indent(4) }}
  ],
  [
    {{ inline_date|indent(4) }}
  ],
  main-column-second-row: [
{% for line in main_lines[1:] %}
    {{ line|indent(4) }}

{% endfor %}
  ],
)
