import streamlit as st
import bcrypt
#from database import conectar
from database.connection import conectar

def tela_login():

    st.title("🔐 Login")

    usuario = st.text_input("Usuário")
    senha = st.text_input("Senha", type="password")

    if st.button("Entrar"):

        with conectar() as conn:
            with conn.cursor() as cur:

                cur.execute(
                    "SELECT senha FROM usuarios WHERE usuario=%s",
                    (usuario,)
                )

                resultado = cur.fetchone()

                if resultado:
                    senha_hash = resultado[0]

                    if bcrypt.checkpw(
                        senha.encode(),
                        senha_hash.encode()
                    ):
                        st.session_state.logado = True
                        st.session_state.usuario = usuario
                        st.success("Login realizado!")
                        st.rerun()

        st.error("Usuário ou senha inválidos")