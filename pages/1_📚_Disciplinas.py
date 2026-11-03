import streamlit as st
import sys
import os

# Ensure services directory is accessible
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from services.subject_service import SubjectService

st.set_page_config(page_title="Disciplinas", page_icon="📚")

st.title("Gestão de Disciplinas")

subject_service = SubjectService()
token = st.session_state.get("auth_token")

# ── Estado persistente na sessão ─────────────────────────────────────────────
if "subjects" not in st.session_state:
    st.session_state["subjects"] = [
        {"id": 1, "name": "Python Basics",   "teacher": "Oriel",   "dia_semana": "Seg"},
        {"id": 2, "name": "No-Code Advanced", "teacher": "Giuliano", "dia_semana": "Qui"},
    ]
if "subject_next_id" not in st.session_state:
    st.session_state["subject_next_id"] = 3

# Se logado, tenta carregar do Xano e atualiza o estado da sessão
if token:
    try:
        xano_subjects = subject_service.list_subjects(token=token)
        if isinstance(xano_subjects, list) and xano_subjects:
            st.session_state["subjects"] = xano_subjects
            # Garante que o próximo ID local seja maior que qualquer ID do Xano
            max_id = max((s.get("id") or 0) for s in xano_subjects)
            st.session_state["subject_next_id"] = max(max_id + 1, st.session_state["subject_next_id"])
    except Exception:
        pass  # Mantém os dados da sessão

subjects = st.session_state["subjects"]

# ── Helpers de CRUD local (session_state) ────────────────────────────────────
def _add_subject(name, teacher, dia_semana):
    new_id = st.session_state["subject_next_id"]
    st.session_state["subjects"].append(
        {"id": new_id, "name": name, "teacher": teacher, "dia_semana": dia_semana}
    )
    st.session_state["subject_next_id"] += 1

def _remove_subject(subject_id):
    st.session_state["subjects"] = [
        s for s in st.session_state["subjects"] if s.get("id") != subject_id
    ]

def _edit_subject(subject_id, name, teacher):
    for s in st.session_state["subjects"]:
        if s.get("id") == subject_id:
            s["name"]    = name
            s["teacher"] = teacher
            break

# ── Abas ─────────────────────────────────────────────────────────────────────
tab_lista, tab_novo = st.tabs(["📋 Listar", "➕ Nova Disciplina"])

with tab_novo:
    st.subheader("Cadastrar Nova Matéria")
    with st.form("form_disciplina"):
        nome      = st.text_input("Nome da Disciplina")
        professor = st.text_input("Nome do Professor")
        dia_semana = st.selectbox("Dia da Aula", ["Seg", "Ter", "Qua", "Qui", "Sex"])

        submitted = st.form_submit_button("Salvar")
        if submitted:
            if not nome or not nome.strip():
                st.error("O nome da disciplina é obrigatório.")
            else:
                # Sempre salva localmente primeiro → garante que aparece na lista
                _add_subject(nome.strip(), professor.strip(), dia_semana)

                # Tenta sincronizar com Xano (se logado)
                if token:
                    try:
                        subject_service.create_subject(
                            name=nome.strip(),
                            teacher=professor.strip(),
                            token=token,
                        )
                        st.success(f"Disciplina **{nome}** cadastrada com sucesso!")
                    except Exception:
                        st.success(f"Disciplina **{nome}** cadastrada! (Dados salvos localmente; sincronização com Xano pendente.)")
                else:
                    st.success(f"Disciplina **{nome}** cadastrada! (Simulação)")

                st.rerun()

with tab_lista:
    if not token:
        st.info("💡 Você está visualizando em modo local. Faça login na página Perfil para sincronizar seus dados com o Xano.")

    # Monta tabela para exibição
    table_data = [
        {
            "Nome":      s.get("name")    or "",
            "Professor": s.get("teacher") or s.get("professor") or "",
            "Dia":       s.get("dia_semana") or "Seg",
        }
        for s in subjects
    ]
    st.dataframe(table_data, use_container_width=True)

    # Gerenciar (Editar / Excluir)
    if subjects:
        with st.expander("⚙️ Gerenciar Disciplina (Editar / Excluir)"):
            opts = {
                f"{s.get('name', 'Sem nome')} (ID: {s.get('id')})": s
                for s in subjects if s.get("id") is not None
            }
            if opts:
                label    = st.selectbox("Selecione a disciplina", list(opts.keys()))
                selected = opts[label]

                col_edit, col_del = st.columns(2)

                with col_edit:
                    novo_nome = st.text_input(
                        "Editar Nome",
                        value=selected.get("name", ""),
                        key=f"edit_nome_{selected['id']}",
                    )
                    novo_prof = st.text_input(
                        "Editar Professor",
                        value=selected.get("teacher") or selected.get("professor", ""),
                        key=f"edit_prof_{selected['id']}",
                    )
                    if st.button("Salvar Alterações", key=f"btn_edit_{selected['id']}"):
                        _edit_subject(selected["id"], novo_nome, novo_prof)
                        if token:
                            try:
                                subject_service.update_subject(selected["id"], token=token, name=novo_nome, teacher=novo_prof)
                            except Exception:
                                pass
                        st.success("Disciplina atualizada!")
                        st.rerun()

                with col_del:
                    st.write("**Excluir Disciplina**")
                    st.caption("Esta ação removerá a disciplina permanentemente.")
                    if st.button("🗑️ Excluir", key=f"btn_del_{selected['id']}", type="secondary"):
                        _remove_subject(selected["id"])
                        if token:
                            try:
                                subject_service.delete_subject(selected["id"], token=token)
                            except Exception:
                                pass
                        st.warning("Disciplina excluída!")
                        st.rerun()
