import os
from bs4 import BeautifulSoup

NAV_ID = "custom-navigation"

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
    nav_html = f'<nav id="{NAV_ID}" style="overflow-y:scroll; max-height:100vh;">\n'
    for item in html_files:
        nav_html += f'  <a href="{item["url"]}">{item["title"]}</a><br/>\n'
    nav_html += '</nav>\n'
    return nav_html

def check_and_update_navigation(base_dir, html_files, navigation_html):
    """Checks if the navigation is present and updates it only if necessary."""
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

        # Write the modified HTML back to the file
        with open(html_path, 'w', encoding='utf-8') as file:
            file.write(str(soup))

if __name__ == "__main__":
    base_dir = 'Rule Notebooks'
    
    # Step 1: Collect all HTML files
    html_files = collect_html_files(base_dir)
    
    # Step 2: Generate navigation HTML
    navigation_html = generate_navigation(html_files)
    
    # Step 3: Check and update navigation in each HTML file
    check_and_update_navigation(base_dir, html_files, navigation_html)
    
    print("Navigation update complete.")
