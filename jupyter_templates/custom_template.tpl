{%- extends 'basic.tpl' -%}
{%- block header -%}
<header>
  <nav>
    <ul>
      {% for chapter in chapters %}
        <li><a href="{{ chapter.url }}">{{ chapter.title }}</a>
          {% if chapter.sections %}
            <ul>
              {% for section in chapter.sections %}
                <li><a href="{{ section.url }}">{{ section.title }}</a>
                  {% if section.subsections %}
                    <ul>
                      {% for subsection in section.subsections %}
                        <li><a href="{{ subsection.url }}">{{ subsection.title }}</a></li>
                      {% endfor %}
                    </ul>
                  {% endif %}
                </li>
              {% endfor %}
            </ul>
          {% endif %}
        </li>
      {% endfor %}
    </ul>
  </nav>
</header>
{%- endblock header -%}
