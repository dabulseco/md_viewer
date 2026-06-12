
import os
import tempfile

def convert_md_to_html(md_content):
    """Converts markdown string to HTML string."""
    import markdown
    # Using 'extra' and 'toc' extensions for a richer HTML output
    html = markdown.markdown(md_content, extensions=['extra', 'toc'])
    return html
