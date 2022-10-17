import streamlit as st


def show_page():
    max_width = st.sidebar.slider("Select width in px", 100, 2000, 1200, 100)
    BACKGROUND = "#EBECES5"
    print(f"[DEBUG] {max_width}")
    st.markdown(
        f"""
        <style>
        .reportview-container .main .block-container{{
            max-width: {max_width}px;
        }}
        .reportview-container{{
            background: {BACKGROUND};
        }}


        footer{{ visibility: hidden; }} #remove streamlit logo
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <center>
            <h1>MutaVi Protein Generation</h1>
        </center>
        <center>
            <i>Generating Next Mutation.</i>
            <hr>
        </center>
        """,
        unsafe_allow_html=True,
    )
