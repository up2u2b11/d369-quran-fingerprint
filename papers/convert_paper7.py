#!/usr/bin/env python3
"""Convert Paper VII markdown to PDF using weasyprint."""
import markdown
from weasyprint import HTML
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
md_path = os.path.join(script_dir, "d369_paper7_corrigendum_verification.md")
pdf_path = os.path.join(script_dir, "d369_paper7_corrigendum_verification.pdf")

with open(md_path, encoding="utf-8") as f:
    md_text = f.read()

html_body = markdown.markdown(md_text, extensions=["tables", "fenced_code"])

html_full = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<style>
@page {{
    size: A4;
    margin: 2.5cm 2cm;
    @bottom-center {{
        content: counter(page);
        font-size: 9pt;
        color: #666;
    }}
}}
body {{
    font-family: "Georgia", "Times New Roman", serif;
    font-size: 11pt;
    line-height: 1.6;
    color: #1a1a1a;
    max-width: 100%;
}}
h1 {{
    font-size: 18pt;
    text-align: center;
    margin-top: 1.5em;
    margin-bottom: 0.5em;
    page-break-before: auto;
    border-bottom: 2px solid #2c5282;
    padding-bottom: 0.3em;
}}
h2 {{
    font-size: 14pt;
    margin-top: 1.2em;
    color: #2c5282;
}}
h3 {{
    font-size: 12pt;
    margin-top: 1em;
    color: #2d3748;
}}
table {{
    border-collapse: collapse;
    width: 100%;
    margin: 1em 0;
    font-size: 10pt;
}}
th {{
    background-color: #2c5282;
    color: white;
    padding: 8px 10px;
    text-align: left;
    font-weight: bold;
}}
td {{
    border: 1px solid #cbd5e0;
    padding: 6px 10px;
}}
tr:nth-child(even) {{
    background-color: #f7fafc;
}}
blockquote {{
    border-left: 4px solid #2c5282;
    margin: 1em 0;
    padding: 0.5em 1em;
    background-color: #ebf8ff;
    font-style: italic;
    color: #2d3748;
}}
code {{
    background-color: #edf2f7;
    padding: 2px 5px;
    border-radius: 3px;
    font-family: "Courier New", monospace;
    font-size: 10pt;
}}
em {{
    font-style: italic;
}}
strong {{
    font-weight: bold;
}}
hr {{
    border: none;
    border-top: 1px solid #e2e8f0;
    margin: 1.5em 0;
}}
ul, ol {{
    margin-left: 1.5em;
}}
li {{
    margin-bottom: 0.3em;
}}
p {{
    text-align: justify;
}}
</style>
</head>
<body>
{html_body}
</body>
</html>"""

HTML(string=html_full).write_pdf(pdf_path)
print(f"PDF generated: {pdf_path}")
print(f"Size: {os.path.getsize(pdf_path):,} bytes")
