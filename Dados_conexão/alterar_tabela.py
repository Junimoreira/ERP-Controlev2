import psycopg2
<<<<<<< HEAD

=======
import pandas as pd

# 🔗 conexão com o banco
>>>>>>> 72df90e (Ajustando tela de clientes e vendas)
conn = psycopg2.connect(
    "postgresql://controlev2_user:ZYlcDCsbPYSHCZeSEYjzXgn5dfRIO7qN@dpg-d7ofi2e7r5hc73b1jtlg-a.virginia-postgres.render.com/controlev2"
)

<<<<<<< HEAD
cur = conn.cursor()

cur.execute("""
	ALTER TABLE clientes ADD COLUMN ie VARCHAR(30);
        ALTER TABLE clientes ADD COLUMN whatsapp VARCHAR(20);
        ALTER TABLE clientes ADD COLUMN cep VARCHAR(10);
        ALTER TABLE clientes ADD COLUMN numero VARCHAR(20);
        ALTER TABLE clientes ADD COLUMN bairro VARCHAR(100);
        ALTER TABLE clientes ADD COLUMN cidade VARCHAR(100);
        ALTER TABLE clientes ADD COLUMN estado VARCHAR(2);
        ALTER TABLE clientes ADD COLUMN complemento VARCHAR(150);
        ALTER TABLE clientes ADD COLUMN ativo BOOLEAN DEFAULT TRUE;
""")

conn.commit()
conn.close()

print("✅ Tabela Clientes alterada!")
=======
cur.execute("""
ALTER TABLE vendas ADD COLUMN desconto NUMERIC DEFAULT 0;

""")
conn.commit()
print("Tabela alterada com sucesso!")

cur.close()
conn.close()
>>>>>>> 72df90e (Ajustando tela de clientes e vendas)
