import json
import os
import sys
import uuid
from datetime import datetime

import streamlit as st

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from services.design_service import apply_edutrack_design

apply_edutrack_design()
st.set_page_config(page_title="Anotações", page_icon="📝", layout="wide")

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
NOTES_FILE = os.path.join(DATA_DIR, "notes.json")

st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background: linear-gradient(180deg, #0b0f19 0%, #0f172a 50%, #0b0f19 100%);
}
.notes-hero {
    background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 60%, #172554 100%);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 20px;
    padding: 1.8rem 2.2rem;
    margin-bottom: 1.2rem;
}
.notes-title { font-size: 2rem; font-weight: 800; margin: 0; }
.notes-subtitle { color: #94a3b8; margin-top: 0.35rem; }
.note-card {
    background: #161e2e;
    border: 1px solid rgba(148,163,184,0.16);
    border-radius: 16px;
    padding: 1.1rem 1.2rem;
    margin-bottom: 0.8rem;
}
.note-category {
    display: inline-block;
    color: #93c5fd;
    background: rgba(59,130,246,0.12);
    border: 1px solid rgba(147,197,253,0.18);
    border-radius: 999px;
    padding: 0.18rem 0.65rem;
    font-size: 0.78rem;
    font-weight: 700;
}
.note-date { color: #94a3b8; font-size: 0.78rem; }
</style>
""", unsafe_allow_html=True)


def load_notes():
    os.makedirs(DATA_DIR, exist_ok=True)
    if not os.path.exists(NOTES_FILE):
        return []
    try:
        with open(NOTES_FILE, "r", encoding="utf-8") as file:
            notes = json.load(file)
            return notes if isinstance(notes, list) else []
    except (OSError, json.JSONDecodeError):
        return []


def save_notes(notes):
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(NOTES_FILE, "w", encoding="utf-8") as file:
        json.dump(notes, file, ensure_ascii=False, indent=2)


if "notes_list" not in st.session_state:
    st.session_state.notes_list = load_notes()

st.markdown("""
<div class="notes-hero">
    <h1 class="notes-title">📝 Anotações</h1>
    <div class="notes-subtitle">Capture ideias, lembretes e conteúdos importantes para estudar depois.</div>
</div>
""", unsafe_allow_html=True)

left, right = st.columns([1.05, 1.75], gap="large")

with left:
    st.markdown("### Nova anotação")

    with st.form("new_note_form", clear_on_submit=True):
        title = st.text_input("Título", placeholder="Ex.: Revisão de cálculo")
        category = st.selectbox("Categoria", ["Estudos", "Tarefa", "Disciplina", "Ideia", "Pessoal"])
        content = st.text_area("Anotação", height=220, placeholder="Escreva aqui...")
        submitted = st.form_submit_button("💾 Salvar anotação", type="primary", width="stretch")

        if submitted:
            title = title.strip()
            content = content.strip()
            if not title:
                st.error("Dê um título para a anotação.")
            elif not content:
                st.error("Escreva alguma anotação antes de salvar.")
            else:
                now = datetime.now()
                st.session_state.notes_list.insert(0, {
                    "id": str(uuid.uuid4()),
                    "title": title,
                    "category": category,
                    "content": content,
                    "updated_at": now.isoformat(),
                })
                save_notes(st.session_state.notes_list)
                st.success("Anotação salva!")
                st.rerun()

with right:
    st.markdown("### Minhas anotações")

    search = st.text_input("🔎 Buscar", placeholder="Título ou conteúdo...")
    category_filter = st.selectbox("Categoria", ["Todas", "Estudos", "Tarefa", "Disciplina", "Ideia", "Pessoal"])

    notes = st.session_state.notes_list
    query = search.strip().lower()

    filtered = []
    for note in notes:
        matches_search = not query or query in note["title"].lower() or query in note["content"].lower()
        matches_category = category_filter == "Todas" or note["category"] == category_filter
        if matches_search and matches_category:
            filtered.append(note)

    if not filtered:
        st.info("Nenhuma anotação encontrada. Crie uma nova ao lado.")
    else:
        st.caption(f"{len(filtered)} anotação(ões) encontrada(s)")

        for note in filtered:
            with st.container(border=True):
                col_text, col_actions = st.columns([4, 1])

                with col_text:
                    st.markdown(f'<span class="note-category">{note["category"]}</span>', unsafe_allow_html=True)
                    st.markdown(f"#### {note['title']}")
                    st.write(note["content"])
                    try:
                        date_text = datetime.fromisoformat(note["updated_at"]).strftime("%d/%m/%Y às %H:%M")
                    except (KeyError, ValueError):
                        date_text = "Data não disponível"
                    st.markdown(f'<span class="note-date">Atualizada em {date_text}</span>', unsafe_allow_html=True)

                with col_actions:
                    edit_key = f"edit_{note['id']}"
                    delete_key = f"delete_{note['id']}"

                    if st.button("✏️ Editar", key=edit_key, use_container_width=True):
                        st.session_state["editing_note"] = note["id"]

                    if st.button("🗑️ Excluir", key=delete_key, use_container_width=True):
                        st.session_state["deleting_note"] = note["id"]

        editing_id = st.session_state.get("editing_note")
        if editing_id:
            editing = next((note for note in notes if note["id"] == editing_id), None)
            if editing:
                st.divider()
                st.markdown("### Editar anotação")
                edit_title = st.text_input("Título", value=editing["title"], key="edit_title")
                edit_category = st.selectbox(
                    "Categoria",
                    ["Estudos", "Tarefa", "Disciplina", "Ideia", "Pessoal"],
                    index=["Estudos", "Tarefa", "Disciplina", "Ideia", "Pessoal"].index(editing["category"]),
                    key="edit_category",
                )
                edit_content = st.text_area("Anotação", value=editing["content"], height=220, key="edit_content")

                edit_buttons = st.columns(2)
                if edit_buttons[0].button("Salvar alterações", type="primary", use_container_width=True):
                    if edit_title.strip() and edit_content.strip():
                        editing["title"] = edit_title.strip()
                        editing["category"] = edit_category
                        editing["content"] = edit_content.strip()
                        editing["updated_at"] = datetime.now().isoformat()
                        save_notes(notes)
                        st.session_state.pop("editing_note", None)
                        st.success("Alterações salvas!")
                        st.rerun()
                    else:
                        st.error("Título e conteúdo não podem ficar vazios.")

                if edit_buttons[1].button("Cancelar", use_container_width=True):
                    st.session_state.pop("editing_note", None)
                    st.rerun()

        deleting_id = st.session_state.get("deleting_note")
        if deleting_id:
            deleting = next((note for note in notes if note["id"] == deleting_id), None)
            if deleting:
                st.warning(f'Excluir a anotação "{deleting["title"]}"?')
                delete_buttons = st.columns(2)
                if delete_buttons[0].button("Confirmar exclusão", type="primary", use_container_width=True):
                    notes = [note for note in notes if note["id"] != deleting_id]
                    st.session_state.notes_list = notes
                    save_notes(notes)
                    st.session_state.pop("deleting_note", None)
                    st.success("Anotação excluída.")
                    st.rerun()
                if delete_buttons[1].button("Cancelar exclusão", use_container_width=True):
                    st.session_state.pop("deleting_note", None)
                    st.rerun()
