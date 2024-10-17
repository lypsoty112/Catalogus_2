import io
from typing import List
import pandas as pd
from docx import Document
from docx.shared import Inches
from docx.enum.section import WD_SECTION
from docxcompose.composer import Composer
import streamlit as st

def create_catalogus(sorted_data: pd.DataFrame, front_page) -> bytes:
    # Extract file contents from the DataFrame
    docs: List[bytes] = sorted_data["file"].tolist()

    front_page_bytes = front_page.getvalue()

    # Initialize progress bar
    progress_bar = st.progress(0)
    total_docs = len(docs)

    # Create a new Document object from the first file
    with io.BytesIO(front_page_bytes) as first_doc:
        master = Document(first_doc)
    composer = Composer(master)

    # Loop through remaining documents and append them to the master document
    for index, doc_bytes in enumerate(docs, start=0):
        # Create a Document object from bytes
        with io.BytesIO(doc_bytes) as doc_stream:
            doc2 = Document(doc_stream)
        
        # Add a page break before appending the new document
        master.add_page_break()
        
        # Append the document to the master
        composer.append(doc2)

        # Update progress bar
        progress_bar.progress(index / total_docs)

    # Save the final combined document to a bytes object
    output_bytes = io.BytesIO()
    master.save(output_bytes)
    output_bytes.seek(0)

    return output_bytes.getvalue()