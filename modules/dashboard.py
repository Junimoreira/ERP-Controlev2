import streamlit as st
from datetime import datetime
from database import conectar

def dashboard():

    st.title("🏠 Dashboard Financeiro")

    mes_atual = datetime.now().strftime("%m/%Y")

    with conectar() as conn:
        with conn.cursor() as cur:

            # ==================================================
            # VENDAS DO MÊS (CORRIGIDO)
            # ==================================================
            cur.execute("""
                SELECT COALESCE(SUM(valor),0)
                FROM entradas
                WHERE DATE_TRUNC('month', CURRENT_DATE)
                      = DATE_TRUNC('month', CURRENT_DATE)
            """)
            vendas = float(cur.fetchone()[0])

            # ==================================================
            # DESPESAS DO MÊS
            # ==================================================
            cur.execute("""
                SELECT COALESCE(SUM(valor),0)
                FROM despesas
            """)
            despesas = float(cur.fetchone()[0])

            # ==================================================
            # TOTAL DE VENDAS
            # ==================================================
            cur.execute("""
                SELECT COUNT(*)
                FROM vendas
            """)
            qtd_vendas = int(cur.fetchone()[0])

            # ==================================================
            # CLIENTES
            # ==================================================
            cur.execute("""
                SELECT COUNT(*)
                FROM clientes
            """)
            clientes = int(cur.fetchone()[0])

    # ==================================================
    # CÁLCULOS
    # ==================================================
    lucro = vendas - despesas
    meta_lucro = despesas * 1.20

    percentual = 0
    if meta_lucro > 0:
        percentual = (vendas / meta_lucro) * 100

    # ==================================================
    # KPIs
    # ==================================================
    c1, c2, c3, c4 = st.columns(4)

    c1.metric("💰 Vendas do mês", f"R$ {vendas:,.2f}")
    c2.metric("📉 Despesas", f"R$ {despesas:,.2f}")
    c3.metric("📈 Resultado", f"R$ {lucro:,.2f}")
    c4.metric("🎯 Meta +20%", f"R$ {meta_lucro:,.2f}")

    st.markdown("---")

    c5, c6 = st.columns(2)
    c5.metric("🧾 Total de Vendas", qtd_vendas)
    c6.metric("👥 Clientes", clientes)

    st.markdown("---")

    # ==================================================
    # SAÚDE FINANCEIRA
    # ==================================================
    st.subheader("📊 Saúde Financeira")

    if vendas < despesas:
        st.error("❌ As vendas ainda não pagam as despesas.")

    elif vendas >= despesas and vendas < meta_lucro:
        st.warning("⚠️ Empresa paga as contas, porém lucro abaixo da meta.")

    else:
        st.success("✅ Empresa saudável! Meta de lucro atingida.")

    # ==================================================
    # BARRA DE META
    # ==================================================
    progresso = min(int(percentual), 100)

    st.progress(progresso)

    st.write(f"Meta atingida em {percentual:.1f}% no mês {mes_atual}")

    # ==================================================
    # DICAS
    # ==================================================
    st.markdown("---")
    st.subheader("📌 Diagnóstico")

    if vendas == 0:
        st.info("Nenhuma venda registrada no mês.")

    elif lucro < 0:
        st.warning("Lucro negativo. Reduza despesas ou aumente vendas.")

    elif lucro > 0 and percentual < 100:
        st.info("Empresa lucrando, mas ainda abaixo da meta ideal.")

    else:
        st.success("Excelente desempenho financeiro.")