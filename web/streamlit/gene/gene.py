import datetime

#from sklearn.decomposition import NMF
#from turtle import back
import streamlit as st
import pandas as pd
import numpy as np

from page import background_and_title

from Template import input_template

from calculation import Calculation
from gene_request.get_cookie import GetAuthkey

import home_page as Home
import case_one as c_one
import case_two as c_two
import case_three as c_three
import case_four as c_four



#from result import Result_app
#from input_page import Input_app
#from hydralit import HydraApp

def main():

    nm_data, pred_data, download_data = False, False, False
    ccl = Calculation()
    gKey = GetAuthkey()

    st.set_page_config(page_title="Genescis Web Test", page_icon=None, layout="centered", initial_sidebar_state='expanded')

    # language check
    col, _, _ = st.columns(3)
    lang = st.sidebar.selectbox(
            "Select Language",
            options=["kor", "eng"],
        )
    st.session_state.lang = lang
    print(f"[Lang] Cnt Lang = {st.session_state.lang}", flush=True)

    background_and_title(st.session_state.lang)

    # Check gkey 
    if 'key_valid_time' not in st.session_state:
        auth_key, record_time = gKey.get_key()
        st.session_state.key_valid_time = record_time
        st.session_state.auth_key = auth_key
    else:
        now_date = datetime.datetime.now()
        time_gap = now_date - st.session_state.key_valid_time
        print(f"[Valid-Time] Cnt Time = {now_date} / Get Key time = {st.session_state.key_valid_time}", flush=True)
        print(f"[Valid-Time] Time Gaps = {time_gap.days}", flush=True)
        if time_gap.days >= 1:
            auth_key, record_time = gKey.get_key()
            st.session_state.key_valid_time = record_time
            st.session_state.auth_key = auth_key

    gene, sequence, spacer, submit_button, clear_button = input_template(st.session_state.lang)

    pages = {
        "Home": Home,
        "Case1[Gene]": c_one,
        "Case2[Sequence]": c_two,
        "Case3[Gene, Sequence]": c_three,
        "Case4[Gene, Sequence, Spacer]": c_four 
    }
    st.sidebar.markdown(
        """
        <hr>
        """,
        unsafe_allow_html=True
    )

    if 'cnt_page' not in st.session_state:
        st.session_state.cnt_page = "Home"
        
    print(f"[Page1] {st.session_state.cnt_page} / clear button {clear_button}", flush=True)

    print(F"[Data Check] gene = {gene}, sequence = {sequence}, spacer = {spacer} button = {submit_button}", flush=True)

    if submit_button:
        if gene == "" and sequence == "":
            print("Error", flush=True)
        elif gene != "" and sequence != "" and spacer != "":
            print("Case4", flush=True)
            case_four_result = ccl.kfserving(st.session_state.auth_key, gene, sequence, spacer, 4)
            st.session_state.case_four = case_four_result
            st.session_state.cnt_page = "Case4[Gene, Sequence, Spacer]"
        elif gene != "" and sequence != "":
            print("Case3", flush=True)
            #case_three_result = ccl.get_case_three(gene, sequence)
            case_three_result = ccl.kfserving(st.session_state.auth_key, gene, sequence, "", 3)
            st.session_state.case_three = case_three_result
            st.session_state.cnt_page = "Case3[Gene, Sequence]"
        elif gene != "":
            print("Case1", flush=True)
            #case_one_result = ccl.kfserving(st.session_state.auth_key, gene, "", "", 1)
            case_one_result = ccl.get_case_one(gene)
            st.session_state.case_one = case_one_result
            st.session_state.cnt_page = "Case1[Gene]"
        elif sequence != "":
            print("Case2", flush=True)
            case_two_result = ccl.kfserving(st.session_state.auth_key, "", sequence, "", 2)
            #case_two_result = ccl.get_case_two(sequence)
            st.session_state.case_two = case_two_result
            st.session_state.cnt_page = "Case2[Sequence]"

    if st.session_state.cnt_page == "Home" or clear_button:
        st.session_state.cnt_page = "Home"
        pages[st.session_state.cnt_page].show_page(st.session_state.lang)
    elif st.session_state.cnt_page == "Case1[Gene]":
        if 'case_one' not in st.session_state:
            pages[st.session_state.cnt_page].show_page(pd.DataFrame())
        else:
            pages[st.session_state.cnt_page].show_page(st.session_state.case_one)
    elif st.session_state.cnt_page == "Case2[Sequence]":
        if 'case_two' not in st.session_state:
            pages[st.session_state.cnt_page].show_page(pd.DataFrame())
        else:
            pages[st.session_state.cnt_page].show_page(st.session_state.case_two)
    elif st.session_state.cnt_page == "Case3[Gene, Sequence]":
        if 'case_three' not in st.session_state:
            pages[st.session_state.cnt_page].show_page(pd.DataFrame())
        else:
            pages[st.session_state.cnt_page].show_page(st.session_state.case_three)
    elif st.session_state.cnt_page == "Case4[Gene, Sequence, Spacer]":
        if 'case_four' not in st.session_state:
            pages[st.session_state.cnt_page].show_page(pd.DataFrame())
        else:
            pages[st.session_state.cnt_page].show_page(st.session_state.case_four)
    
    print(f"[Page2] {st.session_state.cnt_page}", flush=True)

    



if __name__ == "__main__":
    main()