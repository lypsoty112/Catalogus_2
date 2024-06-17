from docx import Document
from docx.oxml.ns import qn
from docx.opc.constants import RELATIONSHIP_TYPE
from docx.opc.part import Part
import io
import pandas as pd

def create_catalogus(sorted_data: pd.DataFrame):
    docs = sorted_data["file"].tolist()
    # Convert the file to a IO bytes object
    file = io.BytesIO(docs[0])
    merged_document = Document(docx=file)

    for index, file in enumerate(docs[1:]):
        # Convert the file to a IO bytes object
        file = io.BytesIO(file)
        sub_doc = Document(docx=file)

        # Ensure that we are not duplicating parts by keeping track of them
        part_map = {}

        for element in sub_doc.element.body:
            merged_document.element.body.append(element)

        # Handle media and other relationships
        for rel in sub_doc.part.rels.values():
            if "image" in rel.target_ref:
                # Get the image part
                image_part = rel.target_part
                image_data = io.BytesIO(image_part.blob)

                new_image_part = merged_document.part.package.get_or_add_image_part(image_data)
                # Add the relationship to the merged document
                merged_document.part.rels.add_relationship(
                    RELATIONSHIP_TYPE.IMAGE,
                    new_image_part,
                    rel.rId
                )
        # Don't add a page break if you've reached the last file.
        merged_document.add_page_break()
        merged_document.add_page_break()

    # Create a BytesIO object to store the merged document
    merged_document_bytes = io.BytesIO()
    
    # Save the merged document to the BytesIO object
    merged_document.save(merged_document_bytes)
    
    # Move the seek pointer to the beginning of the BytesIO object
    merged_document_bytes.seek(0)
    
    # Return the BytesIO object containing the merged document
    return merged_document_bytes
