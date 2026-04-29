import os
import psycopg2


def conectar():
    return psycopg2.connect(
        os.environ["DATABASE_URL"],
        sslmode="require"
    )