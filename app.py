import streamlit as st
from datetime import datetime

from database import conectar
from modules.login import tela_login
from modules.dashboard import dashboard
from modules.clientes import tela_clientes
from modules.produtos import tela_produtos
from modules.vendas import tela_vendas
from modules.financeiro import tela_financeiro

# se existir módulo usuários, descomente:
# from modules.usuarios import tela_usuarios


# -------------------------------------------------
# CONFIG INICIAL
# -------------------------------------------------
st.set_page_config(
    page_title="ERP Controle V4",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)


# -------------------------------------------------
# CSS PROFISSIONAL
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

.kpi-card {
    background: white;
    padding: 20px;
    border-radius: 14px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    text-align: center;
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
defaults = {
    "logado": False,
    "usuario": "",
    "nivel": "usuario"
}

for chave, valor in defaults.items():
    if chave not in st.session_state:
        st.session_state[chave] = valor


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

    st.markdown("## 💰 ERP CONTROLE V4")
    st.markdown("---")

    st.write(f"👤 {st.session_state.usuario}")
    st.write(f"📅 {datetime.now().strftime('%d/%m/%Y')}")

    st.markdown("---")

    menu = st.radio(
        "Menu Principal",
        [
            "🏠 Início",
            "👤 Clientes",
            "📦 Produtos",
            "🛒 Vendas",
            "📊 Financeiro"
        ]
    )

    # MENU ADMIN
    if st.session_state.get("nivel") == "admin":
        st.markdown("---")
        admin_menu = st.radio(
            "Administração",
            [
                "👥 Usuários"
            ]
        )
    else:
        admin_menu = None

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
    '<p class="titulo">📊 ERP CONTROLE V4</p>',
    unsafe_allow_html=True
)

st.markdown(
    '<p class="subtitulo">Sistema de Gestão Empresarial</p>',
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


# -------------------------------------------------
# ADMIN
# -------------------------------------------------
if admin_menu == "👥 Usuários":
    st.subheader("👥 Controle de Usuários")
    st.info("Crie o módulo modules/usuarios.py para ativar esta tela.")