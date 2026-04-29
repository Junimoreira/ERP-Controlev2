from database.connection import conectar
import bcrypt


def criar_tabelas():

    with conectar() as conn:
        with conn.cursor() as cur:

            # -------------------------
            # TABELA USUÁRIOS
            # -------------------------
            cur.execute("""
                CREATE TABLE IF NOT EXISTS usuarios (
                    id SERIAL PRIMARY KEY,
                    nome TEXT,
                    usuario TEXT UNIQUE,
                    senha TEXT,
                    nivel TEXT
                );
            """)

            # Criar admin padrão se não existir
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


            # -------------------------
            # TABELA CLIENTES
            # -------------------------
            cur.execute("""
                CREATE TABLE IF NOT EXISTS clientes (
                    id SERIAL PRIMARY KEY,
                    nome TEXT,
                    cpf TEXT,
                    telefone TEXT,
                    email TEXT
                );
            """)

            conn.commit()