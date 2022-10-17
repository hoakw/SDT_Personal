import pages.create_notebook as note_c
import pages.list_notebook as note_r
import pages.delete_notebook as note_d

import pages.sidebar as side
import streamlit as st
import utils
import argparse
from streamlit_option_menu import option_menu


def main(fastapi_url: str):
    st.set_page_config(
        page_title="Notebook Web Test",
        page_icon=None,
        #layout="wide",
        layout="centered",
        initial_sidebar_state="expanded",
    )

    #side.choose_template()

    ccl = utils.Calculation(fastapi_url)
    with st.sidebar:
        menu_page = option_menu(
            "노트북 CRUD",
            ["생성", "생성리스트", "삭제"],
            icons=["house", "chat-left-text", "chat-left-text"],
            default_index=0,
            styles={
                "menu-title": {"font-size": "20px"},
                "container": {
                    "padding": "5!important",
                    "background-color": "#f0f2f6",
                },  # fafafa
                "icon": {"color": "black", "font-size": "15px"},
                "nav-link": {
                    "font-size": "14px",
                    "text-align": "left",
                    "margin": "0px",
                    "--hover-color": "#eee",
                },
                "nav-link-selected": {"background-color": "#96BDF0"},
            },
        )
    st.session_state.menu = menu_page

    notebook_create = "생성"
    notebook_list = "생성리스트"
    notebook_delete = "삭제"

    pages = {
        notebook_create: note_c,
        notebook_list: note_r,
        notebook_delete: note_d
    }


    if st.session_state.menu == notebook_create:
        notebook_data, c_button_val = note_c.show_page()
        if c_button_val:
            print("[Creating] SDT Creating Notebook!!!")
            ccl.create_notebook(notebook_data)
    if st.session_state.menu == notebook_list:
        notebook_ns, r_button_val = note_r.show_page()
        if r_button_val:
            print("[Get] SDT List of Notebook!!!")
            list_data = ccl.get_notebook_list(notebook_ns)
            note_r.show_list_notebook(list_data)
    if st.session_state.menu == notebook_delete:
        notebook_name, notebook_ns, d_button_val = note_d.show_page()
        if d_button_val:
            print("[Get] SDT Deleting Notebook!!!")
            ccl.delete_notebook(notebook_name, notebook_ns)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--fastapi_url", help="fastapi url")
    
    args = parser.parse_args()
    main(args.fastapi_url)
