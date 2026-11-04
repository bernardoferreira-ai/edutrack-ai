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


# ─────────────────────────────────────────────────────────────────────────────
# 1. Carregamento de Configurações de Ambiente
# ─────────────────────────────────────────────────────────────────────────────
def load_env_file():
    """Carrega variáveis de ambiente do arquivo .env caso exista."""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    env_path = os.path.join(base_dir, ".env")
    if os.path.exists(env_path):
        try:
            with open(env_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        k, v = line.split("=", 1)
                        k = k.strip()
                        v = v.strip().strip('"').strip("'")
                        if k and not os.getenv(k):
                            os.environ[k] = v
        except Exception:
            pass

load_env_file()


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


# ─────────────────────────────────────────────────────────────────────────────
# 3. Gerador Nativo de Documentos PDF 1.4 (Pure Python - Zero Dependências)
# ─────────────────────────────────────────────────────────────────────────────
class PDFCanvas:
    """Gerador minimalista e robusto de PDF compatível com especificação PDF 1.4."""

    def __init__(self, width=595.28, height=841.89):  # Padrão A4 em pontos (72 dpi)
        self.width = width
        self.height = height
        self.stream_commands: List[str] = []

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
        """Compila a estrutura de objetos e a tabela de xref do arquivo PDF."""
        content_stream = "\n".join(self.stream_commands).encode('ascii')
        
        objects = []
        # Objeto 1: Catalog
        objects.append(b"<< /Type /Catalog /Pages 2 0 R >>")
        # Objeto 2: Pages
        objects.append(b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>")
        # Objeto 3: Page
        objects.append(
            f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 {self.width:.2f} {self.height:.2f}] "
            f"/Resources << /Font << /F1 4 0 R /F2 5 0 R >> >> /Contents 6 0 R >>".encode('ascii')
        )
        # Objeto 4: Fonte Normal (Helvetica)
        objects.append(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>")
        # Objeto 5: Fonte Negrito (Helvetica-Bold)
        objects.append(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold >>")
        # Objeto 6: Stream de Conteudo
        objects.append(
            f"<< /Length {len(content_stream)} >>\nstream\n".encode('ascii') +
            content_stream +
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
# 5. Consulta de Dados na API do Xano (ou Fallback)
# ─────────────────────────────────────────────────────────────────────────────
def fetch_student_data(api_url: Optional[str] = None, auth_token: Optional[str] = None):
    """Obtém disciplinas e tarefas da API do Xano via JWT ou carrega dados locais."""
    resolved_api = (
        api_url
        or os.getenv("XANO_API_URL")
        or os.getenv("URL_BASE_ALT")
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
def render_performance_pdf(student_name: str, metrics: Dict[str, Any], tasks: List[Dict[str, Any]]) -> bytes:
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

    # 7. Rodapé do Documento
    canvas.set_stroke_color(*c_gray_border)
    canvas.draw_line(40, 50, 555, 50, line_width=0.6)

    canvas.set_fill_color(*c_text_muted)
    canvas.draw_text("EduTrack AI - Sistema de Gestao Academica Inteligente", 40, 36, size=8, bold=False)
    canvas.draw_text("Documento gerado automaticamente para fins de acompanhamento pedagogico.", 40, 24, size=7, bold=False)

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
    return render_performance_pdf(student_name=student_name, metrics=metrics, tasks=tasks)


def generate_student_report_pdf(
    student_name: str = "Aluno EduTrack",
    output_path: str = "relatorio_desempenho.pdf",
    auth_token: Optional[str] = None,
    api_url: Optional[str] = None,
) -> Dict[str, Any]:
    """Função pública que orquestra a coleta de dados, cálculo de métricas e geração do PDF."""
    subjects, tasks = fetch_student_data(api_url=api_url, auth_token=auth_token)
    metrics = calculate_performance_metrics(subjects, tasks)
    
    pdf_bytes = render_performance_pdf(student_name=student_name, metrics=metrics, tasks=tasks)
    
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

