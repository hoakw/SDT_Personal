import streamlit as st
import pandas as pd

from st_aggrid import AgGrid
from st_aggrid.grid_options_builder import GridOptionsBuilder
from st_aggrid.shared import GridUpdateMode

def show_page():
    
    st.markdown(
        """
        <center>
            <h2>List of Notebook!!</h2>
        </center>
        <center>
            <i>English Home ... </i>
            <hr>
        </center>
        """,
        unsafe_allow_html=True
    )
    namespace = st.text_input(
        "Namespace", "default"
    )

    button_val = st.button(label="Get")

    return namespace, button_val

def show_list_notebook(list_data):
    list_data = pd.DataFrame(list_data)
    print(list_data)

    gb = GridOptionsBuilder.from_dataframe(list_data)
    gb.configure_pagination()
    grid_options = gb.build()

    AgGrid(list_data, 
    gridOptions=grid_options,
    enable_enterprise_modules=True,
    allow_unsafe_jscode=True,
    )
    # for index in range(len(list_data['pod_name'])):
    #     st.write(list_data['pod_name'][0])
    #     st.write(list_data['internel_Address'][0])
    #     st.write(list_data['externel_Address'][0])