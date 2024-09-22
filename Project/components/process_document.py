import streamlit as st
from utils.file_handler import handle_uploaded_file
from utils.chat_response import validate_token_length

"""Handles document upload and token length validation."""
def process_document(uploaded_file):
    file_type = uploaded_file.name.split('.')[-1].lower()
    document_text = handle_uploaded_file(uploaded_file, file_type)

    if document_text:
        # Validating the document token length
        is_valid_document, document_token_count = validate_token_length(document_text, max_tokens=7000)
        if not is_valid_document:
            st.error(f"Maximum token limit for the document has exceeded (Current: {document_token_count} tokens). Please adjust the document.")
            return None, None
        return document_text, document_token_count
    return None, None
