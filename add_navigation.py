import os
from bs4 import BeautifulSoup

# Directory containing the HTML files
html_dir = "Rule Notebooks"

# Base URL for absolute links (update this to your website's base URL)
base_url = "/BIM-Casestudy/Rule%20Notebooks/"

# Function to extract the numerical part of the filename for sorting
def extract_numeric_part(filename):
    parts = filename.split('-')[0]
    try:
        return float(parts.replace('.', ''))
    except ValueError:
        return float('inf')  # In case the file doesn't start with a number, send it to the end

# Function to build the navigation structure
def build_navigation_structure(directory):
    nav_structure = {}
    
    for root, dirs, files in os.walk(directory):
        html_files = [f for f in files if f.endswith('.html') and f != 'index.html']  # Exclude index.html
        if html_files:
            # Sort HTML files numerically based on their filenames
            html_files = sorted(html_files, key=extract_numeric_part)
            
            # Get the chapter name from the folder structure
            path_parts = os.path.relpath(root, directory).split(os.sep)
            if len(path_parts) > 1:  # Ensure there's at least one chapter folder
                chapter = path_parts[0]  # Chapter folder name
                section = path_parts[1] if len(path_parts) > 1 else ""  # Section folder name
                
                # Initialize chapter in the nav structure if not already present
                if chapter not in nav_structure:
                    nav_structure[chapter] = {}
                
                # Add the section to the chapter
                if section not in nav_structure[chapter]:
                    nav_structure[chapter][section] = []
                
                # Append HTML files to the section
                nav_structure[chapter][section].extend(html_files)
    
    return nav_structure

# Function to generate navigation HTML with dropdowns based on the new structure
def generate_navigation_html(nav_structure):
    nav_html = '<nav>\n'
    
    # Add a Home link at the top of the navigation
    nav_html += f'<a href="{base_url}index.html">Home</a>\n'
    
    # Iterate over chapters and sections
    for chapter, sections in nav_structure.items():
        nav_html += f'<details>\n<summary>{chapter}</summary>\n'
        
        # Iterate over sections under the chapter
        for section, files in sections.items():
            nav_html += f'  <details>\n  <summary>{section}</summary>\n'
            
            # List files in the dropdown
            for file in files:
                # Create absolute URL from the base_url and the folder structure
                file_path = base_url + os.path.join(chapter, section, file).replace('\\', '/')
                display_name = file.replace('.html', '')
                nav_html += f'    <a href="{file_path}">{display_name}</a>\n'
            
            nav_html += '  </details>\n'  # Close the section dropdown
        
        nav_html += '</details>\n'  # Close the chapter dropdown
    
    nav_html += '</nav>\n'
    return nav_html

# Function to add navigation to all HTML files
def add_navigation():
    # Build the navigation structure
    nav_structure = build_navigation_structure(html_dir)
    
    # Generate the navigation HTML with dropdowns
    nav_html = generate_navigation_html(nav_structure)
    
    # Go through each file in the navigation structure and update the HTML
    for chapter, sections in nav_structure.items():
        for section, files in sections.items():
            for file in files:
                file_path = os.path.join(html_dir, chapter, section, file)
                
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
