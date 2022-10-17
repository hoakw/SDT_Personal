import streamlit as st

def input_template(lang):
    if lang == "kor":
        button_label = "실행"
        home_label = "홈"
        st.sidebar.markdown(
            """
            <h2>설명</h2>
            <i>한국어 버전</i><br><br>
            """,
            unsafe_allow_html=True
        )
    elif lang == "eng":
        button_label = "Run"
        home_label = "Home"
        st.sidebar.markdown(
            """
            <h2>About</h2>
            <i>English Version</i><br><br>
            """,
            unsafe_allow_html=True
        )

    clear_button = st.sidebar.button(label=home_label)
    st.sidebar.markdown(
        """
        <hr>
        """,
        unsafe_allow_html=True
    )
    with st.sidebar.form(key='case1'):
        option1 = st.text_input(label='Gene Name')
        option2 = st.text_input(label='Target Sequence')
        option3 = st.text_input(label='Spacer Sequence')
        submit_button = st.form_submit_button(label=button_label)

    return option1, option2, option3, submit_button, clear_button
