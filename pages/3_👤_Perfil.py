import streamlit as st
import os
import sys

# Ensure services directory is accessible
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from services.auth_service import AuthService

st.set_page_config(page_title="Perfil - EduTrack AI", page_icon="👤")

auth_service = AuthService()

# Initialize session state keys
if "auth_token" not in st.session_state:
    st.session_state["auth_token"] = None
if "user_profile" not in st.session_state:
    st.session_state["user_profile"] = None

# If user is already authenticated
if st.session_state["auth_token"]:
    st.title("👤 Meu Perfil")
    st.write("Gerencie suas informações de conta no **EduTrack AI**.")

    # Refresh user profile if not cached
    if not st.session_state["user_profile"]:
        try:
            st.session_state["user_profile"] = auth_service.get_me(st.session_state["auth_token"])
        except Exception as e:
            st.warning(f"Não foi possível carregar os detalhes atualizados do perfil: {e}")

    profile = st.session_state["user_profile"] or {}

    # Display user details
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        st.write(f"**Nome:** {profile.get('name', 'N/A')}")
        st.write(f"**E-mail:** {profile.get('email', 'N/A')}")
    with col2:
        st.write(f"**Função (Role):** `{profile.get('role', 'member')}`")
        created_at = profile.get("created_at", "N/A")
        if created_at and "T" in str(created_at):
            created_at = str(created_at).split("T")[0]
        st.write(f"**Membro desde:** {created_at}")

    st.markdown("---")
    st.success("✅ Você está autenticado na plataforma.")

    # Logout button
    if st.button("🚪 Sair da Conta (Logout)", type="secondary"):
        st.session_state["auth_token"] = None
        st.session_state["user_profile"] = None
        st.rerun()

else:
    # Unauthenticated state: Login or Signup
    st.title("👤 Acesso à Conta")
    st.write("Faça login com sua conta ou cadastre-se para acessar o EduTrack AI.")

    tab_login, tab_signup = st.tabs(["🔑 Entrar (Login)", "📝 Criar Conta (Cadastro)"])

    with tab_login:
        st.subheader("Login na Plataforma")
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
        st.subheader("Novo Cadastro")
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

