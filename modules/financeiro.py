import streamlit as st
import pandas as pd
from database.connection import conectar


def tela_financeiro():

    st.subheader("💰 Financeiro")

    abas = st.tabs([
        "➕ Novo Lançamento",
        "📋 Movimentações",
        "📈 Resumo"
    ])

    # ==================================================
    # NOVO LANÇAMENTO
    # ==================================================
    with abas[0]:

        with st.form("form_financeiro"):

            tipo = st.selectbox(
                "Tipo",
                ["Entrada", "Saída"]
            )

            descricao = st.text_input("Descrição")

            valor = st.number_input(
                "Valor",
                min_value=0.0,
                step=0.01,
                format="%.2f"
            )

            data = st.date_input("Data")

            salvar = st.form_submit_button("💾 Salvar")

            if salvar:

                if descricao == "":
                    st.warning("Informe a descrição.")
                    st.stop()

                with conectar() as conn:
                    with conn.cursor() as cur:

                        cur.execute("""
                            INSERT INTO financeiro
                            (tipo, descricao, valor, data)
                            VALUES (%s,%s,%s,%s)
                        """, (
                            tipo,
                            descricao,
                            valor,
                            data
                        ))

                        conn.commit()

                st.success("Lançamento salvo com sucesso!")
                st.rerun()

    # ==================================================
    # MOVIMENTAÇÕES
    # ==================================================
    with abas[1]:

        st.markdown("### 📋 Histórico de Movimentações")

        with conectar() as conn:

            df = pd.read_sql("""
                SELECT id, tipo, descricao, valor, data
                FROM financeiro
                ORDER BY id DESC
            """, conn)

        if not df.empty:

            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True
            )

            st.markdown("### 🗑️ Excluir Lançamento")

            id_excluir = st.selectbox(
                "Selecione ID",
                df["id"]
            )

            if st.button("Excluir"):

                with conectar() as conn:
                    with conn.cursor() as cur:

                        cur.execute(
                            "DELETE FROM financeiro WHERE id=%s",
                            (int(id_excluir),)
                        )

                        conn.commit()

                st.success("Registro excluído.")
                st.rerun()

        else:
            st.info("Nenhum lançamento encontrado.")

    # ==================================================
    # RESUMO
    # ==================================================
    with abas[2]:

        with conectar() as conn:
            with conn.cursor() as cur:

                cur.execute("""
                    SELECT COALESCE(SUM(valor),0)
                    FROM financeiro
                    WHERE tipo='Entrada'
                """)
                entradas = float(cur.fetchone()[0])

                cur.execute("""
                    SELECT COALESCE(SUM(valor),0)
                    FROM financeiro
                    WHERE tipo='Saída'
                """)
                saidas = float(cur.fetchone()[0])

        saldo = entradas - saidas

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("💰 Entradas", f"R$ {entradas:,.2f}")

        with col2:
            st.metric("💸 Saídas", f"R$ {saidas:,.2f}")

        with col3:
            st.metric("📈 Saldo", f"R$ {saldo:,.2f}")