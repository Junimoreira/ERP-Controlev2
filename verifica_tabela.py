import psycopg2
import pandas as pd

# 🔗 conexão com o banco
conn = psycopg2.connect(
    "postgresql://controlev2_user:ZYlcDCsbPYSHCZeSEYjzXgn5dfRIO7qN@dpg-d7ofi2e7r5hc73b1jtlg-a.virginia-postgres.render.com/controlev2"
)

# 📊 consulta
#df = pd.read_sql("""
#SELECT column_name
#FROM information_schema.columns
#WHERE table_name = 'clientes'
#""", conn)

df = pd.read_sql("""
SELECT column_name 
FROM information_schema.columns 
WHERE table_name = 'vendas';
""", conn)


print(df)

# 🔒 fechar conexão
conn.close()