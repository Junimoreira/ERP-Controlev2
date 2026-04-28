import streamlit as st
from modules.clientes import tela_clientes
from database.setup import criar_tabelas

criar_tabelas()

st.set_page_config(page_title="Controle", layout="wide")

menu = st.sidebar.selectbox(
    "Menu",
    ["Clientes", "Produtos", "Vendas"]
)

if menu == "Clientes":
    tela_clientes()