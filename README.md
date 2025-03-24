## Description
These .py files convert specified .html files into .ipynb files, by creating new cells with the matching markdown content and code content, and ignoring cell output from html file.

## Developement process
Most of the code in this project was written using Deepseek AI, and repeatedly tailoring the results to meet my objectives.

## Why
I made this project because I was unable to find an easy to use program that did the following how I wanted to.
**if anybody is aware of existing programs or methods that perform the same functionality please let me know, or send me an email.


## Versions
1. `bobsmith-converter` branch/tag: Specialized for BOB_SMITH prefixed files
2. `generic-converter` branch: Handles any Jupyter HTML export

## Usage
```bash
# For original version
git checkout BobsmithConverter
python bobsmithconverter.py

# For generic version
git checkout GenericConverter
python genericconverter.py