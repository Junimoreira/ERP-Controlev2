import streamlit as st
from database.connection import conectar


def dashboard():

    st.subheader("🏠 Dashboard Financeiro")

    with conectar() as conn:
        with conn.cursor() as cur:

            # Entradas mês
            cur.execute("""
                SELECT COALESCE(SUM(valor),0)
                FROM financeiro
                WHERE tipo='Entrada'
                AND DATE_TRUNC('month', data)=DATE_TRUNC('month', CURRENT_DATE)
            """)
            entradas = cur.fetchone()[0]

            # Saídas mês
            cur.execute("""
                SELECT COALESCE(SUM(valor),0)
                FROM financeiro
                WHERE tipo='Saída'
                AND DATE_TRUNC('month', data)=DATE_TRUNC('month', CURRENT_DATE)
            """)
            saidas = cur.fetchone()[0]

            saldo = entradas - saidas

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("💰 Entradas", f"R$ {entradas:,.2f}")

    with col2:
        st.metric("💸 Saídas", f"R$ {saidas:,.2f}")

    with col3:
        st.metric("📈 Saldo", f"R$ {saldo:,.2f}")