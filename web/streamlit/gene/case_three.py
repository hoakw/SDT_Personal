import streamlit as st
from st_aggrid import AgGrid
from st_aggrid.grid_options_builder import GridOptionsBuilder
from st_aggrid.shared import GridUpdateMode


def show_page(data):
    if data.empty:
        st.markdown(
            """
            <center>
                <h2>Genescis Result Case 3</h2>
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
                <h2>Genescis Result Case 3</h2>
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
        #gb.configure_selection(selection_mode="single", use_checkbox=True)
        grid_options = gb.build()

        ag_data = AgGrid(data, 
        gridOptions=grid_options,
        enable_enterprise_modules=True,
        #allow_unsafe_jscode=True,
        #update_mode=GridUpdateMode.SELECTION_CHANGED,
        )
        _, _, _, _, col = st.columns(5)
        mismatch = col.button(label="Mismatch")
        if mismatch:
            #get_data = dict(ag_data['selected_rows'][0])
            #print(f"[agGrid] {get_data['SPACER']}")
            #print(f"[agGrid] {get_data['TARGET']}")
            st.markdown(
            """
            <center>
                <hr><h2>Genescis Mismatch Result 3</h2>
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