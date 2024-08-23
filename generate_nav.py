import os

def generate_navigation(base_dir):
    nav_items = []

    # Walk through the directory and gather all HTML files
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.endswith('.html'):
                path = os.path.join(root, file)
                relative_path = os.path.relpath(path, base_dir)
                nav_items.append(relative_path)

    # Create the HTML navigation file
    with open(os.path.join(base_dir, 'index.html'), 'w') as f:
        f.write('<!DOCTYPE html>\n<html>\n<head>\n<title>Notebook Navigation</title>\n')
        f.write('<style>\n')
        f.write('body { font-family: Arial, sans-serif; }\n')
        f.write('nav { position: fixed; top: 0; left: 0; width: 200px; height: 100%; overflow-y: auto; background-color: #f4f4f4; padding: 15px; }\n')
        f.write('nav a { display: block; padding: 8px; text-decoration: none; color: #333; }\n')
        f.write('nav a:hover { background-color: #ddd; }\n')
        f.write('main { margin-left: 220px; padding: 20px; }\n')
        f.write('</style>\n</head>\n<body>\n')
        f.write('<nav>\n')
        for item in nav_items:
            f.write(f'<a href="{item}">{item}</a>\n')
        f.write('</nav>\n')
        f.write('<main>\n')
        f.write('<h1>Welcome to the Notebook Collection</h1>\n')
        f.write('</main>\n</body>\n</html>')

if __name__ == "__main__":
    generate_navigation('Rule Notebooks')
