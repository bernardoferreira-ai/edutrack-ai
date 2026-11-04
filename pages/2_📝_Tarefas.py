import streamlit as st
import sys
import os

# Ensure services directory is accessible
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from services.task_service import TaskService
from services.subject_service import SubjectService

st.title("Minhas Tarefas")

# Initialize services and retrieve auth token
task_service = TaskService()
subject_service = SubjectService()
token = st.session_state.get("auth_token")

# Layout de busca e filtro existente
col1, col2 = st.columns([3, 1]) # Coluna 1 é 3x maior que a 2

with col1:
    search = st.text_input("Buscar tarefa...", placeholder="Ex: Estudar Pandas")

with col2:
    filtro = st.selectbox("Status", ["Todas", "Pendente", "Concluída"])

st.markdown("---")

if not token:
    st.info("💡 Você está visualizando em modo local. Faça login na página Perfil para sincronizar suas tarefas com o Xano.")

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
    with st.expander("📌 Tarefa 01: Configuração do Ambiente (Clique para ver)", expanded=True):
        st.write("**Disciplina:** Innovation Lab")
        st.write("**Prazo:** 20/02/2026")
        st.checkbox("Marcar como Concluída", value=True, key="mockup_chk")
else:
    for idx, task in enumerate(filtered_tasks):
        task_id = task.get("id")
        title = task.get("title") or f"Tarefa {idx + 1}"
        sub_id = task.get("subject_id")
        sub_name = subject_map.get(sub_id, "Innovation Lab")
        due_date = task.get("due_date") or "20/02/2026"
        is_completed = (str(task.get("status", "")).lower() == "completed")

        with st.expander(f"📌 {title} (Clique para ver)", expanded=(idx == 0)):
            st.write(f"**Disciplina:** {sub_name}")
            st.write(f"**Prazo:** {due_date}")

            # Checkbox interativo para marcar como concluída
            chk_key = f"task_chk_{task_id}_{idx}"
            chk_val = st.checkbox("Marcar como Concluída", value=is_completed, key=chk_key)
            if chk_val != is_completed:
                new_status = "completed" if chk_val else "pending"
                try:
                    task_service.update_task(task_id, token=token, status=new_status)
                    st.rerun()
                except Exception as e:
                    st.error(f"Erro ao atualizar status: {e}")

            # Opção de exclusão
            if st.button("🗑️ Excluir Tarefa", key=f"del_task_btn_{task_id}_{idx}", type="secondary"):
                try:
                    task_service.delete_task(task_id, token=token)
                    st.warning("Tarefa excluída com sucesso!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Erro ao excluir tarefa: {e}")

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

        btn_salvar_tarefa = st.form_submit_button("Salvar Tarefa")
        if btn_salvar_tarefa:
            if not novo_titulo or not novo_titulo.strip():
                st.error("O título da tarefa é obrigatório.")
            else:
                try:
                    task_service.create_task(
                        title=novo_titulo.strip(),
                        subject_id=sel_sub_id,
                        description=nova_desc.strip() if nova_desc else "",
                        due_date=novo_prazo.strip() if novo_prazo else None,
                        token=token
                    )
                    st.success(f"Tarefa '{novo_titulo}' criada com sucesso!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Erro ao criar tarefa: {e}")
