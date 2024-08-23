import os
from bs4 import BeautifulSoup

NAV_ID = "custom-navigation"
STYLE_ID = "custom-styles"

def collect_html_files(base_dir):
    """Collects all HTML files in the given base directory."""
    html_files = []
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.endswith('.html'):
                path = os.path.join(root, file)
                relative_path = os.path.relpath(path, base_dir)
                html_files.append({
                    'url': relative_path.replace(os.path.sep, '/'),
                    'title': file.replace('.html', '')
                })
    return html_files

def generate_navigation(html_files):
    """Generates the HTML for the navigation menu."""
    nav_html = f'<nav id="{NAV_ID}" style="overflow-y:scroll; max-height:100vh; width: 200px; position: fixed; left: 0; top: 0; background-color: #f8f9fa; padding: 10px;">\n'
    for item in html_files:
        nav_html += f'  <a href="{item["url"]}" style="display: block; margin-bottom: 5px;">{item["title"]}</a>\n'
    nav_html += '</nav>\n'
    return nav_html

def generate_styles():
    """Generates the CSS styles for the navigation and content layout."""
    styles = f'''
    <style id="{STYLE_ID}">
    body {{
        margin-left: 220px;
        font-family: Arial, sans-serif;
    }}
    nav a {{
        color: #007bff;
        text-decoration: none;
    }}
    nav a:hover {{
        text-decoration: underline;
    }}
    </style>
    '''
    return styles

def check_and_update_navigation_and_styles(base_dir, html_files, navigation_html, styles_html):
    """Checks if the navigation and styles are present and updates them only if necessary."""
    for item in html_files:
        html_path = os.path.join(base_dir, item['url'])
        with open(html_path, 'r', encoding='utf-8') as file:
            soup = BeautifulSoup(file, 'html.parser')

            # Find the current navigation menu by ID
            current_nav = soup.find('nav', id=NAV_ID)

            # If navigation is missing or different, update it
            if not current_nav or str(current_nav) != navigation_html:
                print(f"Updating navigation in: {item['url']}")

                # If a navigation exists, replace it. Otherwise, insert a new one.
                if current_nav:
                    current_nav.replace_with(BeautifulSoup(navigation_html, 'html.parser'))
                else:
                    body_tag = soup.body
                    if body_tag:
                        body_tag.insert(0, BeautifulSoup(navigation_html, 'html.parser'))

            # Find or add custom styles
            current_styles = soup.find('style', id=STYLE_ID)
            if not current_styles or str(current_styles) != styles_html:
                print(f"Updating styles in: {item['url']}")

                if current_styles:
                    current_styles.replace_with(BeautifulSoup(styles_html, 'html.parser'))
                else:
                    head_tag = soup.head
                    if head_tag:
                        head_tag.append(BeautifulSoup(styles_html, 'html.parser'))

        # Write the modified HTML back to the file
        with open(html_path, 'w', encoding='utf-8') as file:
            file.write(str(soup))

if __name__ == "__main__":
    base_dir = 'Rule Notebooks'
    
    # Step 1: Collect all HTML files
    html_files = collect_html_files(base_dir)
    
    # Step 2: Generate navigation HTML
    navigation_html = generate_navigation(html_files)
    
    # Step 3: Generate CSS styles
    styles_html = generate_styles()
    
    # Step 4: Check and update navigation and styles in each HTML file
    check_and_update_navigation_and_styles(base_dir, html_files, navigation_html, styles_html)
    
    print("Navigation and styles update complete.")
