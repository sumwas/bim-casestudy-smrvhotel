import os
from bs4 import BeautifulSoup

# Directory containing the HTML files
html_dir = "Rule Notebooks"

# Function to extract the numerical part of the filename for sorting
def extract_numeric_part(filename):
    parts = filename.split('-')[0]
    try:
        return float(parts.replace('.', ''))
    except ValueError:
        return float('inf')  # In case the file doesn't start with a number, send it to the end

# Function to recursively scan folders and add HTML files to the navigation structure
def build_navigation_structure(directory):
    nav_structure = {}
    
    for root, dirs, files in os.walk(directory):
        html_files = [f for f in files if f.endswith('.html')]
        if html_files:
            # Sort HTML files numerically based on their filenames
            html_files = sorted(html_files, key=extract_numeric_part)
            
            # Create a relative path from the root folder
            relative_path = os.path.relpath(root, html_dir)
            
            # Add an entry in the navigation structure for this folder
            nav_structure[relative_path] = html_files
    
    return nav_structure

# Function to generate navigation HTML with dropdowns based on folder structure
def generate_navigation_html(nav_structure):
    nav_html = '<nav>\n'
    
    # Iterate over folders (chapters/sections)
    for folder, files in nav_structure.items():
        folder_name = folder.split('/')[-1]  # Get the last part of the folder path for display
        nav_html += f'<details>\n<summary>{folder_name}</summary>\n'
        
        # List files in the dropdown
        for file in files:
            file_path = os.path.join(folder, file).replace('\\', '/')
            display_name = file.replace('.html', '')
            nav_html += f'<a href="{file_path}">{display_name}</a>\n'
        
        nav_html += '</details>\n'
    
    nav_html += '</nav>\n'
    return nav_html

# Function to add navigation to all HTML files
def add_navigation():
    # Build the navigation structure
    nav_structure = build_navigation_structure(html_dir)
    
    # Generate the navigation HTML with dropdowns
    nav_html = generate_navigation_html(nav_structure)
    
    # Go through each file in the navigation structure and update the HTML
    for folder, files in nav_structure.items():
        for file in files:
            file_path = os.path.join(html_dir, folder, file)
            
            # Open the HTML file
            with open(file_path, 'r', encoding='utf-8') as f:
                soup = BeautifulSoup(f, 'html.parser')
            
            # Check if navigation already exists and update it
            if soup.nav:
                soup.nav.replace_with(BeautifulSoup(nav_html, 'html.parser'))
            else:
                # Insert navigation in the body tag
                soup.body.insert(0, BeautifulSoup(nav_html, 'html.parser'))
            
            # Add CSS styling for the dropdowns
            style_tag = soup.new_tag('style')
            style_tag.string = """
            nav {
                width: 200px;
                position: fixed;
                left: 0;
                top: 0;
                bottom: 0;
                background-color: #f4f4f4;
                padding: 20px;
                overflow-y: auto;
            }
            nav a {
                display: block;
                padding: 8px;
                text-decoration: none;
                color: #333;
            }
            nav a:hover {
                background-color: #ddd;
            }
            details summary {
                cursor: pointer;
                font-weight: bold;
                margin-bottom: 8px;
            }
            body {
                margin-left: 220px; /* Make space for the fixed nav */
            }
            """
            soup.head.append(style_tag)
            
            # Write the updated HTML back to the file
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(str(soup))

# Execute the function
add_navigation()
