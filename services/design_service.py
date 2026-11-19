import streamlit as st


def apply_edutrack_design() -> None:
    """Apply the shared EduTrack visual system without changing app behavior."""
    st.markdown(
        """
        <style>
        /* EduTrack shared visual foundation */
        :root {
            --edutrack-bg: #0b0f19;
            --edutrack-panel: #161e2e;
            --edutrack-panel-soft: #111827;
            --edutrack-border: rgba(148, 163, 184, 0.16);
            --edutrack-text: #f8fafc;
            --edutrack-muted: #94a3b8;
            --edutrack-red: #ef4444;
            --edutrack-radius: 18px;
            --edutrack-shadow: 0 10px 28px rgba(2, 6, 23, 0.30);
        }

        [data-testid="stAppViewContainer"] {
            background: radial-gradient(circle at top right, rgba(30, 64, 175, 0.10), transparent 28%),
                        linear-gradient(180deg, #0b0f19 0%, #0f172a 58%, #0b0f19 100%) !important;
        }
        [data-testid="stSidebar"] {
            border-right: 1px solid var(--edutrack-border) !important;
            box-shadow: 8px 0 24px rgba(2, 6, 23, 0.10);
        }
        [data-testid="block-container"] {
            max-width: 1180px;
            padding-top: 1.35rem;
            padding-bottom: 2.5rem;
        }

        /* Consistent typography */
        h1, h2, h3, h4, h5, h6,
        .hero-title, .page-title, .auth-hero-title,
        .feature-card-title, .subject-title {
            letter-spacing: -0.025em !important;
        }
        .hero-sub, .page-subtitle, .hero-subtitle, .auth-hero-subtitle,
        .feature-card-desc, .subject-prof, .profile-label, .metric-label {
            line-height: 1.55 !important;
        }

        /* Unified cards and containers */
        .hero-card, .page-shell, .card-hero, .auth-hero,
        .kpi-card, .ql-card, .content-card, .filter-panel,
        .metric-card, .summary-card, .grade-card, .feature-card,
        .auth-card-container, .target-box {
            border: 1px solid var(--edutrack-border) !important;
            border-radius: var(--edutrack-radius) !important;
            box-shadow: var(--edutrack-shadow) !important;
            transition: border-color 0.18s ease, box-shadow 0.18s ease, transform 0.18s ease;
        }
        .kpi-card:hover, .ql-card:hover, .metric-card:hover,
        .summary-card:hover, .grade-card:hover, .feature-card:hover {
            border-color: rgba(239, 68, 68, 0.28) !important;
            box-shadow: 0 14px 34px rgba(2, 6, 23, 0.38) !important;
        }

        /* Tabs and expanders */
        .stTabs [data-baseweb="tab-list"] {
            gap: 0.55rem !important;
            border-bottom: 1px solid var(--edutrack-border) !important;
        }
        .stTabs [data-baseweb="tab"] {
            border: 1px solid var(--edutrack-border) !important;
            border-radius: 10px 10px 0 0 !important;
            padding: 0.65rem 1.15rem !important;
        }
        .stTabs [aria-selected="true"] {
            border-color: rgba(239, 68, 68, 0.38) !important;
            box-shadow: inset 0 -2px 0 var(--edutrack-red);
        }
        [data-testid="stExpander"] {
            border: 1px solid var(--edutrack-border) !important;
            border-radius: 14px !important;
            box-shadow: 0 7px 20px rgba(2, 6, 23, 0.20) !important;
            overflow: hidden;
        }

        /* Inputs, forms and native controls */
        [data-baseweb="input"], [data-baseweb="textarea"],
        [data-baseweb="select"] > div,
        [data-testid="stTextInput"] > div,
        [data-testid="stTextArea"] > div,
        [data-testid="stNumberInput"] > div,
        [data-testid="stForm"] {
            border-radius: 10px !important;
        }
        [data-testid="stForm"] {
            border: 1px solid var(--edutrack-border) !important;
            background: rgba(22, 30, 46, 0.76) !important;
            padding: 1.1rem !important;
        }

        /* Tables and dataframe boundaries */
        [data-testid="stDataFrame"], [data-testid="stTable"] {
            border: 1px solid var(--edutrack-border) !important;
            border-radius: 12px !important;
            padding: 0.35rem;
            overflow: hidden;
            box-shadow: 0 8px 22px rgba(2, 6, 23, 0.18);
        }

        /* Buttons */
        button[kind], button {
            border-radius: 10px !important;
            min-height: 42px;
            transition: transform 0.15s ease, box-shadow 0.15s ease, border-color 0.15s ease !important;
        }
        button[kind]:hover, button:hover {
            transform: translateY(-1px);
        }

        /* Status and metadata chips */
        .meta-badge, .status-badge, .status-badge-approved,
        .status-badge-warning, .status-badge-danger,
        .page-pill, .metric-badge, .badge-green,
        .badge-yellow, .badge-red {
            border-radius: 999px !important;
        }

        /* Responsive spacing */
        @media (max-width: 768px) {
            [data-testid="block-container"] {
                padding-left: 0.8rem;
                padding-right: 0.8rem;
            }
            .hero-card, .page-shell, .card-hero, .auth-hero {
                border-radius: 14px !important;
                padding: 1.25rem 1.35rem !important;
            }
            .hero-title, .page-title, .auth-hero-title {
                font-size: 1.55rem !important;
            }
            .kpi-card, .ql-card, .metric-card,
            .summary-card, .grade-card, .feature-card {
                border-radius: 14px !important;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
