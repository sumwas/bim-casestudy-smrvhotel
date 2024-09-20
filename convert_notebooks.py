import os
import subprocess

# Define the root folder where your notebooks are stored
notebooks_root = "Rule Notebooks"

# Walk through all directories and subdirectories
for root, dirs, files in os.walk(notebooks_root):
    for file in files:
        if file.endswith(".ipynb"):
            # Full path to the notebook
            notebook_path = os.path.join(root, file)
            
            # Directory where the notebook is located
            output_dir = root
            
            # Run nbconvert with the correct output directory
            subprocess.run([
                "jupyter", "nbconvert", 
                "--to", "html", 
                notebook_path, 
                "--output-dir", output_dir
            ])

print("Conversion completed.")

