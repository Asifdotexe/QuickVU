"""
This is the streamlit UI for the QuickChat module that allows users to
chat with their data
"""

import streamlit as st
import pandas as pd
from transformers import pipeline

# Load the TAPAS table-question-answering pipeline
pipe = pipeline("table-question-answering",
                model="google/tapas-large-finetuned-wtq")

# Streamlit UI
st.title("Table Question Answering with TAPAS")
st.write("Upload your table data and ask questions about it!")

# File upload section
uploaded_file = st.file_uploader("Upload a CSV or Excel file", type=["csv", "xlsx"])

if uploaded_file is not None:
    # Read the uploaded file as a DataFrame
    if uploaded_file.name.endswith('.csv'):
        table = pd.read_csv(uploaded_file)
    elif uploaded_file.name.endswith('.xlsx'):
        table = pd.read_excel(uploaded_file)

    table = table.astype(str)

    # Display the table
    st.write("Uploaded Table:", table)

    # User input for question
    question = st.text_input("Enter your question about the table:")

    if question:
        # Use the pipeline to get the answer
        result = pipe(table=table, query=question)

        # Display the answer
        st.write(f"Answer: {result['answer']}")
