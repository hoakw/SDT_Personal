import streamlit as st


def show_page(lang):
    if lang == "kor":
        st.markdown(
            """
            <center>
                <h2>Genescis 홈!!</h2>
            </center>
            <center>
                <i>한국어 홈 ... </i>
                <hr>
            </center>
            """,
            unsafe_allow_html=True
        )
    elif lang == "eng":
        st.markdown(
            """
            <center>
                <h2>Genescis Home!!</h2>
            </center>
            <center>
                <i>English Home ... </i>
                <hr>
            </center>
            """,
            unsafe_allow_html=True
        )

