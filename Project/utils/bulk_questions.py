import streamlit as st
import os
import logging
from utils.chat_response import generate_response

OUTPUT_DIR = "output_results"
QUESTION_LIMIT = 30

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

"""Preprocess the uploaded questions file and limit the number of questions"""
def preprocess_questions(questions_file, limit=QUESTION_LIMIT):
    try:
        questions = questions_file.read().decode("utf-8").splitlines()
        processed_questions = [q.strip() for q in questions if q.strip()]
        
        if len(processed_questions) > limit:
            st.warning(f"The uploaded file contains more than {limit} questions. Only the top {limit} questions will be processed.")
            processed_questions = processed_questions[:limit]
        
        return processed_questions
    except Exception as e:
        logging.error(f"Error preprocessing questions: {e}")
        st.error("An error occurred while reading the questions file.")
        return []

"""Saves questions and answers to a file inside the output_results directory"""
def save_results_to_file(file_name, questions, responses):
    results_path = os.path.join(OUTPUT_DIR, file_name)
    try:
        with open(results_path, "w") as f:
            for idx, (question, response, sentence, response_time) in enumerate(responses):
                f.write(f"Q{idx+1}: {question}\n")
                f.write(f"Answer: {response}\n")
                f.write(f"Time spent: {response_time:.2f} seconds \n\n")
                # f.write(f"Extracted Sentence: {sentence}\n\n")
                
        return results_path
    except OSError as e:
        logging.error(f"Error saving results to file: {e}")
        st.error(f"Failed to save the results. Error: {e}")
        return None

"""Generates responses for uploaded questions and saves the results to a file"""
def handle_questions_responses(document_text, questions, result_file_name, display_progress):
    if not questions:
        st.warning("No valid questions found. Please provide a valid questions file.")
        return
    
    try:
        
        # Setting up progress bar
        progress_text = "Generating responses for the questions. Please wait..."
        my_bar = st.progress(0, text=progress_text)

        responses = []
        total_questions = len(questions)
        
        # Generating responses for each question
        for idx, question in enumerate(questions):
            answer, sentence, response_time = generate_response(question, document_text)
            responses.append((question, answer, sentence, response_time))

            # Updating progress bar after each response generation
            display_progress(my_bar, idx, total_questions, progress_text)
        
        # Removing progress bar after completion
        my_bar.empty()

        # Saving responses to file
        results_path = save_results_to_file(result_file_name, questions, responses)
        
        if results_path:
            with open(results_path, "r") as f:
                st.download_button(
                    label="Download Q&A Results",
                    data=f,
                    file_name=result_file_name,
                    mime="text/plain"
                )
        else:
            st.error("Failed to generate results file.")
    
    except Exception as e:
        logging.error(f"Error generating responses: {e}")
        st.error(f"Error generating responses: {e}")
