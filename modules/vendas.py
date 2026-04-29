import streamlit as st
import pandas as pd
from database.connection import conectar


def tela_vendas():

    st.subheader("🛒 Vendas")

    if "carrinho" not in st.session_state:
        st.session_state.carrinho = []

    abas = st.tabs(["🛍 Nova Venda", "📋 Histórico"])

    # ==================================================
    # NOVA VENDA
    # ==================================================
    with abas[0]:

        busca = st.text_input("Código de barras ou nome")

        with conectar() as conn:

            if busca:

                query = f"""
                    SELECT id, nome, preco, estoque, codigo_barras
                    FROM produtos
                    WHERE nome ILIKE '%{busca}%'
                    OR codigo_barras ILIKE '%{busca}%'
                    ORDER BY nome
                """

                df = pd.read_sql(query, conn)

                if not df.empty:

                    produto = st.selectbox(
                        "Produto",
                        df["nome"]
                    )

                    linha = df[df["nome"] == produto].iloc[0]

                    qtd = st.number_input(
                        "Quantidade",
                        1,
                        int(linha["estoque"]),
                        1
                    )

                    if st.button("Adicionar"):

                        st.session_state.carrinho.append({
                            "id": linha["id"],
                            "nome": linha["nome"],
                            "preco": float(linha["preco"]),
                            "qtd": qtd,
                            "subtotal": float(linha["preco"]) * qtd
                        })

                        st.success("Produto adicionado")
                        st.rerun()

        # ----------------------------
        # CARRINHO
        # ----------------------------
        st.markdown("### 🧾 Carrinho")

        if st.session_state.carrinho:

            carrinho = pd.DataFrame(st.session_state.carrinho)

            st.dataframe(
                carrinho,
                use_container_width=True,
                hide_index=True
            )

            total = carrinho["subtotal"].sum()

            st.markdown(f"## Total: R$ {total:.2f}")

            forma = st.selectbox(
                "Forma Pagamento",
                ["Dinheiro", "PIX", "Cartão"]
            )

            if st.button("Finalizar Venda"):

                with conectar() as conn:
                    with conn.cursor() as cur:

                        # salva venda
                        cur.execute("""
                            INSERT INTO vendas
                            (total, forma_pagamento)
                            VALUES (%s,%s)
                            RETURNING id
                        """, (total, forma))

                        venda_id = cur.fetchone()[0]

                        # itens venda
                        for item in st.session_state.carrinho:

                            cur.execute("""
                                INSERT INTO itens_venda
                                (venda_id, produto_id, quantidade,
                                 preco_unitario, subtotal)
                                VALUES (%s,%s,%s,%s,%s)
                            """, (
                                venda_id,
                                item["id"],
                                item["qtd"],
                                item["preco"],
                                item["subtotal"]
                            ))

                            # baixa estoque
                            cur.execute("""
                                UPDATE produtos
                                SET estoque = estoque - %s
                                WHERE id=%s
                            """, (
                                item["qtd"],
                                item["id"]
                            ))

                        conn.commit()

                st.success("Venda finalizada!")

                st.session_state.carrinho = []

                st.rerun()

    # ==================================================
    # HISTÓRICO
    # ==================================================
    with abas[1]:

        with conectar() as conn:

            df = pd.read_sql("""
                SELECT id, data, total, forma_pagamento
                FROM vendas
                ORDER BY id DESC
            """, conn)

        st.dataframe(df, use_container_width=True, hide_index=True)