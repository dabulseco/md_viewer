
import pypandoc
import tempfile
import os

def convert_md_to_docx(md_content):
    """
    Converts markdown string to docx bytes.
    Note: Requires pandoc to be installed on the system.
    """
    try:
        # Create a temporary file to hold the markdown content
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as tmp_md:
            tmp_md.write(md_content)
            tmp_md_path = tmp_md.name

        # Create a temporary directory for the output docx
        with tempfile.TemporaryDirectory() as tmp_dir:
            docx_path = os.path.join(tmp_dir, "output.docx")

            # Convert the markdown file to docx
            pypandoc.convert_file(tmp_md_path, 'docx', outputfile=docx_path)

            # Read the resulting docx bytes
            with open(docx_path, 'rb') as f:
                docx_bytes = f.read()

        # Clean up the temporary markdown file
        if os.path.exists(tmp_md_path):
            os.remove(tmp_md_path)

        return docx_bytes
    except Exception as e:
        raise RuntimeError(f"DOCX conversion failed: {str(e)}. Ensure pandoc is installed.")
