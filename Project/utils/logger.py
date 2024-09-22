import logging

def setup_logger():
    logging.basicConfig(
        filename='chatbot_log.log',
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        filemode='w'  # 'w' to overwrite the log file on each run, use 'a' to append
    )
    print("Hello")

    logging.info("Logger initialized")

