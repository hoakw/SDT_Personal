import pandas as pd
import streamlit as st


def show_page():

    st.markdown(
        """
        <hr>
        <center>
            <h2>Prediction Performance</h2>
        </center>
        <center>
            <i>This result is ...</i>
            <hr>
        </center>
        """,
        unsafe_allow_html=True,
    )
    notebook_name = st.text_input(
        "notebook_name", "default"
    )
    notebook_ns = st.text_input(
        "namespace", "sdt"
    )

    button_val = st.button(label="delete")

    return notebook_name, notebook_ns, button_val
