import os
import psycopg2

def conectar():
    return psycopg2.connect(
        "postgresql://financeiro_db_93s4_user:kem6rdUeGhjKCYShr0qRw24IaZPxNaYT@dpg-d7jfb9q8qa3s73aiih4g-a.oregon-postgres.render.com/financeiro_db_93s4",
        sslmode="require"
    )