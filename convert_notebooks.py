import os
import nbformat
from nbconvert import HTMLExporter
from pathlib import Path

def get_notebooks(base_path):
    notebooks = []
    for root, dirs, files in os.walk(base_path):
        for file in files:
            if file.endswith('.ipynb'):
                notebooks.append(Path(root) / file)
    return notebooks

def create_navigation(notebooks):
    chapters = {}
    for notebook in notebooks:
        relative_path = notebook.relative_to(base_path)
        parts = relative_path.parts
        url = f'{relative_path.with_suffix(".html")}'
        title = parts[-1].replace('.ipynb', '')
        
        # Navigate through the hierarchy
        if len(parts) == 3:
            chapter, section, subsection = parts[0], parts[1], title
            if chapter not in chapters:
                chapters[chapter] = {'title': chapter, 'url': f'{chapter}.html', 'sections': {}}
            if section not in chapters[chapter]['sections']:
                chapters[chapter]['sections'][section] = {'title': section, 'url': f'{section}.html', 'subsections': {}}
            chapters[chapter]['sections'][section]['subsections'][subsection] = {'title': title, 'url': url}
        elif len(parts) == 2:
            chapter, section = parts[0], title
            if chapter not in chapters:
                chapters[chapter] = {'title': chapter, 'url': f'{chapter}.html', 'sections': {}}
            chapters[chapter]['sections'][section] = {'title': section, 'url': url, 'subsections': {}}
        elif len(parts) == 1:
            chapter = title
            chapters[chapter] = {'title': chapter, 'url': f'{chapter}.html'}
            
    return chapters

def convert_notebooks_to_html(notebooks, chapters):
    html_exporter = HTMLExporter(template_file='jupyter_templates/custom_template.tpl')
    for notebook in notebooks:
        with open(notebook) as f:
            nb = nbformat.read(f, as_version=4)
            body, resources = html_exporter.from_notebook_node(nb)
            html_file = f"{notebook.with_suffix('.html')}"
            with open(html_file, 'w') as f:
                f.write(body)
    
    with open('index.html', 'w') as f:
        f.write("<html><body><nav><ul>")
        for chapter, data in chapters.items():
            f.write(f"<li><a href='{data['url']}'>{data['title']}</a>")
            if 'sections' in data:
                f.write("<ul>")
                for section, sec_data in data['sections'].items():
                    f.write(f"<li><a href='{sec_data['url']}'>{sec_data['title']}</a>")
                    if 'subsections' in sec_data:
                        f.write("<ul>")
                        for subsection, sub_data in sec_data['subsections'].items():
                            f.write(f"<li><a href='{sub_data['url']}'>{sub_data['title']}</a></li>")
                        f.write("</ul>")
                    f.write("</li>")
                f.write("</ul>")
            f.write("</li>")
        f.write("</ul></nav></body></html>")

base_path = 'Rule Notebooks'
notebooks = get_notebooks(base_path)
chapters = create_navigation(notebooks)
convert_notebooks_to_html(notebooks, chapters)
