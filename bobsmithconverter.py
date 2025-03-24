import os
import re
#can be installed with pip, in my case already installed when this script is open through anaconda virtual environment
from bs4 import BeautifulSoup
import nbformat as nbf

# Find HTML file with 'BOB_SMITH' in the name
html_files = [f for f in os.listdir() if f.endswith('.html') and 'BOB_SMITH' in f]

if not html_files:
    print("Error: No HTML files with 'BOB_SMITH' in name found in current directory.")
    exit()
elif len(html_files) > 1:
    print(f"Multiple BOB_SMITH HTML files found. Using first match: {html_files[0]}")

input_html = html_files[0]
print(f"Found target file: {input_html}")

# Generate output filename by removing the "BOB_SMITH" prefix from the base name
base_name = os.path.splitext(input_html)[0]
output_ipynb = re.sub(r'^BOB_SMITH_?', '', base_name) + '.ipynb'

# Load the HTML file
with open(input_html, "r", encoding="utf-8") as file:
    html_content = file.read()

soup = BeautifulSoup(html_content, "html.parser")

# Create a new notebook
nb = nbf.v4.new_notebook()

# Define the target phrase to filter (for code cells)
PHRASE_TO_REMOVE1 = """''' Code Removed - Student to include appropriate code to:
(1) address all tasks (2) produce similar results (3) and answer all questions
'''"""

# additional code to remove BOTH phrases
PHRASE_TO_REMOVE2 = """''' Code Removed - Student to include appropriate code to: IMPORT and
(1) address all tasks (2) produce similar results (3) and answer all questions
'''"""

cells = []

# Iterate over notebook cell containers in order
for cell in soup.select("div.jp-Notebook-cell"):
    # Check for a code cell by looking for a <pre> tag inside the cell input wrapper
    code_wrapper = cell.select_one("div.jp-Cell-inputWrapper")
    if code_wrapper:
        pre_tag = code_wrapper.find("pre")
        if pre_tag:
            code_content = pre_tag.get_text()
            # Remove the target phrases from the code content
            cleaned_content = code_content.replace(PHRASE_TO_REMOVE1, "").replace(PHRASE_TO_REMOVE2, "")
            cells.append(nbf.v4.new_code_cell(cleaned_content))
            continue  # Process the next cell

    # Check for a markdown cell by looking for the rendered markdown div with the proper mime type
    md_div = cell.select_one("div.jp-RenderedHTMLCommon[data-mime-type='text/markdown']")
    if md_div:
        # Process header tags to insert corresponding markdown header syntax.
        for header_tag in md_div.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
            level = int(header_tag.name[1])
            # Remove the anchor link, if present
            anchor = header_tag.find("a", class_="anchor-link")
            if anchor:
                anchor.decompose()
            header_text = header_tag.get_text(strip=True)
            markdown_header = "#" * level + " " + header_text
            header_tag.replace_with(markdown_header)
        md_content = md_div.get_text()
        cells.append(nbf.v4.new_markdown_cell(md_content))
        continue

# Assign the ordered cells to the notebook
nb.cells = cells

# Save the new notebook with the generated filename
with open(output_ipynb, "w", encoding="utf-8") as file:
    nbf.write(nb, file)

print(f"Created clean notebook: {output_ipynb}")