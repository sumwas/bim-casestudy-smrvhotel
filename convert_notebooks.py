import os
import nbformat
from nbconvert import HTMLExporter
from nbconvert.preprocessors import ExecutePreprocessor

def collect_notebooks(base_dir):
    notebooks = []
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.endswith('.ipynb'):
                path = os.path.join(root, file)
                relative_path = os.path.relpath(path, base_dir)
                notebooks.append({
                    'url': relative_path.replace(os.path.sep, '/'),
                    'title': file
                })
    return notebooks

def convert_notebooks_to_html(base_dir, notebooks, template_file):
    html_exporter = HTMLExporter(template_file=template_file)
    for notebook in notebooks:
        nb_path = os.path.join(base_dir, notebook['url'])
        with open(nb_path, 'r', encoding='utf-8') as f:
            nb = nbformat.read(f, as_version=4)
            body, resources = html_exporter.from_notebook_node(nb)
            html_file = nb_path.replace('.ipynb', '.html')
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(body)

if __name__ == "__main__":
    base_dir = 'Rule Notebooks'
    template_dir = "jupyter_templates"
    notebooks = collect_notebooks(base_dir)
    convert_notebooks_to_html(template_dir, notebooks, 'custom_template.tpl')
