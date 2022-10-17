import streamlit as st


def choose_template():

    st.sidebar.markdown(
        """
        ## About
        *Please select Species, Serotype, Protein type and click 'Run' button. Thank you.*
        ---
        """,
        unsafe_allow_html=True,
    )
    button_format = "Select {}"