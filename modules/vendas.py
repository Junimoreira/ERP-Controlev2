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
    import streamlit as st
import pandas as pd
from database.connection import conectar
from datetime import date


def tela_vendas():

    st.subheader("🛒 Vendas")

    # ==================================================
    # SESSION STATE
    # ==================================================
    if "carrinho" not in st.session_state:
        st.session_state.carrinho = []

    # ==================================================
    # FUNÇÕES AUXILIARES
    # ==================================================
    def limpar_carrinho():
        st.session_state.carrinho = []

    def remover_item(index):
        st.session_state.carrinho.pop(index)

    # ==================================================
    # ABAS
    # ==================================================
    abas = st.tabs(["🛍 Nova Venda", "📋 Histórico"])

    # ==================================================
    # NOVA VENDA
    # ==================================================
    with abas[0]:

        st.markdown("## 🧾 Nova Venda")

        col1, col2 = st.columns(2)

        with col1:
            cliente = st.text_input("👤 Cliente")

        with col2:
            data_venda = st.date_input(
                "📅 Data da Venda",
                value=date.today()
            )

        forma = st.selectbox(
            "💳 Forma de Pagamento",
            ["Dinheiro", "PIX", "Cartão Débito", "Cartão Crédito"]
        )

        st.markdown("---")

        # ==================================================
        # BUSCA PRODUTO
        # ==================================================
        st.markdown("### 🔎 Buscar Produto")

        busca = st.text_input(
            "Digite nome, código interno ou código de barras"
        )

        with conectar() as conn:

            if busca:

                query = """
                    SELECT id,
                           nome,
                           preco,
                           estoque,
                           codigo_barras
                    FROM produtos
                    WHERE nome ILIKE %s
                       OR CAST(id AS TEXT) ILIKE %s
                       OR codigo_barras ILIKE %s
                    ORDER BY nome
                    LIMIT 20
                """

                df = pd.read_sql(
                    query,
                    conn,
                    params=(
                        f"%{busca}%",
                        f"%{busca}%",
                        f"%{busca}%"
                    )
                )

                if not df.empty:

                    produto = st.selectbox(
                        "Produto encontrado",
                        df["nome"]
                    )

                    linha = df[df["nome"] == produto].iloc[0]

                    estoque = int(linha["estoque"])
                    preco = float(linha["preco"])

                    colp1, colp2, colp3 = st.columns(3)

                    with colp1:
                        st.info(f"💲 Preço: R$ {preco:.2f}")

                    with colp2:
                        st.info(f"📦 Estoque: {estoque}")

                    with colp3:
                        qtd = st.number_input(
                            "Qtd",
                            min_value=1,
                            max_value=max(1, estoque),
                            value=1,
                            step=1
                        )

                    if st.button("➕ Adicionar Produto"):

                        if estoque <= 0:
                            st.error("Produto sem estoque.")
                        else:
                            subtotal = preco * qtd

                            st.session_state.carrinho.append({
                                "id": int(linha["id"]),
                                "nome": linha["nome"],
                                "preco": preco,
                                "qtd": int(qtd),
                                "subtotal": subtotal
                            })

                            st.success("Produto adicionado.")
                            st.rerun()

                else:
                    st.warning("Nenhum produto encontrado.")

        # ==================================================
        # CARRINHO
        # ==================================================
        st.markdown("---")
        st.markdown("### 🛒 Carrinho")

        if st.session_state.carrinho:

            carrinho = pd.DataFrame(st.session_state.carrinho)

            # tabela amigável
            exibir = carrinho.copy()
            exibir["preco"] = exibir["preco"].map(
                lambda x: f"R$ {x:.2f}"
            )
            exibir["subtotal"] = exibir["subtotal"].map(
                lambda x: f"R$ {x:.2f}"
            )

            st.dataframe(
                exibir,
                use_container_width=True,
                hide_index=True
            )

            # remover item
            nomes = [
                f'{i+1} - {item["nome"]}'
                for i, item in enumerate(st.session_state.carrinho)
            ]

            colr1, colr2 = st.columns([3, 1])

            with colr1:
                item_remover = st.selectbox(
                    "Remover item",
                    nomes
                )

            with colr2:
                if st.button("🗑 Remover"):
                    indice = nomes.index(item_remover)
                    remover_item(indice)
                    st.rerun()

            # totais
            total = float(carrinho["subtotal"].sum())

            st.markdown("---")
            st.markdown("### 💸 Desconto")

            tipo_desc = st.selectbox(
                "Tipo de desconto",
                ["Nenhum", "Valor R$", "Percentual %"]
            )

            desconto = 0.0

            if tipo_desc == "Valor R$":
                desconto = st.number_input(
                    "Valor desconto",
                    min_value=0.0,
                    value=0.0,
                    step=1.0
                )

            elif tipo_desc == "Percentual %":
                perc = st.number_input(
                    "Percentual",
                    min_value=0.0,
                    max_value=100.0,
                    value=0.0,
                    step=1.0
                )
                desconto = total * (perc / 100)

            if desconto > total:
                desconto = total

            total_final = total - desconto

            st.markdown(f"### Subtotal: R$ {total:.2f}")
            st.markdown(f"### Desconto: R$ {desconto:.2f}")
            st.markdown(f"## 💰 Total Final: R$ {total_final:.2f}")

            colf1, colf2 = st.columns(2)

            # ==================================================
            # FINALIZAR
            # ==================================================
            with colf1:

                if st.button("✅ Finalizar Venda"):

                    if total_final <= 0:
                        st.error("Total inválido.")
                        st.stop()

                    with conectar() as conn:
                        with conn.cursor() as cur:

                            # grava venda
                            cur.execute("""
                                INSERT INTO vendas
                                (
                                    cliente,
                                    data,
                                    total,
                                    desconto,
                                    forma_pagamento
                                )
                                VALUES (%s,%s,%s,%s,%s)
                                RETURNING id
                            """, (
                                cliente,
                                data_venda,
                                float(total_final),
                                float(desconto),
                                forma
                            ))

                            venda_id = cur.fetchone()[0]

                            # grava itens
                            for item in st.session_state.carrinho:

                                cur.execute("""
                                    INSERT INTO itens_venda
                                    (
                                        venda_id,
                                        produto_id,
                                        quantidade,
                                        preco_unitario,
                                        subtotal
                                    )
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
                                    WHERE id = %s
                                """, (
                                    item["qtd"],
                                    item["id"]
                                ))

                            conn.commit()

                    st.success("Venda finalizada com sucesso.")
                    limpar_carrinho()
                    st.rerun()

            # ==================================================
            # CANCELAR
            # ==================================================
            with colf2:

                if st.button("❌ Cancelar Venda"):
                    limpar_carrinho()
                    st.warning("Carrinho limpo.")
                    st.rerun()

        else:
            st.info("Carrinho vazio.")

    # ==================================================
    # HISTÓRICO
    # ==================================================
    with abas[1]:

        st.markdown("## 📋 Histórico de Vendas")

        with conectar() as conn:

            df = pd.read_sql("""
                SELECT
                    id,
                    data,
                    cliente,
                    total,
                    desconto,
                    forma_pagamento
                FROM vendas
                ORDER BY id DESC
            """, conn)

        if not df.empty:

            df["total"] = df["total"].map(
                lambda x: f"R$ {float(x):.2f}"
            )

            df["desconto"] = df["desconto"].map(
                lambda x: f"R$ {float(x):.2f}"
            )

            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True
            )

        else:
            st.info("Nenhuma venda registrada.")

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