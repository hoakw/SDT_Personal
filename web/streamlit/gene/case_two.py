import streamlit as st
from st_aggrid import AgGrid
from st_aggrid.grid_options_builder import GridOptionsBuilder
from st_aggrid.shared import GridUpdateMode

def show_page(data):
    if data.empty:
        st.markdown(
            """
            <center>
                <h2>Genescis Result Case 2</h2>
            </center>
            <center>
                <h6> This is ... (description) </h6>
            </center>
            <center>
                <i>Please fill in input box and click run button. Now, we not have result data</i>
                <hr>
            </center>
            """,
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            """
            <center>
                <h2>Genescis Result Case 2</h2>
            </center>
            <center>
                <i>This result is ...</i>
                <hr>
            </center>
            """,
            unsafe_allow_html=True
        )
        gb = GridOptionsBuilder.from_dataframe(data)
        gb.configure_pagination()
        grid_options = gb.build()

        AgGrid(data, 
        gridOptions=grid_options,
        enable_enterprise_modules=True,
        allow_unsafe_jscode=True,
        )