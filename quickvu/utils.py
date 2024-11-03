import logging

def setup_logger():
    """
    Sets up a logger for logging information, warnings, and errors.
    """
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    return logging.getLogger(__name__)

logger = setup_logger()
