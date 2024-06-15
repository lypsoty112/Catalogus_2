import streamlit as st
from src.app import parse_documents

st.title('Creating a catalogus')

if files := st.file_uploader('Upload your word files here', type='docx', accept_multiple_files=True):
    df = None
    bar = st.progress(0, "Parsing docs")
    file_count = len(files)
    for n in parse_documents(files):
        if isinstance(n, int):
            bar.progress(int((n + 1) / file_count * 100))
        else:
            df = n

    st.dataframe(df)
