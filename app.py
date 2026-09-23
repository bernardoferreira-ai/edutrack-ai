import streamlit as st
from services.subject_service import SubjectService

# Configuração da Página
st.set_page_config(page_title="EduTrack AI", page_icon="🎓", layout="wide")

# Inicialização do serviço na sessão
if "subject_service" not in st.session_state:
    st.session_state.subject_service = SubjectService()

service: SubjectService = st.session_state.subject_service

# Título Principal
st.title("🎓 EduTrack AI")

# Sidebar (Menu Lateral)
st.sidebar.header("Menu")
menu_option = st.sidebar.radio("Navegar", ["Dashboard", "Disciplinas", "Tarefas"])

# Badge / tradução de status
STATUS_LABELS = {
    "active": "🟢 Ativa",
    "completed": "🔵 Concluída",
    "archived": "⚪ Arquivada"
}

# Conteúdo Dinâmico
if menu_option == "Dashboard":
    st.header("📊 Painel Geral")
    st.write("Bem-vindo ao seu assistente acadêmico!")

    active_count = service.get_active_count()
    all_subjects = service.list_subjects()
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Disciplinas Ativas", str(active_count))
    col2.metric("Total de Disciplinas", str(len(all_subjects)))
    col3.metric("Tarefas Pendentes", "0")

    st.divider()
    st.subheader("Disciplinas em Andamento")
    active_subjects = service.list_subjects(status="active")
    if active_subjects:
        for sub in active_subjects:
            with st.container():
                st.markdown(
                    f"**{sub['name']}** `{sub.get('code', '')}` — *{sub.get('professor', 'Sem professor definido')}* "
                    f"({sub.get('semester', 'Sem semestre')})"
                )
    else:
        st.info("Nenhuma disciplina ativa no momento. Cadastre novas matérias na aba 'Disciplinas'.")

elif menu_option == "Disciplinas":
    st.header("📚 Minhas Disciplinas")
    st.write("Gerencie os cursos e matérias do seu semestre letivo.")

    # Filtros e Ações superiores
    top_col1, top_col2 = st.columns([3, 1])
    with top_col1:
        status_filter = st.selectbox(
            "Filtrar por Status",
            ["Todas", "Ativas", "Concluídas", "Arquivadas"],
            index=0
        )
    with top_col2:
        show_form = st.toggle("➕ Nova Disciplina")

    # Mapeamento do filtro para o serviço
    status_map = {
        "Todas": None,
        "Ativas": "active",
        "Concluídas": "completed",
        "Arquivadas": "archived"
    }
    selected_status = status_map[status_filter]

    # Formulário de Criação
    if show_form:
        with st.form("form_nova_disciplina", clear_on_submit=True):
            st.subheader("Cadastrar Nova Disciplina")
            f_col1, f_col2 = st.columns(2)
            with f_col1:
                nome = st.text_input("Nome da Disciplina *", placeholder="Ex: Innovation Lab")
                codigo = st.text_input("Código da Matéria", placeholder="Ex: ILAB101")
                professor = st.text_input("Professor(a)", placeholder="Ex: Dr. Silva")
            with f_col2:
                semestre = st.text_input("Semestre / Período", placeholder="Ex: 2026.1")
                status = st.selectbox("Status", ["active", "completed", "archived"], format_func=lambda s: STATUS_LABELS.get(s, s))
                cor = st.color_picker("Cor de Identificação", "#3B82F6")

            submitted = st.form_submit_button("Salvar Disciplina", use_container_width=True)
            if submitted:
                if not nome.strip():
                    st.error("O nome da disciplina é obrigatório.")
                else:
                    service.create_subject(
                        name=nome,
                        code=codigo,
                        professor=professor,
                        semester=semestre,
                        color=cor,
                        status=status
                    )
                    st.success(f"Disciplina '{nome}' cadastrada com sucesso!")
                    st.rerun()

    # Listagem de Disciplinas
    subjects = service.list_subjects(status=selected_status)
    if not subjects:
        st.info("Nenhuma disciplina encontrada com o filtro selecionado.")
    else:
        st.write(f"Exibindo **{len(subjects)}** disciplina(s):")
        for sub in subjects:
            with st.expander(f"{sub['name']} ({sub.get('code', 'S/ Cód')}) — {STATUS_LABELS.get(sub.get('status', 'active'))}"):
                c1, c2 = st.columns([3, 1])
                with c1:
                    st.write(f"**Professor(a):** {sub.get('professor') or 'Não informado'}")
                    st.write(f"**Semestre:** {sub.get('semester') or 'Não informado'}")
                    st.write(f"**Status atual:** {STATUS_LABELS.get(sub.get('status'), sub.get('status'))}")
                with c2:
                    st.write("**Ações:**")
                    edit_key = f"edit_btn_{sub['id']}"
                    del_key = f"del_btn_{sub['id']}"
                    
                    if st.button("🗑️ Excluir", key=del_key, use_container_width=True):
                        service.delete_subject(sub["id"])
                        st.warning(f"Disciplina '{sub['name']}' removida.")
                        st.rerun()

                # Seção de Edição Rápida
                with st.popover("✏️ Editar Detalhes"):
                    with st.form(key=f"edit_form_{sub['id']}"):
                        ed_nome = st.text_input("Nome", value=sub["name"])
                        ed_codigo = st.text_input("Código", value=sub.get("code", ""))
                        ed_prof = st.text_input("Professor", value=sub.get("professor", ""))
                        ed_sem = st.text_input("Semestre", value=sub.get("semester", ""))
                        status_keys = ["active", "completed", "archived"]
                        cur_status_idx = status_keys.index(sub.get("status", "active")) if sub.get("status") in status_keys else 0
                        ed_status = st.selectbox("Status", status_keys, index=cur_status_idx, format_func=lambda s: STATUS_LABELS.get(s, s))

                        ed_submit = st.form_submit_button("Salvar Alterações")
                        if ed_submit:
                            service.update_subject(
                                sub["id"],
                                name=ed_nome,
                                code=ed_codigo,
                                professor=ed_prof,
                                semester=ed_sem,
                                status=ed_status
                            )
                            st.success("Disciplina atualizada!")
                            st.rerun()

elif menu_option == "Tarefas":
    st.subheader("Gerenciamento de Tarefas")
    st.info("O módulo de tarefas será vinculado às disciplinas cadastradas.")
    st.checkbox("Exemplo: Estudar Streamlit")