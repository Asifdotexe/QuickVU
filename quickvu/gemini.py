import os
from dotenv import load_dotenv
import google.generativeai as genai

def configure_gemini():
    """
    Load API key from .env file and configure the Gemini model.
    :return: A configured Gemini model instance.
    """
    load_dotenv()

    # Check if API key is loaded
    api_key = os.getenv('GEMINI_API_KEY')
    if api_key is None:
        raise ValueError("API_KEY not found! Please check your .env file.")
    
    # Configure and return Gemini model
    genai.configure(api_key=api_key)
    return genai.GenerativeModel('gemini-1.5-flash')

gemini_model = configure_gemini()


def explain_correlation_matrix(corr_matrix):
    """
    Fetch an explanation for a correlation matrix from the Gemini API.
    
    :param corr_matrix: A string representation of the correlation matrix.
    :return: Explanation text from the Gemini model.
    """
    prompt = f""""Please interpret the correlation matrix in detail, 
                explaining the relationships between the variables in a clear and concise manner. 
                Avoid using symbols like asterisks or double asterisks for formatting. 
                Focus on providing a human-readable explanation that is easy to understand:\n{corr_matrix}\n"""
    try:
        response = gemini_model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"
    
def which_model(usecase: str):
    """Suggests three machine learning models tailored to the given use case.
    
    :param usecase: A string describing the specific use case for which machine learning models need to be suggested
    """
    prompt = f"""Suggest me 3 best machine learning models for the following usecase: \n
    {usecase} \n just return the name of the model and why is it better in the following situation?
    do not return any boilerplate text, just the text and reason """
    try:
        response = gemini_model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"