import streamlit as st
import sys
import os

# Ensure services directory is accessible
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from services.subject_service import SubjectService

st.set_page_config(page_title="Disciplinas", page_icon="📚", layout="wide")

st.markdown(
    """
    <style>
    /* Global App View */
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(180deg, #f8fafc 0%, #f1f5f9 50%, #f8fafc 100%);
    }

    /* Page Header Shell */
    .page-shell {
        background: linear-gradient(135deg, #1e1b4b 0%, #312e81 40%, #4338ca 100%);
        border-radius: 20px;
        padding: 1.8rem 2.2rem;
        color: #ffffff;
        box-shadow: 0 10px 25px -5px rgba(49, 46, 129, 0.25);
        margin-bottom: 1.5rem;
    }
    .page-title {
        font-size: 2rem;
        font-weight: 800;
        margin: 0;
        color: #ffffff;
        letter-spacing: -0.02em;
    }
    .page-subtitle {
        color: rgba(255, 255, 255, 0.85);
        font-size: 0.95rem;
        margin-top: 0.35rem;
    }
    .page-pill {
        background: rgba(255, 255, 255, 0.16);
        border: 1px solid rgba(255, 255, 255, 0.35);
        color: #ffffff;
        font-weight: 700;
        border-radius: 999px;
        padding: 0.5rem 1.1rem;
        backdrop-filter: blur(4px);
    }

    /* Content Cards & Tabs */
    .content-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 18px;
        padding: 1.5rem 1.7rem;
        box-shadow: 0 6px 20px -3px rgba(15, 23, 42, 0.04);
        margin-top: 1rem;
        margin-bottom: 1.2rem;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.6rem;
        background: transparent;
        border-bottom: 2px solid #e2e8f0;
        padding-bottom: 0.2rem;
    }
    .stTabs [data-baseweb="tab"] {
        background: rgba(255, 255, 255, 0.85);
        border: 1px solid #e2e8f0;
        border-radius: 12px 12px 0 0;
        padding: 0.65rem 1.3rem;
        font-weight: 600;
        color: #475569;
        transition: all 0.15s ease;
    }
    .stTabs [aria-selected="true"] {
        background: #ffffff !important;
        color: #4338ca !important;
        border-color: #cbd5e1 #cbd5e1 #ffffff !important;
        font-weight: 700 !important;
    }

    /* Expander Modernization */
    .stExpander {
        background: #ffffff !important;
        border-radius: 18px !important;
        border: 1px solid rgba(226, 232, 240, 0.9) !important;
        box-shadow: 0 4px 16px -2px rgba(15, 23, 42, 0.05) !important;
        overflow: hidden !important;
        margin-bottom: 1.2rem !important;
        transition: all 0.2s ease !important;
    }
    .stExpander:hover {
        border-color: rgba(99, 102, 241, 0.3) !important;
        box-shadow: 0 8px 24px -4px rgba(15, 23, 42, 0.08) !important;
    }
    [data-testid="stExpanderToggleIcon"] {
        color: #4338ca !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="page-shell">
        <div style="display:flex; align-items:center; justify-content:space-between; gap:1.2rem; flex-wrap:wrap;">
            <div>
                <h1 class="page-title">Gestão de Disciplinas</h1>
                <div class="page-subtitle">Acompanhe e gerencie as disciplinas da sua grade acadêmica.</div>
            </div>
            <div class="page-pill">📚 Grade Curricular</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# Initialize service and retrieve auth token
subject_service = SubjectService()
token = st.session_state.get("auth_token")

@st.dialog("Confirmar Exclusão")
def confirmar_exclusao_disciplina(sub_id: int, sub_name: str):
    st.warning(f"Você realmente deseja excluir a disciplina **{sub_name}**?")
    st.caption("Esta ação removerá a disciplina permanentemente.")
    col_sim, col_nao = st.columns(2)
    with col_sim:
        if st.button("Sim, excluir", type="primary", key=f"modal_confirm_del_{sub_id}"):
            try:
                subject_service.delete_subject(sub_id, token=token)
                st.warning("Disciplina excluída com sucesso!")
                st.rerun()
            except Exception as e:
                st.error(f"Erro ao excluir: {e}")
    with col_nao:
        if st.button("Cancelar", key=f"modal_cancel_del_{sub_id}"):
            st.rerun()

# Abas para separar Listagem de Cadastro
tab_lista, tab_novo = st.tabs(["📋 Listar Disciplinas", "➕ Nova Disciplina"])

with tab_novo:
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.subheader("Cadastrar Nova Matéria")
    st.caption("Preencha as informações abaixo para adicionar a disciplina ao seu plano de estudos.")
    with st.form("form_disciplina"):
        nome = st.text_input("Nome da Disciplina", placeholder="Ex: Engenharia de Software")
        professor = st.text_input("Nome do Professor", placeholder="Ex: Prof. Dr. Silva")
        dia_semana = st.selectbox("Dia da Aula", ["Seg", "Ter", "Qua", "Qui", "Sex"])
        
        submitted = st.form_submit_button("Salvar Disciplina", use_container_width=True)
        if submitted:
            if not nome or not nome.strip():
                st.error("O nome da disciplina é obrigatório.")
            else:
                try:
                    subject_service.create_subject(
                        name=nome.strip(),
                        teacher=professor.strip(),
                        dia_semana=dia_semana,
                        token=token
                    )
                    st.success(f"Disciplina '{nome}' cadastrada com sucesso!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Erro ao cadastrar disciplina: {e}")
    st.markdown('</div>', unsafe_allow_html=True)

with tab_lista:
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    if not token:
        st.info("💡 Você está visualizando em modo local. Faça login na página Perfil para sincronizar seus dados com o Xano.")

    try:
        subjects = subject_service.list_subjects(token=token)
    except Exception as e:
        st.error(f"Erro ao carregar disciplinas: {e}")
        subjects = []

    # Mockup ou tabela real
    if subjects:
        table_data = [
            {
                "Nome": s.get("name") or s.get("Nome", ""),
                "Professor": s.get("teacher") or s.get("professor") or s.get("Professor", ""),
                "Dia": s.get("dia_semana") or s.get("Dia", "Seg")
            }
            for s in subjects
        ]
    else:
        table_data = [
            {"Nome": "Python Basics", "Professor": "Oriel", "Dia": "Seg"},
            {"Nome": "No-Code Advanced", "Professor": "Giuliano", "Dia": "Qui"},
        ]

    st.dataframe(table_data, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Gerenciamento (Atualizar e Excluir)
    if subjects:
        with st.expander("⚙️ Gerenciar Disciplina (Editar / Excluir)"):
            subject_options = {
                f"{s.get('name', 'Sem nome')} (ID: {s.get('id')})": s
                for s in subjects if s.get("id") is not None
            }
            if subject_options:
                selected_label = st.selectbox("Selecione a disciplina para gerenciar", list(subject_options.keys()))
                selected_subject = subject_options[selected_label]
                
                col_edit, col_del = st.columns(2)
                with col_edit:
                    st.markdown("**✏️ Atualizar Informações**")
                    novo_nome = st.text_input(
                        "Editar Nome",
                        value=selected_subject.get("name", ""),
                        key=f"edit_nome_{selected_subject['id']}"
                    )
                    novo_prof = st.text_input(
                        "Editar Professor",
                        value=selected_subject.get("teacher") or selected_subject.get("professor", ""),
                        key=f"edit_prof_{selected_subject['id']}"
                    )
                    if st.button("Salvar Alterações", key=f"btn_edit_{selected_subject['id']}", use_container_width=True):
                        try:
                            subject_service.update_subject(
                                selected_subject["id"],
                                token=token,
                                name=novo_nome,
                                teacher=novo_prof
                            )
                            st.success("Disciplina atualizada com sucesso!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Erro ao atualizar: {e}")
                
                with col_del:
                    st.markdown("**🗑️ Excluir Disciplina**")
                    st.caption("Esta ação removerá a disciplina permanentemente.")
                    if st.button("🗑️ Excluir", key=f"btn_del_{selected_subject['id']}", type="secondary", use_container_width=True):
                        sub_name = selected_subject.get("name") or selected_subject.get("Nome") or f"Disciplina #{selected_subject['id']}"
                        confirmar_exclusao_disciplina(selected_subject["id"], sub_name)
