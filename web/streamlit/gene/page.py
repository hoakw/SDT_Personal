import streamlit as st

def background_and_title(lang):
    st.markdown(
        """
        <style>
        .reportview-container {
            background: #EBECES5
        }

        a:link{ color:#325FE5; }
        a:visited{ color:#325FE5; }
        a:hover{ color:#325FE5; }
        a:active{ color:#325FE5}
        </style>
        """,
        unsafe_allow_html=True
    )
    if lang == "kor":
        st.markdown(
            """
            <center>
                <h1>Genescis 유전자 가위 도구</h1>
            </center>
            <center>
                <i>유전자 어쩌구 저쩌구</i>
                <hr>
            </center>
            """,
            unsafe_allow_html=True
        )
    elif lang == "eng":
        st.markdown(
            """
            <center>
                <h1>Genescis Web Testing</h1>
            </center>
            <center>
                <i>English Version!!!</i>
                <hr>
            </center>
            """,
            unsafe_allow_html=True
        )