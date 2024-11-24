import streamlit as st
from quickvu import gemini

with open('app_pages/styles.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

st.markdown('<h1 class="main-header">🔍 Quick Select: Model Selection</h1>', unsafe_allow_html=True)

st.markdown("""
Quick Glance is a data analysis tool that provides summary statistics, visualizes correlations, and generates quick plots to give you a better understanding of your data.
""")

st.sidebar.image('./dataset/logo-png.png', use_container_width=True)

usecase = st.text_area("Describe your use case here:")

if st.button("Show suggestions"):
    if usecase.strip():
        suggestions = gemini.which_model(usecase)
        
        if isinstance(suggestions, str) and suggestions.startswith("Error"):
            st.error(suggestions)
        else:
            for rec in suggestions:
                if st.button(f"{rec['model']}\n\n{rec['reason']}"):
                    st.write(f"You selected: {rec['model']}")
    else:
        st.warning("Please enter a use case before requesting recommendations.")

            
