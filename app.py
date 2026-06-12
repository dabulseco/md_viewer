
import os
import streamlit as st
import markdown
from converters.markdown_html import convert_md_to_html
from converters.markdown_docx import convert_md_to_docx

st.set_page_config(page_title=".md View", layout="wide")

st.title(".md View")
st.markdown("Upload and preview your Markdown files, and export them to HTML or DOCX.")

# Sidebar for file uploads
st.sidebar.header("Upload Files")
uploaded_files = st.sidebar.file_uploader(
    "Choose .md files",
    type="md",
    accept_multiple_files=True
)

# Main area
if uploaded_files:
    # Create a dictionary to store file contents
    file_contents = {}
    for uploaded_file in uploaded_files:
        # Read and decode the content
        content = uploaded_file.read().decode("utf-8")
        file_contents[uploaded_file.name] = content

    st.sidebar.divider()
    st.sidebar.header("Export Settings")

    selected_files = st.sidebar.multiselect(
        "Select files to export",
        options=list(file_contents.keys())
    )

    export_format = st.sidebar.selectbox(
        "Export Format",
        options=["HTML", "DOCX"]
    )

    if st.sidebar.button("Generate Exports") and selected_files:
        # We use a container to hold the download buttons so they don't disappear
        # when the app reruns after interaction
        export_container = st.sidebar.container()
        for file_name in selected_files:
            content = file_contents[file_name]
            if export_format == "HTML":
                html_content = convert_md_to_html(content)
                export_container.download_button(
                    label=f"Download {file_name} (HTML)",
                    data=html_content,
                    file_name=f"{os.path.splitext(file_name)[0]}.html",
                    mime="text/html",
                    key=f"dl_html_{file_name}"
                )
            else:
                try:
                    docx_bytes = convert_md_to_docx(content)
                    export_container.download_button(
                        label=f"Download {file_name} (DOCX)",
                        data=docx_bytes,
                        file_name=f"{os.path.splitext(file_name)[0]}.docx",
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                        key=f"dl_docx_{file_name}"
                    )
                except Exception as e:
                    export_container.error(f"Error converting {file_name}: {e}")

    st.divider()
    st.header("Preview")

    # Display previews
    for file_name, content in file_contents.items():
        with st.expander(f"Preview: {file_name}", expanded=True):
            html_preview = convert_md_to_html(content)
            # Note: st.markdown is usually better for simple MD preview in Streamlit,
            # but using HTML allows us to show the exact rendered HTML output.
            st.markdown(html_preview, unsafe_allow_html=True)

else:
    st.info("Please upload some .md files in the sidebar to get started.")
