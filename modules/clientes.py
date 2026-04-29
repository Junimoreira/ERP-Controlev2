import streamlit as st
import pandas as pd
from database.connection import conectar

# ============================
# FUNÇÕES AUXILIARES
# ============================

def buscar_clientes(nome="", documento=""):

    query = """
        SELECT id, tipo, nome, documento, telefone, email, endereco
        FROM clientes
        WHERE 1=1
    """

    params = []

    if nome:
        query += " AND nome ILIKE %s"
        params.append(f"%{nome}%")

    if documento:
        query += " AND documento ILIKE %s"
        params.append(f"%{documento}%")

    query += " ORDER BY id DESC"

    with conectar() as conn:
        with conn.cursor() as cur:
            cur.execute(query, params)
            return cur.fetchall()


def inserir_cliente(tipo, nome, documento, telefone, email, endereco):

    with conectar() as conn:
        with conn.cursor() as cur:

            cur.execute("""
                INSERT INTO clientes
                (tipo, nome, documento, telefone, email, endereco)
                VALUES (%s,%s,%s,%s,%s,%s)
            """, (
                tipo,
                nome,
                documento,
                telefone,
                email,
                endereco
            ))

            conn.commit()


def atualizar_cliente(id, tipo, nome, documento, telefone, email, endereco):

    with conectar() as conn:
        with conn.cursor() as cur:

            cur.execute("""
                UPDATE clientes
                SET tipo=%s,
                    nome=%s,
                    documento=%s,
                    telefone=%s,
                    email=%s,
                    endereco=%s
                WHERE id=%s
            """, (
                tipo,
                nome,
                documento,
                telefone,
                email,
                endereco,
                id
            ))

            conn.commit()


def excluir_cliente(id):

    with conectar() as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM clientes WHERE id=%s", (id,))
            conn.commit()


# ============================
# TELA CLIENTES
# ============================

def tela_clientes():

    st.title("👤 Clientes")
    st.caption("Cadastro PF e PJ")

    aba1, aba2 = st.tabs(["➕ Cadastrar", "📋 Lista"])

    # ==================================================
    # CADASTRAR
    # ==================================================
    with aba1:

        with st.form("form_cliente", clear_on_submit=True):

            tipo = st.radio(
                "Tipo Cliente",
                ["Pessoa Física", "Pessoa Jurídica"],
                horizontal=True
            )

            nome = st.text_input(
                "Nome Completo" if tipo == "Pessoa Física"
                else "Razão Social"
            )

            documento = st.text_input(
                "CPF" if tipo == "Pessoa Física"
                else "CNPJ"
            )

            telefone = st.text_input("Telefone")
            email = st.text_input("Email")
            endereco = st.text_area("Endereço")

            salvar = st.form_submit_button("💾 Salvar")

            if salvar:

                if nome.strip() == "":
                    st.warning("Informe o nome.")
                    st.stop()

                inserir_cliente(
                    tipo,
                    nome,
                    documento,
                    telefone,
                    email,
                    endereco
                )

                st.success("Cliente cadastrado!")
                st.rerun()

    # ==================================================
    # LISTA
    # ==================================================
    with aba2:

        col1, col2 = st.columns(2)

        with col1:
            busca_nome = st.text_input("🔍 Buscar Nome")

        with col2:
            busca_doc = st.text_input("Buscar CPF/CNPJ")

        dados = buscar_clientes(
            busca_nome,
            busca_doc
        )

        df = pd.DataFrame(
            dados,
            columns=[
                "ID",
                "Tipo",
                "Nome",
                "Documento",
                "Telefone",
                "Email",
                "Endereço"
            ]
        )

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

        st.caption(f"Total: {len(df)}")

        st.divider()

        if not df.empty:

            cliente_id = st.selectbox(
                "Selecione Cliente",
                df["ID"],
                format_func=lambda x:
                f"{x} - {df[df['ID']==x]['Nome'].values[0]}"
            )

            cliente = df[df["ID"] == cliente_id].iloc[0]

            st.subheader("✏️ Editar Cliente")

            tipo = st.selectbox(
                "Tipo",
                ["Pessoa Física", "Pessoa Jurídica"],
                index=0 if cliente["Tipo"] == "Pessoa Física" else 1
            )

            nome = st.text_input(
                "Nome",
                value=cliente["Nome"]
            )

            documento = st.text_input(
                "Documento",
                value=cliente["Documento"]
            )

            telefone = st.text_input(
                "Telefone",
                value=cliente["Telefone"]
            )

            email = st.text_input(
                "Email",
                value=cliente["Email"]
            )

            endereco = st.text_area(
                "Endereço",
                value=cliente["Endereço"]
            )

            col1, col2 = st.columns(2)

            with col1:
                if st.button("💾 Atualizar"):

                    atualizar_cliente(
                        cliente_id,
                        tipo,
                        nome,
                        documento,
                        telefone,
                        email,
                        endereco
                    )

                    st.success("Atualizado!")
                    st.rerun()

            with col2:

                confirmar = st.checkbox(
                    "Confirmar exclusão"
                )

                if st.button("🗑️ Excluir"):

                    if not confirmar:
                        st.warning("Confirme antes.")
                        st.stop()

                    excluir_cliente(cliente_id)

                    st.warning("Excluído!")
                    st.rerun()