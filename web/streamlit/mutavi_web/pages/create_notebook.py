import pandas as pd
import streamlit as st
from st_aggrid import AgGrid
from st_aggrid.grid_options_builder import GridOptionsBuilder
from st_aggrid.shared import GridUpdateMode


def show_page():
    st.markdown(
        """
        <center>
            <h2>Notebook Creation</h2>
        </center>
        """,
        unsafe_allow_html=True,
    )

    notebook_name = st.text_input(
        "Notebooke Name", "default"
    )
    namespace = st.text_input(
        "Namespace", "default"
    )
    image = st.text_input(
        "Image", "jupyter/datascience-notebook:latest"
    )
    pw = st.text_input(
        "Password", "sdt"
    )
    cpu_size = st.text_input(
        "CPU Size", 250
    )
    mem_size = st.text_input(
        "Memory Size", 250
    )

    notebook = {
        "name": notebook_name,
        "namespace": namespace,
        "image": image,
        "password": pw,
        "cpu": cpu_size,
        "mem": mem_size
    }
    
    button_val = st.button(label="run")

    return notebook, button_val
