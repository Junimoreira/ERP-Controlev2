import streamlit as st
import pandas as pd
from database.connection import conectar


def get_vendas_mes():
    with conectar() as conn:
        df = pd.read_sql("""
            SELECT COALESCE(SUM(total),0) as total
            FROM vendas
            WHERE DATE_TRUNC('month', data) = DATE_TRUNC('month', CURRENT_DATE)
        """, conn)
        return float(df["total"][0])


def dashboard():

    st.title("📊 Dashboard Estratégico")
    st.caption("Visão gerencial da loja")

    with conectar() as conn:

        # =========================
        # VENDAS
        # =========================
        vendas = pd.read_sql("""
            SELECT COALESCE(SUM(total),0) AS total
            FROM vendas
            WHERE DATE_TRUNC('month', data) =
                  DATE_TRUNC('month', CURRENT_DATE)
        """, conn)

        total_vendas = float(vendas["total"][0])

        # =========================
        # DESPESAS
        # =========================
        despesas = pd.read_sql("""
            SELECT COALESCE(SUM(valor),0) AS total
            FROM despesas
            WHERE DATE_TRUNC('month', vencimento) =
                  DATE_TRUNC('month', CURRENT_DATE)
        """, conn)

        total_despesas = float(despesas["total"][0])

        # =========================
        # PRODUTOS
        # =========================
        produtos = pd.read_sql("SELECT COUNT(*) AS total FROM produtos", conn)
        total_produtos = int(produtos["total"][0])

        # =========================
        # CLIENTES
        # =========================
        clientes = pd.read_sql("SELECT COUNT(*) AS total FROM clientes", conn)
        total_clientes = int(clientes["total"][0])

        # =========================
        # ESTOQUE BAIXO
        # =========================
        estoque = pd.read_sql("""
            SELECT COUNT(*) AS total
            FROM produtos
            WHERE estoque <= 5
        """, conn)

        estoque_baixo = int(estoque["total"][0])

    # =========================
    # CÁLCULOS
    # =========================
    meta = total_despesas * 1.20
    lucro = total_vendas - total_despesas
    faltam = max(0, meta - total_vendas)

    percentual = (total_vendas / meta * 100) if meta > 0 else 0
    percentual = min(percentual, 100)

    # =========================
    # CARDS
    # =========================
    col1, col2, col3 = st.columns(3)

    col1.metric("🛒 Vendas do Mês", f"R$ {total_vendas:,.2f}")
    col2.metric("💸 Despesas", f"R$ {total_despesas:,.2f}")
    col3.metric("💰 Lucro", f"R$ {lucro:,.2f}")

    st.divider()

    # =========================
    # META
    # =========================
    col1, col2 = st.columns(2)

    col1.metric("🎯 Meta (+20%)", f"R$ {meta:,.2f}")
    col1.metric("📉 Falta", f"R$ {faltam:,.2f}")

    col2.metric("📈 Atingido", f"{percentual:.1f}%")
    st.progress(percentual / 100)

    st.divider()

    # =========================
    # INDICADORES
    # =========================
    col1, col2, col3 = st.columns(3)

    col1.metric("📦 Produtos", total_produtos)
    col2.metric("👤 Clientes", total_clientes)
    col3.metric("⚠️ Estoque Baixo", estoque_baixo)

    st.divider()

    # =========================
    # STATUS
    # =========================
    if percentual >= 100:
        st.success("🏆 Meta batida!")
    elif percentual >= 80:
        st.info("🚀 Quase lá!")
    elif percentual >= 50:
        st.warning("⚡ Em andamento")
    else:
        st.error("🔴 Abaixo da meta")