from database.connection import conectar
import bcrypt


def criar_tabelas():

    with conectar() as conn:
        with conn.cursor() as cur:

            # RESET TABELAS RELACIONADAS
            cur.execute("DROP TABLE IF EXISTS itens_venda CASCADE;")
            cur.execute("DROP TABLE IF EXISTS vendas CASCADE;")
            cur.execute("DROP TABLE IF EXISTS clientes CASCADE;")

            # ==========================
            # USUÁRIOS
            # ==========================
            cur.execute("""
                CREATE TABLE IF NOT EXISTS usuarios (
                    id SERIAL PRIMARY KEY,
                    nome TEXT NOT NULL,
                    usuario TEXT UNIQUE NOT NULL,
                    senha TEXT NOT NULL,
                    nivel TEXT NOT NULL
                );
            """)

            senha_admin = bcrypt.hashpw(
                "1234".encode(),
                bcrypt.gensalt()
            ).decode()

            cur.execute("""
                INSERT INTO usuarios (nome, usuario, senha, nivel)
                SELECT 'Administrador', 'admin', %s, 'admin'
                WHERE NOT EXISTS (
                    SELECT 1 FROM usuarios WHERE usuario='admin'
                );
            """, (senha_admin,))

            # ==========================
            # CLIENTES
            # ==========================
            cur.execute("""
                CREATE TABLE clientes (
                    id SERIAL PRIMARY KEY,
                    tipo TEXT,
                    nome TEXT,
                    documento TEXT,
                    telefone TEXT,
                    email TEXT,
                    endereco TEXT
                );
            """)

            # ==========================
            # PRODUTOS
            # ==========================
            cur.execute("""
                CREATE TABLE IF NOT EXISTS produtos (
                    id SERIAL PRIMARY KEY,
                    nome TEXT NOT NULL,
                    codigo_barras TEXT UNIQUE,
                    categoria TEXT,
                    custo NUMERIC(10,2),
                    preco NUMERIC(10,2),
                    estoque INTEGER DEFAULT 0
                );
            """)

            # ==========================
            # VENDAS
            # ==========================
            cur.execute("""
                CREATE TABLE vendas (
                    id SERIAL PRIMARY KEY,
                    cliente_id INTEGER REFERENCES clientes(id),
                    data TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    total NUMERIC(10,2),
                    forma_pagamento TEXT
                );
            """)

            # ==========================
            # ITENS VENDA
            # ==========================
            cur.execute("""
                CREATE TABLE itens_venda (
                    id SERIAL PRIMARY KEY,
                    venda_id INTEGER REFERENCES vendas(id),
                    produto_id INTEGER REFERENCES produtos(id),
                    quantidade INTEGER,
                    preco_unitario NUMERIC(10,2),
                    subtotal NUMERIC(10,2)
                );
            """)

            # ==========================
            # FINANCEIRO
            # ==========================
            cur.execute("""
                CREATE TABLE IF NOT EXISTS financeiro (
                    id SERIAL PRIMARY KEY,
                    tipo TEXT,
                    descricao TEXT,
                    valor NUMERIC(10,2),
                    data DATE DEFAULT CURRENT_DATE
                );
            """)

            conn.commit()