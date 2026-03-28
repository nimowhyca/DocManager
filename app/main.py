import streamlit as st
import os
import sys

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

sys.path.append(BASE_DIR)

from db.database import init_db

from core.services import DocumentService


if "selected_doc" not in st.session_state:
    st.session_state.selected_doc = None

if "current_page" not in st.session_state:
    st.session_state.current_page = 0

if "search_results" not in st.session_state:
    st.session_state.search_results = []

if "reader_mode" not in st.session_state:
    st.session_state.reader_mode = False


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
    st.header("Search & View")

    col1, col2 = st.columns(2)

    with col1:
        search_tag = st.text_input("Search by Tag")

    with col2:
        search_date = st.date_input("Search by Date", value=None)

    if st.button("Search"):
        st.session_state.search_results = service.search_documents(
            tag=search_tag if search_tag else None,
            date=str(search_date) if search_date else None
        )

    # TASK

    results = st.session_state.search_results

    if results and not st.session_state.reader_mode:
        st.subheader(f"Results: {len(results)} documents")
        container = st.container(height=500)

        with container:
            for doc in results:
                # doc --> obj of Document from models.py
                col1, col2 = st.columns([1, 3])
                # 4 -> 25% left, 75% right

                with col1:
                    if doc.thumbnail_path:
                        st.image(doc.thumbnail_path, width=120)

                with col2:
                    st.write(f"**{doc.name}**")
                    st.write(f"Tags: {doc.tags}")
                    st.write(f"Description: {doc.description}")
                    st.write(f"Lecture Date: {doc.lecture_date}")

                    if st.button("Open",key=f"open_{doc.id}"):
                        st.session_state.selected_doc = doc
                        st.session_state.current_page = 0
                        st.session_state.reader_mode = True
                        st.rerun()

    if st.session_state.reader_mode and st.session_state.selected_doc:
        st.write("Reader Mode Active")

        doc = st.session_state.selected_doc

        st.subheader(f"📖 Reading: {doc.name}")

        # 20260328121602_25_03_2026_notes
        folder_name = os.path.basename(doc.path).replace(".pdf", "")
        image_dir = f"storage/pdfs/{folder_name}"

        st.write("Image dir:", image_dir)
        st.write("Files:", os.listdir(image_dir) if os.path.exists(image_dir) else "NOT FOUND")

        if not os.path.exists(image_dir):
            st.error("Images not found. PDF conversion failed.")
        else:
            images = sorted(os.listdir(image_dir))

            # total_pages = len(images)
            total_pages = doc.total_pages
            current_page = st.session_state.current_page

            col1, col2, col3 = st.columns([1, 2, 1])

            with col1:
                if st.button("⬅ Previous") and current_page > 0:
                    st.session_state.current_page -= 1
                    st.rerun()

            with col3:
                if st.button("Next ➡") and current_page < total_pages - 1:
                    st.session_state.current_page += 1
                    st.rerun()

            img_path = os.path.join(image_dir, images[st.session_state.current_page])
            st.image(img_path, width="stretch")

            st.write(f"FILE : {doc.name}")






with tabs[2]:
    # logic of Analytics
    pass