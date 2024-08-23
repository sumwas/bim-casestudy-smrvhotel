{%- extends 'full.tpl' -%}
{%- block header -%}
<header>
  <nav>
    <ul>
      {% for item in navigation %}
        <li><a href="{{ item.url }}">{{ item.title }}</a></li>
      {% endfor %}
    </ul>
  </nav>
</header>
{%- endblock header -%}

{%- block body -%}
<main>
  {{ super() }}
</main>
{%- endblock body -%}
