import streamlit as st
import os
import sys

# Ensure services directory is accessible
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from services.auth_service import AuthService

st.set_page_config(page_title="Perfil - EduTrack AI", page_icon="👤", layout="wide")

auth_service = AuthService()

# Initialize session state keys
if "auth_token" not in st.session_state:
    st.session_state["auth_token"] = None
if "user_profile" not in st.session_state:
    st.session_state["user_profile"] = None

# Custom CSS for Modern, Polished Styling
st.markdown(
    """
    <style>
    /* Global Container Enhancements */
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(180deg, #f8fafc 0%, #f1f5f9 50%, #f8fafc 100%);
    }

    /* Common Card Components */
    .card-hero {
        background: linear-gradient(135deg, #1e1b4b 0%, #312e81 40%, #4338ca 100%);
        border-radius: 20px;
        padding: 2rem 2.2rem;
        color: #ffffff;
        box-shadow: 0 10px 25px -5px rgba(49, 46, 129, 0.25);
        margin-bottom: 1.5rem;
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 1.5rem;
        flex-wrap: wrap;
    }
    .card-hero-left {
        display: flex;
        align-items: center;
        gap: 1.25rem;
    }
    .avatar-badge {
        width: 64px;
        height: 64px;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.16);
        border: 2px solid rgba(255, 255, 255, 0.35);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 2rem;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    }
    .hero-title {
        font-size: 1.85rem;
        font-weight: 800;
        margin: 0;
        color: #ffffff;
        letter-spacing: -0.02em;
    }
    .hero-subtitle {
        font-size: 0.95rem;
        color: rgba(255, 255, 255, 0.85);
        margin-top: 0.25rem;
    }
    .status-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.4rem;
        background: rgba(16, 185, 129, 0.18);
        border: 1px solid rgba(16, 185, 129, 0.4);
        color: #6ee7b7;
        font-weight: 700;
        font-size: 0.85rem;
        padding: 0.45rem 0.95rem;
        border-radius: 9999px;
        backdrop-filter: blur(4px);
    }

    /* Info Grid Cards */
    .profile-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
        gap: 1rem;
        margin-bottom: 1.5rem;
    }
    .metric-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 16px;
        padding: 1.2rem 1.3rem;
        box-shadow: 0 4px 12px rgba(15, 23, 42, 0.03);
        transition: transform 0.15s ease, box-shadow 0.15s ease;
    }
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(15, 23, 42, 0.06);
    }
    .metric-label {
        font-size: 0.78rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: #64748b;
        display: flex;
        align-items: center;
        gap: 0.4rem;
        margin-bottom: 0.4rem;
    }
    .metric-value {
        font-size: 1.15rem;
        font-weight: 700;
        color: #0f172a;
        word-break: break-word;
    }
    .metric-badge {
        display: inline-block;
        background: #e0e7ff;
        color: #4338ca;
        font-size: 0.85rem;
        font-weight: 700;
        padding: 0.2rem 0.65rem;
        border-radius: 6px;
    }

    /* Section Feature Card */
    .feature-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 18px;
        padding: 1.5rem;
        box-shadow: 0 4px 14px rgba(15, 23, 42, 0.04);
        margin-bottom: 1.5rem;
    }
    .feature-card-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 0.6rem;
    }
    .feature-card-title {
        font-size: 1.25rem;
        font-weight: 700;
        color: #0f172a;
        margin: 0;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    .feature-card-desc {
        color: #64748b;
        font-size: 0.92rem;
        margin-bottom: 1.2rem;
        line-height: 1.45;
    }

    /* Auth View Specific */
    .auth-hero {
        background: linear-gradient(135deg, #1e1b4b 0%, #312e81 40%, #4338ca 100%);
        border-radius: 20px;
        padding: 2.2rem 2rem;
        color: #ffffff;
        text-align: center;
        box-shadow: 0 10px 25px -5px rgba(49, 46, 129, 0.25);
        margin-bottom: 2rem;
    }
    .auth-hero-icon {
        font-size: 2.6rem;
        margin-bottom: 0.5rem;
    }
    .auth-hero-title {
        font-size: 1.9rem;
        font-weight: 800;
        margin: 0;
        color: #ffffff;
    }
    .auth-hero-subtitle {
        font-size: 0.95rem;
        color: rgba(255, 255, 255, 0.85);
        margin-top: 0.4rem;
        max-width: 520px;
        margin-left: auto;
        margin-right: auto;
    }
    .auth-card-container {
        background: #ffffff;
        border: 1px solid rgba(226, 232, 240, 0.9);
        border-radius: 22px;
        padding: 2rem 2.2rem;
        box-shadow: 0 14px 38px -6px rgba(15, 23, 42, 0.09);
        margin-bottom: 2rem;
    }

    /* Auth Form Specific Styling */
    .auth-card-container [data-testid="stForm"] {
        background: transparent !important;
        border: none !important;
        padding: 0 !important;
    }
    .auth-card-container [data-testid="stForm"] input[type="text"],
    .auth-card-container [data-testid="stForm"] input[type="password"] {
        background: #f8fafc !important;
        border: 1.5px solid #e2e8f0 !important;
        border-radius: 12px !important;
        padding: 0.65rem 0.9rem !important;
        font-size: 0.95rem !important;
        color: #0f172a !important;
        transition: border-color 0.2s ease, box-shadow 0.2s ease !important;
    }
    .auth-card-container [data-testid="stForm"] input:focus {
        border-color: #4338ca !important;
        box-shadow: 0 0 0 3px rgba(67, 56, 202, 0.14) !important;
        background: #ffffff !important;
    }
    .auth-card-container [data-testid="stForm"] button {
        background: linear-gradient(135deg, #1e1b4b 0%, #4338ca 100%) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.75rem 1.2rem !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        letter-spacing: 0.01em !important;
        box-shadow: 0 6px 20px -2px rgba(67, 56, 202, 0.35) !important;
        transition: transform 0.15s ease, box-shadow 0.15s ease !important;
        margin-top: 0.6rem !important;
    }
    .auth-card-container [data-testid="stForm"] button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 24px -2px rgba(67, 56, 202, 0.45) !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# If user is already authenticated
if st.session_state["auth_token"]:
    # Refresh user profile if not cached
    if not st.session_state["user_profile"]:
        try:
            st.session_state["user_profile"] = auth_service.get_me(st.session_state["auth_token"])
        except Exception as e:
            st.warning(f"Não foi possível carregar os detalhes atualizados do perfil: {e}")

    profile = st.session_state["user_profile"] or {}
    user_name = profile.get("name") or "Aluno EduTrack"
    user_email = profile.get("email") or "aluno@edutrack.ai"
    user_role = profile.get("role") or "member"
    created_at = profile.get("created_at") or "N/A"
    if created_at and "T" in str(created_at):
        created_at = str(created_at).split("T")[0]

    first_initial = user_name[0].upper() if user_name else "👤"

    # Header Hero Card
    st.markdown(
        f"""
        <div class="card-hero">
            <div class="card-hero-left">
                <div class="avatar-badge">{first_initial}</div>
                <div>
                    <h1 class="hero-title">{user_name}</h1>
                    <div class="hero-subtitle">Gerencie suas credenciais e relatórios acadêmicos no <strong>EduTrack AI</strong></div>
                </div>
            </div>
            <div class="status-badge">● Conta Ativa (Xano)</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # User Information Grid
    st.markdown(
        f"""
        <div class="profile-grid">
            <div class="metric-card">
                <div class="metric-label">👤 Nome Completo</div>
                <div class="metric-value">{user_name}</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">✉️ E-mail</div>
                <div class="metric-value">{user_email}</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">🛡️ Nível de Acesso</div>
                <div class="metric-value"><span class="metric-badge">{str(user_role).upper()}</span></div>
            </div>
            <div class="metric-card">
                <div class="metric-label">📅 Membro Desde</div>
                <div class="metric-value">{created_at}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Opção de Download do Relatório em PDF
    st.markdown(
        """
        <div class="feature-card">
            <div class="feature-card-header">
                <h3 class="feature-card-title">📄 Relatório de Desempenho</h3>
            </div>
            <div class="feature-card-desc">
                Faça o download do seu relatório acadêmico consolidado em formato PDF oficial com disciplinas, tarefas e métricas de progresso.
            </div>
        """,
        unsafe_allow_html=True,
    )

    try:
        from scripts.generate_student_report import generate_report_bytes
        pdf_bytes = generate_report_bytes(
            student_name=user_name,
            auth_token=st.session_state["auth_token"]
        )
        st.download_button(
            label="📥 Baixar Relatório de Desempenho (PDF)",
            data=pdf_bytes,
            file_name=f"relatorio_desempenho_{user_name.replace(' ', '_').lower()}.pdf",
            mime="application/pdf",
            use_container_width=True
        )
    except Exception as e:
        st.warning(f"Não foi possível carregar o relatório PDF: {e}")

    st.markdown("</div>", unsafe_allow_html=True)

    # Logout Action Area
    col_space, col_logout = st.columns([3, 1])
    with col_logout:
        if st.button("🚪 Sair da Conta (Logout)", type="secondary", use_container_width=True):
            st.session_state["auth_token"] = None
            st.session_state["user_profile"] = None
            st.rerun()

else:
    # Unauthenticated state: Login or Signup
    st.markdown(
        """
        <div class="auth-hero">
            <div class="auth-hero-icon">🎓</div>
            <h1 class="auth-hero-title">Portal do Aluno - EduTrack AI</h1>
            <div class="auth-hero-subtitle">
                Faça login para acompanhar disciplinas, prazos e relatórios acadêmicos, ou crie sua conta gratuitamente.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Centralização da caixa de autenticação para layout harmonioso
    col_l, col_center, col_r = st.columns([1, 2.2, 1])

    with col_center:
        st.markdown('<div class="auth-card-container">', unsafe_allow_html=True)
        tab_login, tab_signup = st.tabs(["🔑 Entrar (Login)", "📝 Criar Conta (Cadastro)"])

        with tab_login:
            st.markdown("### Acessar Plataforma")
            st.caption("Entre com seu e-mail e senha cadastrados.")
            with st.form("form_login"):
                email = st.text_input("E-mail", placeholder="aluno@edutrack.ai")
                password = st.text_input("Senha", type="password", placeholder="Digite sua senha")
                btn_login = st.form_submit_button("Entrar", use_container_width=True)

                if btn_login:
                    try:
                        res = auth_service.login(email, password)
                        token = res.get("authToken")
                        if token:
                            st.session_state["auth_token"] = token
                            # Fetch profile
                            try:
                                user_data = auth_service.get_me(token)
                                st.session_state["user_profile"] = user_data
                            except Exception:
                                st.session_state["user_profile"] = {"email": email, "id": res.get("user_id")}
                            st.success("Login efetuado com sucesso!")
                            st.rerun()
                        else:
                            st.error("Token de autenticação não retornado pelo servidor.")
                    except Exception as e:
                        st.error(str(e))

        with tab_signup:
            st.markdown("### Criar Nova Conta")
            st.caption("Preencha os campos abaixo para iniciar seu cadastro.")
            with st.form("form_signup"):
                name = st.text_input("Nome Completo", placeholder="Seu Nome")
                email = st.text_input("E-mail", placeholder="seu.email@exemplo.com")
                password = st.text_input("Senha", type="password", placeholder="Mínimo 8 caracteres, 1 letra e 1 número")
                btn_signup = st.form_submit_button("Cadastrar", use_container_width=True)

                if btn_signup:
                    try:
                        res = auth_service.signup(name, email, password)
                        token = res.get("authToken")
                        if token:
                            st.session_state["auth_token"] = token
                            try:
                                user_data = auth_service.get_me(token)
                                st.session_state["user_profile"] = user_data
                            except Exception:
                                st.session_state["user_profile"] = {"name": name, "email": email, "id": res.get("user_id")}
                            st.success("Cadastro realizado com sucesso!")
                            st.rerun()
                        else:
                            st.error("Token de autenticação não retornado pelo servidor.")
                    except Exception as e:
                        st.error(str(e))

        st.markdown("</div>", unsafe_allow_html=True)
