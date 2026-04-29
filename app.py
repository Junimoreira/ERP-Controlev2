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

criar_tabelas()

# -------------------------------------------------
# CONFIG INICIAL
# -------------------------------------------------
st.set_page_config(
    page_title="ERP Controle Administrativo",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)


# -------------------------------------------------
# CSS
# -------------------------------------------------
st.markdown("""
<style>
.main {
    background-color: #f8f9fa;
}

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg,#111827,#1f2937);
}

section[data-testid="stSidebar"] * {
    color: white !important;
}

.titulo {
    font-size: 30px;
    font-weight: bold;
    color: #111827;
}

.subtitulo {
    color: gray;
    margin-top: -10px;
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

    st.markdown("## 💰 ERP Controle")
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

#elif menu == "👥 Usuários":
#    tela_usuarios()
