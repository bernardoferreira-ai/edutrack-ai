#!/usr/bin/env python3
"""
EduTrack AI - Script de Geração de Relatório de Desempenho do Aluno em PDF.

Gera um arquivo PDF consolidando o progresso acadêmico do aluno:
- Indicadores gerais (total de disciplinas, tarefas, concluídas, pendentes e taxa de conclusão).
- Tabela detalhada por disciplina com barra de progresso.
- Lista resumida de tarefas e seus status.
"""

import os
import sys
import argparse
import json
import unicodedata
from datetime import datetime
from typing import Dict, List, Any, Optional

try:
    import requests
except ImportError:
    requests = None

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if base_dir not in sys.path:
    sys.path.insert(0, base_dir)

try:
    from services.config import get_config
except ImportError:
    def get_config(k, default=None):
        return os.getenv(k, default)


# ─────────────────────────────────────────────────────────────────────────────
# 1. Carregamento de Configurações de Ambiente
# ─────────────────────────────────────────────────────────────────────────────


# ─────────────────────────────────────────────────────────────────────────────
# 2. Dados Padrão de Contingência (Fallback / Offline)
# ─────────────────────────────────────────────────────────────────────────────
FALLBACK_SUBJECTS = [
    {"id": 1, "name": "Innovation Lab", "teacher": "Prof. Coordenador", "hours": 60},
    {"id": 2, "name": "Engenharia de Software", "teacher": "Dra. Ana Silva", "hours": 80},
    {"id": 3, "name": "Calculo Diferencial e Integral", "teacher": "Dr. Carlos Mendes", "hours": 80},
]

FALLBACK_TASKS = [
    {"id": 1, "subject_id": 1, "title": "Configuracao do Ambiente", "status": "completed", "due_date": "20/02/2026"},
    {"id": 2, "subject_id": 1, "title": "Prototipacao no Figma", "status": "completed", "due_date": "25/02/2026"},
    {"id": 3, "subject_id": 2, "title": "Modelagem de Dados e Schemas", "status": "completed", "due_date": "05/03/2026"},
    {"id": 4, "subject_id": 2, "title": "Implementacao de Endpoints CRUD", "status": "pending", "due_date": "15/03/2026"},
    {"id": 5, "subject_id": 3, "title": "Lista de Exercicios - Derivadas", "status": "pending", "due_date": "20/03/2026"},
]

DEFAULT_GRADES_BY_SUBJECT = {
    "Innovation Lab": [
        {"name": "Trabalho 1 - Prototipo", "type": "Trabalho", "weight": 3, "grade": 9.0, "date": "10/03/2026"},
        {"name": "Apresentacao Midterm", "type": "Apresentacao", "weight": 4, "grade": 8.5, "date": "25/03/2026"},
        {"name": "Prova Final", "type": "Prova", "weight": 3, "grade": 7.0, "date": "10/04/2026"},
    ],
    "Engenharia de Software": [
        {"name": "Quiz - UML", "type": "Quiz", "weight": 2, "grade": 6.5, "date": "15/03/2026"},
        {"name": "Trabalho - Modelagem", "type": "Trabalho", "weight": 4, "grade": 8.0, "date": "30/03/2026"},
        {"name": "Prova Bimestral", "type": "Prova", "weight": 4, "grade": 5.5, "date": "15/04/2026"},
    ],
    "Calculo Diferencial e Integral": [
        {"name": "Lista 1 - Limites", "type": "Lista", "weight": 2, "grade": 4.0, "date": "20/03/2026"},
        {"name": "Prova Parcial", "type": "Prova", "weight": 4, "grade": 3.5, "date": "05/04/2026"},
        {"name": "Lista 2 - Derivadas", "type": "Lista", "weight": 2, "grade": 5.0, "date": "20/04/2026"},
        {"name": "Prova Final", "type": "Prova", "weight": 4, "grade": None, "date": "10/05/2026"},
    ],
}

APPROVAL_THRESHOLD = 7.0


# ─────────────────────────────────────────────────────────────────────────────
# 3. Gerador Nativo de Documentos PDF 1.4 (Pure Python - Zero Dependências)
# ─────────────────────────────────────────────────────────────────────────────
class PDFCanvas:
    """Gerador minimalista e robusto de PDF compatível com especificação PDF 1.4 (multi-página)."""

    def __init__(self, width=595.28, height=841.89):  # Padrão A4 em pontos (72 dpi)
        self.width = width
        self.height = height
        # Lista de páginas; cada página é uma lista de comandos de stream
        self._pages: List[List[str]] = [[]]  # começa com a página 1

    @property
    def stream_commands(self) -> List[str]:
        """Referência à página atual (última da lista)."""
        return self._pages[-1]

    def add_page(self):
        """Adiciona uma nova página em branco e faz dela a página atual."""
        self._pages.append([])

    def _sanitize(self, text: str) -> str:
        """Remove acentuações para renderização segura nas fontes nativas Type 1."""
        if not text:
            return ""
        normalized = unicodedata.normalize('NFKD', str(text))
        ascii_text = normalized.encode('ASCII', 'ignore').decode('ASCII')
        # Escapa caracteres especiais do PDF
        return ascii_text.replace('\\', '\\\\').replace('(', '\\(').replace(')', '\\)')

    def set_fill_color(self, r: float, g: float, b: float):
        self.stream_commands.append(f"{r:.3f} {g:.3f} {b:.3f} rg")

    def set_stroke_color(self, r: float, g: float, b: float):
        self.stream_commands.append(f"{r:.3f} {g:.3f} {b:.3f} RG")

    def draw_rect(self, x: float, y: float, w: float, h: float, fill=True, stroke=False):
        self.stream_commands.append(f"{x:.2f} {y:.2f} {w:.2f} {h:.2f} re")
        if fill and stroke:
            self.stream_commands.append("B")
        elif fill:
            self.stream_commands.append("f")
        elif stroke:
            self.stream_commands.append("S")

    def draw_line(self, x1: float, y1: float, x2: float, y2: float, line_width=1.0):
        self.stream_commands.append(f"{line_width:.2f} w")
        self.stream_commands.append(f"{x1:.2f} {y1:.2f} m {x2:.2f} {y2:.2f} l S")

    def draw_text(self, text: str, x: float, y: float, font="F1", size=10, bold=False):
        font_ref = "F2" if bold else "F1"
        clean = self._sanitize(text)
        self.stream_commands.append(
            f"BT /{font_ref} {size:.1f} Tf {x:.2f} {y:.2f} Td ({clean}) Tj ET"
        )

    def build_pdf_bytes(self) -> bytes:
        """Compila a estrutura de objetos e a tabela de xref do arquivo PDF (multi-página)."""
        num_pages = len(self._pages)

        # Calcula os IDs de objeto:
        # Obj 1: Catalog
        # Obj 2: Pages
        # Obj 3..2+num_pages: Page objects
        # Obj 3+num_pages: Font F1
        # Obj 4+num_pages: Font F2
        # Obj 5+num_pages .. 4+2*num_pages: Content streams (um por página)
        font_f1_id = 3 + num_pages
        font_f2_id = 4 + num_pages
        first_stream_id = 5 + num_pages

        # Monta kid refs para o Pages dict
        kids_refs = " ".join(f"{3 + i} 0 R" for i in range(num_pages))

        objects = []

        # Obj 1: Catalog
        objects.append(b"<< /Type /Catalog /Pages 2 0 R >>")

        # Obj 2: Pages
        objects.append(
            f"<< /Type /Pages /Kids [{kids_refs}] /Count {num_pages} >>".encode('ascii')
        )

        # Obj 3..2+num_pages: Page objects (um por página)
        for i in range(num_pages):
            stream_id = first_stream_id + i
            objects.append(
                f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 {self.width:.2f} {self.height:.2f}] "
                f"/Resources << /Font << /F1 {font_f1_id} 0 R /F2 {font_f2_id} 0 R >> >> "
                f"/Contents {stream_id} 0 R >>".encode('ascii')
            )

        # Obj font_f1_id: Fonte Normal (Helvetica)
        objects.append(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>")
        # Obj font_f2_id: Fonte Negrito (Helvetica-Bold)
        objects.append(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold >>")

        # Content streams — um por página
        for page_cmds in self._pages:
            cs = "\n".join(page_cmds).encode('ascii')
            objects.append(
                f"<< /Length {len(cs)} >>\nstream\n".encode('ascii') +
                cs +
                b"\nendstream"
            )

        # Montagem do arquivo com cálculo de offsets (xref)
        out = bytearray()
        out.extend(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")

        offsets = [0]
        for i, obj_data in enumerate(objects, start=1):
            offsets.append(len(out))
            out.extend(f"{i} 0 obj\n".encode('ascii'))
            out.extend(obj_data)
            out.extend(b"\nendobj\n")

        startxref = len(out)
        out.extend(f"xref\n0 {len(objects) + 1}\n".encode('ascii'))
        out.extend(b"0000000000 65535 f \n")
        for off in offsets[1:]:
            out.extend(f"{off:010d} 00000 n \n".encode('ascii'))

        out.extend(
            f"trailer\n<< /Size {len(objects) + 1} /Root 1 0 R >>\n"
            f"startxref\n{startxref}\n%%EOF\n".encode('ascii')
        )
        return bytes(out)


# ─────────────────────────────────────────────────────────────────────────────
# 4. Cálculo de Métricas Acadêmicas
# ─────────────────────────────────────────────────────────────────────────────
def calculate_performance_metrics(subjects: List[Dict[str, Any]], tasks: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Calcula os indicadores acadêmicos agregados do estudante."""
    total_subjects = len(subjects)
    total_tasks = len(tasks)
    
    completed_tasks = 0
    pending_tasks = 0

    for t in tasks:
        st_val = str(t.get("status", "")).lower()
        if st_val in ["completed", "concluida", "concluida"]:
            completed_tasks += 1
        else:
            pending_tasks += 1

    overall_progress = round((completed_tasks / total_tasks * 100.0), 1) if total_tasks > 0 else 0.0

    # Agrupamento por disciplina
    subjects_summary = []
    for s in subjects:
        s_id = s.get("id")
        sub_tasks = [t for t in tasks if t.get("subject_id") == s_id]
        sub_total = len(sub_tasks)
        sub_done = sum(1 for t in sub_tasks if str(t.get("status", "")).lower() in ["completed", "concluida", "concluida"])
        sub_progress = round((sub_done / sub_total * 100.0), 1) if sub_total > 0 else 0.0
        
        subjects_summary.append({
            "id": s_id,
            "name": s.get("name", "Sem Nome"),
            "teacher": s.get("teacher") or s.get("professor") or "Nao informado",
            "hours": s.get("hours", 0),
            "total_tasks": sub_total,
            "completed_tasks": sub_done,
            "progress_percentage": sub_progress
        })

    return {
        "total_subjects": total_subjects,
        "total_tasks": total_tasks,
        "completed_tasks": completed_tasks,
        "pending_tasks": pending_tasks,
        "overall_progress": overall_progress,
        "subjects": subjects_summary
    }


# ─────────────────────────────────────────────────────────────────────────────
# 5. Cálculo de Métricas de Notas por Disciplina
# ─────────────────────────────────────────────────────────────────────────────
def calculate_grades_metrics(subjects: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Calcula a média ponderada e o status de aprovação para cada disciplina."""
    result = []
    for s in subjects:
        name = s.get("name", "")
        evals = DEFAULT_GRADES_BY_SUBJECT.get(name, [])

        # Filtra apenas avaliações com nota lançada
        graded = [e for e in evals if e.get("grade") is not None]

        if graded:
            total_weight = sum(e.get("weight", 1) for e in graded)
            weighted_sum = sum(e.get("grade", 0) * e.get("weight", 1) for e in graded)
            average = round(weighted_sum / total_weight, 1) if total_weight > 0 else 0.0
        else:
            average = None

        if average is None:
            status = "Sem Notas"
            points_missing = None
        elif average >= APPROVAL_THRESHOLD:
            status = "Aprovado"
            points_missing = 0.0
        elif average >= 5.0:
            status = "Em Recuperacao"
            points_missing = round(APPROVAL_THRESHOLD - average, 1)
        else:
            status = "Atencao Critica"
            points_missing = round(APPROVAL_THRESHOLD - average, 1)

        result.append({
            "name": name,
            "evals": evals,
            "average": average,
            "status": status,
            "points_missing": points_missing,
        })
    return result


# ─────────────────────────────────────────────────────────────────────────────
# 5. Consulta de Dados na API do Xano (ou Fallback)
# ─────────────────────────────────────────────────────────────────────────────
def fetch_student_data(api_url: Optional[str] = None, auth_token: Optional[str] = None):
    """Obtém disciplinas e tarefas da API do Xano via JWT ou carrega dados locais."""
    resolved_api = (
        api_url
        or get_config("XANO_API_URL")
        or get_config("URL_BASE_ALT")
        or "https://x8ki-letl-twmt.n7.xano.io/api:dyXfRo9-"
    ).rstrip("/")

    subjects = None
    tasks = None

    if requests and auth_token:
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {auth_token}"
        }
        host = resolved_api.split("/api:")[0] if "/api:" in resolved_api else resolved_api

        # 1. Tenta endpoint consolidado de relatório se disponível
        for rpt_url in [f"{host}/api:reports/student_report", f"{resolved_api}/student_report"]:
            try:
                r = requests.get(rpt_url, headers=headers, timeout=5)
                if r.status_code == 200:
                    data = r.json()
                    if isinstance(data, dict):
                        subjects = data.get("subjects")
                        tasks = data.get("tasks")
                        if subjects is not None and tasks is not None:
                            return subjects, tasks
            except Exception:
                pass

        # 2. Consulta endpoints CRUD de subjects (canonical yhqYbIq3 e fallback)
        for sub_url in [f"{host}/api:yhqYbIq3/subjects", f"{resolved_api}/subjects"]:
            try:
                r = requests.get(sub_url, headers=headers, timeout=5)
                if r.status_code == 200:
                    subjects = r.json()
                    break
            except Exception:
                pass

        # 3. Consulta endpoints CRUD de academic_tasks (canonical T4bwHPe_ e fallback)
        for task_url in [f"{host}/api:T4bwHPe_/academic_tasks", f"{resolved_api}/academic_tasks"]:
            try:
                r = requests.get(task_url, headers=headers, timeout=5)
                if r.status_code == 200:
                    tasks = r.json()
                    break
            except Exception:
                pass

    # Utiliza dados locais de contingência caso não haja conexão com o Xano
    if subjects is None:
        subjects = FALLBACK_SUBJECTS
    if tasks is None:
        tasks = FALLBACK_TASKS

    return subjects, tasks


# ─────────────────────────────────────────────────────────────────────────────
# 6. Renderização Visual do Documento PDF
# ─────────────────────────────────────────────────────────────────────────────
def render_performance_pdf(student_name: str, metrics: Dict[str, Any], tasks: List[Dict[str, Any]], grades_data: Optional[List[Dict[str, Any]]] = None) -> bytes:
    """Renderiza um documento PDF de design profissional com o desempenho acadêmico."""
    canvas = PDFCanvas(width=595.28, height=841.89)  # A4
    now_str = datetime.now().strftime("%d/%m/%Y as %H:%M")

    # Cores do Layout EduTrack AI
    c_blue = (0.12, 0.23, 0.54)     # #1F3B8A
    c_blue_light = (0.92, 0.95, 1.0)
    c_green = (0.06, 0.62, 0.38)    # #10B981
    c_gray_bg = (0.96, 0.97, 0.98)  # #F3F4F6
    c_gray_border = (0.85, 0.88, 0.90)
    c_text_dark = (0.10, 0.12, 0.15)
    c_text_muted = (0.42, 0.46, 0.52)
    c_white = (1.0, 1.0, 1.0)

    # 1. Faixa Superior (Header Banner)
    canvas.set_fill_color(*c_blue)
    canvas.draw_rect(0, 770, 595.28, 72, fill=True, stroke=False)

    canvas.set_fill_color(*c_white)
    canvas.draw_text("EduTrack AI - Gestao Academica", 40, 810, size=18, bold=True)
    canvas.draw_text("Relatorio Oficial de Desempenho do Estudante", 40, 788, size=11, bold=False)

    # 2. Informações de Emissão
    canvas.set_fill_color(*c_text_dark)
    canvas.draw_text(f"Estudante: {student_name}", 40, 740, size=12, bold=True)
    canvas.set_fill_color(*c_text_muted)
    canvas.draw_text(f"Data de Emissao: {now_str}", 380, 740, size=9, bold=False)

    canvas.set_stroke_color(*c_gray_border)
    canvas.draw_line(40, 730, 555, 730, line_width=0.8)

    # 3. Cartões de Métricas Principais (KPIs)
    cards = [
        {"label": "Disciplinas", "val": str(metrics["total_subjects"])},
        {"label": "Total Tarefas", "val": str(metrics["total_tasks"])},
        {"label": "Concluidas", "val": str(metrics["completed_tasks"])},
        {"label": "Pendentes", "val": str(metrics["pending_tasks"])},
        {"label": "Progresso Global", "val": f"{metrics['overall_progress']}%"},
    ]
    card_w = 98.0
    card_h = 52.0
    spacing = 6.0
    start_x = 40.0
    card_y = 665.0

    for i, c in enumerate(cards):
        cx = start_x + i * (card_w + spacing)
        # Fundo do Cartão
        canvas.set_fill_color(*c_gray_bg)
        canvas.set_stroke_color(*c_gray_border)
        canvas.draw_rect(cx, card_y, card_w, card_h, fill=True, stroke=True)

        # Valor
        canvas.set_fill_color(*c_blue)
        canvas.draw_text(c["val"], cx + 12, card_y + 26, size=16, bold=True)

        # Rótulo
        canvas.set_fill_color(*c_text_muted)
        canvas.draw_text(c["label"], cx + 12, card_y + 10, size=8, bold=False)

    # 4. Barra Visual de Progresso Geral
    bar_y = 635.0
    bar_w = 515.0
    bar_h = 14.0
    canvas.set_fill_color(*c_text_dark)
    canvas.draw_text("Taxa Geral de Conclusao das Atividades:", 40, bar_y + 18, size=10, bold=True)

    # Fundo da barra
    canvas.set_fill_color(0.90, 0.92, 0.94)
    canvas.draw_rect(40, bar_y, bar_w, bar_h, fill=True, stroke=False)

    # Preenchimento da barra
    fill_w = max(0.0, min(bar_w, bar_w * (metrics["overall_progress"] / 100.0)))
    if fill_w > 0:
        canvas.set_fill_color(*c_green)
        canvas.draw_rect(40, bar_y, fill_w, bar_h, fill=True, stroke=False)

    # 5. Tabela de Desempenho por Disciplina
    sec_y = 595.0
    canvas.set_fill_color(*c_text_dark)
    canvas.draw_text("Detalhamento por Disciplina", 40, sec_y, size=12, bold=True)

    # Cabeçalho da Tabela
    th_y = sec_y - 24.0
    canvas.set_fill_color(*c_blue_light)
    canvas.set_stroke_color(*c_gray_border)
    canvas.draw_rect(40, th_y, 515, 20, fill=True, stroke=True)

    canvas.set_fill_color(*c_blue)
    canvas.draw_text("Disciplina", 48, th_y + 6, size=9, bold=True)
    canvas.draw_text("Professor", 220, th_y + 6, size=9, bold=True)
    canvas.draw_text("Tarefas", 380, th_y + 6, size=9, bold=True)
    canvas.draw_text("Progresso", 460, th_y + 6, size=9, bold=True)

    # Linhas de Disciplinas
    curr_y = th_y - 20.0
    for idx, s in enumerate(metrics["subjects"]):
        if curr_y < 150:
            break
        # Fundo alternado
        bg_col = c_white if idx % 2 == 0 else c_gray_bg
        canvas.set_fill_color(*bg_col)
        canvas.set_stroke_color(*c_gray_border)
        canvas.draw_rect(40, curr_y, 515, 20, fill=True, stroke=True)

        canvas.set_fill_color(*c_text_dark)
        canvas.draw_text(s["name"][:30], 48, curr_y + 6, size=8, bold=False)
        canvas.draw_text(s["teacher"][:25], 220, curr_y + 6, size=8, bold=False)
        canvas.draw_text(f"{s['completed_tasks']}/{s['total_tasks']}", 380, curr_y + 6, size=8, bold=False)
        canvas.draw_text(f"{s['progress_percentage']}%", 460, curr_y + 6, size=8, bold=True)

        curr_y -= 20.0

    # 6. Lista de Tarefas Recentes
    tasks_y = curr_y - 25.0
    canvas.set_fill_color(*c_text_dark)
    canvas.draw_text("Quadro de Atividades e Tarefas", 40, tasks_y, size=12, bold=True)

    th_tasks_y = tasks_y - 24.0
    canvas.set_fill_color(*c_blue_light)
    canvas.set_stroke_color(*c_gray_border)
    canvas.draw_rect(40, th_tasks_y, 515, 20, fill=True, stroke=True)

    canvas.set_fill_color(*c_blue)
    canvas.draw_text("Titulo da Tarefa", 48, th_tasks_y + 6, size=9, bold=True)
    canvas.draw_text("Prazo", 350, th_tasks_y + 6, size=9, bold=True)
    canvas.draw_text("Status", 450, th_tasks_y + 6, size=9, bold=True)

    row_task_y = th_tasks_y - 20.0
    for idx, t in enumerate(tasks[:10]):
        if row_task_y < 80:
            break
        bg_col = c_white if idx % 2 == 0 else c_gray_bg
        canvas.set_fill_color(*bg_col)
        canvas.set_stroke_color(*c_gray_border)
        canvas.draw_rect(40, row_task_y, 515, 20, fill=True, stroke=True)

        is_done = str(t.get("status", "")).lower() in ["completed", "concluida", "concluida"]
        status_label = "Concluida" if is_done else "Pendente"
        status_color = c_green if is_done else (0.85, 0.45, 0.05)

        canvas.set_fill_color(*c_text_dark)
        canvas.draw_text(str(t.get("title", ""))[:45], 48, row_task_y + 6, size=8, bold=False)
        canvas.draw_text(str(t.get("due_date", "N/A")), 350, row_task_y + 6, size=8, bold=False)
        
        canvas.set_fill_color(*status_color)
        canvas.draw_text(status_label, 450, row_task_y + 6, size=8, bold=True)

        row_task_y -= 20.0

    # 7. Rodapé do Documento (Página 1)
    canvas.set_stroke_color(*c_gray_border)
    canvas.draw_line(40, 50, 555, 50, line_width=0.6)

    canvas.set_fill_color(*c_text_muted)
    canvas.draw_text("EduTrack AI - Sistema de Gestao Academica Inteligente", 40, 36, size=8, bold=False)
    canvas.draw_text("Documento gerado automaticamente para fins de acompanhamento pedagogico.", 40, 24, size=7, bold=False)

    # ─────────────────────────────────────────────────────────────────────────
    # PÁGINA 2 — Boletim de Notas por Disciplina
    # ─────────────────────────────────────────────────────────────────────────
    if grades_data:
        canvas.add_page()

        c_orange = (0.85, 0.45, 0.05)
        c_red    = (0.75, 0.15, 0.15)

        # Header da Página 2
        canvas.set_fill_color(*c_blue)
        canvas.draw_rect(0, 770, 595.28, 72, fill=True, stroke=False)
        canvas.set_fill_color(*c_white)
        canvas.draw_text("EduTrack AI - Gestao Academica", 40, 810, size=18, bold=True)
        canvas.draw_text("Boletim de Notas por Disciplina", 40, 788, size=11, bold=False)

        canvas.set_fill_color(*c_text_dark)
        canvas.draw_text(f"Estudante: {student_name}", 40, 740, size=12, bold=True)
        canvas.set_fill_color(*c_text_muted)
        canvas.draw_text(f"Data de Emissao: {now_str}", 380, 740, size=9, bold=False)

        canvas.set_stroke_color(*c_gray_border)
        canvas.draw_line(40, 730, 555, 730, line_width=0.8)

        g_y = 710.0  # cursor vertical da página 2

        for subj in grades_data:
            # ── Bloco de cada disciplina ──
            subj_name = subj["name"]
            average   = subj["average"]
            status    = subj["status"]
            pts_miss  = subj["points_missing"]
            evals     = subj["evals"]

            # Cor do status
            if status == "Aprovado":
                badge_color = c_green
            elif status == "Em Recuperacao":
                badge_color = c_orange
            else:
                badge_color = c_red

            # Fundo do cabeçalho da disciplina
            canvas.set_fill_color(*c_blue_light)
            canvas.set_stroke_color(*c_gray_border)
            canvas.draw_rect(40, g_y - 18, 515, 22, fill=True, stroke=True)

            canvas.set_fill_color(*c_blue)
            canvas.draw_text(subj_name[:40], 48, g_y - 12, size=10, bold=True)

            # Badge de status (caixa colorida + texto)
            avg_str = f"{average:.1f}" if average is not None else "N/A"
            badge_text = f"Media: {avg_str}  |  {status}"
            canvas.set_fill_color(*badge_color)
            canvas.draw_rect(380, g_y - 17, 170, 18, fill=True, stroke=False)
            canvas.set_fill_color(*c_white)
            canvas.draw_text(badge_text, 384, g_y - 11, size=8, bold=True)

            g_y -= 22

            # Faltando pontos (se aplicável)
            if pts_miss and pts_miss > 0:
                canvas.set_fill_color(*badge_color)
                canvas.draw_text(f"  Faltam {pts_miss} pts para aprovacao", 48, g_y - 2, size=7, bold=False)
                g_y -= 12

            # Cabeçalho da tabela de avaliações
            canvas.set_fill_color(0.80, 0.84, 0.90)
            canvas.set_stroke_color(*c_gray_border)
            canvas.draw_rect(50, g_y - 16, 505, 16, fill=True, stroke=True)
            canvas.set_fill_color(*c_text_dark)
            canvas.draw_text("Avaliacao", 56, g_y - 11, size=7, bold=True)
            canvas.draw_text("Tipo", 280, g_y - 11, size=7, bold=True)
            canvas.draw_text("Peso", 360, g_y - 11, size=7, bold=True)
            canvas.draw_text("Nota", 420, g_y - 11, size=7, bold=True)
            canvas.draw_text("Data", 470, g_y - 11, size=7, bold=True)
            g_y -= 16

            # Linhas de cada avaliação
            for idx_e, ev in enumerate(evals):
                bg = c_white if idx_e % 2 == 0 else c_gray_bg
                canvas.set_fill_color(*bg)
                canvas.set_stroke_color(*c_gray_border)
                canvas.draw_rect(50, g_y - 14, 505, 14, fill=True, stroke=True)

                grade_val = ev.get("grade")
                grade_str = f"{grade_val:.1f}" if grade_val is not None else "Pendente"

                # Cor da nota individual
                if grade_val is None:
                    note_color = c_text_muted
                elif grade_val >= APPROVAL_THRESHOLD:
                    note_color = c_green
                elif grade_val >= 5.0:
                    note_color = c_orange
                else:
                    note_color = c_red

                canvas.set_fill_color(*c_text_dark)
                canvas.draw_text(str(ev.get("name", ""))[:35], 56, g_y - 10, size=7, bold=False)
                canvas.draw_text(str(ev.get("type", "")), 280, g_y - 10, size=7, bold=False)
                canvas.draw_text(str(ev.get("weight", "")), 360, g_y - 10, size=7, bold=False)
                canvas.set_fill_color(*note_color)
                canvas.draw_text(grade_str, 420, g_y - 10, size=7, bold=True)
                canvas.set_fill_color(*c_text_muted)
                canvas.draw_text(str(ev.get("date", "")), 470, g_y - 10, size=7, bold=False)
                g_y -= 14

            g_y -= 10  # espaço entre disciplinas

            # Segurança: se ultrapassar a margem inferior, para
            if g_y < 80:
                break

        # Rodapé da Página 2
        canvas.set_stroke_color(*c_gray_border)
        canvas.draw_line(40, 50, 555, 50, line_width=0.6)
        canvas.set_fill_color(*c_text_muted)
        canvas.draw_text("EduTrack AI - Sistema de Gestao Academica Inteligente", 40, 36, size=8, bold=False)
        canvas.draw_text("Boletim gerado automaticamente. Notas sujeitas a revisao pelo professor.", 40, 24, size=7, bold=False)

    return canvas.build_pdf_bytes()


# ─────────────────────────────────────────────────────────────────────────────
# 7. Função de Entrada e CLI Principal
# ─────────────────────────────────────────────────────────────────────────────
def generate_report_bytes(
    student_name: str = "Aluno EduTrack",
    auth_token: Optional[str] = None,
    api_url: Optional[str] = None,
) -> bytes:
    """Retorna os bytes do PDF gerado diretamente em memória para uso no Streamlit (download_button)."""
    subjects, tasks = fetch_student_data(api_url=api_url, auth_token=auth_token)
    metrics = calculate_performance_metrics(subjects, tasks)
    grades_data = calculate_grades_metrics(subjects)
    return render_performance_pdf(student_name=student_name, metrics=metrics, tasks=tasks, grades_data=grades_data)


def generate_student_report_pdf(
    student_name: str = "Aluno EduTrack",
    output_path: str = "relatorio_desempenho.pdf",
    auth_token: Optional[str] = None,
    api_url: Optional[str] = None,
) -> Dict[str, Any]:
    """Função pública que orquestra a coleta de dados, cálculo de métricas e geração do PDF."""
    subjects, tasks = fetch_student_data(api_url=api_url, auth_token=auth_token)
    metrics = calculate_performance_metrics(subjects, tasks)
    grades_data = calculate_grades_metrics(subjects)

    pdf_bytes = render_performance_pdf(student_name=student_name, metrics=metrics, tasks=tasks, grades_data=grades_data)
    
    # Grava o arquivo PDF no caminho de saída
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    with open(output_path, "wb") as f:
        f.write(pdf_bytes)

    result_summary = {
        "status": "success",
        "output_file": os.path.abspath(output_path),
        "file_size_bytes": len(pdf_bytes),
        "student_name": student_name,
        "metrics": metrics
    }
    return result_summary


def main():
    parser = argparse.ArgumentParser(
        description="Gera o Relatorio em PDF de Desempenho do Aluno para o EduTrack AI."
    )
    parser.add_argument(
        "--output", "-o",
        default="relatorio_desempenho.pdf",
        help="Caminho do arquivo PDF de saida (padrao: relatorio_desempenho.pdf)"
    )
    parser.add_argument(
        "--student-name", "-s",
        default="Aluno EduTrack",
        help="Nome do estudante para exibicao no relatorio"
    )
    parser.add_argument(
        "--auth-token", "-t",
        default=None,
        help="Token JWT de autenticacao para buscar dados reais no Xano"
    )
    parser.add_argument(
        "--api-url", "-u",
        default=None,
        help="URL base da API do Xano (opcional; utiliza .env por padrao)"
    )
    parser.add_argument(
        "--json-output",
        action="store_true",
        help="Imprime o resumo das metricas em JSON no stdout"
    )

    args = parser.parse_args()

    result = generate_student_report_pdf(
        student_name=args.student_name,
        output_path=args.output,
        auth_token=args.auth_token,
        api_url=args.api_url
    )

    if args.json_output:
        print(json.dumps(result, indent=2))
    else:
        print(f"[OK] Relatorio de desempenho gerado com sucesso!")
        print(f"     Arquivo: {result['output_file']} ({result['file_size_bytes']} bytes)")
        print(f"     Disciplinas: {result['metrics']['total_subjects']}")
        print(f"     Tarefas: {result['metrics']['completed_tasks']}/{result['metrics']['total_tasks']} ({result['metrics']['overall_progress']}%)")


if __name__ == "__main__":
    main()

