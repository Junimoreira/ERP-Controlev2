import streamlit as st
import pandas as pd
from database import conectar

def tela_financeiro():

    st.title("📊 Financeiro")

    abas = st.tabs([
        "Resumo",
        "Contas a Pagar",
        "Contas a Receber",
        "Despesas",
        "Fluxo Caixa"
    ])

    # ==================================================
    # RESUMO
    # ==================================================
    with abas[0]:

        with conectar() as conn:
            with conn.cursor() as cur:

                cur.execute("SELECT COALESCE(SUM(valor),0) FROM entradas")
                entradas = float(cur.fetchone()[0])

                cur.execute("SELECT COALESCE(SUM(valor),0) FROM saidas")
                saidas = float(cur.fetchone()[0])

                cur.execute("SELECT COALESCE(SUM(valor),0) FROM despesas")
                despesas = float(cur.fetchone()[0])

        saldo = entradas - saidas - despesas

        c1, c2, c3, c4 = st.columns(4)

        c1.metric("📥 Entradas", f"R$ {entradas:.2f}")
        c2.metric("📤 Saídas", f"R$ {saidas:.2f}")
        c3.metric("📉 Despesas", f"R$ {despesas:.2f}")
        c4.metric("💰 Saldo", f"R$ {saldo:.2f}")

    # ==================================================
    # CONTAS A PAGAR
    # ==================================================
    with abas[1]:

        st.subheader("📄 Nova Conta a Pagar")

        with st.form("form_conta_pagar", clear_on_submit=True):

            descricao = st.text_input("Descrição")
            valor = st.number_input("Valor", min_value=0.0, value=0.0)

            salvar = st.form_submit_button("Salvar Conta")

            if salvar:

                with conectar() as conn:
                    with conn.cursor() as cur:

                        cur.execute("""
                            INSERT INTO contas_pagar
                            (descricao, valor)
                            VALUES (%s,%s)
                        """, (descricao, valor))

                        conn.commit()

                st.success("Conta salva!")
                st.rerun()

        st.markdown("---")

        with conectar() as conn:
            df = pd.read_sql(
                "SELECT * FROM contas_pagar ORDER BY id DESC",
                conn
            )

        st.dataframe(df, use_container_width=True)

    # ==================================================
    # CONTAS A RECEBER
    # ==================================================
    with abas[2]:

        st.subheader("💳 Contas a Receber")

        with conectar() as conn:
            df = pd.read_sql("""
                SELECT *
                FROM contas_receber
                ORDER BY id DESC
            """, conn)

        st.dataframe(df, use_container_width=True)

    # ==================================================
    # DESPESAS
    # ==================================================
    with abas[3]:

        st.subheader("📉 Nova Despesa")

        with st.form("form_despesa", clear_on_submit=True):

            descricao = st.text_input("Descrição")
            valor = st.number_input("Valor", min_value=0.0, value=0.0)

            tipo = st.selectbox(
                "Tipo",
                ["Fixa", "Variável"],
                index=None,
                placeholder="Selecione"
            )

            salvar = st.form_submit_button("Salvar Despesa")

            if salvar:

                with conectar() as conn:
                    with conn.cursor() as cur:

                        cur.execute("""
                            INSERT INTO despesas
                            (descricao, valor, tipo)
                            VALUES (%s,%s,%s)
                        """, (descricao, valor, tipo))

                        conn.commit()

                st.success("Despesa salva!")
                st.rerun()

        st.markdown("---")

        with conectar() as conn:
            df = pd.read_sql("""
                SELECT *
                FROM despesas
                ORDER BY id DESC
            """, conn)

        st.dataframe(df, use_container_width=True)

    # ==================================================
    # FLUXO DE CAIXA
    # ==================================================
    with abas[4]:

        st.subheader("💰 Fluxo de Caixa")

        with conectar() as conn:

            df1 = pd.read_sql("""
                SELECT descricao, valor, 'Entrada' tipo
                FROM entradas
            """, conn)

            df2 = pd.read_sql("""
                SELECT descricao, valor, 'Saída' tipo
                FROM saidas
            """, conn)

        df = pd.concat([df1, df2])

        st.dataframe(df, use_container_width=True)