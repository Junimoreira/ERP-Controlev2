import streamlit as st
import pandas as pd
from database.connection import conectar


# =====================================================
# FUNÇÕES BANCO
# =====================================================

def listar_clientes(busca=""):

    sql = """
        SELECT
            id,
            tipo,
            nome,
            documento,
            ie,
            telefone,
            whatsapp,
            email,
            cep,
            endereco,
            numero,
            bairro,
            cidade,
            estado,
            complemento,
            ativo
        FROM clientes
        WHERE 1=1
    """

    params = []

    if busca:
        sql += """
            AND (
                nome ILIKE %s
                OR documento ILIKE %s
                OR telefone ILIKE %s
            )
        """
        params.extend([
            f"%{busca}%",
            f"%{busca}%",
            f"%{busca}%"
        ])

    sql += " ORDER BY nome"

    with conectar() as conn:
        return pd.read_sql(sql, conn, params=params)


def inserir_cliente(dados):

    with conectar() as conn:
        with conn.cursor() as cur:

            cur.execute("""
                INSERT INTO clientes (
                    tipo,
                    nome,
                    documento,
                    ie,
                    telefone,
                    whatsapp,
                    email,
                    cep,
                    endereco,
                    numero,
                    bairro,
                    cidade,
                    estado,
                    complemento,
                    ativo
                )
                VALUES (
                    %s,%s,%s,%s,%s,%s,%s,
                    %s,%s,%s,%s,%s,%s,%s,%s
                )
            """, dados)

            conn.commit()


def atualizar_cliente(cliente_id, dados):

    with conectar() as conn:
        with conn.cursor() as cur:

            cur.execute("""
                UPDATE clientes
                SET
                    tipo=%s,
                    nome=%s,
                    documento=%s,
                    ie=%s,
                    telefone=%s,
                    whatsapp=%s,
                    email=%s,
                    cep=%s,
                    endereco=%s,
                    numero=%s,
                    bairro=%s,
                    cidade=%s,
                    estado=%s,
                    complemento=%s,
                    ativo=%s
                WHERE id=%s
            """, (*dados, cliente_id))

            conn.commit()


def excluir_cliente(cliente_id):

    with conectar() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "DELETE FROM clientes WHERE id=%s",
                (cliente_id,)
            )
            conn.commit()


# =====================================================
# TELA
# =====================================================

def tela_clientes():

    st.title("👥 Clientes Premium")
    st.caption("Cadastro completo integrado ao ERP")

    abas = st.tabs([
        "➕ Novo Cliente",
        "📋 Consultar / Editar"
    ])

    # =====================================================
    # NOVO CLIENTE
    # =====================================================
    with abas[0]:

        with st.form("form_cliente", clear_on_submit=True):

            st.markdown("### Dados Principais")

            col1, col2 = st.columns(2)

            with col1:
                tipo = st.selectbox(
                    "Tipo",
                    ["Pessoa Física", "Pessoa Jurídica"]
                )

                nome = st.text_input(
                    "Nome"
                    if tipo == "Pessoa Física"
                    else "Razão Social"
                )

                documento = st.text_input(
                    "CPF"
                    if tipo == "Pessoa Física"
                    else "CNPJ"
                )

                ie = st.text_input("Inscrição Estadual")

                telefone = st.text_input("Telefone")

            with col2:
                whatsapp = st.text_input("WhatsApp")
                email = st.text_input("Email")
                cep = st.text_input("CEP")
                endereco = st.text_input("Endereço")
                numero = st.text_input("Número")

            st.markdown("### Endereço")

            col3, col4, col5 = st.columns(3)

            with col3:
                bairro = st.text_input("Bairro")

            with col4:
                cidade = st.text_input("Cidade")

            with col5:
                estado = st.text_input(
                    "UF",
                    max_chars=2
                )

            complemento = st.text_input("Complemento")

            ativo = st.checkbox(
                "Cliente Ativo",
                value=True
            )

            salvar = st.form_submit_button(
                "💾 Salvar Cliente"
            )

            if salvar:

                if nome.strip() == "":
                    st.warning("Informe o nome.")
                    st.stop()

                dados = (
                    tipo,
                    nome,
                    documento,
                    ie,
                    telefone,
                    whatsapp,
                    email,
                    cep,
                    endereco,
                    numero,
                    bairro,
                    cidade,
                    estado.upper(),
                    complemento,
                    ativo
                )

                inserir_cliente(dados)

                st.success("Cliente cadastrado com sucesso.")
                st.rerun()

    # =====================================================
    # CONSULTAR
    # =====================================================
    with abas[1]:

        busca = st.text_input(
            "🔎 Buscar nome, documento ou telefone"
        )

        df = listar_clientes(busca)

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

        st.caption(f"Total de clientes: {len(df)}")

        if not df.empty:

            cliente_id = st.selectbox(
                "Selecione Cliente",
                df["id"],
                format_func=lambda x:
                f"{x} - {df[df['id']==x]['nome'].values[0]}"
            )

            cli = df[df["id"] == cliente_id].iloc[0]

            st.markdown("---")
            st.markdown("## ✏️ Editar Cliente")

            col1, col2 = st.columns(2)

            with col1:

                tipo = st.selectbox(
                    "Tipo",
                    ["Pessoa Física", "Pessoa Jurídica"],
                    index=0 if cli["tipo"] == "Pessoa Física" else 1
                )

                nome = st.text_input(
                    "Nome",
                    value=cli["nome"]
                )

                documento = st.text_input(
                    "Documento",
                    value=cli["documento"]
                )

                ie = st.text_input(
                    "IE",
                    value=cli["ie"]
                )

                telefone = st.text_input(
                    "Telefone",
                    value=cli["telefone"]
                )

            with col2:

                whatsapp = st.text_input(
                    "WhatsApp",
                    value=cli["whatsapp"]
                )

                email = st.text_input(
                    "Email",
                    value=cli["email"]
                )

                cep = st.text_input(
                    "CEP",
                    value=cli["cep"]
                )

                endereco = st.text_input(
                    "Endereço",
                    value=cli["endereco"]
                )

                numero = st.text_input(
                    "Número",
                    value=cli["numero"]
                )

            col3, col4, col5 = st.columns(3)

            with col3:
                bairro = st.text_input(
                    "Bairro",
                    value=cli["bairro"]
                )

            with col4:
                cidade = st.text_input(
                    "Cidade",
                    value=cli["cidade"]
                )

            with col5:
                estado = st.text_input(
                    "UF",
                    value=cli["estado"]
                )

            complemento = st.text_input(
                "Complemento",
                value=cli["complemento"]
            )

            ativo = st.checkbox(
                "Ativo",
                value=cli["ativo"]
            )

            colb1, colb2 = st.columns(2)

            with colb1:

                if st.button("💾 Atualizar"):

                    dados = (
                        tipo,
                        nome,
                        documento,
                        ie,
                        telefone,
                        whatsapp,
                        email,
                        cep,
                        endereco,
                        numero,
                        bairro,
                        cidade,
                        estado.upper(),
                        complemento,
                        ativo
                    )

                    atualizar_cliente(
                        cliente_id,
                        dados
                    )

                    st.success("Cliente atualizado.")
                    st.rerun()

            with colb2:

                confirmar = st.checkbox(
                    "Confirmar exclusão"
                )

                if st.button("🗑 Excluir"):

                    if not confirmar:
                        st.warning(
                            "Confirme a exclusão."
                        )
                        st.stop()

                    excluir_cliente(cliente_id)

                    st.warning("Cliente excluído.")
                    st.rerun()