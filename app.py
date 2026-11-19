import streamlit as st
import sys
import os
from datetime import datetime, date

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from services.subject_service import SubjectService
from services.task_service import TaskService
from services.design_service import apply_edutrack_design

apply_edutrack_design()

st.set_page_config(page_title="EduTrack AI — Dashboard", page_icon="🎓", layout="wide")

# ─────────────────────────────────────────────────────────────────────────────
# CSS Global
# ─────────────────────────────────────────────────────────────────────────────
st.markdown(
    """
    <style>
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(180deg, #0b0f19 0%, #0f172a 50%, #0b0f19 100%);
        color: #f8fafc;
    }
    [data-testid="stSidebar"] {
        background-color: #111827;
        border-right: 1px solid rgba(255, 255, 255, 0.08);
    }

    /* Hero Banner */
    .hero-card {
        background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 60%, #172554 100%);
        border-radius: 20px;
        padding: 2rem 2.4rem;
        color: #ffffff;
        box-shadow: 0 10px 25px -5px rgba(0,0,0,0.4);
        border: 1px solid rgba(255,255,255,0.08);
        margin-bottom: 1.5rem;
        display: flex;
        align-items: center;
        justify-content: space-between;
        flex-wrap: wrap;
        gap: 1rem;
    }
    .hero-title { font-size: 2rem; font-weight: 800; margin: 0; letter-spacing: -0.02em; }
    .hero-sub   { color: rgba(255,255,255,0.80); font-size: 0.95rem; margin-top: 0.3rem; }
    .hero-pill  {
        background: rgba(255,255,255,0.12);
        border: 1px solid rgba(255,255,255,0.25);
        border-radius: 999px;
        padding: 0.5rem 1.2rem;
        font-weight: 700;
        font-size: 0.9rem;
        backdrop-filter: blur(4px);
    }

    /* KPI Cards */
    .kpi-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(170px, 1fr));
        gap: 1rem;
        margin-bottom: 1.5rem;
    }
    .kpi-card {
        background: #161e2e;
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 16px;
        padding: 1.2rem 1.4rem;
        box-shadow: 0 6px 18px rgba(0,0,0,0.25);
    }
    .kpi-label {
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        color: #94a3b8;
        margin-bottom: 0.4rem;
    }
    .kpi-value { font-size: 2rem; font-weight: 800; }

    /* Section Headers */
    .section-title {
        font-size: 1.1rem;
        font-weight: 700;
        color: #f8fafc;
        margin: 1.5rem 0 0.8rem 0;
        padding-bottom: 0.4rem;
        border-bottom: 1px solid rgba(255,255,255,0.08);
    }

    /* Mini boletim badges */
    .badge-green  { color: #6ee7b7; font-weight: 700; }
    .badge-yellow { color: #fcd34d; font-weight: 700; }
    .badge-red    { color: #fca5a5; font-weight: 700; }

    /* Quick-link cards */
    .ql-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
        gap: 0.8rem;
        margin-top: 0.5rem;
    }
    .ql-card {
        background: #161e2e;
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 14px;
        padding: 1rem 1.2rem;
        text-align: center;
        font-size: 0.95rem;
        font-weight: 600;
        color: #f8fafc;
        cursor: pointer;
        transition: all 0.15s ease;
    }
    .ql-card:hover {
        border-color: rgba(239,68,68,0.4);
        box-shadow: 0 4px 14px rgba(239,68,68,0.15);
        transform: translateY(-2px);
    }
    .ql-icon { font-size: 1.8rem; display: block; margin-bottom: 0.4rem; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ─────────────────────────────────────────────────────────────────────────────
# Dados de sessão
# ─────────────────────────────────────────────────────────────────────────────
token       = st.session_state.get("auth_token")
user_profile = st.session_state.get("user_profile")
user_name   = "Estudante"
if user_profile:
    user_name = (
        user_profile.get("name")
        or user_profile.get("nome")
        or user_profile.get("email", "Estudante").split("@")[0]
    )

# Saudação dinâmica por horário
hora = datetime.now().hour
if hora < 12:
    saudacao = "Bom dia"
elif hora < 18:
    saudacao = "Boa tarde"
else:
    saudacao = "Boa noite"

# ─────────────────────────────────────────────────────────────────────────────
# Coleta de dados (services)
# ─────────────────────────────────────────────────────────────────────────────
subject_service = SubjectService()
task_service    = TaskService()

try:
    subjects = subject_service.list_subjects(token=token)
except Exception:
    subjects = []

try:
    tasks = task_service.list_tasks(token=token)
except Exception:
    tasks = []

# Fallback grades (mesmo padrão da página de Notas)
import copy
_DEFAULT_GRADES = {
    "Innovation Lab": [
        {"grade": 8.5}, {"grade": 7.5}, {"grade": 9.0},
    ],
    "Engenharia de Software": [
        {"grade": 7.0}, {"grade": 5.5}, {"grade": 6.5},
    ],
    "Calculo Diferencial e Integral": [
        {"grade": 4.5}, {"grade": 4.0}, {"grade": 5.0},
    ],
}
grades_data = st.session_state.get("grades_data", copy.deepcopy(_DEFAULT_GRADES))

APPROVAL_THRESHOLD = 7.0

# ─────────────────────────────────────────────────────────────────────────────
# Métricas calculadas
# ─────────────────────────────────────────────────────────────────────────────
active_subjects = [s for s in subjects if str(s.get("status", "active")).lower() != "completed"]

completed_tasks = [t for t in tasks if str(t.get("status", "")).lower() in ("completed", "concluida")]
pending_tasks   = [t for t in tasks if str(t.get("status", "")).lower() not in ("completed", "concluida")]
total_tasks     = len(tasks)
progress_pct    = round(len(completed_tasks) / total_tasks * 100) if total_tasks > 0 else 0

# Média geral das notas
all_grades = []
for s in (subjects or [{"name": k} for k in _DEFAULT_GRADES]):
    s_name = s.get("name", "")
    evals  = grades_data.get(s_name, [])
    if evals:
        avg = sum(e["grade"] for e in evals if e.get("grade") is not None) / len(
            [e for e in evals if e.get("grade") is not None]
        ) if any(e.get("grade") is not None for e in evals) else None
        if avg is not None:
            all_grades.append(avg)
overall_avg = round(sum(all_grades) / len(all_grades), 1) if all_grades else 0.0

# ─────────────────────────────────────────────────────────────────────────────
# HERO
# ─────────────────────────────────────────────────────────────────────────────
login_hint = "" if token else " &nbsp;·&nbsp; <span style='color:#fbbf24;font-size:0.85rem;'>⚠️ Modo local — faça login no Perfil</span>"
st.markdown(
    f"""
    <div class="hero-card">
        <div>
            <div class="hero-title">🎓 {saudacao}, {user_name}!</div>
            <div class="hero-sub">Aqui está um resumo do seu semestre acadêmico.{login_hint}</div>
        </div>
        <div class="hero-pill">📅 {date.today().strftime('%d/%m/%Y')}</div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ─────────────────────────────────────────────────────────────────────────────
# KPI CARDS
# ─────────────────────────────────────────────────────────────────────────────
avg_color = "#6ee7b7" if overall_avg >= APPROVAL_THRESHOLD else ("#fcd34d" if overall_avg >= 5.0 else "#fca5a5")
prog_color = "#6ee7b7" if progress_pct >= 70 else ("#fcd34d" if progress_pct >= 40 else "#fca5a5")

st.markdown(
    f"""
    <div class="kpi-grid">
        <div class="kpi-card">
            <div class="kpi-label">📚 Disciplinas Ativas</div>
            <div class="kpi-value" style="color:#93c5fd;">{len(active_subjects)}</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">✅ Tarefas Concluídas</div>
            <div class="kpi-value" style="color:#6ee7b7;">{len(completed_tasks)}</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">⏳ Tarefas Pendentes</div>
            <div class="kpi-value" style="color:#fca5a5;">{len(pending_tasks)}</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">📊 Média Geral</div>
            <div class="kpi-value" style="color:{avg_color};">{overall_avg:.1f}</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">🎯 Progresso do Semestre</div>
            <div class="kpi-value" style="color:{prog_color};">{progress_pct}%</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# Barra de progresso geral
st.caption(f"Taxa de conclusão de tarefas: {len(completed_tasks)}/{total_tasks}")
st.progress(progress_pct / 100)

# ─────────────────────────────────────────────────────────────────────────────
# LAYOUT: col esquerda (tarefas) | col direita (boletim resumido)
# ─────────────────────────────────────────────────────────────────────────────
col_left, col_right = st.columns([3, 2], gap="large")

# ── Próximas Tarefas ─────────────────────────────────────────────────────────
with col_left:
    st.markdown('<div class="section-title">⏰ Próximas Tarefas Pendentes</div>', unsafe_allow_html=True)

    # Ordena por data de vencimento (mais próxima primeiro)
    def _parse_date(t):
        raw = t.get("due_date") or t.get("prazo") or ""
        for fmt in ("%d/%m/%Y", "%Y-%m-%d", "%Y-%m-%dT%H:%M:%SZ"):
            try:
                return datetime.strptime(raw[:10], fmt[:len(raw[:10])]).date()
            except Exception:
                pass
        return date(9999, 12, 31)

    sorted_pending = sorted(pending_tasks, key=_parse_date)[:8]

    if sorted_pending:
        # Mapeia subject_id -> nome
        subj_map = {s.get("id"): s.get("name", f"#{s.get('id')}") for s in subjects}

        rows = []
        for t in sorted_pending:
            due = _parse_date(t)
            days_left = (due - date.today()).days if due.year != 9999 else None
            if days_left is None:
                urgency = ""
            elif days_left < 0:
                urgency = "🔴 Vencida"
            elif days_left == 0:
                urgency = "🔴 Hoje"
            elif days_left <= 3:
                urgency = f"🟠 {days_left}d"
            else:
                urgency = f"🟢 {days_left}d"

            subj_name = subj_map.get(t.get("subject_id"), "—")
            rows.append({
                "Tarefa": t.get("title", "Sem título"),
                "Disciplina": subj_name,
                "Prazo": t.get("due_date") or t.get("prazo") or "—",
                "Urgência": urgency,
            })

        st.dataframe(rows, use_container_width=True, hide_index=True)
    else:
        st.success("🎉 Nenhuma tarefa pendente! Você está em dia.")

# ── Mini Boletim ─────────────────────────────────────────────────────────────
with col_right:
    st.markdown('<div class="section-title">📊 Boletim Resumido</div>', unsafe_allow_html=True)

    display_subjects = subjects if subjects else [{"name": k} for k in _DEFAULT_GRADES]

    for s in display_subjects:
        s_name = s.get("name", "")
        evals  = grades_data.get(s_name, [])
        graded = [e for e in evals if e.get("grade") is not None]
        avg    = round(sum(e["grade"] for e in graded) / len(graded), 1) if graded else None

        if avg is None:
            badge_cls = "badge-yellow"
            status    = "Sem notas"
            avg_str   = "—"
        elif avg >= APPROVAL_THRESHOLD:
            badge_cls = "badge-green"
            status    = "✓ Aprovado"
            avg_str   = f"{avg:.1f}"
        elif avg >= 5.0:
            badge_cls = "badge-yellow"
            status    = "⚠ Recuperação"
            avg_str   = f"{avg:.1f}"
        else:
            badge_cls = "badge-red"
            status    = "✗ Crítico"
            avg_str   = f"{avg:.1f}"

        col_a, col_b, col_c = st.columns([3, 1, 2])
        with col_a:
            st.markdown(f"<small style='color:#94a3b8;'>{s_name[:28]}</small>", unsafe_allow_html=True)
        with col_b:
            st.markdown(f"<span class='{badge_cls}'>{avg_str}</span>", unsafe_allow_html=True)
        with col_c:
            st.markdown(f"<span class='{badge_cls}'>{status}</span>", unsafe_allow_html=True)

        if avg is not None:
            st.progress(min(avg / 10.0, 1.0))
        st.markdown("---")

# ─────────────────────────────────────────────────────────────────────────────
# ATALHOS RÁPIDOS
# ─────────────────────────────────────────────────────────────────────────────
st.markdown('<div class="section-title">🚀 Acesso Rápido</div>', unsafe_allow_html=True)

quick_pages = st.columns(4)

with quick_pages[0]:
    st.page_link(
        "pages/1_📚_Disciplinas.py",
        label="Disciplinas",
        icon="📚",
        width="stretch",
    )

with quick_pages[1]:
    st.page_link(
        "pages/2_📝_Tarefas.py",
        label="Tarefas",
        icon="📝",
        width="stretch",
    )

with quick_pages[2]:
    st.page_link(
        "pages/3_👤_Perfil.py",
        label="Perfil & PDF",
        icon="👤",
        width="stretch",
    )

with quick_pages[3]:
    st.page_link(
        "pages/4_📊_Notas.py",
        label="Notas",
        icon="📊",
        width="stretch",
    )
