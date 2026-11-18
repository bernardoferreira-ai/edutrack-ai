import streamlit as st

# Configuração da Página (Título na aba do navegador)
st.set_page_config(page_title="EduTrack AI", page_icon="🎓", layout="wide")

st.markdown(
    """
    <style>
    /* Dark Theme Global View */
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(180deg, #0b0f19 0%, #0f172a 50%, #0b0f19 100%);
        color: #f8fafc;
    }
    [data-testid="stSidebar"] {
        background-color: #111827;
        border-right: 1px solid rgba(255, 255, 255, 0.08);
    }
    .hero-card {
        background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 60%, #172554 100%);
        border-radius: 20px;
        padding: 2rem 2.2rem;
        color: #ffffff;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.4);
        border: 1px solid rgba(255, 255, 255, 0.08);
        margin-bottom: 1.5rem;
    }
    .metric-container {
        background: #161e2e;
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 1.2rem;
        box-shadow: 0 6px 18px rgba(0, 0, 0, 0.25);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Título Principal
st.markdown(
    """
    <div class="hero-card">
        <h1 style="margin: 0; font-size: 2.2rem; font-weight: 800; color: #ffffff;">🎓 EduTrack AI</h1>
        <p style="margin: 0.4rem 0 0 0; color: rgba(255, 255, 255, 0.85); font-size: 1rem;">
            Seu assistente acadêmico para gestão de disciplinas, prazos e tarefas.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# Sidebar (Menu Lateral)
st.sidebar.header("Menu")
menu_option = st.sidebar.radio("Navegar", ["Dashboard", "Disciplinas", "Tarefas"])

# Conteúdo Dinâmico
if menu_option == "Dashboard":
    st.write("Bem-vindo ao seu assistente acadêmico!")
    st.info("Conecte ao Xano para ver seus dados reais.")
    
    # Exemplo de Métrica Visual
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Disciplinas Ativas", "0")
    with col2:
        st.metric("Tarefas Pendentes", "0")

elif menu_option == "Disciplinas":
    st.subheader("Minhas Disciplinas")
    st.write("Aqui listaremos as matérias cadastradas no backend.")

elif menu_option == "Tarefas":
    st.subheader("Gerenciamento de Tarefas")
    st.checkbox("Exemplo: Estudar Streamlit")
