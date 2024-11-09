import streamlit as st

# Set up the page title and layout for the Home page
st.set_page_config(page_title="Home - QuickVu", layout="wide")

# Custom styles for the homepage
st.markdown("""
    <style>
    body {
        background-color: #FFFFFF;
    }
    .main-header { 
        color: #0b78ee; 
        font-size: 34px; 
        font-weight: 700;
        text-align: left;
        margin-bottom: 20px;
    }
    .sub-header { 
        color: #0b78ee;
        font-size: 24px; 
        font-weight: 600; 
        margin: 20px 0;
    }
    .side-header {
        color: #0b78ee;
        font-size: 18px;
        font-weight: bold;
        margin-bottom: 10px;
    }
    .section-divider {
        border-top: 2px solid #0b78ee;
        margin: 30px 0;
    }
    .instructions {
        font-size: 16px;
        color: #0b78ee;
        margin-bottom: 10px;
    }
    .warning-message {
        color: #0b78ee;
        font-size: 16px;
        font-weight: 500;
        margin: 10px 0;
    }
    .github-section {
        margin-top: 30px;
    }
    .github-img {
        border-radius: 50%;
        width: 120px;
        height: 120px;
        margin-top: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# Main header for the homepage
st.markdown("<h1 class='main-header'>Welcome to QuickVU!</h1>", unsafe_allow_html=True)

# Description of the app
st.markdown("""
Quick VU (Quick Visual Understanding) is an easy-to-use tool for data preparation, analysis, and visualization. It helps you clean, explore, and visualize your data without coding.

Just upload your data, choose your analysis, and Quick VU will guide you through the process.

Use the navigation on the left to explore the tools, or start here:
""")

# Explanation of features and tools
st.markdown("""
### Tools & Features
QuickVu provides several powerful features to streamline your data analysis workflow:

- **Data Preparation via QuickPrep**: Easily clean and preprocess your data before analysis.
- **Data Analysis via QuickGlance**: Use built-in analytics tools to perform various statistical analyses on your datasets.
  
These tools are accessible through the navigation menu on the left side. Explore them by clicking on the options and see how QuickVu can help you streamline your analysis process.
""")

st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
# Section for About Me and GitHub profile
st.markdown("<h2 class='sub-header'>About Me</h2>", unsafe_allow_html=True)

# Adding GitHub profile picture and personal info
col1, col2 = st.columns([0.4, 3])

with col1:
    # Replace the URL with the link to your GitHub profile picture
    st.image("https://avatars.githubusercontent.com/u/115421661?s=400&u=1a6a50ca45e66782ac203da4481f297c7441b206&v=4", caption="My GitHub Profile", width=120, output_format='png')

with col2:
    st.markdown("""
    Hi, I'm [Asif Sayyed](https://github.com/Asifdotexe)!  
    I'm a data science student working on this project to simplify the data analysis process. My goal is to create an easy-to-use tool for those who need to quickly clean and analyze data, whether you're a beginner or just looking for a more efficient way to handle your data.

    If you'd like to learn more about data analysis or this project, feel free to reach out—I'd be happy to help!
    """)

# Additional section or footer if necessary

st.markdown("""
    For any feedback or inquiries, feel free to reach out via my GitHub or email.  
    Happy analyzing!
""")
