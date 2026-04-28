from database.connection import conectar

def criar_tabelas():

    with conectar() as conn:
        with conn.cursor() as cur:

            cur.execute("""
                CREATE TABLE IF NOT EXISTS clientes (
                    id SERIAL PRIMARY KEY,
                    nome TEXT,
                    cpf TEXT,
                    telefone TEXT,
                    email TEXT
                );
            """)

            # depois você pode adicionar outras tabelas aqui
            # produtos, vendas, financeiro...

            conn.commit()