import streamlit as st
import os
import sys

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

sys.path.append(BASE_DIR)

from db.database import init_db

from core.services import DocumentService

init_db()

service = DocumentService()

st.set_page_config(page_title="DocManager",layout="wide")

st.title("🗂️ Smart PDF Document Manager")

st.divider()

tabs = st.tabs(["Upload", "Search & View", "Analytics"])

with tabs[0]:
    st.header("Upload PDF")

    uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])
    tags = st.text_input("Tags (comma separated)")
    description = st.text_area("Description")
    lecture_date = st.date_input("Lecture Date (optional)", value=None)

    if st.button("Upload"):
        # if uploaded_file and tags and description:
        if uploaded_file:
            service.upload_document(uploaded_file, tags, description, lecture_date)
        else :
            st.error("Please upload a file")

with tabs[1]:
    # logic of Search & View
    pass

with tabs[2]:
    # logic of Analytics
    pass