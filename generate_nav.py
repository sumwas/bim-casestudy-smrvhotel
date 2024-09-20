import os

def generate_navigation(base_dir):
    # Recursive function to build folder navigation
    def build_nav(dir_path):
        nav = '<ul>\n'
        for item in sorted(os.listdir(dir_path)):
            item_path = os.path.join(dir_path, item)
            # If it's a directory, create a dropdown
            if os.path.isdir(item_path):
                nav += f'<li><details><summary>{item}</summary>\n'
                nav += build_nav(item_path)  # Recursive call to add nested folders
                nav += '</details></li>\n'
            # If it's an HTML file, add a link
            elif item.endswith('.html'):
                relative_path = os.path.relpath(item_path, base_dir)
                nav += f'<li><a href="{relative_path}" target="content-frame">{item}</a></li>\n'
        nav += '</ul>\n'
        return nav

    # Start generating the HTML navigation file
    with open(os.path.join(base_dir, 'index.html'), 'w') as f:
        f.write('<!DOCTYPE html>\n<html>\n<head>\n<title>Notebook Navigation</title>\n')
        f.write('<style>\n')
        f.write('body { font-family: Arial, sans-serif; }\n')
        f.write('nav { position: fixed; top: 0; left: 0; width: 200px; height: 100%; overflow-y: auto; background-color: #f4f4f4; padding: 15px; }\n')
        f.write('nav ul { list-style-type: none; padding-left: 0; }\n')
        f.write('nav li { margin-bottom: 10px; }\n')
        f.write('nav a { text-decoration: none; color: #333; }\n')
        f.write('nav a:hover { background-color: #ddd; display: block; }\n')
        f.write('main { margin-left: 220px; padding: 20px; }\n')
        f.write('iframe { width: 100%; height: 90vh; border: none; }\n')
        f.write('</style>\n</head>\n<body>\n')
        
        # Write the navigation bar
        f.write('<nav>\n')
        f.write('<h2>Notebook Navigation</h2>\n')
        f.write(build_nav(base_dir))  # Generate folder structure
        f.write('</nav>\n')
        
        # Write the main content area where the HTML files will be loaded
        f.write('<main>\n')
        f.write('<iframe name="content-frame" src=""></iframe>\n')
        f.write('</main>\n')

        f.write('</body>\n</html>')

if __name__ == "__main__":
    generate_navigation('Rule Notebooks')

