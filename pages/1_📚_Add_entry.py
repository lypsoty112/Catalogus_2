from src.database import Database
import streamlit as st

st.set_page_config(
    page_title="Add entry",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title('📚 Add Entry')


db  = Database()


def build_identifier_selector(identifier: dict) -> None:
    if identifier["datatype"] == "str":
        st.write(f"**{identifier['identifier']}**:" + " " + identifier["description"])
        st.text_input(label=identifier["identifier"], label_visibility="collapsed")

# Add a form for adding an entry
with st.form("add_entry_form"):
    st.write("Enter the details of the new entry:")

    for identifier in db.get_identifiers():
        build_identifier_selector(identifier)

    # Add a file upload widget to accept 1 docx file
    uploaded_file = st.file_uploader("Upload the corresponding entry's docx file", type=["docx"])
    if uploaded_file is not None:
        st.write("File uploaded successfully")

    if st.form_submit_button(label="Add Entry"):
        st.toast("Added entry") # TODO: Implement the logic to add the entry to the database