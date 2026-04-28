import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from database import conectar

conn = conectar()
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS usuarios (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100),
    usuario VARCHAR(50) UNIQUE,
    senha TEXT,
    nivel VARCHAR(20)
)
""")

conn.commit()
print("Tabela criada com sucesso!")

cur.close()
conn.close()