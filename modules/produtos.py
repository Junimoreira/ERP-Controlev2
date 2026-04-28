import streamlit as st
import pandas as pd
from database.connection import conectar

# ============================
# FUNÇÕES
# ============================

def buscar_produtos(nome=""):
    query = """
        SELECT id, nome, preco, estoque
        FROM produtos
        WHERE 1=1
    """
    params = []

    if nome:
        query += " AND nome ILIKE %s"
        params.append(f"%{nome}%")

    query += " ORDER BY id DESC"

    with conectar() as conn:
        with conn.cursor() as cur:
            cur.execute(query, params)
            return cur.fetchall()


def inserir_produto(nome, preco, estoque):
    with conectar() as conn:
        with conn.cursor() as cur:

            cur.execute("""
                SELECT id FROM produtos
                WHERE LOWER(nome) = LOWER(%s)
            """, (nome,))

            if cur.fetchone():
                return False

            cur.execute("""
                INSERT INTO produtos (nome, preco, estoque)
                VALUES (%s,%s,%s)
            """, (nome, preco, estoque))

            conn.commit()
            return True


def atualizar_produto(id, nome, preco, estoque):
    with conectar() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                UPDATE produtos
                SET nome=%s, preco=%s, estoque=%s
                WHERE id=%s
            """, (nome, preco, estoque, id))
            conn.commit()


def excluir_produto(id):
    with conectar() as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM produtos WHERE id=%s", (id,))
            conn.commit()


# ============================
# TELA
# ============================

def tela_produtos():

    st.title("📦 Produtos")

    aba1, aba2 = st.tabs(["Cadastrar", "Lista"])

    # ============================
    # CADASTRO
    # ============================
    with aba1:

        with st.form("form_produto", clear_on_submit=True):

            nome = st.text_input("Nome Produto")
            preco = st.number_input("Preço", min_value=0.0, format="%.2f")
            estoque = st.number_input("Estoque", min_value=0, step=1)

            salvar = st.form_submit_button("Salvar Produto")

            if salvar:

                if nome.strip() == "":
                    st.warning("Informe o nome.")
                    st.stop()

                sucesso = inserir_produto(nome, preco, estoque)

                if not sucesso:
                    st.error("Produto já existe.")
                    st.stop()

                st.success("Produto cadastrado!")
                st.rerun()

    # ============================
    # LISTA
    # ============================
    with aba2:

        busca = st.text_input("🔍 Buscar produto")

        dados = buscar_produtos(busca)

        df = pd.DataFrame(
            dados,
            columns=["ID", "Nome", "Preço", "Estoque"]
        )

        st.dataframe(df, use_container_width=True, hide_index=True)
        st.caption(f"Total: {len(df)}")

        st.divider()

        # ============================
        # EDITAR / EXCLUIR
        # ============================
        if not df.empty:

            prod_id = st.selectbox(
                "Selecione",
                df["ID"],
                format_func=lambda x: f"{x} - {df[df['ID']==x]['Nome'].values[0]}"
            )

            produto = df[df["ID"] == prod_id].iloc[0]

            st.subheader("✏️ Editar Produto")

            nome = st.text_input("Nome", value=produto["Nome"])
            preco = st.number_input("Preço", value=float(produto["Preço"]))
            estoque = st.number_input("Estoque", value=int(produto["Estoque"]))

            col1, col2 = st.columns(2)

            # ATUALIZAR
            with col1:
                if st.button("💾 Atualizar"):
                    atualizar_produto(prod_id, nome, preco, estoque)
                    st.success("Atualizado!")
                    st.rerun()

            # EXCLUIR
            with col2:
                confirmar = st.checkbox("Confirmar exclusão")

                if st.button("🗑️ Excluir"):

                    if not confirmar:
                        st.warning("Confirme antes de excluir!")
                        st.stop()

                    excluir_produto(prod_id)
                    st.warning("Excluído!")
                    st.rerun()