import streamlit as st
import sys
import os

# Ensure services directory is accessible
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from services.subject_service import SubjectService
from services.design_service import apply_edutrack_design

# Apply EduTrack visual system design
apply_edutrack_design()

st.set_page_config(page_title="Notas & Desempenho", page_icon="📊", layout="wide")

# Custom CSS for Dark Theme and Status Badges
st.markdown(
    """
    <style>
    /* Dark Theme Global View */
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(180deg, #0b0f19 0%, #0f172a 50%, #0b0f19 100%);
        color: #f8fafc;
    }
    [data-testid="stSidebar"] {
        background-color: #111827;
        border-right: 1px solid rgba(255, 255, 255, 0.08);
    }

    /* Page Header Shell */
    .page-shell {
        background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 60%, #172554 100%);
        border-radius: 20px;
        padding: 1.8rem 2.2rem;
        color: #ffffff;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.4);
        border: 1px solid rgba(255, 255, 255, 0.08);
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
        background: rgba(255, 255, 255, 0.12);
        border: 1px solid rgba(255, 255, 255, 0.25);
        color: #ffffff;
        font-weight: 700;
        border-radius: 999px;
        padding: 0.5rem 1.1rem;
        backdrop-filter: blur(4px);
    }

    /* Summary Metrics Panel */
    .summary-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
        gap: 1rem;
        margin-bottom: 1.5rem;
    }
    .summary-card {
        background: #161e2e;
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 1.2rem 1.4rem;
        box-shadow: 0 6px 18px rgba(0, 0, 0, 0.25);
    }
    .summary-label {
        font-size: 0.8rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: #94a3b8;
        margin-bottom: 0.3rem;
    }
    .summary-value {
        font-size: 1.6rem;
        font-weight: 800;
        color: #f8fafc;
    }

    /* Subject Grade Card */
    .grade-card {
        background: #161e2e;
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 18px;
        padding: 1.6rem 1.8rem;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.28);
        margin-bottom: 1.5rem;
        transition: transform 0.15s ease, box-shadow 0.15s ease;
    }
    .grade-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 28px rgba(0, 0, 0, 0.38);
        border-color: rgba(255, 255, 255, 0.15);
    }
    .grade-card-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 1rem;
        flex-wrap: wrap;
        margin-bottom: 1rem;
        border-bottom: 1px solid rgba(255, 255, 255, 0.08);
        padding-bottom: 0.8rem;
    }
    .subject-title {
        font-size: 1.35rem;
        font-weight: 700;
        color: #f8fafc;
        margin: 0;
    }
    .subject-prof {
        font-size: 0.88rem;
        color: #94a3b8;
        margin-top: 0.2rem;
    }

    /* Badges */
    .status-badge-approved {
        background: rgba(16, 185, 129, 0.18);
        border: 1px solid rgba(16, 185, 129, 0.45);
        color: #6ee7b7;
        font-weight: 700;
        font-size: 0.88rem;
        padding: 0.4rem 0.95rem;
        border-radius: 9999px;
    }
    .status-badge-warning {
        background: rgba(245, 158, 11, 0.18);
        border: 1px solid rgba(245, 158, 11, 0.45);
        color: #fcd34d;
        font-weight: 700;
        font-size: 0.88rem;
        padding: 0.4rem 0.95rem;
        border-radius: 9999px;
    }
    .status-badge-danger {
        background: rgba(239, 68, 68, 0.22);
        border: 1px solid rgba(239, 68, 68, 0.5);
        color: #fca5a5;
        font-weight: 700;
        font-size: 0.88rem;
        padding: 0.4rem 0.95rem;
        border-radius: 9999px;
    }

    /* Target Box */
    .target-box {
        background: #0f172a;
        border-radius: 12px;
        padding: 0.8rem 1.1rem;
        margin-top: 1rem;
        font-size: 0.92rem;
        display: flex;
        align-items: center;
        gap: 0.6rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Header Shell
st.markdown(
    """
    <div class="page-shell">
        <div style="display:flex; align-items:center; justify-content:space-between; gap:1.2rem; flex-wrap:wrap;">
            <div>
                <h1 class="page-title">Boletim & Notas</h1>
                <div class="page-subtitle">Monitore suas notas de trabalhos e provas, médias bimestrais e metas de aprovação.</div>
            </div>
            <div class="page-pill">📊 Rendimento Acadêmico</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# Initialize service and retrieve auth token
subject_service = SubjectService()
token = st.session_state.get("auth_token")

if not token:
    st.info("💡 Você está visualizando em modo local. Faça login na página Perfil para sincronizar seus dados reais com o Xano.")

# Load subjects from backend
try:
    subjects = subject_service.list_subjects(token=token)
except Exception:
    subjects = []

# ─────────────────────────────────────────────────────────────────────────────
# Dados de Notas — inicializados no session_state uma única vez.
# Edições ficam persistentes durante a sessão sem depender do backend.
# ─────────────────────────────────────────────────────────────────────────────
_DEFAULT_GRADES: dict = {
    "Innovation Lab": [
        {"name": "Trabalho 01 - Prototipação e UX", "type": "Trabalho", "weight": "30%", "grade": 8.5, "date": "15/02/2026"},
        {"name": "Prova Prática - Xano & Streamlit", "type": "Prova", "weight": "40%", "grade": 7.5, "date": "28/02/2026"},
        {"name": "Projeto Integrador Final", "type": "Projeto", "weight": "30%", "grade": 9.0, "date": "10/03/2026"},
    ],
    "Engenharia de Software": [
        {"name": "Modelagem de Schemas e Casos de Uso", "type": "Trabalho", "weight": "30%", "grade": 7.0, "date": "10/02/2026"},
        {"name": "Avaliação Bimestral - Arquitetura", "type": "Prova", "weight": "50%", "grade": 5.5, "date": "02/03/2026"},
        {"name": "Code Review e Testes Unitários", "type": "Atividade", "weight": "20%", "grade": 6.5, "date": "12/03/2026"},
    ],
    "Calculo Diferencial e Integral": [
        {"name": "Lista 01 - Limites e Derivadas", "type": "Trabalho", "weight": "25%", "grade": 4.5, "date": "18/02/2026"},
        {"name": "Prova P1 - Derivação e Aplicações", "type": "Prova", "weight": "45%", "grade": 4.0, "date": "05/03/2026"},
        {"name": "Seminário de Funções Vetoriais", "type": "Trabalho", "weight": "30%", "grade": 5.0, "date": "15/03/2026"},
    ],
}

import copy
if "grades_data" not in st.session_state:
    st.session_state["grades_data"] = copy.deepcopy(_DEFAULT_GRADES)

# Atalho para o dicionário de notas editável
grades_data: dict = st.session_state["grades_data"]

# Consolidate subjects list
subject_items = []
if subjects:
    for s in subjects:
        s_name = s.get("name") or s.get("Nome") or f"Disciplina #{s.get('id')}"
        s_prof = s.get("teacher") or s.get("professor") or s.get("Professor") or "Prof. Titular"
        subject_items.append({"id": s.get("id"), "name": s_name, "teacher": s_prof})
else:
    subject_items = [
        {"id": 1, "name": "Innovation Lab", "teacher": "Prof. Giuliano"},
        {"id": 2, "name": "Engenharia de Software", "teacher": "Dra. Ana Silva"},
        {"id": 3, "name": "Calculo Diferencial e Integral", "teacher": "Dr. Carlos Mendes"},
    ]

# Fallback de avaliações para disciplinas sem dados cadastrados
_EVAL_FALLBACK = [
    {"name": "Trabalho Bimestral", "type": "Trabalho", "weight": "40%", "grade": 7.0, "date": "20/02/2026"},
    {"name": "Prova Teórica", "type": "Prova", "weight": "60%", "grade": 7.5, "date": "10/03/2026"},
]

# Calculate averages and overall summary metrics
APPROVAL_THRESHOLD = 7.0
averages = []
approved_count = 0
attention_count = 0

for s in subject_items:
    evals = grades_data.get(s["name"], _EVAL_FALLBACK)
    avg = sum(e["grade"] for e in evals) / len(evals) if evals else 0.0
    averages.append(avg)
    if avg >= APPROVAL_THRESHOLD:
        approved_count += 1
    else:
        attention_count += 1

overall_average = sum(averages) / len(averages) if averages else 0.0

# Summary Metrics Row
st.markdown(
    f"""
    <div class="summary-grid">
        <div class="summary-card">
            <div class="summary-label">📊 Média Geral do Aluno</div>
            <div class="summary-value" style="color: {'#6ee7b7' if overall_average >= APPROVAL_THRESHOLD else '#fcd34d'};">{overall_average:.1f}</div>
        </div>
        <div class="summary-card">
            <div class="summary-label">🟢 Disciplinas Aprovadas (≥ 7.0)</div>
            <div class="summary-value" style="color: #6ee7b7;">{approved_count}</div>
        </div>
        <div class="summary-card">
            <div class="summary-label">🔴 Em Atenção / Abaixo da Média</div>
            <div class="summary-value" style="color: #fca5a5;">{attention_count}</div>
        </div>
        <div class="summary-card">
            <div class="summary-label">🎯 Meta Mínima de Aprovação</div>
            <div class="summary-value" style="color: #93c5fd;">{APPROVAL_THRESHOLD:.1f}</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# Filtro por disciplina
disciplina_nomes = ["Todas as Disciplinas"] + [s["name"] for s in subject_items]
filtro_disciplina = st.selectbox("Filtrar por Disciplina", disciplina_nomes)

# Renderização dos Cards por Disciplina
st.markdown("---")

for s in subject_items:
    s_name = s["name"]
    s_prof = s["teacher"]

    if filtro_disciplina != "Todas as Disciplinas" and filtro_disciplina != s_name:
        continue

    # Garante que disciplinas novas do backend tenham fallback no grades_data
    if s_name not in grades_data:
        grades_data[s_name] = copy.deepcopy(_EVAL_FALLBACK)

    evals = grades_data[s_name]
    current_avg = sum(e["grade"] for e in evals) / len(evals) if evals else 0.0

    # Determinar status e estilo
    if current_avg >= APPROVAL_THRESHOLD:
        status_class = "status-badge-approved"
        status_label = f"● Aprovado (Média {current_avg:.1f})"
        target_message = "🎉 **Parabéns!** Você atingiu a média mínima de aprovação para esta matéria."
        target_color = "#6ee7b7"
    elif current_avg >= 5.0:
        status_class = "status-badge-warning"
        status_label = f"● Em Recuperação (Média {current_avg:.1f})"
        points_needed = APPROVAL_THRESHOLD - current_avg
        target_message = f"⚠️ Faltam **{points_needed:.1f} pontos** para atingir a nota mínima de aprovação (7.0)."
        target_color = "#fcd34d"
    else:
        status_class = "status-badge-danger"
        status_label = f"● Atenção Crítica (Média {current_avg:.1f})"
        points_needed = APPROVAL_THRESHOLD - current_avg
        target_message = f"🚨 Atenção: desempenho abaixo da média. Faltam **{points_needed:.1f} pontos** para atingir a aprovação (7.0)."
        target_color = "#fca5a5"

    st.markdown(
        f"""
        <div class="grade-card">
            <div class="grade-card-header">
                <div>
                    <h3 class="subject-title">📚 {s_name}</h3>
                    <div class="subject-prof">Professor(a): <strong>{s_prof}</strong></div>
                </div>
                <div class="{status_class}">{status_label}</div>
            </div>
        """,
        unsafe_allow_html=True,
    )

    # Barra de Progresso visual da Nota
    st.caption(f"Aproveitamento: {current_avg:.1f} de 10.0")
    st.progress(min(max(current_avg / 10.0, 0.0), 1.0))

    # Tabela de Avaliações + Painel de Status
    col_tabela, col_info = st.columns([2, 1])

    with col_tabela:
        st.markdown("**📝 Discriminação das Avaliações:**")
        table_rows = [
            {
                "Avaliação": e["name"],
                "Tipo": e["type"],
                "Peso": e["weight"],
                "Data": e["date"],
                "Nota Obtida": f"{e['grade']:.1f} / 10.0"
            }
            for e in evals
        ]
        st.dataframe(table_rows, use_container_width=True)

    with col_info:
        st.markdown("**🎯 Status e Meta de Aprovação:**")
        st.markdown(
            f"""
            <div class="target-box" style="border: 1px solid {target_color};">
                <span style="color: {target_color};">{target_message}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # ─────────────────────────────────────────────────────────────────────
    # Seção de Edição de Notas
    # ─────────────────────────────────────────────────────────────────────
    edit_key = f"editing_{s_name}"
    if edit_key not in st.session_state:
        st.session_state[edit_key] = False

    st.markdown("")  # espaço visual

    col_btn, _ = st.columns([1, 3])
    with col_btn:
        btn_label = "✏️ Editar Notas" if not st.session_state[edit_key] else "✖ Cancelar Edição"
        if st.button(btn_label, key=f"btn_edit_{s_name}", use_container_width=True):
            st.session_state[edit_key] = not st.session_state[edit_key]
            st.rerun()

    if st.session_state[edit_key]:
        st.markdown("**✏️ Edição de Notas — altere os valores e clique em Salvar:**")

        with st.form(key=f"form_edit_{s_name}"):
            new_grades = []
            for i, ev in enumerate(evals):
                col_name, col_grade = st.columns([3, 1])
                with col_name:
                    st.markdown(
                        f"<small style='color:#94a3b8;'>{ev['type']} · {ev['weight']} · {ev['date']}</small><br>"
                        f"<strong style='color:#f8fafc;'>{ev['name']}</strong>",
                        unsafe_allow_html=True,
                    )
                with col_grade:
                    new_val = st.number_input(
                        label="Nota",
                        min_value=0.0,
                        max_value=10.0,
                        value=float(ev["grade"]),
                        step=0.1,
                        format="%.1f",
                        key=f"grade_input_{s_name}_{i}",
                    )
                new_grades.append(new_val)
                if i < len(evals) - 1:
                    st.divider()

            col_save, col_reset = st.columns(2)
            with col_save:
                submitted = st.form_submit_button("💾 Salvar Alterações", use_container_width=True, type="primary")
            with col_reset:
                reset = st.form_submit_button("🔄 Restaurar Padrão", use_container_width=True)

        if submitted:
            for i, ev in enumerate(evals):
                grades_data[s_name][i]["grade"] = new_grades[i]
            st.session_state[edit_key] = False
            st.success(f"✅ Notas de **{s_name}** atualizadas com sucesso!")
            st.rerun()

        if reset:
            if s_name in _DEFAULT_GRADES:
                grades_data[s_name] = copy.deepcopy(_DEFAULT_GRADES[s_name])
            st.session_state[edit_key] = False
            st.success(f"🔄 Notas de **{s_name}** restauradas ao padrão.")
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)
