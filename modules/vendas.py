import streamlit as st
from database.connection import conectar

# ============================
# FUNÇÕES
# ============================

def buscar_clientes():
    with conectar() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id, nome FROM clientes ORDER BY nome")
            return cur.fetchall()


def buscar_produtos():
    with conectar() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT id, nome, preco, estoque
                FROM produtos
                ORDER BY nome
            """)
            return cur.fetchall()


def registrar_venda(cliente_id, total, desconto, forma, itens):
    with conectar() as conn:
        with conn.cursor() as cur:

            cur.execute("""
                INSERT INTO vendas (cliente_id, total, desconto, forma_pagamento)
                VALUES (%s,%s,%s,%s)
                RETURNING id
            """, (cliente_id, total, desconto, forma))

            venda_id = cur.fetchone()[0]

            for item in itens:
                cur.execute("""
                    UPDATE produtos
                    SET estoque = estoque - %s
                    WHERE id = %s
                """, (item["qtd"], item["id"]))

            cur.execute("""
                INSERT INTO entradas (descricao, valor)
                VALUES (%s,%s)
            """, ("Venda", total))

            conn.commit()


# ============================
# TELA
# ============================

def tela_vendas():

    st.title("💰 Vendas")

    clientes = buscar_clientes()
    produtos = buscar_produtos()

    clientes_dict = {c[1]: c[0] for c in clientes}
    produtos_dict = {p[1]: p for p in produtos}

    # ============================
    # CLIENTE
    # ============================
    cliente_nome = st.selectbox(
        "Cliente",
        ["Selecione..."] + list(clientes_dict.keys())
    )

    # ============================
    # PRODUTO
    # ============================
    produto_nome = st.selectbox(
        "Produto",
        ["Selecione..."] + list(produtos_dict.keys())
    )

    quantidade = st.number_input("Quantidade", min_value=1, value=1)

    # ============================
    # CARRINHO (session_state)
    # ============================
    if "carrinho" not in st.session_state:
        st.session_state.carrinho = []

    if st.button("➕ Adicionar ao Carrinho"):

        if produto_nome == "Selecione...":
            st.warning("Selecione um produto")
            return

        produto = produtos_dict[produto_nome]

        if quantidade > produto[3]:
            st.error("Estoque insuficiente")
            return

        st.session_state.carrinho.append({
            "id": produto[0],
            "nome": produto[1],
            "preco": float(produto[2]),
            "qtd": quantidade
        })

        st.success("Produto adicionado!")

    # ============================
    # MOSTRAR CARRINHO
    # ============================
    total = 0

    if st.session_state.carrinho:

        st.subheader("🛒 Carrinho")

        for item in st.session_state.carrinho:
            subtotal = item["preco"] * item["qtd"]
            total += subtotal

            st.write(f"{item['nome']} - {item['qtd']}x = R$ {subtotal:.2f}")

    # ============================
    # PAGAMENTO
    # ============================
    desconto = st.number_input("Desconto", min_value=0.0, value=0.0)

    forma = st.selectbox(
        "Forma de Pagamento",
        ["Selecione...", "Dinheiro", "Pix", "Cartão"]
    )

    total_final = max(total - desconto, 0)

    st.metric("Total", f"R$ {total_final:.2f}")

    # ============================
    # FINALIZAR
    # ============================
    if st.button("💾 Finalizar Venda"):

        if cliente_nome == "Selecione...":
            st.warning("Selecione um cliente")
            return

        if not st.session_state.carrinho:
            st.warning("Carrinho vazio")
            return

        if forma == "Selecione...":
            st.warning("Selecione forma de pagamento")
            return

        registrar_venda(
            clientes_dict[cliente_nome],
            total_final,
            desconto,
            forma,
            st.session_state.carrinho
        )

        st.session_state.carrinho = []

        st.success("Venda concluída!")
        st.rerun()