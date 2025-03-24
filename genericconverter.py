import os
import re
from bs4 import BeautifulSoup
import nbformat as nbf

# Get user input for file paths
input_html = input("Enter the path to the HTML file to convert: ").strip()
output_ipynb = input("Enter the output notebook filename: ").strip()

# Ensure output has .ipynb extension
if not output_ipynb.endswith('.ipynb'):
    output_ipynb += '.ipynb'

#Must type .html at end of file name
# Verify input file exists
if not os.path.exists(input_html):
    print(f"Error: File '{input_html}' not found")
    exit()

print(f"Converting: {input_html} -> {output_ipynb}")

# Load the HTML file
with open(input_html, "r", encoding="utf-8") as file:
    html_content = file.read()

soup = BeautifulSoup(html_content, "html.parser")

# Create a new notebook
nb = nbf.v4.new_notebook()

#uncomment if you want to add phrases to remove
# # Define the target phrase to filter (for code cells)
# PHRASE_TO_REMOVE1 = """''' Code Removed - Student to include appropriate code to:
# (1) address all tasks (2) produce similar results (3) and answer all questions
# '''"""

# # additional code to remove BOTH phrases
# PHRASE_TO_REMOVE2 = """''' Code Removed - Student to include appropriate code to: IMPORT and
# (1) address all tasks (2) produce similar results (3) and answer all questions
# '''"""

cells = []

# Iterate over notebook cell containers in order
for cell in soup.select("div.jp-Notebook-cell"):
    # Check for a code cell by looking for a <pre> tag inside the cell input wrapper
    code_wrapper = cell.select_one("div.jp-Cell-inputWrapper")
    if code_wrapper:
        pre_tag = code_wrapper.find("pre")
        if pre_tag:
            code_content = pre_tag.get_text()
            
        
            #uncomment if you want to add phrases to remove
            # Remove the target phrases from the code content
            # cleaned_content = code_content.replace(PHRASE_TO_REMOVE1, "").replace(PHRASE_TO_REMOVE2, "")
            # cells.append(nbf.v4.new_code_cell(cleaned_content))

            cells.append(nbf.v4.new_code_cell(code_content)) #comment this line if you uncomment the lines above
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