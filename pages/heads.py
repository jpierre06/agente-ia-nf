import streamlit as st
from core.data_loader import load_dataframes_from_folders
from core.data_loader import get_info_df


data = load_dataframes_from_folders()
heads = data["heads"]

st.caption("Dicionário de dados dos cabeçalhos das notas fiscais")
st.dataframe(get_info_df(heads))

st.caption("Dados das notas fiscais")
st.dataframe(heads)