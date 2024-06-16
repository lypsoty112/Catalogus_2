from src.database import Database
import streamlit as st

st.set_page_config(
    page_title="Add identifier",
    page_icon="🔑",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title('🔑 Add Identifier')

db = Database()

# Add a form for adding an identifier
with st.form("add_identifier_form"):
    st.write("Enter the details of the new identifier:")
    identifier = st.text_input("Identifier")
    description = st.text_area("Description")
    datatype = st.selectbox("Datatype", ["str", "int", "float", "bool"])
    if st.form_submit_button(label="Add Identifier"):
        try:
            db.add_identifier(identifier, description, datatype)
            st.toast(f"Added identifier: {identifier}")
        except Exception as e:
            st.error(str(e))