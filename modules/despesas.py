import streamlit as st
import pandas as pd
from database.connection import conectar


# ======================================
# FUNÇÕES
# ======================================

def listar_despesas():

    with conectar() as conn:

        df = pd.read_sql("""
            SELECT id,
                   descricao,
                   valor,
                   vencimento,
                   categoria,
                   observacao
            FROM despesas
            ORDER BY vencimento ASC NULLS LAST, id DESC
        """, conn)

    return df


def inserir_despesa(descricao, valor, vencimento, categoria, observacao):

    with conectar() as conn:
        with conn.cursor() as cur:

            cur.execute("""
                INSERT INTO despesas
                (descricao, valor, vencimento, categoria, observacao)
                VALUES (%s,%s,%s,%s,%s)
            """, (
                descricao,
                valor,
                vencimento,
                categoria,
                observacao
            ))

            conn.commit()


def atualizar_despesa(id, descricao, valor, vencimento, categoria, observacao):

    with conectar() as conn:
        with conn.cursor() as cur:

            cur.execute("""
                UPDATE despesas
                SET descricao=%s,
                    valor=%s,
                    vencimento=%s,
                    categoria=%s,
                    observacao=%s
                WHERE id=%s
            """, (
                descricao,
                valor,
                vencimento,
                categoria,
                observacao,
                id
            ))

            conn.commit()


def excluir_despesa(id):

    with conectar() as conn:
        with conn.cursor() as cur:

            cur.execute(
                "DELETE FROM despesas WHERE id=%s",
                (id,)
            )

            conn.commit()


# ======================================
# TELA
# ======================================

def tela_despesas():

    st.title("💸 Controle de Despesas")
    st.caption("Cadastre e acompanhe os custos fixos e variáveis da loja")

    aba1, aba2, aba3 = st.tabs([
        "➕ Nova Despesa",
        "📋 Lista",
        "📈 Resumo"
    ])

    # ======================================
    # NOVA DESPESA
    # ======================================
    with aba1:

        with st.form("form_despesa", clear_on_submit=True):

            descricao = st.text_input("Descrição")

            valor = st.number_input(
                "Valor",
                min_value=0.0,
                step=0.01,
                format="%.2f"
            )

            vencimento = st.date_input("Vencimento")

            categoria = st.selectbox(
                "Categoria",
                [
                    "Fixa",
                    "Variável",
                    "Impostos",
                    "Marketing",
                    "Funcionários",
                    "Outros"
                ]
            )

            observacao = st.text_area("Observação")

            salvar = st.form_submit_button("💾 Salvar")

            if salvar:

                if descricao.strip() == "":
                    st.warning("Informe a descrição.")
                    st.stop()

                inserir_despesa(
                    descricao,
                    valor,
                    vencimento,
                    categoria,
                    observacao
                )

                st.success("Despesa cadastrada com sucesso!")
                st.rerun()

    # ======================================
    # LISTA
    # ======================================
    with aba2:

        busca = st.text_input("🔎 Buscar despesa")

        df = listar_despesas()

        if busca:
            df = df[
                df["descricao"].str.contains(
                    busca,
                    case=False,
                    na=False
                )
            ]

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

        st.caption(f"Total registros: {len(df)}")

        st.divider()

        if not df.empty:

            despesa_id = st.selectbox(
                "Selecione para editar",
                df["id"],
                format_func=lambda x:
                f"{x} - {df[df['id']==x]['descricao'].values[0]}"
            )

            linha = df[df["id"] == despesa_id].iloc[0]

            st.subheader("✏️ Editar Despesa")

            descricao = st.text_input(
                "Descrição ",
                value=linha["descricao"]
            )

            valor = st.number_input(
                "Valor ",
                min_value=0.0,
                value=float(linha["valor"]),
                step=0.01,
                format="%.2f"
            )

            vencimento = st.date_input(
                "Vencimento ",
                value=linha["vencimento"]
            )

            categoria = st.selectbox(
                "Categoria ",
                [
                    "Fixa",
                    "Variável",
                    "Impostos",
                    "Marketing",
                    "Funcionários",
                    "Outros"
                ],
                index=[
                    "Fixa",
                    "Variável",
                    "Impostos",
                    "Marketing",
                    "Funcionários",
                    "Outros"
                ].index(linha["categoria"])
                if linha["categoria"] in [
                    "Fixa",
                    "Variável",
                    "Impostos",
                    "Marketing",
                    "Funcionários",
                    "Outros"
                ] else 0
            )

            observacao = st.text_area(
                "Observação ",
                value=linha["observacao"]
                if linha["observacao"] else ""
            )

            col1, col2 = st.columns(2)

            with col1:

                if st.button("💾 Atualizar"):

                    atualizar_despesa(
                        despesa_id,
                        descricao,
                        valor,
                        vencimento,
                        categoria,
                        observacao
                    )

                    st.success("Atualizado!")
                    st.rerun()

            with col2:

                confirmar = st.checkbox(
                    "Confirmar exclusão"
                )

                if st.button("🗑️ Excluir"):

                    if not confirmar:
                        st.warning("Confirme antes.")
                        st.stop()

                    excluir_despesa(despesa_id)

                    st.warning("Excluído!")
                    st.rerun()

    # ======================================
    # RESUMO
    # ======================================
    with aba3:

        df = listar_despesas()

        total = 0

        if not df.empty:
            total = float(df["valor"].sum())

        meta_20 = total * 1.20

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "💸 Total Despesas",
                f"R$ {total:,.2f}"
            )

        with col2:
            st.metric(
                "🎯 Meta +20%",
                f"R$ {meta_20:,.2f}"
            )