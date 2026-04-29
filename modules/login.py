import streamlit as st
import bcrypt
from database.connection import conectar


def tela_login():

    st.image("logo.png", use_container_width=True)
    st.title("🔐 Login")

    usuario = st.text_input("Usuário")
    senha = st.text_input("Senha", type="password")

    if st.button("Entrar", use_container_width=True):

        with conectar() as conn:
            with conn.cursor() as cur:

                cur.execute(
                    """
                    SELECT senha, nivel
                    FROM usuarios
                    WHERE usuario=%s
                    """,
                    (usuario,)
                )

                resultado = cur.fetchone()

                if resultado:

                    senha_hash = resultado[0]
                    nivel = resultado[1]

                    if bcrypt.checkpw(
                        senha.encode(),
                        senha_hash.encode()
                    ):

                        st.session_state.logado = True
                        st.session_state.usuario = usuario
                        st.session_state.nivel = nivel

                        st.rerun()
                        return

        st.error("Usuário ou senha inválidos")