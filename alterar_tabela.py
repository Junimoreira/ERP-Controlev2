import psycopg2

conn = psycopg2.connect("postgresql://controlev2_user:ZYlcDCsbPYSHCZeSEYjzXgn5dfRIO7qN@dpg-d7ofi2e7r5hc73b1jtlg-a.virginia-postgres.render.com/controlev2")
cur = conn.cursor()

cur.execute("ALTER TABLE vendas ADD COLUMN desconto NUMERIC DEFAULT 0;")

conn.commit()
conn.close()

print("OK")
