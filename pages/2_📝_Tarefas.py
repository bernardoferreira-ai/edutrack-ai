import streamlit as st
import sys
import os

# Ensure services directory is accessible
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from services.task_service import TaskService
from services.subject_service import SubjectService

st.title("Minhas Tarefas")

task_service    = TaskService()
subject_service = SubjectService()
token = st.session_state.get("auth_token")

# ── Estado persistente na sessão ─────────────────────────────────────────────
if "tasks" not in st.session_state:
    st.session_state["tasks"] = [
        {
            "id": 1, "subject_id": 1,
            "title": "Tarefa 01: Configuração do Ambiente",
            "description": "",
            "due_date": "20/02/2026",
            "status": "completed",
        }
    ]
if "task_next_id" not in st.session_state:
    st.session_state["task_next_id"] = 2

# Garante que subjects existam (pode ter sido criado em outra aba)
if "subjects" not in st.session_state:
    st.session_state["subjects"] = [
        {"id": 1, "name": "Python Basics",    "teacher": "Oriel",    "dia_semana": "Seg"},
        {"id": 2, "name": "No-Code Advanced", "teacher": "Giuliano", "dia_semana": "Qui"},
    ]

# Se logado, tenta carregar do Xano e atualiza o estado da sessão
if token:
    try:
        xano_tasks = task_service.list_tasks(token=token)
        if isinstance(xano_tasks, list) and xano_tasks:
            st.session_state["tasks"] = xano_tasks
            max_id = max((t.get("id") or 0) for t in xano_tasks)
            st.session_state["task_next_id"] = max(max_id + 1, st.session_state["task_next_id"])
    except Exception:
        pass

    try:
        xano_subjects = subject_service.list_subjects(token=token)
        if isinstance(xano_subjects, list) and xano_subjects:
            st.session_state["subjects"] = xano_subjects
    except Exception:
        pass

subjects     = st.session_state["subjects"]
subject_map  = {
    s.get("id"): s.get("name") or f"Disciplina #{s.get('id')}"
    for s in subjects if s.get("id") is not None
}

# ── Helpers de CRUD local (session_state) ────────────────────────────────────
def _add_task(title, subject_id, description, due_date):
    new_id = st.session_state["task_next_id"]
    st.session_state["tasks"].append({
        "id": new_id, "subject_id": subject_id,
        "title": title, "description": description,
        "due_date": due_date, "status": "pending",
    })
    st.session_state["task_next_id"] += 1

def _remove_task(task_id):
    st.session_state["tasks"] = [
        t for t in st.session_state["tasks"] if t.get("id") != task_id
    ]

def _update_task(task_id, **fields):
    for t in st.session_state["tasks"]:
        if t.get("id") == task_id:
            t.update({k: v for k, v in fields.items() if v is not None})
            break

# ── Layout de busca e filtro existente ───────────────────────────────────────
col1, col2 = st.columns([3, 1])  # Coluna 1 é 3x maior que a 2

with col1:
    search = st.text_input("Buscar tarefa...", placeholder="Ex: Estudar Pandas")

with col2:
    filtro = st.selectbox("Status", ["Todas", "Pendente", "Concluída"])

st.markdown("---")

if not token:
    st.info("💡 Você está visualizando em modo local. Faça login na página Perfil para sincronizar suas tarefas com o Xano.")

# Filtrar tarefas da sessão por status e busca
all_tasks = st.session_state["tasks"]

status_map = {"Pendente": "pending", "Concluída": "completed"}
if filtro != "Todas":
    mapped_status = status_map.get(filtro, filtro.lower())
    all_tasks = [t for t in all_tasks if (t.get("status") or "").lower() == mapped_status]

filtered_tasks = [
    t for t in all_tasks
    if not search
    or search.lower() in (t.get("title") or "").lower()
    or search.lower() in (t.get("description") or "").lower()
]

# ── Renderizar tarefas ────────────────────────────────────────────────────────
if not filtered_tasks:
    with st.expander("📌 Tarefa 01: Configuração do Ambiente (Clique para ver)", expanded=True):
        st.write("**Disciplina:** Innovation Lab")
        st.write("**Prazo:** 20/02/2026")
        st.checkbox("Marcar como Concluída", value=True, key="mockup_chk")
else:
    for idx, task in enumerate(filtered_tasks):
        task_id      = task.get("id")
        title        = task.get("title") or f"Tarefa {idx + 1}"
        sub_name     = subject_map.get(task.get("subject_id"), "Innovation Lab")
        due_date     = task.get("due_date") or "20/02/2026"
        is_completed = (task.get("status", "").lower() == "completed")

        with st.expander(f"📌 {title} (Clique para ver)", expanded=(idx == 0)):
            st.write(f"**Disciplina:** {sub_name}")
            st.write(f"**Prazo:** {due_date}")

            chk_val = st.checkbox(
                "Marcar como Concluída",
                value=is_completed,
                key=f"task_chk_{task_id}_{idx}",
            )
            if chk_val != is_completed:
                new_status = "completed" if chk_val else "pending"
                _update_task(task_id, status=new_status)
                if token:
                    try:
                        task_service.update_task(task_id, token=token, status=new_status)
                    except Exception:
                        pass
                st.rerun()

            if st.button("🗑️ Excluir Tarefa", key=f"del_task_{task_id}_{idx}", type="secondary"):
                _remove_task(task_id)
                if token:
                    try:
                        task_service.delete_task(task_id, token=token)
                    except Exception:
                        pass
                st.warning("Tarefa excluída!")
                st.rerun()

# ── Cadastrar nova tarefa ─────────────────────────────────────────────────────
with st.expander("➕ Nova Tarefa"):
    with st.form("form_nova_tarefa"):
        novo_titulo = st.text_input("Título da Tarefa", placeholder="Ex: Estudar Pandas")

        sub_choices = {
            f"{s.get('name', 'Sem nome')} (ID: {s.get('id')})": s.get("id")
            for s in subjects if s.get("id") is not None
        }
        if sub_choices:
            sel_sub_label = st.selectbox("Disciplina", list(sub_choices.keys()))
            sel_sub_id    = sub_choices[sel_sub_label]
        else:
            st.info("Nenhuma disciplina cadastrada. Cadastre disciplinas na tela de Disciplinas.")
            sel_sub_id = 1

        novo_prazo = st.text_input("Prazo", value="20/02/2026")
        nova_desc  = st.text_area("Descrição (opcional)", placeholder="Detalhes da tarefa...")

        if st.form_submit_button("Salvar Tarefa"):
            if not novo_titulo or not novo_titulo.strip():
                st.error("O título da tarefa é obrigatório.")
            else:
                # Salva localmente primeiro → garante que aparece na lista
                _add_task(
                    title=novo_titulo.strip(),
                    subject_id=sel_sub_id,
                    description=nova_desc.strip() if nova_desc else "",
                    due_date=novo_prazo.strip() or "20/02/2026",
                )

                # Tenta sincronizar com Xano (se logado)
                if token:
                    try:
                        task_service.create_task(
                            title=novo_titulo.strip(),
                            subject_id=sel_sub_id,
                            description=nova_desc.strip() if nova_desc else "",
                            due_date=novo_prazo.strip() or None,
                            token=token,
                        )
                        st.success(f"Tarefa **'{novo_titulo}'** criada com sucesso!")
                    except Exception:
                        st.success(f"Tarefa **'{novo_titulo}'** criada! (Dados salvos localmente; sincronização com Xano pendente.)")
                else:
                    st.success(f"Tarefa **'{novo_titulo}'** criada! (Simulação)")

                st.rerun()
