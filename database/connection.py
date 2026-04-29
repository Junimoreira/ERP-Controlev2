import os
import psycopg2

def conectar():
    return psycopg2.connect(
        "postgresql://controlev2_user:ZYlcDCsbPYSHCZeSEYjzXgn5dfRIO7qN@dpg-d7ofi2e7r5hc73b1jtlg-a/controlev2",
        
    )

#sslmode="require"