import streamlit as st
from core.data_loader import load_dataframes_from_folders
from core.data_loader import get_info_df


data = load_dataframes_from_folders()
items = data["items"]

st.caption("Dicionário de dados dos itens das notas fiscais")
st.dataframe(get_info_df(items))

st.caption("Dados de itens das notas fiscais")
st.dataframe(items)