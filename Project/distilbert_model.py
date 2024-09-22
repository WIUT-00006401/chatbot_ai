import streamlit as st
from transformers import pipeline, AutoTokenizer
import os
import time

# Setting up the question-answering pipeline using the DistilBERT model
model_name = "distilbert-base-cased-distilled-squad"
qa_pipeline = pipeline("question-answering", model=model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

# Function to save results to a text file
def save_results_to_file(results, folder="output_results"):
    # Ensure the results folder exists
    if not os.path.exists(folder):
        os.makedirs(folder)
    
    # Generating a filename with a timestamp
    filename = f"{folder}/distilbert_results.txt"
    
    # Writing the results to the file
    with open(filename, "w") as f:
        for i, result in enumerate(results):
            f.write(f"Q{i+1}: {result['question']}\n")
            f.write(f"Answer: {result['answer']}\n")
            f.write(f"Time Spent: {result['time_spent']:.2f} seconds\n\n")
    
    return filename

# Main Streamlit app
def main():
    st.title("Document-based Q&A System with DistilBERT")

    # File uploader to upload a document (only .txt)
    uploaded_file = st.file_uploader("Upload a Text file", type=["txt"])

    if uploaded_file is not None:
        # Reading text from uploaded .txt file
        document_text = str(uploaded_file.read(), "utf-8")

        if document_text:
            st.write("### Document Text (Preview):")
            st.write(document_text[:1000] + "...")

            # Input for multiple questions
            questions_input = st.text_area("Enter your questions (one per line):")

            if st.button("Generate Answers"):
                if questions_input:
                    questions = questions_input.strip().split("\n")

                    # List to store results
                    results = []

                    # Perform Q&A for each question and measure time
                    for question in questions:
                        start_time = time.time()  # Start time

                        result = qa_pipeline({
                            'context': document_text,
                            'question': question
                        })

                        end_time = time.time()  # End time

                        # Calculating time spent for generating the answer
                        time_spent = end_time - start_time


                        results.append({
                            'question': question,
                            'answer': result['answer'],
                            'time_spent': time_spent
                        })

                    # Displaying the answers and token counts
                    st.write("### Answers, Tokens, and Time Spent:")
                    for i, result in enumerate(results):
                        st.write(f"**Q{i+1}:** {result['question']}")
                        st.write(f"**Answer:** {result['answer']}")
                        st.write(f"**Time Spent:** {result['time_spent']:.2f} seconds")
                        st.write("---")

                    # Saving the results to a file
                    saved_file = save_results_to_file(results)
                    st.success(f"Results saved to {saved_file}")
                else:
                    st.warning("Please enter at least one question.")
        else:
            st.write("No text could be extracted from the file.")
    else:
        st.write("Please upload a document to proceed.")

if __name__ == "__main__":
    main()
