from src.database import Database
import streamlit as st
import os

entry = {}
TOTAL_DOCS: int = 165
DONE_DOCS_FOLDER: os.PathLike = "./data/Superrigardo medailles en uitleg/doing/done"

st.set_page_config(
    page_title="Add entry",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title('📚 Add Entry')


db  = Database()

def display_status():
    # Load the number of word documents in the folder
    pct_progress = len(os.listdir(DONE_DOCS_FOLDER)) / TOTAL_DOCS
    st.progress(text=f"Upload progess: **{pct_progress * 100:.2f}%**", value=pct_progress)


def build_identifier_selector(identifier: dict) -> None:
    st.write(f"**{identifier['identifier']}**:" + " " + identifier["description"])
    if identifier["datatype"] == "str":
        entry[identifier['identifier']] = st.text_input(label=identifier["identifier"], label_visibility="collapsed")
    elif identifier["datatype"] == "int":
        entry[identifier['identifier']] = st.number_input(label=identifier["identifier"], label_visibility="collapsed", step=1, value=-1)
    elif identifier["datatype"] == "float":
        entry[identifier['identifier']] = st.number_input(label=identifier["identifier"], label_visibility="collapsed", step=0.001 , value=-1.0)
    elif identifier["datatype"] == "bool":
        entry[identifier['identifier']] = st.checkbox(label=identifier["identifier"])
# Add a form for adding an entry


display_status()
with st.form("add_entry_form", clear_on_submit=True):
    st.write("Enter the details of the new entry:")

    for identifier in db.get_identifiers():
        build_identifier_selector(identifier)

    # Add a file upload widget to accept 1 docx file
    uploaded_file = st.file_uploader("Upload the corresponding entry's docx file", type=["docx"])
    if uploaded_file is not None:
        st.write("File uploaded successfully")

    if st.form_submit_button(label="Add Entry"):
        print(entry)
        db.add_entry(entry, uploaded_file)
        st.toast("Added entry")
