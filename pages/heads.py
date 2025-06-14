import streamlit as st
from core.csv import get_csv_content

heads = get_csv_content('data/202401_NFs.zip', '202401_NFs_Cabecalho.csv')
st.dataframe(heads)