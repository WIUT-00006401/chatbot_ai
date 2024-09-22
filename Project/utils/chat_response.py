
import logging
import spacy
import time
from transformers import T5Tokenizer, T5ForConditionalGeneration

"""Loads the SpaCy model for sentence segmentation globally"""
try:
    nlp = spacy.load("en_core_web_sm")
except Exception as e:
    logging.error(f"Error loading SpaCy model: {e}")
    raise e

"""Loads the T5 model for question answering globally"""
try:
    model = T5ForConditionalGeneration.from_pretrained("t5-base")
    tokenizer = T5Tokenizer.from_pretrained("t5-base")
except Exception as e:
    logging.error(f"Error loading T5 model or tokenizer: {e}")
    raise e

"""Validates the number of tokens in the text based on max_tokens limit."""
def validate_token_length(text, max_tokens):
    input_ids = tokenizer.encode(text, return_tensors="pt")
    num_tokens = len(input_ids[0])
    return num_tokens <= max_tokens, num_tokens

"""Generates an answer based on the document and the question."""
def generate_answer(document, question, max_length=300):
    input_text = f"question: {question} context: {document}"
    input_ids = tokenizer.encode(input_text, return_tensors="pt")

    try:
        output = model.generate(input_ids, max_length=max_length)
        answer = tokenizer.decode(output[0], skip_special_tokens=True)
        return answer
    except Exception as e:
        logging.error(f"Error generating answer: {e}")
        raise e

"""Extracts the sentence that contains the generated answer using SpaCy."""
def extract_sentence_with_spacy(document, answer):
    doc = nlp(document)
    for sentence in doc.sents:
        if answer.strip().lower() in sentence.text.strip().lower():
            return sentence.text
    return "No specific sentence found."

"""Generates the response and finds the sentence with the answer."""
def generate_response(question, document_text):
    logging.info(f"Processing question: {question}")

    # Validating the question token length (20 tokens limit)
    is_valid_question, question_token_count = validate_token_length(question, max_tokens=20)
    if not is_valid_question:
        logging.warning(f"Question exceeds token limit (Current: {question_token_count} tokens)")
        return f"Question exceeds 20 token limit (Current: {question_token_count} tokens)", "N/A", 0

    try:
        start_time = time.time()

        # Generating the answer using T5
        answer = generate_answer(document_text, question)
        
        # Extracting the sentence that contains the answer
        sentence = extract_sentence_with_spacy(document_text, answer)

        # Calculating response time
        response_time = time.time() - start_time

        logging.info(f"Generated Answer: {answer}")
        logging.info(f"Extracted Sentence: {sentence}")
        logging.info(f"Response Time: {response_time:.2f} seconds")

        return answer, sentence, response_time
    except Exception as e:
        logging.error(f"Error during processing: {e}")
        return "Sorry, I couldn't process the question.", "N/A", 0
