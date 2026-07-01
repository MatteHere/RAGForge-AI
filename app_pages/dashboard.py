import streamlit as st

from services.document_service import DocumentService
from services.workspace_service import WorkspaceService


def navigate_to(page_name: str):
    st.session_state.selected_page = page_name
    st.rerun()


def metric_card(icon, icon_class, title, value, note):
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-row">
                <div class="metric-icon {icon_class}">{icon}</div>
                <div>
                    <div class="metric-title">{title}</div>
                    <div class="metric-value">{value}</div>
                    <div class="metric-note">{note}</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_dashboard():
    document_service = DocumentService()
    workspace_service = WorkspaceService()

    total_documents = document_service.count_documents()
    total_workspaces = workspace_service.count_workspaces()
    knowledge_base_status = "Ready" if total_documents > 0 else "Empty"

    st.markdown(
        """
        <div class="main-title">RAGForge AI</div>
        <div class="main-subtitle">
            <b>Production RAG Application</b> for domain-specific 
            <b>Ask My Docs</b> workflows using hybrid retrieval, 
            reranking, citation enforcement, and evaluation.
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        metric_card("▯", "blue-icon", "Total Documents", total_documents, "Across all workspaces")

    with col2:
        metric_card("▭", "purple-icon", "Workspaces", total_workspaces, "Active workspaces")

    with col3:
        metric_card("?", "green-icon", "Questions Asked", "0", "Total queries")

    with col4:
        metric_card("≋", "yellow-icon", "Knowledge Base Status", knowledge_base_status, "Based on indexed data")

    st.markdown("## ⚡ Quick Actions")
    st.caption("Get started with RAGForge AI")

    action_col1, action_col2, action_col3 = st.columns(3)

    with action_col1:
        with st.container(border=True):
            st.markdown("### ☁️ Upload Documents")
            st.write("Add documents to your knowledge base and prepare them for indexing.")
            if st.button("Open Document Workspace", use_container_width=True):
                navigate_to("Document Workspace")

    with action_col2:
        with st.container(border=True):
            st.markdown("### 💬 Open AI Chat")
            st.write("Ask questions about your documents and get citation-backed answers.")
            if st.button("Open AI Chat", use_container_width=True):
                navigate_to("AI Chat")

    with action_col3:
        with st.container(border=True):
            st.markdown("### 📖 View Knowledge Base")
            st.write("Search indexed chunks and inspect retrieval results.")
            if st.button("Open Knowledge Base", use_container_width=True):
                navigate_to("Knowledge Base")