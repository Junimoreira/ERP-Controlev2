import psycopg2

conn = psycopg2.connect(
    "postgresql://controlev2_user:ZYlcDCsbPYSHCZeSEYjzXgn5dfRIO7qN@dpg-d7ofi2e7r5hc73b1jtlg-a.virginia-postgres.render.com/controlev2"
)

cur = conn.cursor()

cur.execute("""
SELECT column_name
FROM information_schema.columns
WHERE table_name = 'clientes'
ORDER BY ordinal_position;
""")

colunas = cur.fetchall()

for coluna in colunas:
    print(coluna[0])

cur.close()
conn.close()