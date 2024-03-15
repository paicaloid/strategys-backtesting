import glob
from pathlib import Path

import streamlit as st

st.set_page_config(layout="wide", page_title="Crypto Dashboard")

st.markdown(
    """
    <style>
        footer {display: none}
        [data-testid="stHeader"] {display: none}
    </style>
    """,
    unsafe_allow_html=True,
)

params_col, chart_col, data_col = st.columns([0.5, 1.2, 0.6])

with params_col:
    with st.form(key="params_form"):
        st.markdown(
            '<p class="params_text">CHART DATA PARAMETERS', unsafe_allow_html=True
        )
        st.divider()

        symbol_path = sorted(glob.glob("temp/*.csv"))
        symbol_list = [Path(file).stem for file in symbol_path]
        symbols = st.selectbox("Index", symbol_list, key="index_selectbox")

        number = st.number_input("Insert a number", value=0, step=1, placeholder=None)
        # st.write("The current number is ", number)

        st.markdown("")
        update_chart = st.form_submit_button("Update chart")
        st.markdown("")

        if update_chart:
            st.write("The current number is ", number)
