import streamlit as st

st.title("Your feedback is valueable to me! 😊")

st.write(
    """
    Your feedback is very crucial to me!  
    It helps me improve and tailor the app to your needs. Please take a moment to fill out our feedback form.
    """
)

st.markdown("---")

st.markdown(
    """
    ### **[📝 Fill out our feedback form here!](https://forms.gle/xQ5Gq8zbY8xCpqDq8)**  
    """
, unsafe_allow_html=True)

st.markdown("---")

st.write(
    """
    In the form, you can:
    - **Rate your experience** with the app.  
    - **Report any bugs** or issues you've encountered.  
    - **Suggest new features** you'd like to see.  
    - **Share general feedback** to help us improve.
    """
)

# Add a call-to-action message
st.info(
    """
    Your feedback will only take a few minutes to complete, and it will go a long way in helping us enhance your experience.  
    Thank you for your time and support! 🌟
    """
)

# Optionally, add some visuals (e.g., emojis or icons) for aesthetics
st.markdown("📝 **Your thoughts make a difference!**")
st.markdown("---")

# Closing note
st.write(
    """
    If you have any immediate concerns or questions, feel free to reach out to us via [email](mailto:asifdotexe@gmail.com).
    """
)
