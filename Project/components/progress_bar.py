import streamlit as st

"""Updates the progress bar based on current progress."""
def display_progress(my_bar, current_idx, total_questions, progress_text):
    progress_percent = int(((current_idx + 1) / total_questions) * 100)
    my_bar.progress(progress_percent, text=progress_text)


