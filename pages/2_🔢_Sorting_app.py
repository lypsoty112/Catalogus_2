import streamlit as st
from src.database import Database
from src.merge import create_catalogus

# Set the page configuration
st.set_page_config(
    page_title="Sorting app",
    page_icon="🔢",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title('🔢 Sorting app')

# Initialize session state for sorted data, download button visibility, and front page
if 'sorted_data' not in st.session_state:
    # Load data only if it is not already sorted
    db = Database()
    data = db.get_data()
    st.session_state.sorted_data = data

if 'show_download_button' not in st.session_state:
    st.session_state.show_download_button = False

if 'front_page' not in st.session_state:
    st.session_state.front_page = None

# Columns to hide
invisible_columns = ["_id", "file"]

# Display the data in a placeholder
placeholder = st.empty()
placeholder.dataframe(st.session_state.sorted_data.drop(columns=invisible_columns))

with st.form("sort_form"):
    st.write("Sort the data:")
    sort_columns = st.multiselect("Sort by", st.session_state.sorted_data.columns)
    sort_orders = []
    for col in sort_columns:
        sort_order = st.checkbox(f"Descending for {col}", value=False, key=f"sort_order_{col}")
        sort_orders.append(not sort_order)

    if st.form_submit_button(label="Sort"):
        if sort_columns:
            # Sort the data and update session state
            st.session_state.sorted_data = st.session_state.sorted_data.sort_values(
                by=sort_columns, ascending=sort_orders
            )
            placeholder.dataframe(st.session_state.sorted_data.drop(columns=invisible_columns))
            st.toast("Data sorted")
            st.session_state.show_download_button = False  # Hide download button until "Prepare for Download" is clicked
        else:
            st.warning("Please select at least one column to sort by.")

# Upload a front page document (Word)
uploaded_file = st.file_uploader(
    "Upload a front page document (Word file)", type=["docx"]
)

if uploaded_file is not None:
    st.session_state.front_page = uploaded_file
    st.success("Front page uploaded successfully.")

# Button to show the download option
if st.button("Prepare for Download"):
    st.session_state.show_download_button = True


# Show download button only if "Prepare for Download" has been clicked
if st.session_state.show_download_button:
    try:
        # Pass the uploaded front page if available
        sorted_data_document = create_catalogus(
            st.session_state.sorted_data,
            front_page=st.session_state.front_page
        )
        st.download_button(
            label="Download sorted data",
            data=sorted_data_document,
            file_name="Katalogo-de-Esperanto-Medaljonoj-Moneroj.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        )
    except Exception as e:
        st.error(f"An error occurred: {e}")
