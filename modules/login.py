import streamlit as st
import bcrypt
from database.connection import conectar


def tela_login():

    st.markdown("""
    <style>

    .login-box{
        max-width:420px;
        margin:auto;
        padding-top:40px;
    }

    .stButton button{
        width:100%;
        height:45px;
        border:none;
        border-radius:10px;
        background:#44d62c;
        color:white;
        font-size:18px;
        font-weight:600;
    }

    .stButton button:hover{
        background:#35b420;
    }

    </style>
    """, unsafe_allow_html=True)

    with st.container():

        st.markdown('<div class="login-box">', unsafe_allow_html=True)

        st.image("logo.png", width=180)

        st.markdown(
            "<h1 style='text-align:center;'>Login</h1>",
            unsafe_allow_html=True
        )

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
                            st.rerun()

            st.error("Usuário ou senha inválidos")

        st.markdown("</div>", unsafe_allow_html=True)