import streamlit as st

from app_pages.ai_chat import render_ai_chat
from app_pages.dashboard import render_dashboard
from app_pages.document_workspace import render_document_workspace
from app_pages.evaluation import render_evaluation
from app_pages.knowledge_base import render_knowledge_base
from app_pages.search_analytics import render_search_analytics
from config.settings import APP_NAME
from ui.styles import load_custom_css


APP_PAGES = [
    "Dashboard",
    "Document Workspace",
    "Knowledge Base",
    "AI Chat",
    "Search Analytics",
    "Evaluation",
    "Settings",
]


def configure_page():
    st.set_page_config(
        page_title=APP_NAME,
        page_icon="🧠",
        layout="wide",
        initial_sidebar_state="expanded",
    )


def render_sidebar():
    with st.sidebar:
        st.markdown('<div class="sidebar-logo">📄</div>', unsafe_allow_html=True)
        st.markdown('<div class="sidebar-title">RAGForge AI</div>', unsafe_allow_html=True)

        current_page = st.session_state.get("selected_page", "Dashboard")

        selected_page = st.radio(
            "Navigation",
            APP_PAGES,
            index=APP_PAGES.index(current_page),
            label_visibility="collapsed",
        )

        st.session_state.selected_page = selected_page

        st.markdown(
            '<div class="status-box">'
            '<div><span class="status-dot">●</span> '
            '<span class="status-title">System Status</span></div>'
            '<div class="status-text">All Systems Operational</div>'
            '</div>',
            unsafe_allow_html=True,
        )

        return selected_page


def render_placeholder_page(title: str, description: str):
    st.title(title)
    st.info(description)


def main():
    configure_page()
    load_custom_css()

    if "selected_page" not in st.session_state:
        st.session_state.selected_page = "Dashboard"

    selected_page = render_sidebar()

    if selected_page == "Dashboard":
        render_dashboard()

    elif selected_page == "Document Workspace":
        render_document_workspace()

    elif selected_page == "Knowledge Base":
        render_knowledge_base()

    elif selected_page == "AI Chat":
        render_ai_chat()

    elif selected_page == "Search Analytics":
        render_search_analytics()

    elif selected_page == "Evaluation":
        render_evaluation()

    elif selected_page == "Settings":
        render_placeholder_page(
            "⚙️ Settings",
            "This module will manage models, providers, chunking, retrieval, and API settings.",
        )


if __name__ == "__main__":
    main()