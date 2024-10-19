#!/usr/bin/env python3

import sys
import os
import re
import hashlib

# Check for the correct number of arguments
if len(sys.argv) < 3:
    sys.stderr.write("Usage: ./markdown2html.py README.md README.html\n")
    sys.exit(1)

input_file = sys.argv[1]
output_file = sys.argv[2]

# Check if the Markdown file exists
if not os.path.exists(input_file):
    sys.stderr.write(f"Missing {input_file}\n")
    sys.exit(1)

# Open the input file and read its content
with open(input_file, 'r') as markdown_file:
    markdown_content = markdown_file.readlines()

html_content = []
in_unordered_list = False
in_ordered_list = False

# Helper function to close lists
def close_lists():
    global in_unordered_list, in_ordered_list
    if in_unordered_list:
        html_content.append("</ul>\n")
        in_unordered_list = False
    if in_ordered_list:
        html_content.append("</ol>\n")
        in_ordered_list = False

# Process each line of the markdown content
for line in markdown_content:
    line = line.rstrip()
    
    # Parse Headings
    if line.startswith('#'):
        heading_level = len(line.split(' ')[0])  # Number of '#' symbols
        content = line.strip('#').strip()  # Heading text content
        html_content.append(f"<h{heading_level}>{content}</h{heading_level}>\n")
        close_lists()
    
    # Parse Unordered List
    elif line.startswith('- '):
        if not in_unordered_list:
            html_content.append("<ul>\n")
            in_unordered_list = True
        content = line[2:].strip()  # Get the list item text
        html_content.append(f"<li>{content}</li>\n")
    
    # Parse Ordered List
    elif line.startswith('* '):
        if not in_ordered_list:
            html_content.append("<ol>\n")
            in_ordered_list = True
        content = line[2:].strip()  # Get the list item text
        html_content.append(f"<li>{content}</li>\n")
    
    else:
        close_lists()
        # Replace bold and emphasis syntax
        line = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', line)  # Bold
        line = re.sub(r'__(.*?)__', r'<em>\1</em>', line)  # Emphasis
        
        # Parse special ((...)) and [[...]] syntax
        if '((' in line and '))' in line:
            content = re.sub(r'[cC]', '', line.strip('((').strip('))'))  # Remove all 'c' and 'C'
            html_content.append(f"<p>{content}</p>\n")
        elif '[[' in line and ']]' in line:
            md5_hash = hashlib.md5(line.strip('[[').strip(']]').encode()).hexdigest()
            html_content.append(f"<p>{md5_hash}</p>\n")
        elif line:  # Simple paragraph
            html_content.append(f"<p>{line}</p>\n")
        else:
            html_content.append("<br/>\n")  # Line break

# Ensure lists are closed at the end
close_lists()

# Write the processed HTML content to the output file
with open(output_file, 'w') as html_file:
    html_file.writelines(html_content)

sys.exit(0)
