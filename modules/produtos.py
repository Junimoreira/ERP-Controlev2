import streamlit as st
import pandas as pd
from database.connection import conectar


def tela_produtos():

    st.subheader("📦 Cadastro de Produtos")

    abas = st.tabs(["➕ Novo Produto", "📋 Lista Produtos"])

    # ==================================================
    # ABA CADASTRO
    # ==================================================
    with abas[0]:

        with st.form("form_produto"):

            nome = st.text_input("Nome Produto")
            codigo = st.text_input("Código de Barras")
            categoria = st.text_input("Categoria")

            col1, col2, col3 = st.columns(3)

            with col1:
                custo = st.number_input("Custo", 0.0, step=0.01)

            with col2:
                preco = st.number_input("Preço Venda", 0.0, step=0.01)

            with col3:
                estoque = st.number_input("Estoque Inicial", 0, step=1)

            salvar = st.form_submit_button("💾 Salvar Produto")

            if salvar:

                if nome == "":
                    st.warning("Digite o nome.")
                    st.stop()

                with conectar() as conn:
                    with conn.cursor() as cur:

                        cur.execute("""
                            INSERT INTO produtos
                            (nome, codigo_barras, categoria, custo, preco, estoque)
                            VALUES (%s,%s,%s,%s,%s,%s)
                        """, (
                            nome,
                            codigo,
                            categoria,
                            custo,
                            preco,
                            estoque
                        ))

                        conn.commit()

                st.success("Produto cadastrado com sucesso!")
                st.rerun()

    # ==================================================
    # ABA LISTAGEM
    # ==================================================
    with abas[1]:

        busca = st.text_input("🔎 Buscar Produto")

        with conectar() as conn:

            query = """
                SELECT id, nome, codigo_barras, categoria,
                       custo, preco, estoque
                FROM produtos
            """

            df = pd.read_sql(query, conn)

        if busca:
            df = df[df["nome"].str.contains(busca, case=False)]

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

        # EXCLUIR
        st.markdown("### 🗑️ Excluir Produto")

        if not df.empty:

            id_excluir = st.selectbox(
                "Selecione ID",
                df["id"]
            )

            if st.button("Excluir Produto"):

                with conectar() as conn:
                    with conn.cursor() as cur:
                        cur.execute(
                            "DELETE FROM produtos WHERE id=%s",
                            (id_excluir,)
                        )
                        conn.commit()

                st.success("Produto excluído.")
                st.rerun()