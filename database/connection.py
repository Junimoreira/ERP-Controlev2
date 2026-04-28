import os
import psycopg2

def conectar():
    return psycopg2.connect(os.getenv("DATABASE_URL"))