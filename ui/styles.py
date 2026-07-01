import streamlit as st


def load_custom_css():
    st.markdown(
        """
        <style>
        header[data-testid="stHeader"] {
            background: #F8FAFC !important;
            height: 3.2rem !important;
            border-bottom: 1px solid #E2E8F0 !important;
        }

        div[data-testid="stToolbar"] {
            display: flex !important;
        }

        div[data-testid="stDecoration"] {
            display: none !important;
        }

        footer {
            visibility: hidden;
        }

        .stApp {
            background: #F8FAFC;
            color: #0F172A;
        }

        .block-container {
            padding-top: 2.5rem;
            padding-left: 3rem;
            padding-right: 3rem;
            max-width: 1500px;
        }

        section[data-testid="stSidebar"] {
            background: #FFFFFF !important;
            border-right: 1px solid #E2E8F0 !important;
        }

        section[data-testid="stSidebar"] > div {
            background: #FFFFFF !important;
        }

        section[data-testid="stSidebar"] * {
            color: #0F172A !important;
        }

        .sidebar-logo {
            width: 72px;
            height: 72px;
            border-radius: 18px;
            background: linear-gradient(135deg, #2563EB, #3B82F6);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 34px;
            margin: 1rem 0 1rem 0;
            box-shadow: 0 14px 35px rgba(37, 99, 235, 0.25);
        }

        .sidebar-title {
            font-size: 1.4rem;
            font-weight: 900;
            color: #0F172A !important;
            margin-bottom: 1.5rem;
        }

        .status-box {
            margin-top: 4rem;
            width: 100%;
            background: #F8FAFC;
            border: 1px solid #E2E8F0;
            border-radius: 14px;
            padding: 1rem;
        }

        .status-dot {
            color: #22C55E !important;
            font-weight: 900;
        }

        .status-title {
            color: #0F172A !important;
            font-size: 0.9rem;
            font-weight: 800;
        }

        .status-text {
            color: #16A34A !important;
            font-size: 0.85rem;
            font-weight: 800;
            margin-top: 0.4rem;
        }

        .main-title {
            color: #0F172A;
            font-size: 4rem;
            font-weight: 950;
            letter-spacing: -2px;
            margin-bottom: 1rem;
        }

        .main-subtitle {
            color: #475569;
            font-size: 1.15rem;
            line-height: 1.7;
            font-weight: 600;
            max-width: 900px;
            margin-bottom: 2.5rem;
        }

        .metric-card {
            background: #FFFFFF;
            border: 1px solid #E2E8F0;
            border-radius: 18px;
            padding: 1.5rem;
            min-height: 160px;
            box-shadow: 0 18px 45px rgba(15, 23, 42, 0.08);
        }

        .metric-row {
            display: flex;
            gap: 1.2rem;
            align-items: flex-start;
        }

        .metric-icon {
            width: 56px;
            height: 56px;
            border-radius: 14px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 28px;
            font-weight: 900;
        }

        .blue-icon {
            color: #2563EB;
            background: #EFF6FF;
            border: 1px solid #BFDBFE;
        }

        .purple-icon {
            color: #7C3AED;
            background: #F5F3FF;
            border: 1px solid #DDD6FE;
        }

        .green-icon {
            color: #0F766E;
            background: #F0FDFA;
            border: 1px solid #99F6E4;
        }

        .yellow-icon {
            color: #B45309;
            background: #FFFBEB;
            border: 1px solid #FDE68A;
        }

        .metric-title {
            color: #475569;
            font-size: 1rem;
            font-weight: 800;
            margin-bottom: 0.7rem;
        }

        .metric-value {
            color: #0F172A;
            font-size: 2.4rem;
            font-weight: 950;
            line-height: 1;
        }

        .metric-note {
            color: #64748B;
            font-size: 0.95rem;
            font-weight: 600;
            margin-top: 0.8rem;
        }

        .section-heading {
            color: #0F172A;
            font-size: 1.8rem;
            font-weight: 900;
            margin-top: 3rem;
            margin-bottom: 0.3rem;
        }

        .section-subtitle {
            color: #475569;
            font-size: 1.05rem;
            font-weight: 600;
            margin-bottom: 1.5rem;
        }

        .action-card {
            background: #FFFFFF;
            border: 1px solid #E2E8F0;
            border-radius: 18px;
            padding: 1.7rem;
            min-height: 250px;
            box-shadow: 0 18px 45px rgba(15, 23, 42, 0.08);
            position: relative;
        }

        .action-card-blue {
            border-bottom: 4px solid #2563EB;
        }

        .action-card-purple {
            border-bottom: 4px solid #7C3AED;
        }

        .action-card-yellow {
            border-bottom: 4px solid #F59E0B;
        }

        .action-icon {
            width: 66px;
            height: 66px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 32px;
            margin-bottom: 1.5rem;
        }

        .action-title {
            color: #0F172A;
            font-size: 1.35rem;
            font-weight: 900;
            margin-bottom: 0.7rem;
        }

        .action-desc {
            color: #475569;
            font-size: 1rem;
            line-height: 1.55;
            font-weight: 600;
            max-width: 360px;
        }

        .action-arrow {
            position: absolute;
            right: 1.5rem;
            bottom: 1.3rem;
            font-size: 2rem;
            font-weight: 900;
        }

        .blue-text {
            color: #2563EB;
        }

        .purple-text {
            color: #7C3AED;
        }

        .yellow-text {
            color: #F59E0B;
        }

        div[data-testid="stRadio"] label {
            font-weight: 800 !important;
            color: #0F172A !important;
        }

        div[data-testid="stRadio"] p {
            font-weight: 800 !important;
            color: #0F172A !important;
        }

        .stTextInput input,
        .stTextArea textarea,
        .stSelectbox div {
            background: #FFFFFF !important;
            color: #0F172A !important;
            border-radius: 12px !important;
        }

        .stButton > button,
        .stFormSubmitButton > button {
            background: linear-gradient(135deg, #2563EB, #3B82F6) !important;
            color: #FFFFFF !important;
            border: none !important;
            border-radius: 12px !important;
            padding: 0.7rem 1rem !important;
            font-weight: 900 !important;
            box-shadow: 0 12px 30px rgba(37, 99, 235, 0.22);
        }

        .stButton > button:hover,
.stFormSubmitButton > button:hover {
    transform: translateY(-1px);
    box-shadow: 0 16px 35px rgba(37, 99, 235, 0.30);
}

/* ==========================================================
   KNOWLEDGE BASE SEARCH RESULT CARDS
========================================================== */

.search-result-card {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 22px;
    padding: 24px;
    margin-bottom: 22px;
    box-shadow: 0 15px 40px rgba(15,23,42,0.08);
    transition: all .25s ease;
}

.search-result-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 25px 60px rgba(15,23,42,0.12);
}

.result-top-row {
    display: flex;
    align-items: center;
    gap: 18px;
    margin-bottom: 18px;
}

.result-rank {
    width: 52px;
    height: 52px;
    border-radius: 16px;
    background: linear-gradient(135deg,#2563EB,#3B82F6);
    color: white;
    display:flex;
    align-items:center;
    justify-content:center;
    font-size:20px;
    font-weight:900;
}

.result-title {
    font-size:1.4rem;
    font-weight:900;
    color:#0F172A;
}

.result-subtitle {
    color:#64748B;
    font-size:.92rem;
    margin-top:4px;
}

.result-badges {
    display:flex;
    flex-wrap:wrap;
    gap:10px;
    margin-bottom:20px;
}

.result-badge {
    padding:8px 14px;
    border-radius:999px;
    font-size:.82rem;
    font-weight:800;
}

.method-badge{
    background:#EFF6FF;
    color:#2563EB;
    border:1px solid #BFDBFE;
}

.score-badge{
    background:#ECFDF5;
    color:#15803D;
    border:1px solid #A7F3D0;
}

.chunk-badge{
    background:#F5F3FF;
    color:#7C3AED;
    border:1px solid #DDD6FE;
}

.result-preview{
    background:#F8FAFC;
    border:1px solid #E2E8F0;
    border-radius:18px;
    padding:18px;
}

.result-paragraph{
    color:#334155;
    line-height:1.9;
    font-size:1rem;
    margin-bottom:14px;
}

.result-highlight{
    background:#FEF3C7;
    color:#92400E;
    padding:2px 5px;
    border-radius:5px;
    font-weight:800;
}

.result-divider{
    border-top:1px solid #E2E8F0;
    margin:18px 0;
}

.result-footer{
    display:flex;
    justify-content:space-between;
    align-items:center;
    margin-top:18px;
}

.result-chip{
    background:#EEF2FF;
    color:#4338CA;
    padding:7px 14px;
    border-radius:999px;
    font-size:.82rem;
    font-weight:800;
}

.result-action{
    color:#2563EB;
    font-weight:800;
    cursor:pointer;
    transition:.2s;
}

.result-action:hover{
    color:#1D4ED8;
}

/* ==========================================================
   END KNOWLEDGE BASE
========================================================== */

</style>
        """,
        unsafe_allow_html=True,
    )