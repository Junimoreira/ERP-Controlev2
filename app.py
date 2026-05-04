import streamlit as st
import psycopg2
import os
import pandas as pd

st.set_page_config(page_title="Dashboard ERP", layout="wide")

# ===================== CONEXÃO =====================
DATABASE_URL = os.getenv("DATABASE_URL")
def get_conn():
    return psycopg2.connect(DATABASE_URL)

# ===================== CONSULTAS =====================
def get_total_vendas():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT COALESCE(SUM(valor),0) FROM vendas")
    total = cur.fetchone()[0]
    conn.close()
    return total

def get_total_produtos():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM produtos")
    total = cur.fetchone()[0]
    conn.close()
    return total

def get_total_clientes():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM clientes")
    total = cur.fetchone()[0]
    conn.close()
    return total

def get_estoque_baixo():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM produtos WHERE estoque <= 5")
    total = cur.fetchone()[0]
    conn.close()
    return total

# ===================== UI =====================
st.set_page_config(page_title="Dashboard ERP", layout="wide")

st.title("📊 Dashboard ERP Dinâmico")

# ===================== DADOS =====================
vendas = get_total_vendas()
produtos = get_total_produtos()
clientes = get_total_clientes()
estoque_baixo = get_estoque_baixo()

# ===================== CARDS =====================
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div style="
        background: rgba(255,255,255,0.07);
        padding: 25px;
        border-radius: 15px;
        text-align:center;
        box-shadow: 0 10px 25px rgba(0,0,0,0.5);
    ">
        <h4>💰 Vendas Totais</h4>
        <h2>R$ {vendas:,.2f}</h2>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div style="
        background: rgba(255,255,255,0.07);
        padding: 25px;
        border-radius: 15px;
        text-align:center;
        box-shadow: 0 10px 25px rgba(0,0,0,0.5);
    ">
        <h4>📦 Produtos</h4>
        <h2>{produtos}</h2>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div style="
        background: rgba(255,255,255,0.07);
        padding: 25px;
        border-radius: 15px;
        text-align:center;
        box-shadow: 0 10px 25px rgba(0,0,0,0.5);
    ">
        <h4>👥 Clientes</h4>
        <h2>{clientes}</h2>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div style="
        background: rgba(255,255,255,0.07);
        padding: 25px;
        border-radius: 15px;
        text-align:center;
        box-shadow: 0 10px 25px rgba(0,0,0,0.5);
    ">
        <h4>⚠️ Estoque Baixo</h4>
        <h2>{estoque_baixo}</h2>
    </div>
    """, unsafe_allow_html=True)

def get_dados_curva_abc():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        SELECT nome,
               SUM(valor_venda * quantidade_vendida) AS faturamento
        FROM produtos
        GROUP BY nome
        ORDER BY faturamento DESC
    """)

    dados = cur.fetchall()
    conn.close()

    return dados