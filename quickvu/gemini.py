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