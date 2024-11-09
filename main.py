import streamlit as st

# Define your pages using st.Page objects
pages = {
    "Main Pages": [
        st.Page("pages/home.py", title="Home", icon="🏠"),
    ],
    "Apps": [
        st.Page("pages/quickPrep.py", title="Quick Prep", icon="🔧"),
        st.Page("pages/quickGlance.py", title="Quick Glance", icon="👀",),
    ]
}

# Setup navigation in the sidebar
pg = st.navigation(pages, position="sidebar", expanded=True)

# Run the selected page
pg.run()
