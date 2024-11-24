import os
import json
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
    """
    Suggests three machine learning models tailored to the given use case.

    :param usecase: A string describing the specific use case for which machine learning models need to be suggested.
    :return: A list of dictionaries, where each dictionary contains a model name and the reason for its recommendation.
    """
    prompt = (
        f"Suggest me 3 best machine learning models for the following usecase:\n"
        f"{usecase}\n"
        f"just return the name of the model and why is it better in the following situation?\n"
        f"do not return any boilerplate text, just the text and reason.\n"
        f"Return the output in '|' delimited format: 'model | reason | model | reason | model | reason'."
        f"Only recommend machine learning models that can be quickly imported from popular machine learning libraries"
    )
    try:
        response = gemini_model.generate_content(prompt)
        text = response.text.strip('|').strip()  # Remove trailing and leading pipes or spaces

        # Split the response into parts
        parts = [part.strip() for part in text.split('|') if part.strip()]
        
        # Ensure valid format
        if len(parts) % 2 != 0:
            raise ValueError(f"Response format is invalid. Response text: {text}")
        if len(parts) < 6:  # Ensure at least 3 models with reasons
            raise ValueError(f"Expected at least 6 parts (3 models and reasons), but got {len(parts)}: {text}")

        # Extract models and reasons in pairs
        recommendations = [
            {'model': parts[i].strip(), 'reason': parts[i + 1].strip()} for i in range(0, len(parts), 2)
        ]

        # Return only the first 3 pairs
        return recommendations[:3]
    except Exception as e:
        return f"Error: {str(e)}"