from docx import Document
from docx.opc.constants import RELATIONSHIP_TYPE
import io
import pandas as pd

def create_catalogus(sorted_data: pd.DataFrame):
    # Extract file paths from the DataFrame
    docs = sorted_data["file"].tolist()
    # Convert the first file to a IO bytes object
    file = io.BytesIO(docs[0])
    # Create a new Document object from the first file
    merged_document = Document(docx=file)

    # Iterate over the remaining documents to merge them
    for index, file in enumerate(docs[1:]):
        # Convert the current file to a IO bytes object
        file = io.BytesIO(file)
        # Create a Document object for the current file
        sub_doc = Document(docx=file)

        # Append all elements from the body of the sub-document to the merged document
        for element in sub_doc.element.body:
            merged_document.element.body.append(element)

        # Handle media and other relationships from the sub-document
        for rel in sub_doc.part.rels.values():
            if "image" in rel.target_ref:
                # Get the image part from the relationship
                image_part = rel.target_part
                # Read the image data into a BytesIO object
                image_data = io.BytesIO(image_part.blob)

                # Add or get the image part in the merged document's package
                new_image_part = merged_document.part.package.get_or_add_image_part(image_data)
                # Add the relationship for the new image part in the merged document
                merged_document.part.rels.add_relationship(
                    RELATIONSHIP_TYPE.IMAGE,
                    new_image_part,
                    rel.rId
                )

    # Create a BytesIO object to store the merged document
    merged_document_bytes = io.BytesIO()
    
    # Save the merged document to the BytesIO object
    merged_document.save(merged_document_bytes)
    
    # Move the seek pointer to the beginning of the BytesIO object for reading
    merged_document_bytes.seek(0)
    
    # Return the BytesIO object containing the merged document
    return merged_document_bytes
