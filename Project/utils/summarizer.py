import streamlit as st
import logging
import time
from transformers import T5Tokenizer, T5ForConditionalGeneration

"""Loads the T5 model for question answering globally"""
try:
    model = T5ForConditionalGeneration.from_pretrained("t5-base")
    tokenizer = T5Tokenizer.from_pretrained("t5-base")
except Exception as e:
    logging.error(f"Error loading T5 model or tokenizer: {e}")
    raise e

"""Summarizes the document using the T5 model."""
def summarize_document(document):
    try:
        # Preparing the input for the model
        input_text = f"summarize: {document}"
        input_ids = tokenizer.encode(input_text, return_tensors="pt")

        # Generating the summary using the model
        summary_ids = model.generate(
            input_ids,
            max_length=150,
            min_length=50,
            length_penalty=2.0,
            num_beams=4,
            early_stopping=True
        )

        # Decoding the summary into readable text
        summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
        return summary
    except Exception as e:
        logging.error(f"Summarization failed: {str(e)}")
        return "An error occurred during summarization."

"""Summarizes the uploaded document and logs the result."""
def summarize_uploaded_document(document_text):
    if not document_text or len(document_text.strip()) == 0:
        logging.warning("The uploaded document is empty or invalid.")
        return "The document is empty or invalid."

    try:
        with st.spinner('Summarizing the document...'):
            start_time = time.time()

            # Summarizing the document
            summary = summarize_document(document_text)

            # Calculating the time taken for summarization
            time_taken = time.time() - start_time
            logging.info(f"Document summarized in {time_taken:.2f} seconds.")
        return summary
    except Exception as e:
        logging.error(f"Error summarizing document: {str(e)}")
        return "An error occurred during summarization."

