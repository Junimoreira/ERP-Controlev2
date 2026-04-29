import streamlit as st
import pandas as pd
from database.connection import conectar


def dashboard():

    st.title("📊 Dashboard Estratégico")
    st.caption("Visão gerencial da loja")

    with conectar() as conn:

        # ==========================================
        # VENDAS DO MÊS
        # ==========================================
        vendas = pd.read_sql("""
            SELECT COALESCE(SUM(total),0) AS total
            FROM vendas
            WHERE DATE_TRUNC('month', data) =
                  DATE_TRUNC('month', CURRENT_DATE)
        """, conn)

        total_vendas = float(vendas["total"][0])

        # ==========================================
        # DESPESAS DO MÊS
        # ==========================================
        despesas = pd.read_sql("""
            SELECT COALESCE(SUM(valor),0) AS total
            FROM despesas
            WHERE DATE_TRUNC('month', vencimento) =
                  DATE_TRUNC('month', CURRENT_DATE)
        """, conn)

        total_despesas = float(despesas["total"][0])

        # ==========================================
        # PRODUTOS CADASTRADOS
        # ==========================================
        produtos = pd.read_sql("""
            SELECT COUNT(*) AS total
            FROM produtos
        """, conn)

        total_produtos = int(produtos["total"][0])

        # ==========================================
        # CLIENTES CADASTRADOS
        # ==========================================
        clientes = pd.read_sql("""
            SELECT COUNT(*) AS total
            FROM clientes
        """, conn)

        total_clientes = int(clientes["total"][0])

        # ==========================================
        # ESTOQUE BAIXO
        # ==========================================
        estoque = pd.read_sql("""
            SELECT COUNT(*) AS total
            FROM produtos
            WHERE estoque <= 5
        """, conn)

        estoque_baixo = int(estoque["total"][0])

    # ==========================================
    # CÁLCULOS
    # ==========================================
    meta = total_despesas * 1.20
    lucro = total_vendas - total_despesas
    faltam = max(0, meta - total_vendas)

    percentual = 0
    if meta > 0:
        percentual = min((total_vendas / meta) * 100, 100)

    # ==========================================
    # CARDS PRINCIPAIS
    # ==========================================
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "🛒 Vendas do Mês",
            f"R$ {total_vendas:,.2f}"
        )

    with col2:
        st.metric(
            "💸 Despesas",
            f"R$ {total_despesas:,.2f}"
        )

    with col3:
        st.metric(
            "💰 Lucro Atual",
            f"R$ {lucro:,.2f}"
        )

    st.divider()

    # ==========================================
    # META
    # ==========================================
    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "🎯 Meta do Mês (+20%)",
            f"R$ {meta:,.2f}"
        )

        st.metric(
            "📉 Falta Vender",
            f"R$ {faltam:,.2f}"
        )

    with col2:

        st.metric(
            "📈 Meta Atingida",
            f"{percentual:.1f}%"
        )

        st.progress(percentual / 100)

    st.divider()

    # ==========================================
    # INDICADORES
    # ==========================================
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "📦 Produtos",
            total_produtos
        )

    with col2:
        st.metric(
            "👤 Clientes",
            total_clientes
        )

    with col3:
        st.metric(
            "⚠️ Estoque Baixo",
            estoque_baixo
        )

    st.divider()

    # ==========================================
    # STATUS META
    # ==========================================
    if percentual >= 100:
        st.success("🏆 Meta batida! Excelente resultado.")
    elif percentual >= 80:
        st.info("🚀 Faltando pouco para bater a meta.")
    elif percentual >= 50:
        st.warning("⚡ Meta em andamento.")
    else:
        st.error("🔴 Atenção: vendas abaixo do esperado.")