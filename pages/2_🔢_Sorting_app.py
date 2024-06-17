import streamlit as st
from src.database import Database
from src.merge import create_catalogus

st.set_page_config(
    page_title="Sorting app",
    page_icon="🔢",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title('🔢 Sorting app')

# Get the data from the database 
db = Database()
data = db.get_data()

invisible_columns = ["_id", "file"]

# Display the data in a placeholder
placeholder = st.empty()
placeholder.dataframe(data.drop(columns=invisible_columns))


with st.form("sort_form"):
    st.write("Sort the data:")
    sort_columns = st.multiselect("Sort by", data.columns)
    sort_orders = []
    for col in sort_columns:
        sort_order = st.checkbox(f"Descending for {col}", value=False, key=f"sort_order_{col}")
        sort_orders.append(not sort_order)

    if st.form_submit_button(label="Sort"):
        if sort_columns:
            data = data.sort_values(by=sort_columns, ascending=sort_orders)
            placeholder.dataframe(data.drop(columns=invisible_columns))
            st.toast("Data sorted")
        else:
            st.warning("Please select at least one column to sort by.")


st.download_button(
    label="Download sorted data",
    data=create_catalogus(data),
    file_name="sorted_data.docx",
    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
)