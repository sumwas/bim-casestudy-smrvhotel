import os
from bs4 import BeautifulSoup

# Directory containing the HTML files
html_dir = "Rule Notebooks"

# Function to extract the numerical part of the filename for sorting
def extract_numeric_part(filename):
    parts = filename.split('-')[0]
    try:
        # Replace '.' with an empty string and convert to float for proper sorting
        return float(parts.replace('.', ''))
    except ValueError:
        return float('inf')  # In case the file doesn't start with a number, send it to the end

# Function to add navigation to all HTML files
def add_navigation():
    # Gather all the HTML files
    html_files = [f for f in os.listdir(html_dir) if f.endswith('.html')]
    
    # Sort files numerically based on their filenames
    html_files = sorted(html_files, key=extract_numeric_part)

    # Create the navigation bar HTML
    nav_html = '<nav>\n'
    for file in html_files:
        file_path = os.path.join(html_dir, file)
        display_name = file.replace('.html', '')
        nav_html += f'<a href="{file}">{display_name}</a>\n'
    nav_html += '</nav>\n'

    # Add navigation to each HTML file
    for file in html_files:
        file_path = os.path.join(html_dir, file)
        
        # Open the HTML file
        with open(file_path, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f, 'html.parser')
        
        # Check if navigation already exists and update it
        if soup.nav:
            soup.nav.replace_with(BeautifulSoup(nav_html, 'html.parser'))
        else:
            # Insert navigation in the body tag
            soup.body.insert(0, BeautifulSoup(nav_html, 'html.parser'))

        # Add CSS styling (can be customized as needed)
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

