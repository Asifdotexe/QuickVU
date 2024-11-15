import streamlit as st

# Define your pages using st.Page objects
pages = {
    "Main Pages": [
        st.Page("app_pages/home.py", title="Home", icon=":material/home:"),
    ],
    "Apps": [
        st.Page("app_pages/quickPrep.py", title="Quick Prep: Data Cleaning", icon=":material/mop:"),
        st.Page("app_pages/quickGlance.py", title="Quick Glance: Data Analysis", icon=":material/search:",),
    ],
    "Others": {
        st.Page("app_pages/quickFeedback.py", title="Feedback", icon=":material/rate_review:")
    }
}

# Setup navigation in the sidebar
pg = st.navigation(pages, position="sidebar", expanded=True)

# Run the selected page
pg.run()
