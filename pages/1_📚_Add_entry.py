from src.database import Database
import streamlit as st

entry = {}

st.set_page_config(
    page_title="Add entry",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title('📚 Add Entry')


db  = Database()


def build_identifier_selector(identifier: dict) -> None:
    st.write(f"**{identifier['identifier']}**:" + " " + identifier["description"])
    if identifier["datatype"] == "str":
        entry[identifier['identifier']] = st.text_input(label=identifier["identifier"], label_visibility="collapsed")
    elif identifier["datatype"] == "int":
        entry[identifier['identifier']] = st.number_input(label=identifier["identifier"], label_visibility="collapsed", step=1)
    elif identifier["datatype"] == "float":
        entry[identifier['identifier']] = st.number_input(label=identifier["identifier"], label_visibility="collapsed", step=0.001)
    elif identifier["datatype"] == "bool":
        entry[identifier['identifier']] = st.checkbox(label=identifier["identifier"])
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
        print(entry)
        db.add_entry(entry, uploaded_file)
        st.toast("Added entry")
