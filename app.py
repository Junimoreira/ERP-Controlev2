import streamlit as st
from datetime import datetime
from modules.login import tela_login
from modules.dashboard import dashboard
from modules.clientes import tela_clientes
from modules.produtos import tela_produtos
from modules.vendas import tela_vendas
from modules.financeiro import tela_financeiro
#from modules.usuarios import tela_usuarios
from database.setup import criar_tabelas
from modules.estoque import tela_estoque
from modules.despesas import tela_despesas

criar_tabelas()

# -------------------------------------------------
# CONFIG INICIAL
# -------------------------------------------------
st.set_page_config(
    page_title="Controle Administrativo",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)


# -------------------------------------------------
# CSS
# -------------------------------------------------
st.markdown("""
<style>

/* Fundo geral */
.main {
    background-color: #f8fafc;
}

/* Sidebar */
section[data-testid="stSidebar"]{
    background: linear-gradient(180deg,#07152b,#0b2545);
    padding-top: 10px;
    width: 280px !important;
}

/* Textos sidebar */
section[data-testid="stSidebar"] *{
    color:white !important;
}

/* Remove scroll lateral */
section[data-testid="stSidebar"] > div {
    overflow-y: auto;
    overflow-x: hidden;
}

/* Radio menu */
div[role="radiogroup"] label{
    padding: 12px 14px;
    margin-bottom: 8px;
    border-radius: 12px;
    font-size: 18px;
    transition: 0.2s;
}

div[role="radiogroup"] label:hover{
    background: rgba(255,255,255,0.08);
}

/* Botão sair */
.stButton button{
    width:100%;
    border-radius:12px;
    height:45px;
    border:none;
    background:#2563eb;
    color:white;
    font-weight:600;
}

.stButton button:hover{
    background:#1d4ed8;
}

/* Títulos */
.titulo{
    font-size:32px;
    font-weight:700;
    color:#0f172a;
}

.subtitulo{
    color:#64748b;
    margin-top:-8px;
}

</style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# SESSION STATE
# -------------------------------------------------
if "logado" not in st.session_state:
    st.session_state.logado = False

if "usuario" not in st.session_state:
    st.session_state.usuario = ""

if "nivel" not in st.session_state:
    st.session_state.nivel = "usuario"


# -------------------------------------------------
# LOGIN
# -------------------------------------------------
if not st.session_state.logado:
    tela_login()
    st.stop()


# -------------------------------------------------
# SIDEBAR
# -------------------------------------------------
with st.sidebar:

    with st.sidebar:

    st.image("logo.png", width=140)

    st.markdown(
        "<h2 style='text-align:center;margin-bottom:0;'>ERP Controle</h2>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<p style='text-align:center;color:#94a3b8;'>Sistema Comercial</p>",
        unsafe_allow_html=True
    )

    st.markdown("---")

    st.write(f"👤 {st.session_state.usuario}")
    st.write(f"📅 {datetime.now().strftime('%d/%m/%Y')}")

    st.markdown("---")

    opcoes = [
        "🏠 Início",
        "👤 Clientes",
        "📦 Estoque",
        "📦 Produtos",
        "🛒 Vendas",
        "💸 Despesas",
        "📊 Financeiro",
    ]

    #if st.session_state.nivel == "admin":
    #    opcoes.append("👥 Usuários")

    menu = st.radio("Menu", opcoes)

    st.markdown("---")

    if st.button("🚪 Sair", use_container_width=True):
        st.session_state.logado = False
        st.session_state.usuario = ""
        st.session_state.nivel = "usuario"
        st.rerun()


# -------------------------------------------------
# TOPO
# -------------------------------------------------
st.markdown(
    '<p class="titulo">ERP Controle Administrativo</p>',
    unsafe_allow_html=True
)

st.markdown(
    '<p class="subtitulo">Sistema de Gestão</p>',
    unsafe_allow_html=True
)

st.markdown("---")


# -------------------------------------------------
# NAVEGAÇÃO
# -------------------------------------------------
if menu == "🏠 Início":
    dashboard()

elif menu == "👤 Clientes":
    tela_clientes()

elif menu == "📦 Produtos":
    tela_produtos()

elif menu == "🛒 Vendas":
    tela_vendas()

elif menu == "📊 Financeiro":
    tela_financeiro()

elif menu == "📦 Estoque":
    tela_estoque()
elif menu == "💸 Despesas":
    tela_despesas()

#elif menu == "👥 Usuários":
#    tela_usuarios()
