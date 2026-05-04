import streamlit as st
import pandas as pd
from database.connection import conectar
from datetime import date


def tela_vendas():

    st.subheader("🛒 Vendas")

    # ================================
    # SESSION
    # ================================
    if "carrinho" not in st.session_state:
        st.session_state.carrinho = []

    def limpar_carrinho():
        st.session_state.carrinho = []

    def remover_item(index):
        st.session_state.carrinho.pop(index)

    abas = st.tabs(["🛍 Nova Venda", "📋 Histórico"])

    # ================================
    # NOVA VENDA
    # ================================
    with abas[0]:

        with conectar() as conn:

            # ---------------- CLIENTE ----------------
            clientes = pd.read_sql(
                "SELECT id, nome FROM clientes ORDER BY nome",
                conn
            )

            cliente_map = dict(zip(clientes["nome"], clientes["id"]))
            cliente_nome = st.selectbox("👤 Cliente", list(cliente_map.keys()))
            cliente_id = cliente_map[cliente_nome]

            data_venda = st.date_input("📅 Data", value=date.today())

            forma = st.selectbox(
                "💳 Forma de Pagamento",
                ["Dinheiro", "PIX", "Cartão"]
            )

            st.markdown("---")

            # ---------------- BUSCA PRODUTO ----------------
            busca = st.text_input("🔎 Buscar produto")

            if busca:

                query = """
                    SELECT id, nome, preco, estoque, codigo_barras
                    FROM produtos
                    WHERE nome ILIKE %s
                       OR codigo_barras ILIKE %s
                    ORDER BY nome
                    LIMIT 20
                """

                df = pd.read_sql(
                    query,
                    conn,
                    params=(f"%{busca}%", f"%{busca}%")
                )

                if not df.empty:

                    produto_map = {
                        f'{row["nome"]} (R$ {row["preco"]:.2f})': row
                        for _, row in df.iterrows()
                    }

                    produto_sel = st.selectbox("Produto", list(produto_map.keys()))
                    linha = produto_map[produto_sel]

                    preco = float(linha["preco"])
                    estoque = int(linha["estoque"])

                    col1, col2, col3 = st.columns(3)

                    with col1:
                        st.info(f"💲 R$ {preco:.2f}")

                    with col2:
                        st.info(f"📦 Estoque: {estoque}")

                    with col3:
                        qtd = st.number_input(
                            "Qtd",
                            min_value=1,
                            max_value=max(1, estoque),
                            value=1
                        )

                    if st.button("➕ Adicionar"):

                        if estoque <= 0:
                            st.error("Sem estoque")
                        else:
                            subtotal = preco * qtd

                            st.session_state.carrinho.append({
                                "id": int(linha["id"]),
                                "nome": linha["nome"],
                                "preco": preco,
                                "qtd": int(qtd),
                                "subtotal": subtotal
                            })

                            st.success("Produto adicionado!")
                            st.rerun()

                else:
                    st.warning("Produto não encontrado")

        # ---------------- CARRINHO ----------------
        st.markdown("### 🛒 Carrinho")

        if st.session_state.carrinho:

            carrinho = pd.DataFrame(st.session_state.carrinho)

            st.dataframe(carrinho, use_container_width=True, hide_index=True)

            subtotal = carrinho["subtotal"].sum()

            desconto = st.number_input("Desconto (R$)", min_value=0.0)

            total = max(subtotal - desconto, 0)

            st.markdown(f"Subtotal: R$ {subtotal:.2f}")
            st.markdown(f"Desconto: R$ {desconto:.2f}")
            st.success(f"💰 Total da Venda: R$ {total:.2f}")

            # REMOVER ITEM
            nomes = [
                f'{i+1} - {item["nome"]}'
                for i, item in enumerate(st.session_state.carrinho)
            ]

            colr1, colr2 = st.columns([3, 1])

            with colr1:
                item_remover = st.selectbox("Remover item", nomes)

            with colr2:
                if st.button("🗑"):
                    indice = nomes.index(item_remover)
                    remover_item(indice)
                    st.rerun()

            # FINALIZAR VENDA
            if st.button("✅ Finalizar Venda"):

                if total <= 0:
                    st.error("Total inválido")
                    st.stop()

                try:
                    with conectar() as conn:
                        with conn.cursor() as cur:

                            # INSERT VENDA
                            cur.execute("""
                                INSERT INTO vendas
                                (cliente_id, data, total, desconto, forma_pagamento)
                                VALUES (%s,%s,%s,%s,%s)
                                RETURNING id
                            """, (
                                cliente_id,
                                data_venda,
                                float(total),
                                float(desconto),
                                forma
                            ))

                            venda_id = cur.fetchone()[0]

                            # ITENS + ESTOQUE
                            for item in st.session_state.carrinho:

                                cur.execute("""
                                    INSERT INTO itens_venda
                                    (venda_id, produto_id, quantidade, preco_unitario, subtotal)
                                    VALUES (%s,%s,%s,%s,%s)
                                """, (
                                    venda_id,
                                    item["id"],
                                    item["qtd"],
                                    item["preco"],
                                    item["subtotal"]
                                ))

                                # atualização segura de estoque
                                cur.execute("""
                                    UPDATE produtos
                                    SET estoque = estoque - %s
                                    WHERE id = %s AND estoque >= %s
                                """, (
                                    item["qtd"],
                                    item["id"],
                                    item["qtd"]
                                ))

                                if cur.rowcount == 0:
                                    raise Exception(f'Estoque insuficiente para {item["nome"]}')

                            conn.commit()

                    st.success("Venda finalizada com sucesso!")
                    limpar_carrinho()
                    st.rerun()

                except Exception as e:
                    st.error(f"Erro ao finalizar venda: {e}")

        else:
            st.info("Carrinho vazio")

    # ================================
    # HISTÓRICO
    # ================================
    with abas[1]:

        with conectar() as conn:

            df = pd.read_sql("""
                SELECT 
                    v.id,
                    v.data,
                    c.nome AS cliente,
                    v.total,
                    v.desconto,
                    v.forma_pagamento
                FROM vendas v
                LEFT JOIN clientes c ON c.id = v.cliente_id
                ORDER BY v.id DESC
            """, conn)

        if not df.empty:

            df["data"] = pd.to_datetime(df["data"]).dt.strftime("%d/%m/%Y")
            df["total"] = df["total"].apply(lambda x: f"R$ {x:.2f}")

            st.dataframe(df, use_container_width=True, hide_index=True)

        else:
            st.info("Nenhuma venda registrada")