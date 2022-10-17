import pandas as pd
import streamlit as st

from st_aggrid import AgGrid
from st_aggrid.grid_options_builder import GridOptionsBuilder
from st_aggrid.shared import GridUpdateMode

def show_page(data, df_data):
    if data is False:
        st.markdown(
            """
            <hr>
            <center>
                <h2>Sample Sequence</h2>
            </center>
            <center>
                <h6> This is ... (description) </h6>
            </center>
            <center>
                <i>Please select target virus and click run button. Now, we not have result data</i>
                <hr>
            </center>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            """
            <hr>
            <center>
                <h2>Sample Sequence</h2>
            </center>
            <center>
                <i>This result is ...</i>
                <hr>
            </center>
            """,
            unsafe_allow_html=True,
        )

        gb = GridOptionsBuilder.from_dataframe(df_data)
        gb.configure_pagination()
        grid_options = gb.build()

        AgGrid(df_data, 
        gridOptions=grid_options,
        enable_enterprise_modules=True,
        allow_unsafe_jscode=True,
        )
        
        #col1, col2, col3, col4 = st.columns(4)

        st.download_button("Download a file", data, file_name="MutaVi_fasta.txt")
