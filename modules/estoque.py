import streamlit as st
import pandas as pd
from database.connection import conectar


# ==================================================
# FUNÇÕES AUXILIARES
# ==================================================

def listar_produtos():

    with conectar() as conn:

        df = pd.read_sql("""
            SELECT id, nome, codigo_barras, categoria,
                   custo, preco, estoque
            FROM produtos
            ORDER BY nome
        """, conn)

    return df


def entrada_estoque(produto_id, quantidade):

    with conectar() as conn:
        with conn.cursor() as cur:

            cur.execute("""
                UPDATE produtos
                SET estoque = estoque + %s
                WHERE id = %s
            """, (quantidade, produto_id))

            conn.commit()


def saida_estoque(produto_id, quantidade):

    with conectar() as conn:
        with conn.cursor() as cur:

            cur.execute("""
                UPDATE produtos
                SET estoque = estoque - %s
                WHERE id = %s
            """, (quantidade, produto_id))

            conn.commit()


# ==================================================
# TELA ESTOQUE
# ==================================================

def tela_estoque():

    st.title("📦 Controle de Estoque")
    st.caption("Entradas, saídas e acompanhamento")

    abas = st.tabs([
        "📋 Estoque Atual",
        "➕ Entrada",
        "➖ Saída",
        "⚠️ Estoque Baixo"
    ])

    # ==================================================
    # ESTOQUE ATUAL
    # ==================================================
    with abas[0]:

        busca = st.text_input("🔎 Buscar Produto")

        df = listar_produtos()

        if busca:
            df = df[
                df["nome"].str.contains(
                    busca,
                    case=False,
                    na=False
                )
            ]

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

        st.caption(f"Total Produtos: {len(df)}")

    # ==================================================
    # ENTRADA
    # ==================================================
    with abas[1]:

        df = listar_produtos()

        if not df.empty:

            produto_id = st.selectbox(
                "Produto",
                df["id"],
                format_func=lambda x:
                f"{x} - {df[df['id']==x]['nome'].values[0]}"
            )

            qtd = st.number_input(
                "Quantidade Entrada",
                min_value=1,
                step=1
            )

            if st.button("💾 Confirmar Entrada"):

                entrada_estoque(produto_id, qtd)

                st.success("Entrada registrada!")
                st.rerun()

    # ==================================================
    # SAÍDA
    # ==================================================
    with abas[2]:

        df = listar_produtos()

        if not df.empty:

            produto_id = st.selectbox(
                "Produto ",
                df["id"],
                format_func=lambda x:
                f"{x} - {df[df['id']==x]['nome'].values[0]}"
            )

            estoque_atual = int(
                df[df["id"] == produto_id]["estoque"].values[0]
            )

            st.info(f"Estoque atual: {estoque_atual}")

            qtd = st.number_input(
                "Quantidade Saída",
                min_value=1,
                max_value=max(1, estoque_atual),
                step=1
            )

            if st.button("🗑️ Confirmar Saída"):

                if qtd > estoque_atual:
                    st.warning("Estoque insuficiente.")
                    st.stop()

                saida_estoque(produto_id, qtd)

                st.success("Saída registrada!")
                st.rerun()

    # ==================================================
    # ESTOQUE BAIXO
    # ==================================================
    with abas[3]:

        limite = st.number_input(
            "Mostrar produtos abaixo de:",
            min_value=0,
            value=5
        )

        df = listar_produtos()

        baixo = df[df["estoque"] <= limite]

        if not baixo.empty:

            st.warning("Produtos com estoque baixo")

            st.dataframe(
                baixo,
                use_container_width=True,
                hide_index=True
            )

        else:
            st.success("Nenhum produto com estoque baixo.")