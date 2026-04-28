import streamlit as st
import pandas as pd
from database.connection import conectar

# ============================
# FUNÇÕES AUXILIARES
# ============================

def buscar_clientes(nome="", cpf=""):
    query = """
        SELECT id, nome, cpf, telefone, email
        FROM clientes
        WHERE 1=1
    """
    params = []

    if nome:
        query += " AND nome ILIKE %s"
        params.append(f"%{nome}%")

    if cpf:
        query += " AND cpf ILIKE %s"
        params.append(f"%{cpf}%")

    query += " ORDER BY id DESC"

    with conectar() as conn:
        with conn.cursor() as cur:
            cur.execute(query, params)
            return cur.fetchall()


def inserir_cliente(nome, cpf, telefone, email):
    with conectar() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO clientes (nome, cpf, telefone, email)
                VALUES (%s,%s,%s,%s)
            """, (nome, cpf, telefone, email))
            conn.commit()


def atualizar_cliente(id, nome, cpf, telefone, email):
    with conectar() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                UPDATE clientes
                SET nome=%s, cpf=%s, telefone=%s, email=%s
                WHERE id=%s
            """, (nome, cpf, telefone, email, id))
            conn.commit()


def excluir_cliente(id):
    with conectar() as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM clientes WHERE id=%s", (id,))
            conn.commit()


# ============================
# TELA
# ============================

def tela_clientes():

    st.title("👤 Clientes")
    st.caption("Gerencie seus clientes cadastrados")

    aba1, aba2 = st.tabs(["Cadastrar", "Lista"])

    # ==================================================
    # CADASTRO
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
                    st.warning("Informe o nome.")
                    st.stop()

                inserir_cliente(nome, cpf, telefone, email)

                st.success("Cliente cadastrado!")
                st.rerun()

    # ==================================================
    # LISTA
    # ==================================================
    with aba2:

        col1, col2 = st.columns(2)

        with col1:
            busca_nome = st.text_input("🔍 Buscar nome")

        with col2:
            busca_cpf = st.text_input("Buscar CPF")

        dados = buscar_clientes(busca_nome, busca_cpf)

        df = pd.DataFrame(
            dados,
            columns=["ID", "Nome", "CPF", "Telefone", "Email"]
        )

        st.dataframe(df, use_container_width=True, hide_index=True)
        st.caption(f"Total: {len(df)}")

        st.divider()

        if not df.empty:

            cliente_id = st.selectbox(
                "Selecione",
                df["ID"],
                format_func=lambda x: f"{x} - {df[df['ID']==x]['Nome'].values[0]}"
            )

            cliente = df[df["ID"] == cliente_id].iloc[0]

            st.subheader("✏️ Editar")

            nome = st.text_input("Nome", value=cliente["Nome"])
            cpf = st.text_input("CPF", value=cliente["CPF"])
            telefone = st.text_input("Telefone", value=cliente["Telefone"])
            email = st.text_input("Email", value=cliente["Email"])

            col1, col2 = st.columns(2)

            # ATUALIZAR
            with col1:
                if st.button("💾 Atualizar"):
                    atualizar_cliente(cliente_id, nome, cpf, telefone, email)
                    st.success("Atualizado!")
                    st.rerun()

            # EXCLUIR COM CONFIRMAÇÃO
            with col2:
                confirmar = st.checkbox("Confirmar exclusão")

                if st.button("🗑️ Excluir"):

                    if not confirmar:
                        st.warning("Confirme antes de excluir!")
                        st.stop()

                    excluir_cliente(cliente_id)
                    st.warning("Excluído!")
                    st.rerun()