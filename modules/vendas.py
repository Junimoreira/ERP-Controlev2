import streamlit as st
from database import conectar


def tela_vendas():

    st.title("💰 Vendas")

    with conectar() as conn:
        with conn.cursor() as cur:

            # ---------------------------------
            # CLIENTES
            # ---------------------------------
            cur.execute("""
                SELECT id, nome
                FROM clientes
                ORDER BY nome
            """)
            clientes = cur.fetchall()

            clientes_dict = {c[1]: c[0] for c in clientes}

            lista_clientes = ["Selecione..."] + list(clientes_dict.keys())

            cliente_nome = st.selectbox(
                "Cliente",
                lista_clientes,
                key="venda_cliente"
            )

            # ---------------------------------
            # PRODUTOS
            # ---------------------------------
            cur.execute("""
                SELECT id, nome, preco, estoque
                FROM produtos
                ORDER BY nome
            """)
            produtos = cur.fetchall()

            produtos_dict = {
                f"{p[1]} | R$ {float(p[2]):.2f} | Estoque {p[3]}": p
                for p in produtos
            }

            lista_produtos = ["Selecione..."] + list(produtos_dict.keys())

            produto_nome = st.selectbox(
                "Produto",
                lista_produtos,
                key="venda_produto"
            )

            # ---------------------------------
            # CAMPOS
            # ---------------------------------
            quantidade = st.number_input(
                "Quantidade",
                min_value=1,
                value=1,
                key="venda_qtd"
            )

            desconto = st.number_input(
                "Desconto",
                min_value=0.0,
                value=0.0,
                key="venda_desc"
            )

            forma = st.selectbox(
                "Forma de Pagamento",
                ["Selecione...", "Dinheiro", "Pix", "Cartão"],
                key="venda_forma"
            )

            # ---------------------------------
            # VALIDAÇÃO INICIAL
            # ---------------------------------
            if cliente_nome == "Selecione..." or produto_nome == "Selecione...":
                st.info("Selecione cliente e produto para continuar.")
                return

            produto = produtos_dict[produto_nome]

            produto_id = produto[0]
            nome_produto = produto[1]
            preco = float(produto[2])
            estoque = int(produto[3])

            # ---------------------------------
            # TOTAL
            # ---------------------------------
            total = (preco * quantidade) - desconto

            if total < 0:
                total = 0

            st.metric("Total da Venda", f"R$ {total:.2f}")

            # ---------------------------------
            # BOTÃO
            # ---------------------------------
            if st.button("Finalizar Venda", use_container_width=True):

                if forma == "Selecione...":
                    st.error("Selecione a forma de pagamento.")
                    return

                if quantidade > estoque:
                    st.error("Estoque insuficiente.")
                    return

                # salva venda
                cur.execute("""
                    INSERT INTO vendas
                    (cliente_id, total, desconto, forma_pagamento)
                    VALUES (%s,%s,%s,%s)
                """, (
                    clientes_dict[cliente_nome],
                    total,
                    desconto,
                    forma
                ))

                # baixa estoque
                cur.execute("""
                    UPDATE produtos
                    SET estoque = estoque - %s
                    WHERE id = %s
                """, (
                    quantidade,
                    produto_id
                ))

                # financeiro
                cur.execute("""
                    INSERT INTO entradas
                    (descricao, valor)
                    VALUES (%s,%s)
                """, (
                    f"Venda - {nome_produto}",
                    total
                ))

                conn.commit()

                # ---------------------------------
                # LIMPAR CAMPOS
                # ---------------------------------
                st.session_state.venda_cliente = "Selecione..."
                st.session_state.venda_produto = "Selecione..."
                st.session_state.venda_qtd = 1
                st.session_state.venda_desc = 0.0
                st.session_state.venda_forma = "Selecione..."

                st.success("Venda realizada com sucesso!")
                st.rerun()