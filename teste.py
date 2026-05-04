import psycopg2

try:
    conn = psycopg2.connect("postgresql://controlev2_user:ZYlcDCsbPYSHCZeSEYjzXgn5dfRIO7qN@dpg-d7ofi2e7r5hc73b1jtlg-a.virginia-postgres.render.com/controlev2")
    print("Conectado com sucesso!")
except Exception as e:
    print(e)