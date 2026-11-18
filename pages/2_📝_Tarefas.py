import streamlit as st
import sys
import os

# Ensure services directory is accessible
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from services.task_service import TaskService
from services.subject_service import SubjectService

st.set_page_config(page_title="Tarefas", page_icon="📝", layout="wide")

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

    /* Search & Filter Panel */
    .filter-panel {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 18px;
        padding: 1.4rem 1.7rem;
        box-shadow: 0 6px 20px -3px rgba(15, 23, 42, 0.04);
        margin-bottom: 1.5rem;
    }

    /* Expander Modernization */
    .stExpander {
        background: #ffffff !important;
        border-radius: 18px !important;
        border: 1px solid rgba(226, 232, 240, 0.9) !important;
        box-shadow: 0 4px 16px -2px rgba(15, 23, 42, 0.05) !important;
        overflow: hidden !important;
        margin-bottom: 1rem !important;
        transition: all 0.2s ease !important;
    }
    .stExpander:hover {
        border-color: rgba(99, 102, 241, 0.3) !important;
        box-shadow: 0 8px 24px -4px rgba(15, 23, 42, 0.08) !important;
    }
    [data-testid="stExpanderToggleIcon"] {
        color: #4338ca !important;
    }

    /* Task Meta Badges */
    .task-meta-bar {
        display: flex;
        gap: 0.6rem;
        flex-wrap: wrap;
        margin-bottom: 1rem;
        align-items: center;
    }
    .meta-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.35rem;
        padding: 0.35rem 0.8rem;
        border-radius: 8px;
        font-size: 0.85rem;
        font-weight: 600;
    }
    .badge-subject {
        background: #eef2ff;
        color: #4338ca;
    }
    .badge-date {
        background: #f1f5f9;
        color: #475569;
    }
    .badge-status-completed {
        background: rgba(16, 185, 129, 0.12);
        color: #059669;
        font-weight: 700;
    }
    .badge-status-pending {
        background: rgba(245, 158, 11, 0.12);
        color: #d97706;
        font-weight: 700;
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
                <h1 class="page-title">Minhas Tarefas</h1>
                <div class="page-subtitle">Organize suas atividades, acompanhe prazos e monitore seu progresso.</div>
            </div>
            <div class="page-pill">📝 Gestão de Tarefas</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# Initialize services and retrieve auth token
task_service = TaskService()
subject_service = SubjectService()
token = st.session_state.get("auth_token")

def excluir_tarefa(task_id: int) -> bool:
    """Função utilitária para excluir uma tarefa pelo ID."""
    return task_service.delete_task(task_id, token=token)

@st.dialog("Confirmar Exclusão")
def confirmar_exclusao_tarefa(task_id: int, task_title: str):
    st.warning(f"Você realmente deseja excluir a tarefa **{task_title}**?")
    st.caption("Esta ação removerá a tarefa permanentemente.")
    col_sim, col_nao = st.columns(2)
    with col_sim:
        if st.button("Sim, excluir", type="primary", key=f"modal_confirm_del_task_{task_id}"):
            try:
                excluir_tarefa(task_id)
                st.warning("Tarefa excluída com sucesso!")
                st.rerun()
            except Exception as e:
                st.error(f"Erro ao excluir: {e}")
    with col_nao:
        if st.button("Cancelar", key=f"modal_cancel_del_task_{task_id}"):
            st.rerun()

# Layout de busca e filtro em painel estilizado
st.markdown('<div class="filter-panel">', unsafe_allow_html=True)
col1, col2 = st.columns([3, 1])

with col1:
    search = st.text_input("Buscar tarefa...", placeholder="Ex: Estudar Pandas")

with col2:
    filtro = st.selectbox("Status", ["Todas", "Pendente", "Concluída"])

if not token:
    st.info("💡 Você está visualizando em modo local. Faça login na página Perfil para sincronizar suas tarefas com o Xano.")

st.markdown('</div>', unsafe_allow_html=True)

# Carregar disciplinas para mapear subject_id -> nome
try:
    subjects = subject_service.list_subjects(token=token)
except Exception:
    subjects = []

subject_map = {
    s.get("id"): s.get("name") or s.get("Nome") or f"Disciplina #{s.get('id')}"
    for s in subjects if s.get("id") is not None
}

# Carregar tarefas do backend
try:
    all_tasks = task_service.list_tasks(token=token, status=filtro)
except Exception as e:
    st.error(f"Erro ao carregar tarefas: {e}")
    all_tasks = []

# Filtragem de busca por texto
filtered_tasks = [
    t for t in all_tasks
    if not search
    or search.lower() in (t.get("title") or "").lower()
    or search.lower() in (t.get("description") or "").lower()
]

# Renderizar tarefas ou mockup inicial
if not filtered_tasks:
    if not st.session_state.get("hide_mockup_task"):
        with st.expander("📌 Tarefa 01: Configuração do Ambiente (Clique para ver)", expanded=True):
            st.markdown(
                """
                <div class="task-meta-bar">
                    <span class="meta-badge badge-subject">📚 Innovation Lab</span>
                    <span class="meta-badge badge-date">📅 Prazo: 20/02/2026</span>
                    <span class="meta-badge badge-status-completed">✅ Concluída</span>
                </div>
                """,
                unsafe_allow_html=True,
            )
            col_m1, col_m2 = st.columns([3, 1])
            with col_m1:
                st.checkbox("Marcar como Concluída", value=True, key="mockup_chk")
            with col_m2:
                if st.button("🗑️ Excluir Tarefa", key="del_task_btn_mockup", type="secondary", use_container_width=True):
                    st.session_state["hide_mockup_task"] = True
                    st.warning("Tarefa excluída com sucesso!")
                    st.rerun()
else:
    for idx, task in enumerate(filtered_tasks):
        task_id = task.get("id")
        title = task.get("title") or f"Tarefa {idx + 1}"
        sub_id = task.get("subject_id")
        sub_name = subject_map.get(sub_id, "Innovation Lab")
        due_date = task.get("due_date") or "20/02/2026"
        is_completed = (str(task.get("status", "")).lower() == "completed")
        badge_status_class = "badge-status-completed" if is_completed else "badge-status-pending"
        badge_status_label = "✅ Concluída" if is_completed else "⏳ Pendente"

        with st.expander(f"📌 {title} (Clique para ver)", expanded=(idx == 0)):
            st.markdown(
                f"""
                <div class="task-meta-bar">
                    <span class="meta-badge badge-subject">📚 {sub_name}</span>
                    <span class="meta-badge badge-date">📅 Prazo: {due_date}</span>
                    <span class="meta-badge {badge_status_class}">{badge_status_label}</span>
                </div>
                """,
                unsafe_allow_html=True,
            )

            col_chk, col_del = st.columns([3, 1])
            with col_chk:
                chk_key = f"task_chk_{task_id}_{idx}"
                chk_val = st.checkbox("Marcar como Concluída", value=is_completed, key=chk_key)
                if chk_val != is_completed:
                    new_status = "completed" if chk_val else "pending"
                    try:
                        task_service.update_task(task_id, token=token, status=new_status)
                        st.rerun()
                    except Exception as e:
                        st.error(f"Erro ao atualizar status: {e}")

            with col_del:
                if st.button("🗑️ Excluir Tarefa", key=f"del_task_btn_{task_id}_{idx}", type="secondary", use_container_width=True):
                    confirmar_exclusao_tarefa(task_id, title)

# Gerenciamento de Tarefas (Exclusão por seleção)
if all_tasks:
    with st.expander("⚙️ Gerenciar Tarefas (Excluir)"):
        task_options = {
            f"{t.get('title', 'Sem título')} (ID: {t.get('id')})": t.get("id")
            for t in all_tasks if t.get("id") is not None
        }
        if task_options:
            sel_task_label = st.selectbox("Selecione a tarefa para excluir", list(task_options.keys()))
            sel_task_id = task_options[sel_task_label]
            st.caption("Esta ação removerá a tarefa permanentemente.")
            if st.button("🗑️ Excluir Tarefa Selecionada", key="btn_del_selected_task", type="secondary", use_container_width=True):
                confirmar_exclusao_tarefa(sel_task_id, sel_task_label)

# Seção para cadastrar nova tarefa
with st.expander("➕ Nova Tarefa"):
    with st.form("form_nova_tarefa"):
        novo_titulo = st.text_input("Título da Tarefa", placeholder="Ex: Estudar Pandas")

        # Opções de disciplinas disponíveis
        sub_choices = {
            f"{s.get('name') or s.get('Nome', 'Sem nome')} (ID: {s.get('id')})": s.get("id")
            for s in subjects if s.get("id") is not None
        }

        if sub_choices:
            sel_sub_label = st.selectbox("Disciplina", list(sub_choices.keys()))
            sel_sub_id = sub_choices[sel_sub_label]
        else:
            st.info("Nenhuma disciplina cadastrada. Cadastre disciplinas na tela de Disciplinas.")
            sel_sub_id = 1

        novo_prazo = st.text_input("Prazo", value="20/02/2026")
        nova_desc = st.text_area("Descrição (opcional)", placeholder="Detalhes da tarefa...")

        btn_salvar_tarefa = st.form_submit_button("Salvar Tarefa", use_container_width=True)
        if btn_salvar_tarefa:
            if not novo_titulo or not novo_titulo.strip():
                st.error("O título da tarefa é obrigatório.")
            else:
                try:
                    task_service.create_task(
                        title=novo_titulo.strip(),
                        subject_id=sel_sub_id,
                        description=nova_desc.strip() if nova_desc and nova_desc.strip() else None,
                        due_date=novo_prazo.strip() if novo_prazo else None,
                        token=token
                    )
                    st.success(f"Tarefa '{novo_titulo}' criada com sucesso!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Erro ao criar tarefa: {e}")
