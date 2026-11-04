import streamlit as st
import sys
import os

# Ensure services directory is accessible
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from services.subject_service import SubjectService

st.set_page_config(page_title="Disciplinas", page_icon="📚")

st.title("Gestão de Disciplinas")

# Initialize service and retrieve auth token
subject_service = SubjectService()
token = st.session_state.get("auth_token")

# Abas para separar Listagem de Cadastro
tab_lista, tab_novo = st.tabs(["📋 Listar", "➕ Nova Disciplina"])

with tab_novo:
    st.subheader("Cadastrar Nova Matéria")
    with st.form("form_disciplina"):
        nome = st.text_input("Nome da Disciplina")
        professor = st.text_input("Nome do Professor")
        dia_semana = st.selectbox("Dia da Aula", ["Seg", "Ter", "Qua", "Qui", "Sex"])
        
        submitted = st.form_submit_button("Salvar")
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
                    st.success(f"Disciplina {nome} cadastrada com sucesso!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Erro ao cadastrar disciplina: {e}")

with tab_lista:
    if not token:
        st.info("💡 Você está visualizando em modo local. Faça login na página Perfil para sincronizar seus dados com o Xano.")

    try:
        subjects = subject_service.list_subjects(token=token)
    except Exception as e:
        st.error(f"Erro ao carregar disciplinas: {e}")
        subjects = []

    # Mockup de uma tabela
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

    # Gerenciamento (Atualizar e Excluir)
    if subjects:
        with st.expander("⚙️ Gerenciar Disciplina (Editar / Excluir)"):
            subject_options = {
                f"{s.get('name', 'Sem nome')} (ID: {s.get('id')})": s
                for s in subjects if s.get("id") is not None
            }
            if subject_options:
                selected_label = st.selectbox("Selecione a disciplina", list(subject_options.keys()))
                selected_subject = subject_options[selected_label]
                
                col_edit, col_del = st.columns(2)
                with col_edit:
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
                    if st.button("Salvar Alterações", key=f"btn_edit_{selected_subject['id']}"):
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
                    st.write("**Excluir Disciplina**")
                    st.caption("Esta ação removerá a disciplina permanentemente.")
                    if st.button("🗑️ Excluir", key=f"btn_del_{selected_subject['id']}", type="secondary"):
                        try:
                            subject_service.delete_subject(selected_subject["id"], token=token)
                            st.warning("Disciplina excluída com sucesso!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Erro ao excluir: {e}")
