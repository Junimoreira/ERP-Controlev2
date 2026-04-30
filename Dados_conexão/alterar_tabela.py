import psycopg2

conn = psycopg2.connect(
    "postgresql://controlev2_user:ZYlcDCsbPYSHCZeSEYjzXgn5dfRIO7qN@dpg-d7ofi2e7r5hc73b1jtlg-a.virginia-postgres.render.com/controlev2"
)

cur = conn.cursor()

cur.execute("""
	ALTER TABLE vendas ADD COLUMN IF NOT EXISTS cliente VARCHAR(150);
        ALTER TABLE vendas ADD COLUMN IF NOT EXISTS desconto NUMERIC(10,2) DEFAULT 0;
        ALTER TABLE vendas ADD COLUMN IF NOT EXISTS forma_pagamento VARCHAR(50);
""")

conn.commit()
conn.close()

print("✅ Tabela Vendas alterada!")
