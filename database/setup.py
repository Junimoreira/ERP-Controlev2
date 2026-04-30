from database.connection import conectar
import bcrypt


def criar_tabelas():
    """
    Cria tabelas apenas se não existirem.
    Seguro para produção (Render).
    Não apaga dados.
    """

    with conectar() as conn:
        with conn.cursor() as cur:

            # ==================================================
            # USUÁRIOS
            # ==================================================
            cur.execute("""
                CREATE TABLE IF NOT EXISTS usuarios (
                    id SERIAL PRIMARY KEY,
                    nome VARCHAR(150) NOT NULL,
                    usuario VARCHAR(80) UNIQUE NOT NULL,
                    senha TEXT NOT NULL,
                    nivel VARCHAR(30) NOT NULL DEFAULT 'usuario'
                );
            """)

            # Cria admin padrão se não existir
            senha_admin = bcrypt.hashpw(
                "1234".encode(),
                bcrypt.gensalt()
            ).decode()

            cur.execute("""
                INSERT INTO usuarios (nome, usuario, senha, nivel)
                SELECT 'Administrador', 'admin', %s, 'admin'
                WHERE NOT EXISTS (
                    SELECT 1 FROM usuarios WHERE usuario = 'admin'
                );
            """, (senha_admin,))

            # ==================================================
            # CLIENTES
            # ==================================================
            cur.execute("""
                CREATE TABLE IF NOT EXISTS clientes (
                    id SERIAL PRIMARY KEY,
                    tipo VARCHAR(20),
                    nome VARCHAR(150) NOT NULL,
                    documento VARCHAR(30),
                    ie VARCHAR(30),
                    telefone VARCHAR(30),
                    whatsapp VARCHAR(30),
                    email VARCHAR(150),
                    cep VARCHAR(15),
                    endereco VARCHAR(200),
                    numero VARCHAR(20),
                    bairro VARCHAR(100),
                    cidade VARCHAR(100),
                    estado VARCHAR(2),
                    complemento VARCHAR(150),
                    ativo BOOLEAN DEFAULT TRUE,
                    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)

            # ==================================================
            # PRODUTOS
            # ==================================================
            cur.execute("""
                CREATE TABLE IF NOT EXISTS produtos (
                    id SERIAL PRIMARY KEY,
                    nome VARCHAR(150) NOT NULL,
                    codigo_barras VARCHAR(100) UNIQUE,
                    categoria VARCHAR(100),
                    custo NUMERIC(10,2) DEFAULT 0,
                    preco NUMERIC(10,2) DEFAULT 0,
                    estoque INTEGER DEFAULT 0,
                    ativo BOOLEAN DEFAULT TRUE,
                    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)

            # ==================================================
            # VENDAS
            # ==================================================
            cur.execute("""
                CREATE TABLE IF NOT EXISTS vendas (
                    id SERIAL PRIMARY KEY,
                    cliente_id INTEGER REFERENCES clientes(id),
                    data TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    total NUMERIC(10,2) DEFAULT 0,
                    forma_pagamento VARCHAR(50),
                    status VARCHAR(30) DEFAULT 'FINALIZADA'
                );
            """)

            # ==================================================
            # ITENS VENDA
            # ==================================================
            cur.execute("""
                CREATE TABLE IF NOT EXISTS itens_venda (
                    id SERIAL PRIMARY KEY,
                    venda_id INTEGER REFERENCES vendas(id) ON DELETE CASCADE,
                    produto_id INTEGER REFERENCES produtos(id),
                    quantidade INTEGER NOT NULL,
                    preco_unitario NUMERIC(10,2) NOT NULL,
                    subtotal NUMERIC(10,2) NOT NULL
                );
            """)

            # ==================================================
            # FINANCEIRO
            # ==================================================
            cur.execute("""
                CREATE TABLE IF NOT EXISTS financeiro (
                    id SERIAL PRIMARY KEY,
                    tipo VARCHAR(30),
                    descricao VARCHAR(200),
                    valor NUMERIC(10,2) NOT NULL,
                    data DATE DEFAULT CURRENT_DATE
                );
            """)

            # ==================================================
            # DESPESAS
            # ==================================================
            cur.execute("""
                CREATE TABLE IF NOT EXISTS despesas (
                    id SERIAL PRIMARY KEY,
                    descricao VARCHAR(200) NOT NULL,
                    valor NUMERIC(10,2) NOT NULL,
                    vencimento DATE,
                    categoria VARCHAR(100),
                    observacao TEXT,
                    pago BOOLEAN DEFAULT FALSE,
                    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)

            conn.commit()