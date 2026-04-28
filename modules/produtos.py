import streamlit as st
import pandas as pd
from database import conectar


def tela_produtos():

    st.title("📦 Produtos")

    aba1, aba2 = st.tabs(["Cadastrar", "Lista"])

    # -----------------------------------------
    # ABA CADASTRAR
    # -----------------------------------------
    with aba1:

        nome = st.text_input(
            "Nome Produto",
            key="prod_nome"
        )

        preco = st.number_input(
            "Preço",
            min_value=0.0,
            value=0.0,
            format="%.2f",
            key="prod_preco"
        )

        estoque = st.number_input(
            "Estoque",
            min_value=0,
            value=0,
            step=1,
            key="prod_estoque"
        )

        if st.button("Salvar Produto", use_container_width=True):

            nome = nome.strip()

            if nome == "":
                st.error("Informe o nome do produto.")
                return

            with conectar() as conn:
                with conn.cursor() as cur:

                    # evita duplicado
                    cur.execute("""
                        SELECT id
                        FROM produtos
                        WHERE LOWER(nome) = LOWER(%s)
                    """, (nome,))

                    existe = cur.fetchone()

                    if existe:
                        st.error("Já existe produto com esse nome.")
                        return

                    cur.execute("""
                        INSERT INTO produtos
                        (nome, preco, estoque)
                        VALUES (%s,%s,%s)
                    """, (
                        nome,
                        preco,
                        estoque
                    ))

                    conn.commit()

            # limpar campos
            st.session_state.prod_nome = ""
            st.session_state.prod_preco = 0.0
            st.session_state.prod_estoque = 0

            st.success("Produto cadastrado com sucesso!")
            st.rerun()

    # -----------------------------------------
    # ABA LISTA
    # -----------------------------------------
    with aba2:

        with conectar() as conn:
            with conn.cursor() as cur:

                cur.execute("""
                    SELECT id, nome, preco, estoque
                    FROM produtos
                    ORDER BY id DESC
                """)

                dados = cur.fetchall()

        if dados:

            df = pd.DataFrame(
                dados,
                columns=["ID", "Nome", "Preço", "Estoque"]
            )

            df["Preço"] = df["Preço"].apply(
                lambda x: f"R$ {float(x):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
            )

            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True
            )

        else:
            st.info("Nenhum produto cadastrado.")