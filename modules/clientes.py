import streamlit as st
import pandas as pd
from database import conectar

def tela_clientes():

    st.title("👤 Clientes")

    aba1, aba2 = st.tabs(["Cadastrar", "Lista"])

    # ==================================================
    # CADASTRAR CLIENTE
    # ==================================================
    with aba1:

        with st.form("form_cliente", clear_on_submit=True):

            nome = st.text_input("Nome")
            cpf = st.text_input("CPF")
            telefone = st.text_input("Telefone")
            email = st.text_input("Email")

            salvar = st.form_submit_button("Salvar Cliente")

            if salvar:

                if nome.strip() == "":
                    st.warning("Informe o nome do cliente.")
                    st.stop()

                with conectar() as conn:
                    with conn.cursor() as cur:

                        cur.execute("""
                            INSERT INTO clientes
                            (nome, cpf, telefone, email)
                            VALUES (%s,%s,%s,%s)
                        """, (
                            nome,
                            cpf,
                            telefone,
                            email
                        ))

                        conn.commit()

                st.success("Cliente cadastrado com sucesso!")
                st.rerun()

    # ==================================================
    # LISTA CLIENTES
    # ==================================================
   with aba2:

    with conectar() as conn:
        with conn.cursor() as cur:

            cur.execute("""
                SELECT id, nome, cpf, telefone, email
                FROM clientes
                ORDER BY id DESC
            """)

            dados = cur.fetchall()

    df = pd.DataFrame(
        dados,
        columns=["ID", "Nome", "CPF", "Telefone", "Email"]
    )

    st.dataframe(df, use_container_width=True, hide_index=True)

    st.caption(f"Total de clientes: {len(df)}")

    st.divider()

    # ============================
    # SELECIONAR CLIENTE
    # ============================
    if not df.empty:

        cliente_selecionado = st.selectbox(
            "Selecione um cliente",
            df["ID"],
            format_func=lambda x: f"{x} - {df[df['ID']==x]['Nome'].values[0]}"
        )

        cliente = df[df["ID"] == cliente_selecionado].iloc[0]

        novo_nome = st.text_input("Nome", value=cliente["Nome"])
        novo_cpf = st.text_input("CPF", value=cliente["CPF"])
        novo_telefone = st.text_input("Telefone", value=cliente["Telefone"])
        novo_email = st.text_input("Email", value=cliente["Email"])

        col1, col2 = st.columns(2)

        # ============================
        # EDITAR
        # ============================
        with col1:
            if st.button("Atualizar Cliente"):

                with conectar() as conn:
                    with conn.cursor() as cur:

                        cur.execute("""
                            UPDATE clientes
                            SET nome=%s, cpf=%s, telefone=%s, email=%s
                            WHERE id=%s
                        """, (
                            novo_nome,
                            novo_cpf,
                            novo_telefone,
                            novo_email,
                            cliente_selecionado
                        ))

                        conn.commit()

                st.success("Cliente atualizado!")
                st.rerun()

        # ============================
        # EXCLUIR
        # ============================
        with col2:
            if st.button("Excluir Cliente"):

                with conectar() as conn:
                    with conn.cursor() as cur:

                        cur.execute(
                            "DELETE FROM clientes WHERE id=%s",
                            (cliente_selecionado,)
                        )

                        conn.commit()

                st.warning("Cliente excluído!")
                st.rerun()